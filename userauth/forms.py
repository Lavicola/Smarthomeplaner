from allauth.account.forms import SignupForm
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUser
from django import forms
from django.utils.translation import ugettext_lazy as _


LANGUAGE_CHOICE = [
    ( 'de', _('German')),
    ('en', _('English')),
    ]



class RegisterUser(SignupForm):
    language = forms.CharField(label=_('Which Language do you prefer?'), widget=forms.Select(choices=LANGUAGE_CHOICE))
    
    class Meta:
        fields  = ("email","password1","password2","language")
        model = CustomUser

