# Generated by Django 3.1.3 on 2021-06-10 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20210608_2059'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, help_text='Leave this parameter empty, it will get generated automatically.'),
        ),
    ]
