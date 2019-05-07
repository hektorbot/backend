# Generated by Django 2.2 on 2019-05-07 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('job_id', models.CharField(default='', max_length=255)),
                ('job_name', models.CharField(default='', max_length=255)),
                ('input_file', models.FileField(upload_to='%Y/%m/%d/')),
                ('style_file', models.FileField(upload_to='%Y/%m/%d/')),
                ('neural_output_file', models.FileField(blank=True, default=None, null=True, upload_to='neural_style/%Y/%m/%d/')),
                ('has_failed', models.BooleanField(default=False)),
            ],
        ),
    ]
