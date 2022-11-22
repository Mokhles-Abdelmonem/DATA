from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DetailView, UpdateView,View,DeleteView
from django.urls import reverse 
from io import StringIO
import pandas as pd
import subprocess
import pyarrow as pa
import pyarrow.csv as csv
from .models import  BaseData, SaveData
from users.auth.decorators import  HandelError , error_decorator
import jwt , datetime

from rest_framework import viewsets


# Create your views here.


class FilesTableView(LoginRequiredMixin, ListView):
    template_name = 'csvdata/filestable.html'
    def get_context_data(self):
        context = super(FilesTableView, self).get_context_data()
        data =  BaseData.objects.filter(user=self.request.user)
        context["base_files"] = data
        return context

    def get_queryset(self):
        data = BaseData.objects.filter(user=self.request.user)
        return data




class StreamlitView(LoginRequiredMixin, View):
    template_name = 'csvdata/streamlit_frame.html'
    @HandelError.error_decorator
    def get(self, request, *args, **kwargs):
        id = kwargs.pop("pk")
        basedata = BaseData.objects.get(id=id)
        
        file_payload = {
            'id': id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload=file_payload, key='file_Key', algorithm='HS256')

        context = {"file_id":id,"token":token}
        return render(request, self.template_name, context)






class EndSession(LoginRequiredMixin, View):
    @HandelError.error_decorator
    def get(self, request, *args, **kwargs):
        file_id = kwargs.pop("pk")
        basedata= BaseData.objects.get(id=file_id)
        return redirect("/discoverdata/files/")





# available_ports = range(8501,9501)

# class StreamlitView(LoginRequiredMixin, View):
#     template_name = 'csvdata/streamlit_frame.html'
#     @HandelError.error_decorator
#     def get(self, request, *args, **kwargs):
#         id = kwargs.pop("pk")
#         basedata= BaseData.objects.get(id=id)
#         last_saved_data = SaveData.objects.filter(data_model=basedata).order_by("-date")[0]
#         file_path = str(basedata.base_file)
#         file_path_parts = file_path.split('.')
#         file_name = file_path_parts[0]
#         extention = file_path_parts[1]
#         if extention in ['xlsx', 'xls','ods'] :
#             file_path = f"{file_name}.csv"
#         if StreamlitPort.objects.filter(basedata=basedata).exists() :
#             port_obj =  StreamlitPort.objects.get(basedata=basedata)
#             port_number = port_obj.port_number
#         else:
#             with open(file_path, "w+", encoding='utf-8') as file:
#                 file.write(last_saved_data.saved_data)
            
#             streamlit_ports = StreamlitPort.objects.all()
#             live_ports = []
#             if streamlit_ports :
#                 live_ports = [port.port_number for port in streamlit_ports]
#             ports_available = list(set(available_ports) - set(live_ports))
#             port_number = ports_available[0]
#             port_obj =  StreamlitPort.objects.create(
#                 basedata=basedata,
#                 port_number=port_number,
#                 )
#             cmd = f'streamlit run discoverdata/streamlitapp.py --server.port {port_number} --server.headless true'
#             result = subprocess.Popen(cmd, shell=True)
#         context = {"file_path":file_path, "port_number":port_number}
#         return render(request, self.template_name, context)





# _________________________ API _________________________



from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import FileTokenSerializer

class FileApi(APIView):
    serializer_class = FileTokenSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.data["token"]
        print("\n token  \n ")
        print(token)
        decode_token = jwt.decode(token, key='file_Key', algorithms=['HS256'])
        basedata = BaseData.objects.get(id=decode_token['id'])
        saved_data = SaveData.objects.filter(data_model=basedata).order_by("-date")[0]
        
        return Response({'data':saved_data.saved_data})