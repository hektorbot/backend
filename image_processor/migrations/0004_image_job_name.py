# Generated by Django 2.2 on 2019-05-04 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image_processor', '0003_image_job_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='job_name',
            field=models.CharField(default=False, max_length=255),
        ),
    ]
