# Generated by Django 4.0.5 on 2022-07-07 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashflow', '0008_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
