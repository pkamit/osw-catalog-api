"""
Serializer for article api
"""
from rest_framework import serializers
#from drf_writable_nested import WritableNestedModelSerializer

from core.models import (
    Article,
    Category,
    AttributeVariants,
    ArticleImage,
)

class CategorySerializer(serializers.ModelSerializer):
    " Serializers for Category"

    class Meta:
        model = Category
        fields = ['id' , 'name']
        read_only_fields = ['id']

class AttributeVariantsSerializer(serializers.ModelSerializer):
    """ Serializer for uploading images to article"""

    class Meta:
        model =  AttributeVariants
        fields  =  ['id', 'type', 'name' , 'price']
        read_only_fields = ['id', 'type']
       # extra_kwargs = {'type': {'required': 'True'}}

class ArticleImageSerializers(serializers.ModelSerializer):
    """ Serializer for article image"""

    class Meta:
        model = ArticleImage
        fields = '__all__'


class AttributeVariantsWithoutSerializer(serializers.ModelSerializer):
    """ Serializer for uploading images to article"""

    class Meta:
        model =  AttributeVariants
        fields  =  ['id', 'type',  'name' , 'price']
        read_only_fields = ['id' , 'type']
       # extra_kwargs = {'type': {'required': 'True'}}



class ArticleSerializer(serializers.ModelSerializer):
    """ Serializer for articleS"""
    categories = CategorySerializer(many=True, required=False)
    attributes = AttributeVariantsSerializer(many=True, required=False)

    images = ArticleImageSerializers(many=True, required=False)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'short_description', 'price', 'stock' , 'categories' ,
            'attributes' , 'images' , 'uploaded_images'
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

    def _get_or_create_attributes(self, attributes, article):
        """ Handle getting or creating tags as needed"""
        auth_user = self.context['request'].user
        for attribute in attributes:
            attribute_obj , created = AttributeVariants.objects.get_or_create(
                user=auth_user,
                **attribute
            )
            article.attributes.add(attribute_obj)

    def _get_or_create_images(self, images, article):
        """ Handle getting or creating tags as needed"""

        for attribute in images:
            attribute_obj , created = ArticleImage.objects.get_or_create(

                **attribute
            )
            ArticleImage.uploaded_images.add(attribute_obj)


    def create(self, validated_data):
        """ Creat a article."""
        categories = validated_data.pop('categories' , [])
        attributes = validated_data.pop('attributes' , [])
        uploaded_images = validated_data.pop('uploaded_images', [] )



        article = Article.objects.create(**validated_data)
        self._get_or_create_categories(categories , article)
        self._get_or_create_attributes(attributes , article)
        for image in uploaded_images:
            newArticleImage = ArticleImage.objects.create(article=article, image=image)
        return article

    def update(self, instance, validated_data):
        """ Update article."""
        categories = validated_data.pop('categories' , None)
        attributes = validated_data.pop('attributes' , None)
        uploaded_images = validated_data.pop('uploaded_images', None )

        if categories is not None:
            instance.categories.clear()
            self._get_or_create_categories(categories , instance)

        if attributes is not None:
            instance.attributes.clear()
            self._get_or_create_attributes(attributes , instance)

        if uploaded_images is not None:
            instance.uploaded_images.clear()
            article_image_model_instance = [ArticleImage(article=instance, images=image) for image in uploaded_images]
            uploaded_images.objects.bulk_create(
                article_image_model_instance
            )



        for attr , value in validated_data.items():
            setattr(instance , attr , value)
        instance.save()
        return instance

class ArticleDetailSerializer(ArticleSerializer):
    """ Extending detail page"""
    class Meta(ArticleSerializer.Meta):
        fields = ArticleSerializer.Meta.fields+['description', 'image' , 'attributes']


class ArticleImageSerializer(serializers.ModelSerializer):
    """ Serializer for uploading images to article"""

    class Meta:
        model =  Article
        fields  =  ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required': 'True'}}







