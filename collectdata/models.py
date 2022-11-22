from cgi import print_directory
from contextlib import redirect_stdout
from datetime import date
from statistics import mode
from django.db import models
from django.contrib.auth.models import User
from .validators import validate_file_size, validate_file_extention
import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
import subprocess
import uuid
from django.dispatch import Signal
from django.db.models.signals import post_save
from IPython.display import HTML
from django.shortcuts import render, redirect
from io import StringIO


# Create your models here.



class BaseData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    base_file = models.FileField(verbose_name="base_file", upload_to='mydocs/', validators=[validate_file_size,validate_file_extention])
    date = models.DateTimeField(auto_now_add=True)
    rows_num = models.IntegerField(blank=True, null=True)
    cols_num = models.IntegerField(blank=True, null=True)
    nulls_num = models.IntegerField(blank=True, null=True)
    duplicates_num = models.IntegerField(blank=True, null=True)
    token = models.CharField(max_length=2000, blank=True, null=True)


    def __str__(self):
        return self.user.username
        
    @property
    def file_refine(self):
        full_file_name = self.file_name
        file_name = full_file_name.split('.')[0]
        cmd1 = f'openrefine-client_0-3-10_windows.exe --create mydocs/{full_file_name} --encoding=UTF-8'
        cmd2 = f'openrefine-client_0-3-10_windows.exe --export --output=mydocs/refined_{file_name}.csv "{file_name}"'
        result1 = subprocess.call(cmd1, shell=True)
        result2 = subprocess.call(cmd2, shell=True)
        df = pd.read_csv(f'mydocs/refined_{file_name}.csv',sep=",")
        SaveData.objects.create(data_model=self,saved_data=df.to_csv(index=False))

        
        
    


class SaveData(models.Model):
    data_model = models.ForeignKey(BaseData, on_delete=models.CASCADE)
    saved_data = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.data_model.user.username