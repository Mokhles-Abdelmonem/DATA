from enum import unique
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DetailView, View
from .forms import CSVDataForm
from django.urls import reverse
from .models import BaseData
from django.http import HttpResponse, response, JsonResponse
import subprocess
import uuid 
from django.shortcuts import render, redirect

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
                data_obj.file_refine
        return redirect(self.get_success_url())
    
    def get_success_url(self):
        url = reverse("user-files")
        return url
    
