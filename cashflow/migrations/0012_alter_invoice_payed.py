# Generated by Django 4.0.5 on 2022-07-22 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashflow', '0011_alter_invoice_payed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='payed',
            field=models.BooleanField(default=1),
        ),
    ]
