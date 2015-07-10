from registration.forms import RegistrationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field
from crispy_forms.bootstrap import StrictButton


class HorizontalRegForm(RegistrationForm):

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
        self.fields['email'].label = "Email"
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Confirm"
        self.fields['username'].label = "Username"
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Field('username', css_class="input-lg"),
            Field('email', css_class="input-lg"),
            Field('password1', css_class="input-lg"),
            Field('password2', css_class="input-lg"),
            Div(
                Div(
                    StrictButton('Sign Me Up!', type="submit",
                                css_class='btn-lg btn-default btn-block'),
                    css_class="col-md-offset-3 col-md-8"
                ), css_class="row"
            )
        )
