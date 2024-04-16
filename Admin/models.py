from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User



class food_items(models.Model):
    name=models.CharField(max_length=50)
    image = models.ImageField(upload_to='images')

class location(models.Model):
    region_name=models.CharField(max_length=50)



class contact_Db(models.Model):
    username=models.CharField(max_length=20,null=True,blank=True)
    name = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=30, null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    subject = models.CharField(max_length=20, null=True, blank=True)
    message = models.CharField(max_length=20, null=True, blank=True)






    
 
   


