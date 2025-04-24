from django import forms

class CSVUploadForm(forms.Form):
    name = forms.CharField(max_length=100, label="Update Name")
    file = forms.FileField(label="Select File")
