# Generated by Django 3.2.8 on 2021-12-27 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0007_alter_customerpaymentdetail_fees_taken'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customerpaymentdetail',
            name='user',
        ),
        migrations.AddField(
            model_name='customerpaymentdetail',
            name='user_email',
            field=models.EmailField(max_length=255, null=True),
        ),
    ]
