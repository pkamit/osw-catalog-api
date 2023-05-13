"""
Database models.
"""
import uuid
import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

def article_image_file_path(instance, filename):
    """ Generate file path for new article image"""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'
    return os.path.join('uploads', 'article', filename)

class UserManager(BaseUserManager):
    """ Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """ create save and return a new user."""
        if not email:
           raise ValueError('User lshould have email field')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """ crate and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    """ User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

class Article(models.Model):
    """ Article object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255 , default='')
    short_description=models.CharField(max_length=255, default='')
    price= models.DecimalField(max_digits=5, decimal_places=2, default='0.00')
    description= models.TextField(blank=True)
    stock=models.CharField(max_length=255, blank=True)
    categories= models.ManyToManyField('Category')
    image = models.ImageField(null=True, upload_to=article_image_file_path)
    attributes= models.ManyToManyField('AttributeVariants')
   # uploaded_images = models.ManyToManyField('ArticleImage', related_name='+')

    class Meta:
        verbose_name_plural = '1. Article'
        indexes = [
            models.Index(fields=['title',]),
            models.Index(fields=['short_description',]),

        ]
    def __str__(self):
        return self.title

class Category(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        )
    name=models.CharField(max_length=50)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = '4. Category'
        indexes = [
            models.Index(fields=['name',]),

        ]

    def __str__(self):
        return self.name

class AttributeVariants(models.Model):
    """ Article vairants model"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True
        )

    type = models.CharField(default=None, max_length=32, null=False)
    name = models.CharField(default=None, max_length=32, null=False)
    price = models.DecimalField(max_digits=5, decimal_places=2, default='0.00')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = '2. Article Attributes'
        indexes = [
            models.Index(fields=['type',]),

        ]

    def __str__(self):
        return self.name

class ArticleImage(models.Model):
    """ Article images"""
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=article_image_file_path)

    class Meta:
        verbose_name_plural = '3. Article Image'

    # def __str__(self):
        # return "%s" % (self.article.title)
