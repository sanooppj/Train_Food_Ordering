# Generated by Django 5.0.4 on 2024-04-10 15:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VendorApp', '0005_alter_food_vendor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='vendor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='VendorApp.vendor'),
        ),
    ]
