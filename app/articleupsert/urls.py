""" URL mapping for article import and update"""

from django.urls import path

from . import views

app_name = 'articleupsert'

urlpatterns = [
    path('import', views.article_upsert , name='article_upsert' )
]
