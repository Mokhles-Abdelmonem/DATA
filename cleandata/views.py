from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DetailView, UpdateView,View
from django.urls import reverse
from collectdata.models import BaseData, SaveData
from django.http import HttpResponse, response, JsonResponse
import pandas as pd 
from django.contrib.auth.decorators import login_required
from io import StringIO
from .forms import ProcessForm
from . import process
class UserFilesView(LoginRequiredMixin, ListView):
    template_name = 'csvdata/userFiles.html'
    def get_context_data(self):
        context = super(UserFilesView, self).get_context_data()
        data =  BaseData.objects.filter(user=self.request.user)
        context["base_files"] = data
        return context
    
    def get_queryset(self):

        data = BaseData.objects.filter(user=self.request.user)

        return data

ProcessDict = dict([(name, cls) for name, cls in process.__dict__.items() if isinstance(cls, type)])


class BaseFileView(LoginRequiredMixin, View):

    template_name = 'csvdata/filedetails.html'
    def get_context_data(self, **kwargs):
        kwargs['form'] = ProcessForm()
        return kwargs

    def post(self, request, *args, **kwargs):
        ctxt = {}
        process_form = ProcessForm(request.POST)
        if process_form.is_valid():
            # Here, save the response
            valueslist = request.POST.getlist("valueslist[]")
            if valueslist :
                kwargs["valueslist"] = valueslist
            TheProcess = process_form.cleaned_data.pop("process")
            kwargs.update(process_form.cleaned_data)
            THeClass = ProcessDict[TheProcess]
            THeClass(**kwargs)
        else:
            ctxt['form'] = process_form
        return render(request, self.template_name, self.get_context_data(**ctxt))





















# @login_required(login_url='login')
# def dropColumn(request, *args, **kwargs) :
#     column = kwargs["column"]
#     data_obj = BaseData.objects.get(id=kwargs["pk"])
#     saved_data = SaveData.objects.filter(data_model=data_obj).order_by("-date")[0]
#     data = StringIO(saved_data.saved_data)
#     df = pd.read_csv(data,sep=",",index_col=False)
#     df_droped = df.drop(columns=[column])
#     SaveData.objects.create(data_model=data_obj, saved_data=df_droped.to_csv(index=False))
#     return redirect("basefile-details",pk=data_obj.id)

# @login_required(login_url='login')
# def dropNaAll(request, *args, **kwargs) :
#     axis = kwargs["axis"]
#     data_obj = BaseData.objects.get(id=kwargs["pk"])
#     saved_data = SaveData.objects.filter(data_model=data_obj).order_by("-date")[0]
#     data = StringIO(saved_data.saved_data)
#     df = pd.read_csv(data,sep=",",index_col=False)
#     df_droped = df.dropna(axis=axis)
#     SaveData.objects.create(data_model=data_obj, saved_data=df_droped.to_csv(index=False))
#     return redirect("basefile-details",pk=data_obj.id)

# @login_required(login_url='login')
# def dropNaInCol(request, *args, **kwargs) :
#     column = kwargs["column"]
#     data_obj = BaseData.objects.get(id=kwargs["pk"])
#     saved_data = SaveData.objects.filter(data_model=data_obj).order_by("-date")[0]
#     data = StringIO(saved_data.saved_data)
#     df = pd.read_csv(data,sep=",",index_col=False)
#     df_droped  = df[df[column].notna()]
#     SaveData.objects.create(data_model=data_obj, saved_data=df_droped.to_csv(index=False))
#     return redirect("basefile-details",pk=data_obj.id)

# @login_required(login_url='login')
# def fillNaAll(request, *args, **kwargs) :
#     axis = kwargs["axis"]
#     data_obj = BaseData.objects.get(id=kwargs["pk"])
#     saved_data = SaveData.objects.filter(data_model=data_obj).order_by("-date")[0]
#     data = StringIO(saved_data.saved_data)
#     df = pd.read_csv(data,sep=",",index_col=False)
#     df_droped = df.dropna(axis=axis)
#     SaveData.objects.create(data_model=data_obj, saved_data=df_droped.to_csv(index=False))
#     return redirect("basefile-details",pk=data_obj.id)

# @login_required(login_url='login')
# def replaceNaAll(request, *args, **kwargs) :
#     fillnull = kwargs["fillnull"]
#     data_obj = BaseData.objects.get(id=kwargs["pk"])
#     saved_data = SaveData.objects.filter(data_model=data_obj).order_by("-date")[0]
#     data = StringIO(saved_data.saved_data)
#     df = pd.read_csv(data,sep=",",index_col=False)
#     df_droped = df.fillna(fillnull)
#     SaveData.objects.create(data_model=data_obj, saved_data=df_droped.to_csv(index=False))
#     return redirect("basefile-details",pk=data_obj.id)

# @login_required(login_url='login')
# def fillNaInCol(request, *args, **kwargs) :
#     column = kwargs["column"]
#     fillnull = kwargs["fillnull"]
#     data_obj = BaseData.objects.get(id=kwargs["pk"])
#     saved_data = SaveData.objects.filter(data_model=data_obj).order_by("-date")[0]
#     data = StringIO(saved_data.saved_data)
#     df = pd.read_csv(data,sep=",",index_col=False)
#     df[column] = df[column].fillna(fillnull)
#     SaveData.objects.create(data_model=data_obj, saved_data=df.to_csv(index=False))
#     return redirect("basefile-details",pk=data_obj.id)

# @login_required(login_url='login')
# def splitCol(request, *args, **kwargs) :
#     column = kwargs["column"]
#     sep = kwargs["sep"]
#     id=kwargs["pk"]
#     data_obj = BaseData.objects.get(id=id)
#     saved_data = SaveData.objects.filter(data_model=data_obj).order_by("-date")[0]
#     data = StringIO(saved_data.saved_data)
#     df = pd.read_csv(data,sep=",",index_col=False)
#     splited_columns = df[column].str.split(sep,expand=True)
#     for index ,col in enumerate(splited_columns):
#         col.columns = [f"new column {index}"]
#         df = pd.concat([df,col], axis=1)
#     SaveData.objects.create(data_model=data_obj, saved_data=df.to_csv(index=False))
#     return redirect("basefile-details",pk=data_obj.id)



