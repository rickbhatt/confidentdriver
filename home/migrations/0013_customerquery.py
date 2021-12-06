# Generated by Django 3.2.8 on 2021-12-06 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_upgrade_initial_plan'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerQuery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('phone_no', models.CharField(max_length=10, null=True)),
                ('question', models.CharField(max_length=200, null=True)),
            ],
        ),
    ]