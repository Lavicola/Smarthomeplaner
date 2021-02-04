from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form):
        form_field = form.cleaned_data
        user.email = form_field.get('email')
        # all your custom fields
        user.country = form_field.get('country')
        if 'password1' in form_field:
            user.set_password(form_field["password1"])
        else:
            user.set_unusable_password()
        user.save()
        return user