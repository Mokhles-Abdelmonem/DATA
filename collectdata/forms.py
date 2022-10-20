from ast import Try
from dataclasses import fields
from django import forms
from . import models
from django.forms.widgets import  FileInput 



class CSVDataForm(forms.ModelForm):
    class Meta:
        model = models.BaseData
        fields = ["base_file"]
        widgets = {
            'base_file': FileInput(attrs={"id": "user_input_csv_file","multiple": True, "value":"upload", "class": "form-control user-csv-file",}),

        }
        labels = {
            "": "",
        }