# Generated by Django 4.2.11 on 2025-05-06 19:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0039_auto_20250505_1910'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('unprocessed', 'Необработанный'), ('confirmed', 'Подтверждённый'), ('assembled', 'Собран'), ('delivering', 'В доставке'), ('completed', 'Завершён')], db_index=True, default='unprocessed', max_length=20, verbose_name='статус'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0)], verbose_name='цена на момент заказа'),
        ),
    ]
