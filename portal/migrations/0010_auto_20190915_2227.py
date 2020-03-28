# Generated by Django 2.2.5 on 2019-09-15 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0009_auto_20190915_2214'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banning',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_datetime', models.DateField(auto_now_add=True)),
                ('description', models.TextField(max_length=1000)),
                ('finish_datetime', models.DateField()),
            ],
        ),
        migrations.RemoveField(
            model_name='clientrating',
            name='isBanned',
        ),
        migrations.RemoveField(
            model_name='labourrequest',
            name='isBanned',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='isBanned',
        ),
        migrations.RemoveField(
            model_name='workerrating',
            name='isBanned',
        ),
        migrations.AddField(
            model_name='clientrating',
            name='banning',
            field=models.OneToOneField(null=True, on_delete=True, to='portal.Banning'),
        ),
        migrations.AddField(
            model_name='labourrequest',
            name='banning',
            field=models.OneToOneField(null=True, on_delete=True, to='portal.Banning'),
        ),
        migrations.AddField(
            model_name='profile',
            name='banning',
            field=models.OneToOneField(null=True, on_delete=True, to='portal.Banning'),
        ),
        migrations.AddField(
            model_name='workerrating',
            name='banning',
            field=models.OneToOneField(null=True, on_delete=True, to='portal.Banning'),
        ),
    ]