from django.urls import path, re_path
from .views import CsvFileView
urlpatterns = [
    path('get-data/', CsvFileView.as_view(), name='get-data'),
]
