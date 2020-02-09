from django.contrib.auth import (
    logout
)
from django.contrib.auth.views import (
    LoginView, 
    LogoutView,  
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView, 
    PasswordResetCompleteView, 
    PasswordChangeView,
    PasswordChangeDoneView
)
from django.urls import path, re_path, include, reverse_lazy
from django.views.generic import TemplateView

from .views import logout, login_view, UserSettingsView, SignUpView

app_name = 'accounts'

urlpatterns = [
    re_path(
        r'^signup/',
        view=SignUpView.as_view(),
        name='signup',
    ),
    re_path(
        r'^settings/',
        view=UserSettingsView.as_view(),
        name='usersettings',
    ),
    re_path(
        r'^login/$',
        login_view,
        name='login',
    ),
    re_path(
        r'^logout/$',
        LogoutView.as_view(),
        kwargs={'next_page': '/'},
        name='logout'
    ),
    path('password_change/', PasswordChangeView.as_view(success_url=reverse_lazy('accounts:password_change_done')), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', PasswordResetView.as_view(template_name='registration/password_reset_form.html',
    email_template_name='registration/password_reset_email.html',success_url = reverse_lazy('accounts:password_reset_done')), name='password_reset'),
    re_path(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    TemplateView.as_view(template_name="registration/password_reset_confirm.html"),
    name='password_reset_confirm'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
