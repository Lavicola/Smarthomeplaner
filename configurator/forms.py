from django import forms

class SmarthomeMapForm(forms.Form):
    canvas_map = forms.JSONField()


class AJAXSaveRoomForm(forms.Form):
    json_data = forms.JSONField()