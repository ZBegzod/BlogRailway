from django.urls import path, include
from rest_framework import routers

from Article.views import (
    ArticleListAPIView, ArticleCreateAPIView,
    ArticleUpdateAPIView, ArticleDestroyAPIView,
    CategoryAPIView, CategoryDetailAPIView

)

router = routers.SimpleRouter()
router.register(r'category', CategoryAPIView, basename='category-list-create')
router.register(r'category/detail', CategoryDetailAPIView, basename='category-detail')
urlpatterns = router.urls

urlpatterns += [
    path("list", ArticleListAPIView.as_view()),
    path("create", ArticleCreateAPIView.as_view()),
    path("update/<uuid:pk>", ArticleUpdateAPIView.as_view()),
    path("delete/<uuid:pk>", ArticleDestroyAPIView.as_view())
]
