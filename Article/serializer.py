import uuid
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from Article.models import Article, Category, ArticleImages


class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']


class ArticleImageModelSerializer(serializers.ModelSerializer):
    image = serializers.CharField()

    class Meta:
        model = ArticleImages
        fields = ['id', 'image']


class ArticleModelSerializer(serializers.ModelSerializer):
    article_images = ArticleImageModelSerializer(many=True)

    class Meta:
        model = Article
        fields = [
            'id', 'category', 'title',
            'text', 'created_at',
            'article_images']
        read_only_fields = ('created_at',)

    def create(self, validated_data):
        bulk_create_array = []
        article_images = validated_data.pop('article_images')
        article = Article.objects.create(**validated_data)

        if article_images:
            for image in article_images:
                bulk_create_array.append(
                    ArticleImages(article=article, **image))
            if bulk_create_array:
                ArticleImages.objects.bulk_create(bulk_create_array)
        return article

    def update(self, instance, validated_data):
        image_list = set()
        bulk_update_array = []
        bulk_create_array = []

        article_images_data = self.initial_data.get('article_images')
        article_images = {image.id: image for image in instance.article_images.all()}

        instance.title = validated_data.get('title', instance.title)
        instance.category = validated_data.get('category', instance.category)
        instance.text = validated_data.get('text', instance.text)
        instance.save()

        if article_images_data:
            for image in article_images_data:
                if 'id' in image:
                    image_object = article_images.get(uuid.UUID(image['id']))
                    if image_object:
                        image_object.image = image.get('image', image_object.image)
                        image_list.add(image_object.id)
                        bulk_update_array.append(image_object)
                    else:
                        bulk_create_array.append(
                            ArticleImages(
                                article=instance,
                                image=image.get('image')
                            )
                        )

            if bulk_create_array:
                ArticleImages.objects.bulk_create(bulk_create_array)
            if bulk_update_array:
                ArticleImages.objects.bulk_update(bulk_update_array, ['image'])

            image_id_for_delete = set()
            for image_id in article_images.keys():
                if image_id not in image_list:
                    image_id_for_delete.add(image_id)

            if image_id_for_delete:
                ArticleImages.objects.filter(pk__in=image_id_for_delete).delete()

        return instance


class DestroyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id']
