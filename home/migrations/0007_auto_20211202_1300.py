# Generated by Django 3.2.8 on 2021-12-02 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20211202_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='date_of_acceptance',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='contract',
            name='date_of_expiration',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
