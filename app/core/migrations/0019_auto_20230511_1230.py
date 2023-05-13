# Generated by Django 3.2.19 on 2023-05-11 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_alter_articleimage_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': '4. Category'},
        ),
        migrations.AddField(
            model_name='article',
            name='uploaded_images',
            field=models.ManyToManyField(related_name='_core_article_uploaded_images_+', to='core.ArticleImage'),
        ),
    ]