# Generated by Django 3.2.8 on 2021-12-20 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0004_alter_customerpaymentdetail_paid'),
    ]

    operations = [
        migrations.CreateModel(
            name='VisitorCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.TextField(null=True)),
                ('date_of_record', models.DateTimeField(null=True)),
            ],
        ),
    ]
