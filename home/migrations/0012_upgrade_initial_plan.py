# Generated by Django 3.2.8 on 2021-12-03 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_alter_upgrade_date_of_upgradation'),
    ]

    operations = [
        migrations.AddField(
            model_name='upgrade',
            name='initial_plan',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
