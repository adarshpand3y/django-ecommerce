# Generated by Django 3.1.3 on 2021-06-17 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='last_changed_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='order',
            name='ordered_at',
            field=models.DateTimeField(),
        ),
    ]