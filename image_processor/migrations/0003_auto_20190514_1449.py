# Generated by Django 2.2 on 2019-05-14 14:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('image_processor', '0002_auto_20190512_2240'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='job_id',
        ),
        migrations.RemoveField(
            model_name='image',
            name='job_name',
        ),
        migrations.RemoveField(
            model_name='image',
            name='st_content_weight_blend',
        ),
        migrations.RemoveField(
            model_name='image',
            name='st_iterations',
        ),
        migrations.RemoveField(
            model_name='image',
            name='st_pooling',
        ),
        migrations.RemoveField(
            model_name='image',
            name='st_preserve_colors',
        ),
        migrations.RemoveField(
            model_name='image',
            name='st_style_layer_weight_exp',
        ),
    ]
