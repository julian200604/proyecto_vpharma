# Generated by Django 5.1.1 on 2024-10-23 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_remove_order_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='city',
            field=models.CharField(default='escribe tu ciudad', max_length=100, verbose_name='Ciudad - Municipio'),
        ),
    ]
