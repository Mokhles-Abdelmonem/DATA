from django.urls import path, re_path
from .views import UserFilesView, BaseFileView, DeleteFileView, export , deleteSelected


urlpatterns = [
    path('files/', UserFilesView.as_view(), name='user-files'),
    path('basefile-details/<int:pk>/', BaseFileView.as_view(), name='basefile-details'),
    path('delete/<int:pk>/', DeleteFileView.as_view() ,name='delete-data'),
    path('multi-delete/', deleteSelected, name="delete-multi-data"),
    path('export/<int:pk>/', export , name='export'),

]
