# Generated by Django 2.2 on 2019-05-05 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image_processor', '0004_image_job_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='job_id',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='image',
            name='job_name',
            field=models.CharField(default='', max_length=255),
        ),
    ]
