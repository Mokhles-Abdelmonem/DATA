from django.urls import path, re_path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', Dashboard.as_view(), name='dashboard'),
    path('register/', SignUpView2.as_view(), name='register'),
    path('login/', LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('pass/', ChangePassword.as_view(), name='ch_pass'),
    path('settings/', UserSettings.as_view(), name='settings'),
    path('issuse/', IssuseReportView.as_view(), name='report-issuse'),
    path('mokhles-portfolio/', PortfolioView.as_view(), name='portfolio'),
]
