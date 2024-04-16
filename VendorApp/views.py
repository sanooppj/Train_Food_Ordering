from django.shortcuts import render, redirect,get_object_or_404 ,redirect
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDictKeyError

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
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.contrib import messages



@never_cache
def vendor_index_page(request):
    try:
         vendor_profile = Vendor.objects.filter(name=request.session['Username'])
    except KeyError:
         vendor_profile=None
    return render(request,"vendor_index_page.html",{'vendor_profile':vendor_profile})

def add_food_details(request):
    data=food_items.objects.all()
    data1=location.objects.all()
    return render(request,"add_food_details.html",{"data":data,"data1":data1})


from django.shortcuts import render, redirect
from .models import Food, Vendor

def add_food_single_details(request):
    if 'Username' in request.session:
        vendor_name = request.session['Username']
        vendor = Vendor.objects.get(name=vendor_name)  # This assumes vendor name is unique

        data = Food.objects.filter(vendor=vendor)
        return render(request, "add_food_single_details.html", {"data": data})
    else:
        # Redirect to login or another appropriate page if the username isn't in the session
        return redirect('login_url')  # Replace 'login_url' with the actual URL name for your login view








def single_food_table(request):
    # Get the vendor profiles based on the current user's session username
    try:
        vendor_profiles = Vendor.objects.filter(name=request.session['Username'])
    except KeyError:
         vendor_profiles=None
    # Retrieve all food items associated with these vendors
    if vendor_profiles.exists():
        food = Food_single.objects.filter(vendor__in=vendor_profiles)
    else:
        food = []  # No food items to display if no vendors exist

    # Render the page with the food items and vendor profiles
    return render(request, "single_food_table.html", {'food': food, "vendor_profiles": vendor_profiles})


def food_save(request):
    if request.method=="POST":
        name = request.POST.get("name")
        category = request.POST.get("category")
        food_type = request.POST.get("type")
        image = request.FILES.get("image")
        description = request.POST.get("description")
        vendor_name = request.POST.get("Username") 
        region = request.POST.get("region_name")
        vendor = Vendor.objects.get(name=vendor_name)
        food = Food(name=name, category=category, type=food_type, image=image,  description=description, vendor=vendor,region=region)
        food.save()

    return redirect(add_food_details)


def food_table(request):
    # Get the vendor profiles based on the current user's session username
    try:
        vendor_profiles = Vendor.objects.filter(name=request.session['Username'])
    except KeyError:
         vendor_profiles=None

    # Retrieve all food items associated with these vendors
    if vendor_profiles.exists():
        food = Food.objects.filter(vendor__in=vendor_profiles)
    else:
        food = []  # No food items to display if no vendors exist

    # Render the page with the food items and vendor profiles
    return render(request, "food_table.html", {'food': food, "vendor_profiles": vendor_profiles})


def edit_food_details(request,food_id):
    data=food_items.objects.all()
    data1=location.objects.all()
    food=Food.objects.get(id=food_id)
    return render(request,"edit_food_details.html",{"data":data,"data1":data1,"food":food})

def update_food_details(request,food_id):
    if request.method=="POST":
        name = request.POST.get("name")
        category = request.POST.get("category")
        food_type = request.POST.get("type")
        image = request.FILES.get("image")
        description = request.POST.get("description")
        vendor_name = request.POST.get("Username")
        region = request.POST.get("region_name")
        vendor = Vendor.objects.get(name=vendor_name)
        try:
            img = request.FILES['image']
            fs = FileSystemStorage()
            file = fs.save(img.name, img)
        except:
            file = Food.objects.get(id=food_id).image
        Food.objects.filter(id=food_id).update(name=name, category=category, type=food_type, image=file,  description=description, vendor=vendor,region=region)
        return redirect(food_table)

def food_delete(request, food_id):
    food = Food.objects.get(id=food_id)
    food.delete()
    return redirect(food_table)


def edit_food_single_details(request,food_id):
    if 'Username' in request.session:
        vendor_name = request.session['Username']
        vendor = Vendor.objects.get(name=vendor_name)  # This assumes vendor name is unique

        data = Food.objects.filter(vendor=vendor)
    food=Food_single.objects.get(id=food_id)
    return render(request,"edit_food_single.html",{"data":data,"food":food})

def update_food_single(request,food_id):
    if request.method=="POST":
        name = request.POST.get("name")
        main_category = request.POST.get("main_category")
        price = request.POST.get("price")
        description = request.POST.get("description")
        vendor_name = request.POST.get("Username")
        vendor = Vendor.objects.get(name=vendor_name)
        try:
            img = request.FILES['image']
            fs = FileSystemStorage()
            file = fs.save(img.name, img)
        except:
            file = Food_single.objects.get(id=food_id).image
        Food_single.objects.filter(id=food_id).update(single_name=name, main_category=main_category, image=file, price=price, description=description, vendor=vendor)
        return redirect(single_food_table)

def single_food_delete(request, food_id):
    food = Food_single.objects.get(id=food_id)
    food.delete()
    return redirect(single_food_table)


def food_single_save(request):
    if request.method=="POST":
        name = request.POST.get("name")
        main_category = request.POST.get("main_category")
        image = request.FILES.get("image")
        price = request.POST.get("price")
        description = request.POST.get("description")
        vendor_name = request.POST.get("Username")
        vendor = Vendor.objects.get(name=vendor_name)
        food = Food_single(single_name=name, main_category=main_category, image=image, price=price, description=description, vendor=vendor,)
        food.save()

    return redirect(add_food_single_details)



from django.shortcuts import render, get_object_or_404

def food_reviews(request, food_id):
    food_item = get_object_or_404(Food_single, pk=food_id)
    reviews = Food_review_Db.objects.filter(food=food_item).order_by('-created_at')
    return render(request, 'food_single_reviews.html', {'food_item': food_item, 'reviews': reviews})





def vendor_review(request):
    if 'Username' in request.session:
        vendor_name = request.session['Username']
        vendor = Vendor.objects.filter(name=vendor_name).first()
        if vendor is not None:
            reviews = Vendor_review_Db.objects.filter(vendor=vendor).order_by('-created_at')
        else:
            reviews = []

        context = {
            'vendor': vendor,
            'reviews': reviews,
        }
        return render(request, 'vendor_review.html', context)
    else:
        # Handle the case where there is no 'Username' in session
        return render(request, 'error.html', {'message': 'No vendor information found. Please log in.'})



def delete_review(request, review_id):
    review = Vendor_review_Db.objects.get(pk=review_id)
    if review.vendor.name == request.session['Username']:
        review.delete()
        return redirect('vendor_review')  # Redirects back to the review page
    else:
        return HttpResponseForbidden("You do not have permission to delete this review.")





def vendor_profile_page(request):
    try:
        vendor_profile = Vendor.objects.filter(name=request.session['Username'])
    except KeyError:
        vendor_profile=None
    return render(request,"vendor_profile_page.html",{'vendor_profile':vendor_profile})

def vendor_profile_add_details(request):
    try:
        vendor_profile = Vendor.objects.filter(name=request.session['Username'])
    except KeyError:
        vendor_profile = None
    return render (request, "vendor_profile_add_details.html",{'vendor_profile':vendor_profile})



def vendor_save_profile(request):
    if request.method == "POST":
        un = request.POST.get('Username')
        em = request.POST.get('email')
        des = request.POST.get('description')
        add = request.POST.get('address')
        con = request.POST.get('contact')
        web = request.POST.get('website')
        loc = request.POST.get('location')
        img = request.FILES.get('image', 'images/usericon1.png')
        if len(con) != 10:
            messages.error(request, 'Contact number must be exactly 10 digits.')
            return redirect(vendor_profile_add_details)
        obj = Vendor(name=un, email=em, description=des, address=add, contact=con, website=web, location=loc, logo=img)
        obj.save()
        messages.success(request, 'Your profile details has been saved.')
        return redirect(vendor_profile_page)

def vendor_profile_edit(request):
    try:
        vendor_profile = Vendor.objects.filter(name=request.session['Username'])
    except KeyError:
        vendor_profile = None

    try:
        profile = Vendor.objects.get(name=request.session['Username'])
    except ObjectDoesNotExist:
        return redirect('vendor_profile_add_details')
    return render(request, "vendor_profile_edit.html",{'vendor_profile':vendor_profile,'profile':profile})

def vendor_update_profile(request, p_id):
    if request.method == "POST":
        current_username = request.POST.get('Username')
        new_username = request.POST.get('new_username')
        current_email = request.POST.get('Email')
        new_email = request.POST.get('new_email')
        des = request.POST.get('description')
        add = request.POST.get('address')
        con = request.POST.get('contact')
        web = request.POST.get('website')
        loc = request.POST.get('location')
        if len(con) != 10:
            messages.error(request, 'Contact number must be exactly 10 digits.')
            return redirect(vendor_profile_edit)
        try:
            if 'image' in request.FILES:
                img = request.FILES['image']
                fs = FileSystemStorage()
                file = fs.save(img.name, img)
            else:
                if 'image_removed' in request.POST and request.POST.get('image_removed') == 'True':
                    file = 'images/usericon1.png'
                else:
                    file = Vendor.objects.get(id=p_id).logo
        except:
            file = Vendor.objects.get(id=p_id).logo
        request.session['Username'] = new_username
        request.session['Email'] = new_email
        Signup_db.objects.filter(username=current_username,email=current_email).update(username=new_username,email=new_email)
        Vendor.objects.filter(id=p_id).update(name=new_username,email=new_email, description=des, address=add, contact=con, website=web, location=loc, logo=file)
        return redirect(vendor_profile_page)

def vendor_delete_profile(request):
    try:
        profile = Vendor.objects.get(name=request.session['Username'])
        profile.delete()
        messages.success(request, 'Your profile details has been successfully deleted.')
    except profile.DoesNotExist:
        pass  # Profile doesn't exist, nothing to delete
    return redirect('vendor_profile_page')


    try:
        vendor_profile = Vendor.objects.filter(name=request.session['Username'])
    except KeyError:
        vendor_profile = None

    # user_profile1 = SignUp_Db.objects.get(Username=request.session['Username'])
    # user_profile = Profile.objects.filter(Username=request.session['Username'])
    #
    # if request.method == 'POST':
    #     oldpass = request.POST['currentpassword']
    #     newpass = request.POST['newpassword']
    #     confirm_newpass = request.POST['confirmpassword']
    #
    #     # Check if old password matches
    #     if oldpass != user_profile1.Password:
    #         messages.error(request, "Incorrect current password")
    #         return redirect('profile_change_password')
    #
    #     # Check if new password is the same as the old one
    #     if oldpass == newpass:
    #         messages.error(request, "New Password should not be the same as the Previous Password")
    #         return redirect('profile_change_password')
    #
    #     # Check if new password and confirm password match
    #     if newpass != confirm_newpass:
    #         messages.error(request, "Password not matching")
    #         return redirect('profile_change_password')
    #
    #     # Add more password complexity checks if needed
    #     # For example, you can use regular expressions to enforce specific patterns
    #
    #     # If all conditions are met, update the password
    #     user_profile1.Password = newpass
    #     user_profile1.Cpassword = newpass
    #     user_profile1.save()
    #
    #     messages.success(request, "Password changed successfully")
    #     return redirect('Login_page')  # Redirect to the login page after changing password

    return render(request, "vendor_profile_change_password.html",{"vendor_profile":vendor_profile})
def vendor_delete_account(request):
    if request.method == 'POST':
        # Get the username and email of the logged-in user
        username = request.session.get('Username')
        email = request.session.get('Email')

        try:
            # Delete user data from Vendor model
            Vendor.objects.filter(name=username, email=email).delete()

            # Delete user data from Signup_db
            Signup_db.objects.filter(username=username, email=email).delete()

            # Delete associated food items
            Food.objects.filter(vendor__name=username, vendor__email=email).delete()

            # Delete associated food_single items
            Food_single.objects.filter(vendor__name=username, vendor__email=email).delete()

            # Clear session data
            request.session.flush()

            # Delete user from the auth.User table
            user = User.objects.get(username=username, email=email)
            user.delete()

            messages.success(request, "Current account deleted successfully.")
            # Redirect to a page indicating successful account deletion
            return redirect('login_page')

        except Exception as e:
            messages.error(request, f"An error occurred while deleting the account: {str(e)}")
            # Redirect to a page indicating failure
            return redirect('profile_page')

    # Handle cases where the request method is not POST
    return redirect('profile_page')



from collections import defaultdict
from django.shortcuts import render
from django.http import HttpResponse

def users_order_details(request):
    vendor_name = request.session.get('Username')

    if vendor_name:
        # Fetch all items for this vendor, including those in orders marked as deleted for the user
        order_items = OrderItem.objects.filter(vendor_name=vendor_name).select_related(
            'order', 'order__booking').order_by('-order__created_at')

        grouped_order_items = defaultdict(list)
        order_prices = defaultdict(float)

        for item in order_items:
            key = item.order.order_id
            html_content = f'<div class="description-line"><span style="font-size:15px;font-weight:bold;color:rgb(237, 3, 3);">x{item.quantity}</span> {item.food_name}</div>'
            grouped_order_items[key].append(html_content)
            order_prices[key] += item.total_price

        orders = []
        unique_orders = set(item.order for item in order_items)
        sorted_orders = sorted(unique_orders, key=lambda x: x.created_at, reverse=True)

        for order in sorted_orders:
            orders.append({
                'order_id': order.order_id,
                'username': order.booking.Username,
                'items_description': ''.join(grouped_order_items[order.order_id]),
                'total_price': order_prices[order.order_id],
                'order_status': order.order_status,
                'order_status_class': 'text-success' if order.order_status != 'Cancelled' else 'text-danger',
                'created_at': order.created_at.strftime("%Y-%m-%d %H:%M:%S"),  # Formatting the datetime
                'vendor_name': vendor_name
            })

        return render(request, 'users_order_details.html', {'orders': orders})
    else:
        return HttpResponse("Vendor name not found in session")

