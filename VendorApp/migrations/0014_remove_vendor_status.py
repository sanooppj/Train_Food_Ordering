# Generated by Django 5.0.4 on 2024-04-12 16:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("VendorApp", "0013_remove_food_status_vendor_status"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="vendor",
            name="status",
        ),
    ]
