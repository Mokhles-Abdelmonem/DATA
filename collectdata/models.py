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
from django.template.defaulttags import register


# Create your models here.
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def lower(value): # Only one argument.
    """Converts a string into all lowercase"""
    return value.lower()


class BaseData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    base_file = models.FileField(verbose_name="base_file", upload_to='mydocs/', validators=[validate_file_size,validate_file_extention])
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    @property
    def read_file(self):
        pd.set_option('display.width', 100)
        pd.set_option('colheader_justify', 'center')    
        saved_data = SaveData.objects.filter(data_model=self).order_by("-date")[0]
        data = StringIO(saved_data.saved_data)
        df = pd.read_csv(data, sep=",")
        return df
    @property
    def file_checkout(self):
        df = self.read_file
        count_null = df.isnull().values.sum().sum()
        count_row, count_col = df.shape
        dupnum = df.duplicated().any().sum()
        data_frame =  df.to_html(classes='table table-striped text-center',justify='center', header=False)
        df_html = data_frame.replace("<td>","<td contenteditable>").replace('<tbody>','<tbody class="tbody-container">')
        df_colmns = {}
        dftypes = dict(df.dtypes)
        return  {
            "count_row":count_row,
             "count_col":count_col,
              "count_null":count_null,
              "duplicate_num":dupnum,
              "data_frame":df_html,
              "df_colmns":list(df),
              "coltype_dict" : dict(df.dtypes),
              }

    @property
    def data_frame(self):
        df = self.read_file
        data_frame =  df.to_html(classes='table table-striped text-center',justify='center', header=False)
        df_html = data_frame.replace("<td>","<td contenteditable>").replace('<tbody>','<tbody class="tbody-container">')
        return {"df_html":df_html}

    @property
    def file_refine(self):
        file_path = str(self.base_file)
        full_file_name = file_path.split('/')[-1]
        file_name = full_file_name.split('.')[0]
        cmd1 = f'openrefine-client_0-3-10_windows.exe --create mydocs/{full_file_name} --encoding=UTF-8'
        cmd2 = f'openrefine-client_0-3-10_windows.exe --export --output=mydocs/refined_{file_name}.csv "{file_name}"'
        result1 = subprocess.call(cmd1, shell=True)
        result2 = subprocess.call(cmd2, shell=True)
        df = pd.read_csv(f'mydocs/refined_{file_name}.csv',sep=",")
        print(df)
        SaveData.objects.create(data_model=self,saved_data=df.to_csv(index=False))
    @property
    def hasnull(self):
        df = self.read_file
        return df.isnull().values.any()
        
    @property
    def last_savedata(self):
        saved_data = SaveData.objects.filter(data_model=self).order_by("-date")
        if len(saved_data) > 1:
            return True
        return False
        
        
    


class SaveData(models.Model):
    data_model = models.ForeignKey(BaseData, on_delete=models.CASCADE)
    saved_data = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.data_model.user.username