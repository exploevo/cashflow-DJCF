# Generated by Django 4.0.5 on 2022-07-22 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashflow', '0010_invoice_payed_alter_client_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='payed',
            field=models.BooleanField(default=0),
        ),
    ]