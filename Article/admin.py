from django.contrib import admin
from Article.models import (
    Article, ArticleImages, Category
)

# Register your models here.

admin.site.register(Category)
admin.site.register(Article)
admin.site.register(ArticleImages)
