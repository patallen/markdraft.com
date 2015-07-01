from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper


class LoginForm(forms.ModelForm):
    username = forms.CharField(label='')
    password = forms.CharField(widget=forms.PasswordInput(), label='')

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.field_template = 'bootstrap3/layout/inline_field.html'
        self.helper.form_class = 'form-inline'

    class Meta:
        model = User
        fields = ('username', 'password')
