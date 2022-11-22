from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DetailView, UpdateView,View,DeleteView
from django.urls import reverse , reverse_lazy
from collectdata.models import BaseData, SaveData
from django.http import HttpResponse, response, JsonResponse
import pandas as pd 
from django.contrib.auth.decorators import login_required
from io import StringIO
from .forms import ProcessForm
from . import process
from django.core.paginator import Paginator
from django.template.defaulttags import register
import csv
from users.auth.decorators import  HandelError , error_decorator

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def lower(value): # Only one argument.
    """Converts a string into all lowercase"""
    return value.lower()

@register.filter(name='zip')
def zip_lists(a, b):
  return zip(a, b)


class UserFilesView(LoginRequiredMixin, ListView):
    template_name = 'csvdata/userfiles.html'
    def get_context_data(self):
        context = super(UserFilesView, self).get_context_data()
        data =  BaseData.objects.filter(user=self.request.user)
        context["base_files"] = data
        return context
    
    def get_queryset(self):
        data = BaseData.objects.filter(user=self.request.user)
        return data

    def file_checkout(self, df):
        count_null = df.isnull().values.sum().sum()
        count_row, count_col = df.shape
        dupnum = df.duplicated().any().sum()
        return  {
            "count_row":count_row,
             "count_col":count_col,
              "count_null":count_null,
              "duplicate_num":dupnum,
              "df_colmns":list(df),
              "coltype_dict" : dict(df.dtypes),
              }



ProcessDict = dict([(name, cls) for name, cls in process.__dict__.items() if isinstance(cls, type)])


class BaseFileView(LoginRequiredMixin, View):
    form_class =  ProcessForm
    template_name = 'csvdata/filedetails.html'
    @HandelError.error_decorator
    def get(self, request, *args, **kwargs):
        id = kwargs["pk"]
        saved_data = self.saved_data(id)
        df = self.get_or_update_df(saved_data)
        form = self.form_class()
        page_number = request.GET.get('page')
        index_pages , columns = self.pageing(page_number, df)
        context = {
            'obj_id':id,
            'form': form,
            'col_type_dict': dict(df.dtypes),
            'columns':columns,
            'index_pages':index_pages,
            'hasnull':self.hasnull(df),
            'hasduplicated':self.hasduplicated(df),
            'has_more_savedata':self.has_more_savedata(saved_data),
        }
        return render(request, self.template_name, context)

    @HandelError.error_decorator
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
            print("\n TheProcess")
            print(TheProcess)
            THeClass = ProcessDict[TheProcess]
            result = THeClass(**kwargs)
            if result.df_empty():
                print("\n TheClass is empty \n Worked ")
                ctxt["empty_df"] = "the last action cases empty data frame so its ignored"

        else:
            ctxt['form'] = process_form
        ctxt['obj_id'] = kwargs["pk"]
        return render(request, self.template_name, ctxt)

    def get_or_update_df(self, saved_data, df=False):
        if not df :
            df = self.read_file(saved_data)
        return df

    def saved_data(self,id):
        basedata= BaseData.objects.get(id=id)
        saved_data = SaveData.objects.filter(data_model=basedata).order_by("-date")
        return saved_data

    def read_file(self, saved_data):
        last_saved_data = saved_data[0]
        data = StringIO(last_saved_data.saved_data)
        df = pd.read_csv(data, sep=",")
        return df

        

    def hasnull(self, df):
        return df.isnull().values.any()


    def hasduplicated(self, df):
        return df.duplicated().any()


    def has_more_savedata(self, saved_data):
        if len(saved_data) > 1:
            return True
        return False


    def pageing(self, page_number, df) :
        df_split = df.to_dict('split')
        index, columns, data  = df_split['index'], df_split['columns'], df_split['data']
        index_pages = list(zip(index, data))
        paginator = Paginator(index_pages, 15) 
        page_number = page_number
        page_obj = paginator.get_page(page_number)
        return page_obj, columns


@login_required(login_url='login')
@error_decorator
def deletefile(request,  id):
    user = request.user
    print("\n id \n ")
    print(id)
    data_obj = BaseData.objects.get(id=id)
    if user == data_obj.user:
        data_obj.delete()
    return redirect(reverse('user-files'))

@login_required(login_url='login')
@error_decorator
def deleteSelected(request):
    user = request.user
    base_data_ids = request.POST.getlist('ids[]')
    for id in base_data_ids:
        data_obj = BaseData.objects.get(id=id)
        if user == data_obj.user:
            data_obj.delete()
    return redirect(reverse('user-files'))




@login_required(login_url='login')
@error_decorator
def export(request, *args, **kwargs) :
    id = kwargs["pk"]
    basedata= BaseData.objects.get(id=id)
    last_saved_data = SaveData.objects.filter(data_model=basedata).order_by("-date")[0]
    data = StringIO(last_saved_data.saved_data)
    df = pd.read_csv(data, sep=",")
    filename = basedata.file_name.split('.')[0]
    file_type = request.GET['type']

    if file_type == 'csv':
        content_type = 'text/csv'
        extension = 'csv'
    elif file_type == 'excel':
        content_type = 'vnd.ms-excel'
        extension = 'xlsx'
    else:
        return HttpResponse({'error_not_authorized'})


    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}.{extension}"'
    writer = csv.writer(response)
    writer.writerow([column for column in df.columns])
    writer.writerows(df.values.tolist())
    return response
