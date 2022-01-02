# Generated by Django 2.1.10 on 2019-08-29 12:09

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spare', '0007_auto_20190828_0900'),
    ]

    operations = [
        migrations.AddField(
            model_name='sell',
            name='purchase_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=20, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
        migrations.AddField(
            model_name='sell',
            name='selling_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=20, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
        migrations.AddField(
            model_name='sell',
            name='vat',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='loan',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=20),
        ),
    ]