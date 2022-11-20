from django.urls import path, re_path
from .views import FilesTableView, StreamlitView, KillPort 


urlpatterns = [
    path('files/', FilesTableView.as_view(), name='files-table'),
    path('streamlit/<int:pk>/', StreamlitView.as_view(), name='streamlit-frame'),
    path('kill-port/<int:num>/', KillPort.as_view(), name='kill-port'),

    # path('basefile-details/<int:pk>/', BaseFileView.as_view(), name='basefile-details'),
    # path('test/<int:pk>/', test , name='test'),
]
