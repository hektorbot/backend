# Generated by Django 2.2 on 2019-05-14 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image_processor', '0003_auto_20190514_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='input_file',
            field=models.ImageField(upload_to='%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='image',
            name='neural_output_file',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='neural_style/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='image',
            name='style_file',
            field=models.ImageField(upload_to='%Y/%m/%d/'),
        ),
    ]
