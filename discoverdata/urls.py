from django.urls import path, re_path
from .views import FilesTableView, StreamlitView, EndSession  ,FileApi 


urlpatterns = [
    path('files/', FilesTableView.as_view(), name='files-table'),
    path('streamlit/<int:pk>/', StreamlitView.as_view(), name='streamlit-frame'),
    path('end-ses/<int:pk>/', EndSession.as_view(), name='end-sessions'),

    # path('basefile-details/<int:pk>/', BaseFileView.as_view(), name='basefile-details'),
    # path('test/<int:pk>/', test , name='test'),

    # _________________________ API _________________________


    path('rest-api-file/', FileApi.as_view(), name='rest-api-file'),

]
