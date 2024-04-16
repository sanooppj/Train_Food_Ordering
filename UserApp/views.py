from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Avg, Q
from django.shortcuts import render, redirect,get_object_or_404 ,redirect
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

from UserApp.models import *
from VendorApp.models import *
from UserApp.views import *
from Admin.views import *
from VendorApp.views import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import authenticate, login,logout
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
import razorpay
from django.views.decorators.csrf import csrf_exempt
import uuid









def login_page(request):
    return render(request, "login_page.html")


def signup_page(request):
    return render(request, "signup_page.html")



from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password
from .models import Signup_db  # Ensure you import your Signup_db model

def register_user(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        email = request.POST.get('email')
        name = request.POST.get('name')
        password = request.POST.get('password')
        c_password = request.POST.get('c_password')

        # Check if email or username exists
        email_exists = User.objects.filter(email=email).exists()
        username_exists = User.objects.filter(username=name).exists()

        if email_exists:
            try:
                existing_user_type = Signup_db.objects.get(email=email).user_type
                if existing_user_type != user_type:
                    pass  # Different user type can register
                else:
                    messages.error(request, 'An account with this email already exists!')
                    return redirect('signup_page')  # Adjust the redirect as needed
            except ObjectDoesNotExist:
                pass  # Signup_db does not have this email, unlikely scenario

        if username_exists:
            messages.error(request, 'An account with this username already exists!')
            return redirect('signup_page')  # Adjust the redirect as needed

        if password != c_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('signup_page')

        # Create User object
        user = User.objects.create_user(username=name, email=email, password=password)

        # Save additional data to Signup_db
        Signup_db.objects.create(user_type=user_type, username=name, email=email, password=make_password(password))

        messages.success(request, 'Account registered successfully!')
        return redirect('login_page')  # Adjust the redirect as needed

    return render(request, 'signup_page.html')

from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import login
from .models import Signup_db
from django.contrib.auth.hashers import check_password

def login_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user_type = request.POST.get('user_type')


        # Check if user is an admin
        if user_type == 'admin':
            superuser = User.objects.filter(email=email, is_superuser=True).first()
            if superuser and superuser.check_password(password):
                login(request, superuser)
                request.session['username'] = superuser.username  # Set session variable
                return redirect('admin_index_page')

        # Check if user is a customer or vendor
        try:
            user = Signup_db.objects.get(email=email, user_type=user_type)
        except Signup_db.DoesNotExist:
            user = None

        try:
            user = Signup_db.objects.get(email=email, user_type=user_type)
        except Signup_db.DoesNotExist:
            messages.error(request, 'No account found with these credentials.')
            return redirect('login_page')

        if user and check_password(password, user.password):
            if user_type == 'vendor' and not user.is_approved:
                # If user is a vendor and not approved, do not allow login
                messages.error(request, 'Your account is pending approval from an administrator.')
                return redirect('login_page')

            else:
                # Proceed with login for approved vendors and all customers
                login(request, user)  # Ensure you have configured your authentication backend
                request.session['Username'] = user.username
                request.session['Email'] = user.email
                request.session['Password'] = user.password
                messages.success(request, f'Successfully logged in as "{user.username}"')

                # Redirect based on user type
                if user_type == 'customer':
                    return redirect('Home_page')  # Redirect to customer dashboard
                elif user_type == 'vendor':
                    return redirect('vendor_index_page')  # Redirect to vendor dashboard
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('login_page')
    else:
        return redirect('login_page')



def user_logout(request):
    logout(request)
    return redirect('login_page')
    
@never_cache
def Home_page(request):
    try:
        vendor_profile = Vendor.objects.filter(name=request.session['Username'])
    except KeyError:
        vendor_profile = None
    location_names=location.objects.all()
    food=food_items.objects.all()
    data=food_items.objects.all()
    vendors = Vendor.objects.all()
    return render(request,"Home.html",{'data':data,'vendors':vendors,'location_names':location_names,'food':food,'vendor_profile':vendor_profile})



import random

def search_foods(request):
    food_items = None
    search_heading = "Search Results"  # Default heading

    if request.method == 'POST':
        selected_location = request.POST.get('selected_location', '')
        selected_food_name = request.POST.get('selected_food', '')

        if selected_location and selected_food_name:
            food_items = Food.objects.filter(region__icontains=selected_location, name__icontains=selected_food_name)
            search_heading = f"Results for {selected_food_name} in {selected_location}"
        elif selected_location:
            vendors = Vendor.objects.filter(location__icontains=selected_location)
            food_items = []
            for vendor in vendors:
                vendor_foods = list(Food.objects.filter(vendor=vendor))
                if vendor_foods:  # Ensuring there is at least one food item
                    food_items.append(random.choice(vendor_foods))
            search_heading = f"Results of Restaurants in {selected_location}"
        elif selected_food_name:
            food_items = Food.objects.filter(name__icontains=selected_food_name)
            search_heading = f"Results for {selected_food_name}"
        else:
            food_items = Food.objects.none()
            search_heading = "Please enter search criteria"
    else:
        food_items = Food.objects.none()

    context = {
        'food': food_items,
        'search_heading': search_heading,
        'location_search_only': selected_location and not selected_food_name
    }
    return render(request, 'filter_food_restaurant.html', context)
    
def view_food_restaurant(request):
    return render(request,"view_food_restaurant.html")

def profile_page(request):
    try:
        user_profile = Customer.objects.filter(name=request.session['Username'])
    except KeyError:
        return redirect('Home_page')
    return render(request,"profile_page.html",{'user_profile':user_profile})

@never_cache
def profile_add_details(request):
    try:
        user_profile = Customer.objects.filter(name=request.session['Username'])
    except KeyError:
        return redirect('Home_page')
    return render (request, "profile_add_details.html",{'user_profile':user_profile})



@never_cache
def save_profile(request):
    if request.method == "POST":
        un = request.POST.get('Username')
        em = request.POST.get('email')
        age = request.POST.get('age')
        dob = request.POST.get('dob')
        mob = request.POST.get('mobile')
        con = request.POST.get('country')
        st = request.POST.get('state')
        ct = request.POST.get('city')
        img = request.FILES.get('image', 'images/usericon1.png')
        if len(mob) != 10:
            messages.error(request, 'Contact number must be exactly 10 digits.')
            return redirect(profile_add_details)
        obj = Customer(name=un, email=em, date_of_birth=dob, age=age, mobile=mob, country=con, state=st, city=ct, profile_picture=img)
        obj.save()
        return redirect(profile_page)

@never_cache
def profile_edit(request):
    try:
        user_profile = Customer.objects.filter(name=request.session['Username'])
    except KeyError:
        return redirect('Home_page')

    try:
        profile = Customer.objects.get(name=request.session['Username'])
    except ObjectDoesNotExist:
        return redirect('profile_add_details')
    return render(request, "profile_edit.html",{'user_profile':user_profile,'profile':profile})

def update_profile(request, p_id):
    if request.method == "POST":
        current_username = request.POST.get('Username')
        new_username = request.POST.get('new_username')
        current_email = request.POST.get('Email')
        new_email = request.POST.get('new_email')
        age = request.POST.get('age')
        dob = request.POST.get('dob')
        mob = request.POST.get('mobile')
        con = request.POST.get('country')
        st = request.POST.get('state')
        ct = request.POST.get('city')
        if len(mob) != 10:
            messages.error(request, 'Contact number must be exactly 10 digits.')
            return redirect(profile_edit)
        try:
            if 'image' in request.FILES:
                img = request.FILES['image']
                fs = FileSystemStorage()
                file = fs.save(img.name, img)
            else:
                if 'image_removed' in request.POST and request.POST.get('image_removed') == 'True':
                    file = 'images/usericon1.png'
                else:
                    file = Customer.objects.get(id=p_id).profile_picture
        except:
            file = Customer.objects.get(id=p_id).profile_picture
        request.session['Username'] = new_username
        request.session['Email'] = new_email
        Signup_db.objects.filter(username=current_username,email=current_email).update(username=new_username,email=new_email)
        Customer.objects.filter(id=p_id).update(name=new_username, email=new_email, date_of_birth=dob, age=age, mobile=mob, country=con, state=st, city=ct, profile_picture=file)
        return redirect(profile_page)

def delete_profile(request):
    try:
        profile = Customer.objects.get(name=request.session['Username'])
        profile.delete()
        messages.success(request, 'Your profile details has been successfully deleted.')
    except profile.DoesNotExist:
        pass  # Profile doesn't exist, nothing to delete
    return redirect('profile_page')

def profile_change_password(request):
    user_profile1 = Signup_db.objects.get(username=request.session['Username'])
    user_profile = Customer.objects.filter(name=request.session['Username'])
    
    if request.method == 'POST':
        oldpass = request.POST['currentpassword']
        newpass = request.POST['newpassword']
        confirm_newpass = request.POST['confirmpassword']
    
        # Check if old password matches
        if oldpass != user_profile1.password:
            messages.error(request, "Incorrect current password")
            return redirect('profile_change_password')
    
        # Check if new password is the same as the old one
        if oldpass == newpass:
            messages.error(request, "New Password should not be the same as the Previous Password")
            return redirect('profile_change_password')
    
        # Check if new password and confirm password match
        if newpass != confirm_newpass:
            messages.error(request, "Password not matching")
            return redirect('profile_change_password')
    
        # Add more password complexity checks if needed
        # For example, you can use regular expressions to enforce specific patterns
    
        # If all conditions are met, update the password
        user_profile1.password = newpass
        user_profile1.save()
    
        messages.success(request, "Password changed successfully")
        return redirect('login_page')  # Redirect to the login page after changing password

    return render(request, "profile_change_password.html",{'user_profile':user_profile})





def delete_account(request):
    if request.method == 'POST':
        # Get the username or email of the logged-in user
        username_user = request.session.get('Username')
        email = request.session.get('Email')

        # Delete user data from SignUp_Db
        Signup_db.objects.filter(username=username_user).delete()
        Signup_db.objects.filter(email=email).delete()

        # Delete user profile
        Customer.objects.filter(name=username_user).delete()

        # Delete user cart items
        CartDb.objects.filter(Username=username_user).delete()
        BookingDb.objects.filter(Username=username_user).delete()



        # Clear session data
        request.session.flush()

        messages.success(request, "Current account deleted succesfully.")
        # Redirect to a page indicating successful account deletion
        return redirect('Home_page')

    # Handle cases where the request method is not POST
    return redirect('profile_page')





def menu_page(request):
    vendors = Vendor.objects.all()
    data=food_items.objects.all()
    location_names = location.objects.all()
    food = food_items.objects.all()

    return render(request,"menu_page.html",{"data":data,'vendors':vendors,"food":food,'location_names':location_names})

@never_cache
def cart_page(request):
    if 'Username' not in request.session:
        # Store the current page's URL in the session
        request.session['redirect_to'] = request.build_absolute_uri()
        # Add an info-level message
        messages.warning(request, 'You need to log in first before viewing your cart.')
        # Redirect back to the current page
        return redirect(
            request.META.get('HTTP_REFERER', '/'))

    try:
        user_profile = Customer.objects.filter(name=request.session['Username'])
    except KeyError:
        return redirect('Home_page')

    data = CartDb.objects.filter(Username=request.session['Username'])
    total_price = 0
    for i in data:
        total_price = total_price + i.tprice
    return render(request,"cart_page.html",{'data': data, 'total_price': total_price, 'user_profile': user_profile})

@never_cache
def save_cart(request):
    if 'Username' not in request.session:
        # Store the current page's URL in the session
        request.session['redirect_to'] = request.build_absolute_uri()
        # Add an info-level message
        messages.warning(request, 'You need to login before adding into cart.')
        # Redirect back to the current page
        return redirect(
            request.META.get('HTTP_REFERER', '/'))
    if request.method == "POST":
        username = request.POST.get('Username')
        food_id = request.POST.get('food_id')
        quantity = int(request.POST.get('quantity', 0))
        price = int(request.POST.get('price', 0))
        total_price = int(request.POST.get('tprice', 0))


        try:
            # Get the food object based on its ID
            food = Food_single.objects.get(id=food_id)
        except Food.DoesNotExist:
            # Handle the case where the food ID does not exist
            return HttpResponse("The specified food does not exist.", status=404)

        # Check if the item already exists in the cart for the logged-in user
        existing_item = CartDb.objects.filter(Username=username, food=food).first()

        if existing_item:
            return redirect('cart_page')

        else:
            # If the item does not exist, create a new entry in the cart
            obj = CartDb(Username=username, food=food, quantity=quantity, price=price, tprice=total_price)
            obj.save()
            messages.success(request, 'The item is added to cart')

        return redirect('single_product', food_id=food_id)

    # Add a default return statement in case the method is not POST
    return HttpResponse("Invalid request method", status=405)

def Update_cart(request):
    if request.method == 'POST':
        cart_items = request.POST.getlist('cart_item')  # List of cart item IDs
        quantities = request.POST.getlist('new_quantity')  # List of corresponding quantities
        items_updated = 0  # Initialize a counter for updated items

        for cart_item_id, quantity in zip(cart_items, quantities):
            try:
                cart_item = CartDb.objects.get(pk=cart_item_id)
                if cart_item:
                    cart_item.quantity = int(quantity)
                    cart_item.tprice = cart_item.price * cart_item.quantity  # Calculate the new total price
                    cart_item.save()
                    items_updated += 1  # Increment the counter for each successfully updated item
            except CartDb.DoesNotExist:
                continue  # Skip to the next iteration if an item doesn't exist

        # Create a message based on the number of items updated
        if items_updated > 0:
            message = f'The item count has been updated.'
            messages.success(request, mark_safe(message))
        else:
            message = 'No items were updated.'
            messages.error(request, mark_safe(message))

        # Redirect or return JSON response
        return JsonResponse({'success': True, 'message': message})
    else:
        # Handle the wrong request method
        return JsonResponse({'success': False, 'error': 'Invalid request method'})

def delete_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        try:
            cart_item = CartDb.objects.get(id=item_id)
            cart_item.delete()
            message = f'The item has been deleted.'
            messages.success(request, mark_safe(message))
            return JsonResponse({'success': True})
        except CartDb.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Item does not exist'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})



def Checkout_page(request):
    try:
        profile = Customer.objects.get(name=request.session['Username'])
    except KeyError:
        return redirect('Home_page')
    username = request.session.get('Username')
    data=CartDb.objects.filter(Username=username)

    total_price = sum(item.tprice for item in data)

    return render(request,"checkout_page.html",{"data":data,'total_price': total_price,'profile':profile})

def save_booking_details(request):
    if request.method == 'POST':
        username = request.POST.get('username')

        # Check if there's an existing booking for the user
        existing_booking = BookingDb.objects.filter(Username=username).first()

        if existing_booking:
            # If there's an existing booking, update the fields
            existing_booking.name = request.POST.get('name')
            existing_booking.age = request.POST.get('age')
            existing_booking.mobile_number = request.POST.get('mobile')
            existing_booking.email = request.POST.get('email')
            existing_booking.date = request.POST.get('date')
            existing_booking.train_number = request.POST.get('train_number')
            existing_booking.compartment_number = request.POST.get('compartment')
            existing_booking.seat_number = request.POST.get('seat')
            existing_booking.deliver_station = request.POST.get('deliver_station')
            existing_booking.save()  # Save the updated booking details
        else:
            # If no existing booking, create a new booking entry
            booking = BookingDb(
                Username=username,
                name=request.POST.get('name'),
                age=request.POST.get('age'),
                mobile_number=request.POST.get('mobile'),
                email=request.POST.get('email'),
                date=request.POST.get('date'),
                train_number=request.POST.get('train_number'),
                compartment_number=request.POST.get('compartment'),
                seat_number=request.POST.get('seat'),
                deliver_station=request.POST.get('deliver_station')
            )
            booking.save()

        # Redirect to payment section page
        return redirect('payment_section')

def payment_section(request):
    username = request.session.get('Username')
    details=BookingDb.objects.get(Username=username)
    data = CartDb.objects.filter(Username=username)
    total_price = sum(i.tprice for i in data)
    tax = 70
    grand_total = total_price + tax  

    order_currency = 'INR'
    client = razorpay.Client(auth=('rzp_test_IzIBFTmzd3zzKk', 'mMvIdZd7a4EU1pMd9tSQEbE0'))

    payment = client.order.create({'amount': int(grand_total * 100), 'currency': "INR", 'payment_capture': '1'})

    # Get the order ID
    order_id = payment['id']

    # Render payment section template with necessary data
    return render(request, "payment_section.html", {
        "data": data,
        "payment": payment,
        "grand_total": grand_total,
        "total_price": total_price,
        "order_id": order_id,  
        "details": details,
    })

    return render(request,"payment_section.html")


@csrf_exempt
def place_order(request):
    if request.method == 'POST':
        username = request.POST.get('Username')
        total_price = int(request.POST.get('total_price'))
        shipping = int(request.POST.get('shipping'))
        grand_total = int(request.POST.get('grand_total'))
        amount_to_be_paid = int(request.POST.get('amountToBePaid'))
        payment_method = request.POST.get('payment_method')

        # Generate a unique order ID
        order_id = str(uuid.uuid4().hex)[:12]

        booking = get_object_or_404(BookingDb, Username=username)


        # Create the order object
        order = Order.objects.create(
            Username=username,
            booking=booking,
            total_price=total_price,
            shipping=shipping,
            grand_total=grand_total,
            amount_to_be_paid=amount_to_be_paid,
            payment_method=payment_method,
            order_status='Order Confirmed',
            order_id=order_id,
            created_at=timezone.now()
        )

        # Retrieve cart items
        cart_items = CartDb.objects.filter(Username=username)



        # Add cart items to the order
        for cart_item in cart_items:
            item_total_price = cart_item.quantity * cart_item.price
            OrderItem.objects.create(
                order=order,
                food_name=cart_item.food.single_name,
                vendor_name=cart_item.food.vendor.name,
                picture=cart_item.food.image,
                quantity=cart_item.quantity,
                price=cart_item.price,
                total_price=item_total_price
            )

        # Clear the cart after placing the order
        cart_items.delete()

        messages.success(request, "Your order has been placed successfully!")
        return redirect('order_confirmed', order_id=order_id)





from django.shortcuts import render, get_object_or_404
from .models import Order, OrderItem
from django.conf import settings
import random


@never_cache
def order_confirmed(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    booking = order.booking

    # Generate OTP
    otp = random.randint(100000, 999999)

    # Send OTP to the email saved in booking
    send_otp_via_email(booking.email, otp)

    # Optionally, you can pass OTP to the template for display or just confirm it was sent
    return render(request, "order_complete.html", {"order": order, "order_items": order_items, "otp": otp})



from django.core.mail import send_mail
import random

def send_otp_via_email(email, otp):
    subject = 'Your OTP for Order Confirmation'
    message = f'Your OTP is: {otp}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email,]
    send_mail(subject, message, email_from, recipient_list)




def profile_orders(request):
    try:
        user_profile = Customer.objects.filter(name=request.session['Username'])
        orders = Order.objects.filter(Username=request.session['Username'], is_deleted=False).order_by('-created_at')
    except KeyError:
        return redirect('Home_page')
    return render(request, "profile_orders.html", {'orders': orders, 'user_profile': user_profile})


def order_view(request,order_id):
    order=Order.objects.get(id=order_id)
    try:
        user_profile = Customer.objects.filter(name=request.session['Username'])
    except KeyError:
        return redirect('Home_page')
    return render(request,"order_view.html",{'order': order,'user_profile': user_profile})


@csrf_exempt
def update_order_status(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        light_position = request.POST.get('light_position')

        try:
            order = Order.objects.get(id=order_id)
            # Update order status only if the current status is not "Cancelled"
            if order.order_status != 'Cancelled':
                order.order_status = light_position
                order.save()
                return JsonResponse({'message': 'Order status updated successfully'}, status=200)
            else:
                return JsonResponse({'message': 'Order is cancelled, status cannot be updated'}, status=400)
        except Order.DoesNotExist:
            return JsonResponse({'message': 'Order not found'}, status=404)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)

def cancel_order(request, order_id):
    if request.method == "POST":
        order = Order.objects.get(id=order_id)
        order.order_status = 'Order Cancelled'
        order.save()
        messages.success(request, 'Your order is cancelled successfully.')
        return redirect(request.META.get('HTTP_REFERER', ''))

from django.views.decorators.http import require_POST

from django.views.decorators.http import require_POST
from django.http import JsonResponse

@require_POST
def delete_selected_orders(request):
    order_ids = request.POST.getlist('selected_orders[]')
    updated_count = 0

    for order_id in order_ids:
        try:
            order = Order.objects.get(id=order_id, Username=request.session['Username'])
            # Mark the order as deleted instead of actually deleting it.
            order.is_deleted = True
            order.save()
            updated_count += 1
        except Order.DoesNotExist:
            # Optionally log this situation or handle it in another appropriate way.
            continue

    message = f'{updated_count} orders marked as deleted successfully.'
    return JsonResponse({'message': message}, status=200)





def about_page(request):
    return render(request,"about_page.html")
def contact_page(request):
    return render(request,"contact_page.html")


def contact_save(request):
    if request.method=="POST":
        b = request.POST.get("username")
        c = request.POST.get("name")
        d = request.POST.get("email")
        e = request.POST.get("mobile")
        f = request.POST.get("subject")
        g = request.POST.get("message")
        obj = contact_Db(username=b, name=c,email=d,phone=e,subject=f,message=g)
        obj.save()
        messages.success(request, 'Your message has been sended sucessfully.')
        return redirect(contact_page)



def view_food_restaurant(request, name):
    food_items = Food.objects.filter(name=name,)
    return render(request, "view_food_restaurant.html", {"food_items": food_items, "food_name": name})


from django.shortcuts import render, get_object_or_404

def food_inner_page(request, vendor_id, name):
    # Retrieve the vendor by ID
    vendor = Vendor.objects.get(pk=vendor_id)

    # Try to fetch the main Food category to get the vendor's name and filter by vendor
    main_food = Food.objects.filter(name=name, vendor=vendor).first()
    if main_food:
        food_items = Food_single.objects.filter(main_category=name, vendor=vendor)
    else:
        food_items = Food_single.objects.none()  # Return an empty queryset

    return render(request, "food_inner_page.html", {
        'food_items': food_items,
        "food_name": name,
        "vendor_name": vendor.name if vendor else "No Vendor"
    })


from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Avg



@never_cache
def single_product(request, food_id):
    food = get_object_or_404(Food_single, pk=food_id)
    related_foods = Food.objects.filter(vendor=food.vendor).exclude(id=food_id)
    all_reviews = Food_review_Db.objects.filter(food=food).order_by('-created_at')  # Use 'food' instead of 'pro'
    existing_item = CartDb.objects.filter(Username=request.session.get('Username'), food=food).first()

    # Filter reviews with description
    reviews_with_description = all_reviews.filter(~Q(review_text=''))

    # Pagination
    page_number = request.GET.get('page', 1)
    paginator = Paginator(all_reviews, 5)  # Modify as needed

    try:
        reviews = paginator.page(page_number)
    except PageNotAnInteger:
        reviews = paginator.page(1)
    except EmptyPage:
        reviews = paginator.page(paginator.num_pages)

    # Rating statistics
    total_reviews = reviews_with_description.count()
    total_ratings = all_reviews.count()
    avg_rating_result = all_reviews.aggregate(Avg('rating'))['rating__avg']
    total_average_rating = round(avg_rating_result, 1) if avg_rating_result else None

    # Calculate the count of colored ratings for each star
    colored_ratings_count = {
        '1': all_reviews.filter(rating=1).count(),
        '2': all_reviews.filter(rating=2).count(),
        '3': all_reviews.filter(rating=3).count(),
        '4': all_reviews.filter(rating=4).count(),
        '5': all_reviews.filter(rating=5).count(),
    }

    # Calculate percentages for each star
    colored_ratings_percentage = {
        key: (count / total_ratings) * 100 if total_ratings != 0 else 0
        for key, count in colored_ratings_count.items()
    }

    return render(request, "single_product.html", {
        "food": food,
        "related_foods": related_foods,
        "reviews": reviews,
        "total_reviews": total_reviews,
        "total_ratings": total_ratings,
        "total_average_rating": total_average_rating,
        "colored_ratings_count": colored_ratings_count,
        "colored_ratings_percentage": colored_ratings_percentage,
        "existing_item": existing_item,
    })

@never_cache
def save_food_review(request, food_id):
    if 'Username' not in request.session:
        request.session['redirect_to'] = request.build_absolute_uri()
        messages.warning(request, 'You need to log in first before writing a review.')
        return redirect(request.META.get('HTTP_REFERER', '/'))

    food = get_object_or_404(Food_single, id=food_id)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        review_text = request.POST.get('review', '').strip()
        reviewer_name = request.POST.get('name', '').strip()
        reviewer_image = request.FILES.get('image', None)
        username = request.session.get('Username', 'Anonymous')

        reviewer_name = reviewer_name if reviewer_name else username

        if rating in ['1', '2', '3', '4', '5'] and (review_text or reviewer_name):
            new_review = Food_review_Db.objects.create(
                food=food,  # Assign the food instance here
                rating=int(rating),
                review_text=review_text,
                reviewer_name=reviewer_name,
                reviewer_image=reviewer_image if reviewer_image else 'Images/usericon1.png'
            )
            return HttpResponseRedirect(reverse('single_product', args=[food_id]) + '?page=last')

    return redirect(reverse('single_food_item', args=[food_id]))


from django.dispatch import receiver
from django.db.models.signals import post_save,post_delete
@receiver([post_save, post_delete], sender=Food_review_Db)
def update_average_rating(sender, instance, **kwargs):
    if hasattr(instance, 'food') and instance.food:
        employee = instance.food
        # Calculate the new average rating for the employee
        total_ratings = Food_review_Db.objects.filter(food=employee).aggregate(Avg('rating'))['rating__avg']
        average_rating = round(total_ratings, 1) if total_ratings is not None else 0.0
        # Update the average_rating field in the Register_employee_Db model
        Food_single.objects.filter(id=employee.id).update(average_rating=average_rating)




@never_cache
def vendor_single_page(request,vendor_id):
    vendor = Vendor.objects.get(pk=vendor_id)
    foods = vendor.food_set.filter()
    pro = Vendor.objects.get(id=vendor_id)
    all_reviews = Vendor_review_Db.objects.filter(vendor=pro).order_by('-created_at')

    # Filter reviews with description
    reviews_with_description = all_reviews.filter(~Q(review_text=''))

    # Pagination
    page_number = request.GET.get('page', 1)  # Get the current page number, default to 1
    paginator = Paginator(all_reviews, 6)  # Show 5 reviews per page

    try:
        reviews = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        reviews = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        reviews = paginator.page(paginator.num_pages)

    # Calculate total number of reviews with description
    total_reviews = reviews_with_description.count()

    # Calculate total number of ratings (total number of reviews)
    total_ratings = all_reviews.count()

    # Calculate total average rating
    avg_rating_result = all_reviews.aggregate(Avg('rating'))['rating__avg']
    total_average_rating = round(avg_rating_result, 1) if avg_rating_result is not None else None

    # Calculate the count of colored ratings for each star
    colored_ratings_count = {
        '1': all_reviews.filter(rating=1).count(),
        '2': all_reviews.filter(rating=2).count(),
        '3': all_reviews.filter(rating=3).count(),
        '4': all_reviews.filter(rating=4).count(),
        '5': all_reviews.filter(rating=5).count(),
    }

    # Calculate percentages for each star
    colored_ratings_percentage = {
        key: (count / total_ratings) * 100 if total_ratings != 0 else 0
        for key, count in colored_ratings_count.items()
    }


    return render(request, "vendor_single_page.html", {
                "pro": pro,
                "reviews": reviews,
                "total_reviews": total_reviews,
                "total_ratings": total_ratings,
                "total_average_rating": total_average_rating,
                "colored_ratings_count": colored_ratings_count,
                "colored_ratings_percentage": colored_ratings_percentage,
                 "foods": foods, 'vendor': vendor
            })
@never_cache
def save_review(request, vendor_id):
    if 'Username' not in request.session:
        request.session['redirect_to'] = request.build_absolute_uri()
        messages.warning(request, 'You need to log in first before writing a review.')
        return redirect(request.META.get('HTTP_REFERER', '/'))

    pro = get_object_or_404(Vendor, id=vendor_id)

    if request.method == 'POST':
        rating = request.POST.get('rating', '0')
        review_text = request.POST.get('review', '').strip()
        reviewer_name = request.POST.get('name', '').strip()
        reviewer_image = request.FILES.get('image')
        username = request.POST.get('username', '').strip()

        # Default to username if reviewer_name is not provided
        if not reviewer_name:
            reviewer_name = username or 'Anonymous'  # Fallback to 'Anonymous' if username is also not provided

        # If reviewer_image is not provided, use a default image
        if not reviewer_image:
            reviewer_image = 'Images/usericon1.png'

        # Validate the rating and ensure there is either text or a reviewer's name
        if rating in ['1', '2', '3', '4', '5'] and (review_text or reviewer_name):
            new_review = Vendor_review_Db.objects.create(
                vendor=pro,
                rating=rating,
                review_text=review_text,
                reviewer_name=reviewer_name,
                reviewer_image=reviewer_image,
                username=username,
            )
            return HttpResponseRedirect(reverse('vendor_single_page', args=[vendor_id]) + '?page=last')

    all_reviews = Vendor_review_Db.objects.filter(vendor=pro).order_by('-created_at')
    paginator = Paginator(all_reviews, 5)
    page_number = request.GET.get('page', 1)

    try:
        reviews = paginator.page(page_number)
    except PageNotAnInteger:
        reviews = paginator.page(1)
    except EmptyPage:
        reviews = paginator.page(paginator.num_pages)

    return render(request, "vendor_single_page.html", {"pro": pro, "reviews": reviews})




from django.dispatch import receiver
from django.db.models.signals import post_save,post_delete
@receiver([post_save, post_delete], sender=Vendor_review_Db)
def update_average_rating(sender, instance, **kwargs):
    if hasattr(instance, 'vendor') and instance.vendor:
        employee = instance.vendor
        # Calculate the new average rating for the employee
        total_ratings = Vendor_review_Db.objects.filter(vendor=employee).aggregate(Avg('rating'))['rating__avg']
        average_rating = round(total_ratings, 1) if total_ratings is not None else 0.0
        # Update the average_rating field in the Register_employee_Db model
        Vendor.objects.filter(id=employee.id).update(average_rating=average_rating)

def Forgot_page(request):
    return render(request, "Forgot_page.html")



from django.core.mail import send_mail
from django.utils import timezone
import datetime
import secrets


TOKEN_EXPIRATION_MINUTES = 10  # Adjust as needed


def generate_token():
    return secrets.token_urlsafe(32)





def forgot_password(request):
    if request.method == 'POST':
        em = request.POST.get('email')
        user = Signup_db.objects.filter(email=em).first()
        if user:
            # Generate a unique token
            token = generate_token()
            # Set the expiration time for the token
            token_expiration = timezone.now() + datetime.timedelta(minutes=TOKEN_EXPIRATION_MINUTES)
            # Store the token and expiration time in the user object
            user.password_reset_token = token
            user.token_expiration = token_expiration
            user.save()
            # Send the email with the recovery link
            subject = "Password Reset"
            expiration_message = f"This link will expire in {TOKEN_EXPIRATION_MINUTES} minutes. Please reset your password before then."
            # Format the message with HTML for a clickable hyperlink
            message = f"Click the following link to reset your password: <a href='http://127.0.0.1:5050/UserApp/change_password/{token}/'>Reset Password</a><br><br>{expiration_message}"
            frm = 'traintreats12345@gmail.com'  # Sender email (change accordingly)
            to = em  # Recipient email
            send_mail(subject, '', frm, [to], html_message=message)
            # Extend session expiration
            request.session.set_expiry(TOKEN_EXPIRATION_MINUTES * 60)  # Convert minutes to seconds
            return render(request, 'Verification_page.html', {'expiration_minutes': TOKEN_EXPIRATION_MINUTES})
        else:
            messages.error(request, "Sorry, this email is not registered.")
            return redirect('forgot_password')
    return render(request, 'Forgot_page.html',)


from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages

def change_password(request, token):
    user = Signup_db.objects.filter(password_reset_token=token).first()
    if user:
        if user.token_expiration < timezone.now():
            return HttpResponse("Sorry, the password reset link has expired.")
        if request.method == 'POST':
            p1 = request.POST.get('password')
            p2 = request.POST.get('confirm_password')
            if p1 == p2:
                # Hash the new password before saving
                hashed_password = make_password(p1)
                user.password = hashed_password
                user.Cpassword = hashed_password  # Assuming you need to hash the confirmation password as well
                user.password_reset_token = None
                user.token_expiration = None
                user.save()
                messages.success(request, "Password changed successfully.")
                return redirect('login_page')
            else:
                return HttpResponse('Passwords do not match.')
        return render(request, 'Change_password_page.html')
    else:
        return HttpResponse("Invalid or expired password reset link.")


def verification_page(request):
    return render(request, 'Verification_page.html')