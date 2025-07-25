# airdrop/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('', RegisterView.as_view(), name='register'),
    path('export-csv/<str:wallet>', ExportCSVView.as_view()),
    ]
