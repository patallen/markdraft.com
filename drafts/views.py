from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from drafts.forms import SignupForm


class SignupView(CreateView):
    template_name = 'signup.html'
    form_class = SignupForm
    success_url = '/'
