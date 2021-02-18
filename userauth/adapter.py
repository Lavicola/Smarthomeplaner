from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form):
        form_field = form.cleaned_data
        user.email = form_field.get('email')
        user.country = form_field.get('country')
        if ('password1' and 'password2' in form_field):
            if( form_field["password1"] == form_field["password2"]):           
                user.set_password(form_field["password1"])
                user.save()
        return user