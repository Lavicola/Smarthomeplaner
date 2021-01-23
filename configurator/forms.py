from django import forms

class SmarthomeMapForm(forms.Form):
    canvas_map = forms.JSONField()