from django.urls import path
from rest_framework import routers

from Article.views import (
    CategoryAPIView,
    ArticleListAPIView,
    ArticleCreateAPIView,
    ArticleDetailAPIView,
    CategoryDetailAPIView
)

router = routers.DefaultRouter()
router.register(r'category', CategoryAPIView, basename='category-list-create')
router.register(r'category/detail', CategoryDetailAPIView, basename='category-detail')
router.register(r'detail', ArticleDetailAPIView, basename='category-detail')
urlpatterns = router.urls

urlpatterns += [
    path("list", ArticleListAPIView.as_view()),
    path("create", ArticleCreateAPIView.as_view()),
]
