from django.urls import path
from . import views

app_name = 'multistepform'

urlpatterns = [
    path('', views.home, name='home'),
    path('formsumission', views.msfsubmission.as_view(), name='msfsubmission')
]
