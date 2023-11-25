import uuid
from django.db import models
from ckeditor.fields import RichTextField


# Create your models here.

class Category(models.Model):
    id = models.UUIDField(
        db_index=True,
        default=uuid.uuid4, unique=True,
        primary_key=True, editable=False)
    title = models.CharField(max_length=255)

    class Meta:
        indexes = [
            models.Index(fields=[
                'id', 'title'
            ])
        ]

    def __str__(self):
        return self.title


class Article(models.Model):
    id = models.UUIDField(
        db_index=True,
        default=uuid.uuid4, unique=True,
        primary_key=True, editable=False)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='article_categories')
    title = models.CharField(max_length=255, db_index=True)
    text = RichTextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=[
                'id', 'created_at', 'title'
            ])
        ]

    def __str__(self):
        return self.title


class ArticleImages(models.Model):
    id = models.UUIDField(
        db_index=True,
        default=uuid.uuid4, unique=True,
        primary_key=True, editable=False)
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='article_images')
    images = models.ImageField(upload_to='images/articles')

    class Meta:
        indexes = [
            models.Index(fields=['id'])
        ]

    def __str__(self):
        return self.article
