# forms.py
from django import forms

class UploadZipForm(forms.Form):
    dataset_zip = forms.FileField()