"""
Test for Article API.
"""
import os
import tempfile
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from PIL import Image
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Article

from article.serializers import ArticleSerializer

ARTICLES_URL = reverse('article:article-list')

def detail_url(article_id):
    """ create and return a article detail URL."""
    return reverse('article:article-detail', args=[article_id])

def image_upload_url(article_id):
    """ Cretae and return an Image uplaod Url"""
    return reverse('article:article-upload-image', args=[article_id])

def create_article(user, **params):
    """ Create and return a sample Article"""
    defaults = {
        'title': 'sample article title',
        'short_description': 'sample article short description',
        'price': Decimal('5.50'),
        'description': 'sample article long description',
        'stock':'1'
         }
    defaults.update(**params)

    article = Article.objects.create(user=user, **defaults)
    return article

def create_user(**params):
    """ create and return New user"""
    return get_user_model().objects.create_user(**params)


class PublicArticleAPITests(TestCase):
    """ Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """ Test auth is required to call API"""
        res = self.client.get(ARTICLES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateArticleAPITests(TestCase):
    """ test authentiocated api tests"""
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com' , password='test123')
        self.client.force_authenticate(self.user)

    def test_retrieve_articles(self):
        create_article(self.user)
        create_article(self.user)

        res = self.client.get(ARTICLES_URL)
        articles = Article.objects.all().order_by('-id')
        serializer = ArticleSerializer(articles, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data , serializer.data)

    def test_create_article(self):
        """ Test creating a Article"""
        payload = {
            'title': 'Sample article',
            'short_description': 'This is short description',
            'price': Decimal('10.26')
        }
        res = self.client.post(ARTICLES_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        article = Article.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(article, k), v)
        self.assertEqual(article.user, self.user)

    def test_partial_update(self):
        """ test partial update of a article"""
        original_short_description = 'This is sample short description'
        article = create_article(
            user=self.user,
            title='Sample article title',
            short_description=original_short_description
        )
        payload = {'title': 'new article title'}
        url=detail_url(article.id)
        res=self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        article.refresh_from_db()
        self.assertEqual(article.title, payload['title'])
        self.assertEqual(article.short_description, original_short_description)
        self.assertEqual(article.user, self.user)

    def test_full_update(self):
        """ Test full update of article"""
        article = create_article(
            user=self.user,
            title='Sample article title',
            short_description='sample short description',
            description='sample article description'
        )
        payload = {
            'title': 'New article title',
            'short_description': 'New sample short description',
            'description': 'New sample recipe description',
            'price': Decimal('16.50'),
        }
        url = detail_url(article.id)
        res = self.client.put(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        article.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(article, k), v)
        self.assertEqual(article.user, self.user)



class ImageUploadTests(TestCase):
    """ Test for image upload api"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'password123'
        )
        self.client.force_authenticate(self.user)
        self.article = create_article(user=self.user)

    def tearDown(self):
        self.article.image.delete()

    def test_upload_image(self):
        """ test uploading an image to a recipe"""
        url = image_upload_url(self.article.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            img = Image.new('RGB' , (10,10))
            img.save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {'image': image_file}
            res= self.client.post(url, payload, format='multipart')

        self.article.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.article.image.path))