from django import forms

# used to validate and sanitize the json and 
class AJAXForm(forms.Form):
    json_data = forms.JSONField()
    canvas_map = forms.JSONField()