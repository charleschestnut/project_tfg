# Generated by Django 2.2.5 on 2019-09-14 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0006_administrator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='administrator',
            name='id_worker',
            field=models.PositiveIntegerField(unique=True),
        ),
    ]