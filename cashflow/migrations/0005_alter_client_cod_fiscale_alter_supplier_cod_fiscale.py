# Generated by Django 4.0.5 on 2022-06-19 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashflow', '0004_alter_invoice_client_alter_invoice_payment_days_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='cod_fiscale',
            field=models.CharField(blank=True, max_length=16),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='cod_fiscale',
            field=models.CharField(blank=True, max_length=16),
        ),
    ]
