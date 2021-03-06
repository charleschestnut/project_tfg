# Generated by Django 2.2.5 on 2020-04-09 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0013_auto_20200328_1607'),
    ]

    operations = [
        migrations.CreateModel(
            name='BadWord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='labourrequest',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=4, null=True),
        ),
    ]
