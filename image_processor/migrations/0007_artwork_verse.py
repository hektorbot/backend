# Generated by Django 2.2.1 on 2019-06-24 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image_processor', '0006_artwork_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='artwork',
            name='verse',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
    ]