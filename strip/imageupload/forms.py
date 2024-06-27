from django import forms
from .models import UrineStrip

class UrineStripForm(forms.ModelForm):
    class Meta:
        model = UrineStrip
        fields = ['image']
