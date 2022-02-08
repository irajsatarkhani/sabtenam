from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
app_name = "main"


urlpatterns = [
    path("", views.home, name="homepage"),
    path("login/", views.login_request, name="login"),
    path("register/", views.register_request, name="register"),
    path("logout/", views.logout_request, name= "logout"),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='register/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="register/password_reset_confirm.html"),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='register/password_reset_complete.html'),
         name='password_reset_complete'),
    path("password_reset/", views.password_reset_request, name="password_reset"),
    path('password-reset-confirm/<uidb64>/<token>/',     auth_views.PasswordResetConfirmView.as_view(template_name='register/password_reset_confirm.html'),
    name='password_reset_confirm'),


]