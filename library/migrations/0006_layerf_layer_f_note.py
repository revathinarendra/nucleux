# Generated by Django 4.2.4 on 2024-12-24 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_alter_layerf_layer_f_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='layerf',
            name='layer_f_note',
            field=models.TextField(blank=True),
        ),
    ]
