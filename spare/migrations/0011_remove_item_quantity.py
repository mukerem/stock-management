# Generated by Django 2.1.10 on 2019-08-29 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spare', '0010_auto_20190829_1432'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='quantity',
        ),
    ]