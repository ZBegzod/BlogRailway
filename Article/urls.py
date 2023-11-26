from django.urls import path
from Article.views import (
    ArticleListAPIView, ArticleCreateAPIView,
    ArticleUpdateAPIView, ArticleDestroyAPIView
)

urlpatterns = [
    path("list", ArticleListAPIView.as_view()),
    path("create", ArticleCreateAPIView.as_view()),
    path("update/<uuid:pk>", ArticleUpdateAPIView.as_view()),
    path("delete/<uuid:pk>", ArticleDestroyAPIView.as_view()),
]
