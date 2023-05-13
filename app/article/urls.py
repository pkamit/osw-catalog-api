"""
url mappings for the article api
"""
from django.urls import (
    path,
    include,
)
from rest_framework.routers import DefaultRouter

from article import views

router = DefaultRouter()
router.register('articles', views.ArticleViewSet)
router.register('categories', views.CategoryViewSet)
router.register('attributevariants', views.AttributeVariantsViewSet)
app_name = 'article'

urlpatterns = [
    path('', include(router.urls)),
]