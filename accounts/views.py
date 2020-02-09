import logging

from django.http import HttpResponse
from django.shortcuts import render_to_response, HttpResponseRedirect, render
from django.views.generic import FormView
from django.template import RequestContext
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage

# from axes.decorators import axes_dispatch
from braces.views import LoginRequiredMixin

from .forms import UserSettingsForm, SignUpForm


logger = logging.getLogger(__name__)


# @axes_dispatch
def login_view(request):
    username = password = ''
    # Flag to keep track whether the login was invalid.
    login_failed = False
    next = request.GET.get('next', '/dashboard/view')
    # if request.user.is_authenticated():
    #     return HttpResponseRedirect('/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password, request=request)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(next)
            else:
                login_failed = True
                messages.error(request, "User does not exist.Check your email to activate account! or register account")
        else:
            messages.error(request, "Invalid username or password.Please try again!")
    return render(request, 'accounts/login.html', {'redirect_to':next})


class SignUpView(FormView):
    success_url = '/dashboard/view'
    form_class = SignUpForm
    template_name = 'accounts/signup.html'

    def get_initial(self):
        # Force logout.
        logout(self.request)

        return {'time_zone': settings.TIME_ZONE}

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form.full_clean()

        if form.is_valid():

            username = form.cleaned_data['username'].replace(' ', '').lower()
            password = form.cleaned_data['password']

            

            user = User.objects.create(username=username)
            user.email = form.cleaned_data['email']
            user.organization = form.cleaned_data['organization']
            user.set_password(password)
            user.is_active = False
            user.save()

            
            user.settings.save()

            logger.info('New user signed up: %s (%s)', user, user.email)

            # Automatically authenticate the user after user creation.
            user_auth = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password'],request=request)
            # login(request, user_auth)
            current_site = get_current_site(request)
            mail_subject = 'Please access your email & Activate your account!.'
            message = render_to_string('accounts/emails/account_activate.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
        else:
            return self.form_invalid(form)

        #     return self.form_valid(form)
        # else:
        #     return self.form_invalid(form)

class UserSettingsView(LoginRequiredMixin, FormView):
    success_url = '.'
    form_class = UserSettingsForm
    template_name = 'accounts/usersettings.html'

    def get_initial(self):
        user = self.request.user
        settings = user.settings

        return {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'organization': user.settings.organization,
        }

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Settings Saved!')

        return super(UserSettingsView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form.full_clean()

        if form.is_valid():
            user = request.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.organization = form.cleaned_data['organization']
            user.save()

            user.settings.save()

            logger.info('Account Settings updated by %s', user)

            return self.form_valid(form)
        else:
            return self.form_invalid(form)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')