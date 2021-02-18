from django import forms


class AJAXForm(forms.Form):
    json_data = forms.JSONField()
    canvas_map = forms.JSONField()