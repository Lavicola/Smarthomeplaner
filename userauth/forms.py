from allauth.account.forms import SignupForm
from django.contrib.auth.forms import UserCreationForm
from django_countries.fields import CountryField
from users.models import CustomUser


class RegisterUser(SignupForm):
    country = CountryField(blank_label=_'(Select country)').formfield()
    
    class Meta:
        fields  = ("email","password1","password2","country")
        model = CustomUser

