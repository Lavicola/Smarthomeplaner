from django import forms

class SmarthomeMapForm(forms.Form):
    your_name = forms.JSONField()