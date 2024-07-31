from django.urls import path
from django.contrib.auth import views as auth_view

from .forms import LoginForm,MySetPasswordForm,MyPasswordResetForm
from .views import *

urlpatterns = [
    path("create-account/",signup, name="account-signup"),
    path("account-login/",signin, name="account-login"),
    #path("account-login/",auth_view.LoginView.as_view(template_name='accounts/sigNin.html',authentication_form=LoginForm), name="account-login"),
    path("account-logout/",auth_view.LogoutView.as_view(next_page='account-login'), name="account-logout"),
    path('password-reset/',auth_view.PasswordResetView.as_view(template_name='accounts/password_reset.html',form_class=MyPasswordResetForm),name='password-reset'),
    path('password-reset-done/',auth_view.PasswordResetDoneView.as_view(template_name='accounts/passwordresetdone.html'),name='password_reset_done'),
    path('confirm-password-reset/<uidb64>/<token>',auth_view.PasswordResetConfirmView.as_view(template_name='accounts/confirm_password_reset.html',form_class=MySetPasswordForm),name='password_reset_confirm'),
    path('password-reset-complete/',auth_view.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),name='password-reset-complete'),
]