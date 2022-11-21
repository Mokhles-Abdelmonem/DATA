from enum import unique
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DetailView, View
from .forms import CSVDataForm
from django.urls import reverse
from .models import BaseData , SaveData
from django.http import HttpResponse, response, JsonResponse
import subprocess
import uuid 
from django.shortcuts import render, redirect
from users.auth.decorators import  HandelError , error_decorator
import pandas as pd
import threading
# from .tasks import refine_task

class CsvFileView(LoginRequiredMixin, CreateView):
    form_class = CSVDataForm
    model = BaseData
    template_name = 'csvdata/csvfile.html'
    def get_context_data(self, **kwargs):
        context = super(CsvFileView, self).get_context_data()
        if self.request.POST:
            context["docs"] = CSVDataForm(self.request.POST, self.request.FILES)
        else:

            context["docs"] = CSVDataForm()
        return context

    def form_valid(self, form):
        if self.request.FILES:
            for f in self.request.FILES.getlist('base_file'):
                data_obj = self.model.objects.create(
                    user =self.request.user ,
                    file_name = str(f),
                    base_file=f,
                )
                # refine_task.apply_async(args=[data_obj.id])
                t = threading.Thread(target=read__save_file, args=[data_obj.id])
                t.daemon = True
                t.start()
        return redirect(self.get_success_url())
    
    def get_success_url(self):
        url = reverse("user-files")
        return url
    

def read__save_file(obj_id):
    data_obj = BaseData.objects.get(id=obj_id)
    file_path = str(data_obj.base_file)
    full_file_name = file_path.split('/')[-1]
    file_name_parts = full_file_name.split('.')
    file_name = file_name_parts[0]
    extention = file_name_parts[1]
    if extention in ['xlsx', 'xls','ods'] :
        df = pd.read_excel(f'mydocs/{full_file_name}')

    else:
        sep_dict = {'csv':',','tsv':'\t'}
        sep = sep_dict.get(extention)
        try:
            df = pd.read_csv(f'mydocs/{full_file_name}', sep=sep)
        except:
            cmd1 = f'openrefine-client_0-3-10_windows.exe --create mydocs/{full_file_name} --encoding=UTF-8'
            cmd2 = f'openrefine-client_0-3-10_windows.exe --export --output=mydocs/refined_{file_name}.csv "{file_name}"'
            result1 = subprocess.call(cmd1, shell=True)
            result2 = subprocess.call(cmd2, shell=True)
            df = pd.read_csv(f'mydocs/refined_{file_name}.csv',sep=",")
            

    data_obj.rows_num , data_obj.cols_num = df.shape
    data_obj.nulls_num = df.isnull().values.sum().sum()
    data_obj.duplicates_num = df.duplicated().any().sum()
    data_obj.save()
    SaveData.objects.create(data_model=data_obj, saved_data=df.to_csv(index=False))
    return 'task finished successfully'
   