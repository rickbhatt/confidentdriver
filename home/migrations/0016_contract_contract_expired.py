# Generated by Django 3.2.8 on 2021-12-11 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_alter_customerquery_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='contract_expired',
            field=models.BooleanField(default=False),
        ),
    ]
