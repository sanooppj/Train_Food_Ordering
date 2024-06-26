# Generated by Django 5.0.4 on 2024-04-09 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='address',
            new_name='city',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='customer',
            name='country',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='customer',
            name='state',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
