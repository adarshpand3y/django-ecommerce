# Generated by Django 3.1.3 on 2021-06-29 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0022_auto_20210629_2106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='val',
            field=models.FloatField(blank=True, help_text='Do NOT change this field. It gets updated automatically.'),
        ),
    ]
