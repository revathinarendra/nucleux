# Generated by Django 4.2.4 on 2024-12-11 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_alter_layerd_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='layera',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='layerb',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='layerc',
            name='slug',
            field=models.SlugField(blank=True, max_length=300, unique=True),
        ),
    ]
