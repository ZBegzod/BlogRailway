from rest_framework import status
from .pagination import Pagination

from rest_framework import generics, viewsets
from Article.models import Article, Category
from rest_framework.response import Response

from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    UpdateModelMixin
)
from Article.serializer import (
    LoginSerializer,
    ArticleModelSerializer,
    CategoryModelSerializer
)
from .permissions import IsSuperOrReadOnly


class LoginAPIView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data, context={'request': self.request})
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            serializer.validated_data['refresh'] = str(refresh)
            serializer.validated_data['access'] = str(refresh.access_token)
            serializer.validated_data['username'] = user.username
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


# Create your views here.
class CategoryDetailAPIView(RetrieveModelMixin,
                            DestroyModelMixin,
                            UpdateModelMixin,
                            viewsets.GenericViewSet):
    queryset = Category.objects.all()
    permission_classes = [IsSuperOrReadOnly]
    serializer_class = CategoryModelSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        message = {'data': "category deleted successfully"}
        return Response(data=message, status=status.HTTP_204_NO_CONTENT)


class CategoryAPIView(ListModelMixin, CreateModelMixin,
                      viewsets.GenericViewSet):
    pagination_class = Pagination
    queryset = Category.objects.all()
    permission_classes = [IsSuperOrReadOnly]
    serializer_class = CategoryModelSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleListAPIView(generics.ListAPIView):
    queryset = Article.objects.all()
    pagination_class = Pagination
    serializer_class = ArticleModelSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.query_params.get('title')
        category = self.request.query_params.get('category')

        if title:
            queryset.filter(title__icontains=title)
        if category:
            queryset.filter(category=category)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        context = {'request': request}
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.serializer_class(page, many=True, context=context)
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(queryset, many=True, context=context)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ArticleCreateAPIView(generics.CreateAPIView):
    queryset = Article.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = ArticleModelSerializer

    def post(self, request, *args, **kwargs):
        context = {'request': request}
        serializer = self.serializer_class(data=request.data, context=context)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetailAPIView(RetrieveModelMixin,
                           DestroyModelMixin,
                           UpdateModelMixin,
                           viewsets.GenericViewSet):
    queryset = Article.objects.all()
    permission_classes = [IsSuperOrReadOnly]
    serializer_class = ArticleModelSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            self.get_object(), data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        article = self.get_object()
        if article.article_images.exists():
            article.article_images.delete()
        article.delete()
        message = 'constructor deleted successfully!'
        return Response(data={'message': message}, status=status.HTTP_204_NO_CONTENT)
