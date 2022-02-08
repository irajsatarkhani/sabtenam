from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm
# Create your views here.
from .forms import NewUserForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from .forms import ContactForm

def home(request):
	return render(request,'register/home.html')

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("main:homepage")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="register/register.html", context={"register_form":form})

# .............................
def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("main:homepage")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="register/login.html", context={"login_form":form})
# .............logout
def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.")
	return redirect("main:logout")

# بازیابی پسورد
# def password_reset_request(request):
# 	if request.method == "POST":
# 		password_reset_form = PasswordResetForm(request.POST)
# 		if password_reset_form.is_valid():
# 			data = password_reset_form.cleaned_data['email']
# 			associated_users = User.objects.filter(Q(email=data))
# 			if associated_users.exists():
# 				for user in associated_users:
# 					subject = "Password Reset Requested"
# 					email_template_name = "register/password_reset_email.txt"
# 					c = {
# 					"email":user.email,
# 					'domain':'127.0.0.1:8000',
# 					'site_name': 'Website',
# 					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
# 					"user": user,
# 					'token': default_token_generator.make_token(user),
# 					'protocol': 'http',
# 					}
# 					email = render_to_string(email_template_name, c)
# 					try:
# 						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
# 					except BadHeaderError:
# 						return HttpResponse('Invalid header found.')
# 					return redirect ("/password_reset/done/")
# 	password_reset_form = PasswordResetForm()
# 	return render(request=request, template_name="register/password_reset.html", context={"password_reset_form":password_reset_form})

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "main/password/password_reset_email.txt"
					c = {
						"email": user.email,
						'domain': '127.0.0.1:8000',
						'site_name': 'Website',
						"uid": urlsafe_base64_encode(force_bytes(user.pk)),
						'token': default_token_generator.make_token(user),
						'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
					except BadHeaderError:

						return HttpResponse('Invalid header found.')

					messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
					return redirect("main:homepage")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="register/password_reset.html",
				  context={"password_reset_form": password_reset_form})


# Create your views here.
def contact(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			subject = "Website Inquiry"
			body = {
				'first_name': form.cleaned_data['first_name'],
				'last_name': form.cleaned_data['last_name'],
				'email': form.cleaned_data['email_address'],
				'message': form.cleaned_data['message'],
			}
		message = "\n".join(body.values())

		try:
			send_mail(subject, message, 'admin@example.com', ['admin@example.com'])
		except BadHeaderError:
			return HttpResponse('Invalid header found.')
		messages.success(request, "Message sent.")
		return redirect("main:homepage")


form = ContactForm()
return render(request, "main/contact.html", {'form': form})