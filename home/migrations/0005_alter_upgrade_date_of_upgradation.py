# Generated by Django 3.2.8 on 2021-11-28 20:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20211128_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upgrade',
            name='date_of_upgradation',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
