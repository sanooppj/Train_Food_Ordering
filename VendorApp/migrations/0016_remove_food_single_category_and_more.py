# Generated by Django 4.2.5 on 2024-04-13 07:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("VendorApp", "0015_food_single"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="food_single",
            name="category",
        ),
        migrations.RemoveField(
            model_name="food_single",
            name="region",
        ),
        migrations.RemoveField(
            model_name="food_single",
            name="type",
        ),
    ]
