# Generated by Django 5.1.4 on 2025-03-11 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_app', '0007_alter_transaction_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='currency',
            field=models.CharField(default='USD', max_length=10),
        ),
    ]
