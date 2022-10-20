from django import forms

class ProcessForm(forms.Form):
    process  = forms.CharField(max_length=500,required=True)
    value1  = forms.CharField(max_length=500,required=False)
    value2  = forms.CharField(max_length=500,required=False)
