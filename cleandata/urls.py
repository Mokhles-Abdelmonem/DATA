from django.urls import path, re_path
from .views import UserFilesView, BaseFileView


urlpatterns = [
    path('files/', UserFilesView.as_view(), name='user-files'),
    path('basefile-details/<int:pk>/', BaseFileView.as_view(), name='basefile-details'),


    # path('<int:pk>/drop-col/<str:column>/',dropColumn, name='drop-column'),
    # path('<int:pk>/drop-row-null/<str:column>/',dropNaInCol, name='drop-null-rows'),
    # path('<int:pk>/drop-null/<int:axis>/',dropNaAll, name='drop-all-nan'),
    # path('basefile-details/<int:pk>/replace-null/<str:fillnull>/',replaceNaAll, name='replace-all-nan'),
    # path('basefile-details/<int:pk>/replace-null/<str:fillnull>/<str:column>/',fillNaInCol, name='replace-col-nan'),
    # path('basefile-details/<int:pk>/split-col/<str:sep>/<str:column>/',splitCol, name='split-col'),

]
