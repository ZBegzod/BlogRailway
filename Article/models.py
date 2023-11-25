from django.db import models
from ckeditor.fields import RichTextField


# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Article(models.Model):
    title = models.CharField(max_length=255)
    text = RichTextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ArticleImages(models):
    article = models.ForeignKey(Article, related_name='article_images', on_delete=models.CASCADE)
    images = models.ImageField(upload_to='images/articles/')

