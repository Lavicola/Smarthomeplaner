from allauth.account.forms import SignupForm
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUser
from django import forms
from django.utils.translation import ugettext_lazy as _
from users import models



class RegisterUser(SignupForm):
    language_choice = forms.ChoiceField(choices=CustomUser.Language.choices) #use the model field. Form will be always up to date
    
    class Meta:
        fields  = ("email","password1","password2","language_choice")
        model = CustomUser

