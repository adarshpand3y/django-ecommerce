# Generated by Django 3.1.3 on 2021-06-17 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0016_auto_20210617_2137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address1',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='order',
            name='address2',
            field=models.CharField(default='', max_length=100),
        ),
    ]