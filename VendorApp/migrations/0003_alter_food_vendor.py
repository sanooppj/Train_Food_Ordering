# Generated by Django 5.0.4 on 2024-04-10 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VendorApp', '0002_food'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='vendor',
            field=models.CharField(max_length=200, null=True),
        ),
    ]