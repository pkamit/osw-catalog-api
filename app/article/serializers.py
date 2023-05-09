"""
Serializer for article api
"""
from rest_framework import serializers
#from drf_writable_nested import WritableNestedModelSerializer

from core.models import (
    Article,
    Category,
)

class CategorySerializer(serializers.ModelSerializer):
    " Serializers for Category"

    class Meta:
        model = Category
        fields = ['id' , 'name']
        read_only_fields = ['id']


class ArticleSerializer(serializers.ModelSerializer):
    """ Serializer for articleS"""
    categories = CategorySerializer(many=True, required=False)
    class Meta:
        model = Article
        fields = [
            'id', 'title', 'short_description', 'price', 'stock' , 'categories' , 'image'
        ]
        read_only_fields = ['id']

    def _get_or_create_categories(self, categoires, article):
        """ Handle getting or creating tags as needed"""
        auth_user = self.context['request'].user
        for category in categoires:
            category_obj , created = Category.objects.get_or_create(
                user=auth_user,
                **category
            )
            article.categories.add(category_obj)

    def create(self, validated_data):
        """ Creat a article."""
        categories = validated_data.pop('categories' , [])
        article = Article.objects.create(**validated_data)
        self._get_or_create_categories(categories , article)
        return article

    def update(self, instance, validated_data):
        """ Update article."""
        categories = validated_data.pop('categories' , None)
        if categories is not None:
            instance.categories.clear()
            self._get_or_create_categories(categories , instance)

        for attr , value in validated_data.items():
            setattr(instance , attr , value)
        instance.save()
        return instance

class ArticleDetailSerializer(ArticleSerializer):
    """ Extending detail page"""
    class Meta(ArticleSerializer.Meta):
        fields = ArticleSerializer.Meta.fields+['description', 'image']


class ArticleImageSerializer(serializers.ModelSerializer):
    """ Serializer for uploading images to article"""

    class Meta:
        model =  Article
        fields  =  ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required': 'Ture'}}

class ArticleNewImageSerializer(serializers.ModelSerializer):
    """ Serializer for uploading images to article"""

    class Meta:
        model =  Article
        fields  =  ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required': 'Ture'}}



