# Generated by Django 4.0.5 on 2022-06-19 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashflow', '0005_alter_client_cod_fiscale_alter_supplier_cod_fiscale'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='doc_num',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
    ]