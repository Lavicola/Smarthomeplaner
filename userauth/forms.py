from allauth.account.forms import SignupForm
from django.contrib.auth.forms import UserCreationForm
from django_countries.fields import CountryField
from users.models import CustomUser


class RegisterUser(SignupForm):
    country = CountryField(blank_label='(Select country)').formfield()



    def signup(self, request, user):
        raise Exception("Sorry, no numbers below zero")
        user = super(RegisterUser, self).save(request)
        raise Exception("Sorry, no numbers below zero")

        user.country = "DE"
        user.save()
        return user




    
    class Meta:
        fields  = ("email","password1","password2","country")
        model = CustomUser

