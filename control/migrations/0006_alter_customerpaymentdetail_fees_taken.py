# Generated by Django 3.2.8 on 2021-12-25 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0005_visitorcount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerpaymentdetail',
            name='fees_taken',
            field=models.IntegerField(max_length=5, null=True),
        ),
    ]
