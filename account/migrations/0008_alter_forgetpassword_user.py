# Generated by Django 3.2.8 on 2022-01-02 23:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_alter_forgetpassword_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forgetpassword',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
