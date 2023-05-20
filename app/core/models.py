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

class Attribute(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = '4. Attribute'
        indexes = [
            models.Index(fields=['name',]),


        ]

    def __str__(self):
        return self.name




class Article(models.Model):
    """ Article object."""
    VARIANTS = (
        ('None', 'None'),
        ('Size', 'Size'),
        ('Color', 'Color'),
        ('Size-Color', 'Size-Color')
    )

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
    variant=models.CharField(max_length=10,choices=VARIANTS, default='None')
   # attributes_new = models.ManyToManyField(AttributeValue)

    class Meta:
        verbose_name_plural = '1. Article'
        indexes = [
            models.Index(fields=['title',]),
            models.Index(fields=['short_description',]),

        ]
    def __str__(self):
        return self.title

class AttributeValue(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = '5. Attribute Value'
        indexes = [
            models.Index(fields=['value',]),


        ]

    def __str__(self):
        return self.value

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

""" New category Model"""

class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class PAttribute(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    attributes = models.ManyToManyField(PAttribute, through='ProductAttribute')

    def __str__(self):
        return self.title


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute = models.ForeignKey(PAttribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.product.title} - {self.attribute.name}: {self.value}"


""" Multistep forms"""
class personal(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return self.name

class professional(models.Model):
    designation = models.CharField(max_length=100)
    organization =  models.CharField(max_length=100)
    place = models.CharField(max_length=100)

    def __str__(self):
        return self.designation

class orderdetails(models.Model):
    typeofproducts = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.typeofproducts


