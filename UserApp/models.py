from django.db import models
from VendorApp.models import  *




from django.db import models

class Signup_db(models.Model):
    user_type_choices = [
        ('customer', 'customer'),
        ('vendor', 'vendor'),
    ]
    user_type = models.CharField(max_length=50, choices=user_type_choices, null=True)
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, null=True)
    password = models.CharField(max_length=100, null=True)
    is_approved = models.BooleanField(default=False)  # False means pending approval
    last_login = models.DateTimeField(null=True, blank=True)
    password_reset_token = models.CharField(max_length=100, blank=True, null=True)
    token_expiration = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({'approved' if self.is_approved else 'pending'})"





class Customer(models.Model):
    name=models.CharField(max_length=50)
    email = models.EmailField(max_length=255)
    mobile = models.IntegerField( validators=[RegexValidator(r'^\d{10}$')], null=True)
    age = models.IntegerField(null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='images', null=True)
    country = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)

class CartDb(models.Model):
    Username = models.CharField(max_length=100,null=True,blank=True)
    food = models.ForeignKey(Food_single, on_delete=models.CASCADE, related_name='cart_items', default=1)
    quantity = models.IntegerField(null=True,blank=True)
    price = models.IntegerField(null=True,blank=True)
    tprice = models.IntegerField(null=True,blank=True)


class BookingDb(models.Model):
    Username = models.CharField(max_length=100,null=True,blank=True)
    name = models.CharField(max_length=100, null=True)
    age = models.CharField(max_length=100, null=True)
    mobile_number = models.IntegerField( validators=[RegexValidator(r'^\d{10}$')], null=True)
    email = models.EmailField(max_length=255)
    date = models.DateField( blank=True,null=True)
    train_number = models.TextField( blank=True, null=True)
    compartment_number = models.TextField( blank=True, null=True)
    seat_number = models.TextField( blank=True, null=True)
    deliver_station = models.CharField( max_length=100,blank=True, null=True)
    
class Order(models.Model):
    STATUS = (
        ('Order Confirmed', 'Order Confirmed'),
        ('Order Processing', "Order Processing"),
        ('Out for delivery', "Out for delivery"),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )
    Username=models.CharField(max_length=100,null=True,blank=True)
    vendor_name= models.CharField(max_length=30,blank=True,null=True)
    booking = models.ForeignKey(BookingDb, on_delete=models.CASCADE)
    total_price = models.IntegerField(blank=True,null=True)
    shipping = models.IntegerField(blank=True,null=True)
    grand_total = models.IntegerField(blank=True,null=True)
    amount_to_be_paid = models.IntegerField(blank=True,null=True)
    is_deleted = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=50)
    order_status =models.CharField(max_length=50,choices=STATUS,default='Order Confirmed')
    created_at = models.DateTimeField(auto_now_add=True) 
    order_id = models.CharField(max_length=100, unique=True)  # Assuming order_id is a unique identifier for each order


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    vendor_name= models.CharField(max_length=30,blank=True,null=True)
    picture = models.ImageField(upload_to="Images", null=True, blank=True,)
    food_name = models.CharField(max_length=30,blank=True,null=True)
    quantity = models.IntegerField()
    price = models.IntegerField()
    total_price=models.IntegerField(null=True)


class Food_review_Db(models.Model):
    username = models.TextField(max_length=100)
    food = models.ForeignKey(Food_single, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review_text = models.TextField()
    reviewer_name = models.CharField(max_length=100)
    reviewer_image = models.ImageField(upload_to='reviewer_images', null=True, blank=True,
                                       default='Images/usericon1.jpg')

    created_at = models.DateTimeField(auto_now_add=True)

class Vendor_review_Db(models.Model):
    username = models.TextField(max_length=100)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review_text = models.TextField(max_length=100)
    reviewer_name = models.CharField(max_length=100)
    reviewer_image = models.ImageField(upload_to='reviewer_images', null=True, blank=True,
                                       default='Images/usericon.jpg')

    created_at = models.DateTimeField(auto_now_add=True)

