# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include  # add this

urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    # path("", include("apps.authentication.urls")), # Auth routes - login / register

    # ADD NEW Routes HERE

    # Leave `Home.Urls` as last the last line
    # path("", include("apps.home.urls")),


    path("", include("users.urls")),
    path("collectdata/", include("collectdata.urls")),
    path("cleandata/", include("cleandata.urls")),
    path("discoverdata/", include("discoverdata.urls")),
]
