# Generated by Django 3.2.8 on 2021-12-03 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_alter_upgrade_upgraded_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upgrade',
            name='date_of_upgradation',
            field=models.DateTimeField(null=True),
        ),
    ]