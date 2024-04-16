from django.core.validators import RegexValidator
from django.db import models

# Create your models here.

class Vendor(models.Model):

    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    description = models.CharField(max_length=200,null=True)
    address = models.CharField(max_length=200,null=True)
    contact = models.IntegerField(validators=[RegexValidator(r'^\d{10}$')], null=True)
    location = models.CharField(max_length=100,blank=True, null=True)
    website = models.URLField(null=True)
    logo = models.ImageField(upload_to='images',null=True,blank=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)




class Food(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=500)
    image = models.ImageField(upload_to="images")
    description = models.CharField(max_length=500)
    region = models.CharField(max_length=50, null=True, blank=True)
    type = models.CharField(max_length=500, default="veg")

    def save(self, *args, **kwargs):
        # Using a transaction to ensure atomicity of the update process
        with transaction.atomic():
            if self.pk:  # Check if this is an update operation
                original = Food.objects.get(pk=self.pk)
                if original.name != self.name:
                    # Updating all related Food_single records if name changes
                    updated_count = Food_single.objects.filter(main_category=original.name, vendor=self.vendor).update(
                        main_category=self.name)
                    print(
                        f"Updated {updated_count} Food_single records' main_category from {original.name} to {self.name}")
            super().save(*args, **kwargs)  # Call the "real" save method

    def delete(self, *args, **kwargs):
        # Delete related Food_single items
        related_count = Food_single.objects.filter(main_category=self.name, vendor=self.vendor).count()
        Food_single.objects.filter(main_category=self.name, vendor=self.vendor).delete()
        print(f"Deleted {related_count} related Food_single items")
        super().delete(*args, **kwargs)  # Call the "real" delete method

class Food_single(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True)
    single_name = models.CharField(max_length=200)
    main_category =  models.CharField(max_length=500)
    image = models.ImageField(upload_to="images")
    price = models.PositiveIntegerField()
    description = models.CharField(max_length=500)
    average_rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)