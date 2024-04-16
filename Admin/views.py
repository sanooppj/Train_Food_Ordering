from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, get_object_or_404,redirect
from Admin.models import *
from VendorApp.models import *
from UserApp.models import *
from django.http import JsonResponse






from django.views.decorators.cache import never_cache

@never_cache
def admin_index_page(request):
    return render(request, "admin_index_page.html")

def vendors_details(request):
    # Filter data to only include entries where user_type is 'vendor'
    data = Signup_db.objects.filter(user_type='vendor')

    return render(request, "vendors_details.html", {'data': data})

def vendors_food_history(request):
    return render(request, "vendors_food_history.html")

def vendors_requests(request):
    data=Food.objects.all()
    return render(request, "vendors_requests.html",{'data':data})



def users_orders_page(request):
    users = Signup_db.objects.filter(user_type='customer')

    return render(request, "users_orders_page.html", {"users": users})

def users_orders_status(request, username):
    user = get_object_or_404(Signup_db, username=username)
    orders = Order.objects.filter(Username=username)
    return render(request, "users_orders_status.html", {"user": user, "orders": orders})




def add_food_items(request):
    return render(request, "add_food_items.html")

def food_items_save(request):
    if request.method=="POST":
        name=request.POST.get("name")
        image=request.FILES["image"]
        obj=food_items(name=name,image=image)
        obj.save()
        return redirect(add_food_items)

def admin_food_table(request):
    # Query all food items
    food = food_items.objects.all()

    # Pass the queryset to the template context
    return render(request, 'food_item_table.html', {'food': food})


def edit_food_items(request,food_id):
    food=food_items.objects.get(id=food_id)
    return render(request, "edit_food_items.html",{'food':food})

def update_food_item(request,food_id):
    if request.method=="POST":
        name=request.POST.get("name")
        try:
            img = request.FILES['image']
            fs = FileSystemStorage()
            file = fs.save(img.name, img)
        except:
            file = food_items.objects.get(id=food_id).image
        food_items.objects.filter(id=food_id).update(name=name,image=file)
        return redirect(admin_food_table)


def food_item_delete(request, food_id):
    food = food_items.objects.get(id=food_id)
    food.delete()
    return redirect(admin_food_table)



from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404

def approve_vendor(request, user_id):
    vendor = get_object_or_404(Signup_db, pk=user_id, user_type='vendor')
    vendor.is_approved = True
    vendor.save()

    # Send email notification
    send_mail(
        'Vendor Approval Notification',
        'Your vendor account has been approved by the admin.',
        'traintreats12345@gmail.com',
        [vendor.email],
        fail_silently=False,
    )

    return redirect(request.META.get('HTTP_REFERER', ''))

def reject_vendor(request, user_id):
    vendor = get_object_or_404(Signup_db, pk=user_id, user_type='vendor')
    vendor.is_approved = False
    vendor.save()

    # Send email notification
    send_mail(
        'Vendor Rejection Notification',
        'Your vendor account has been rejected by the admin.',
        'traintreats12345@gmail.com',
        [vendor.email],
        fail_silently=False,
    )

    return redirect(request.META.get('HTTP_REFERER', ''))



from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction

def delete_vendor(request, user_id):
    # Ensure that this view can only be accessed by an admin
    if not request.user.is_superuser:
        messages.error(request, "You are not authorized to perform this action.")
        return redirect('vendors_details')

    with transaction.atomic():
        vendor = get_object_or_404(Signup_db, pk=user_id, user_type='vendor')

        # Delete all related food items
        Food.objects.filter(vendor__email=vendor.email).delete()

        # Delete the Vendor entry, if exists
        Vendor.objects.filter(email=vendor.email).delete()

        Signup_db.objects.filter(username=vendor.username, email=vendor.email).delete()


        # Delete user from the auth.User table
        user = User.objects.get(username=vendor.username, email=vendor.email)
        user.delete()

        # Finally, delete the Signup_db entry
        vendor.delete()

        messages.success(request, "The vendor and all associated data have been deleted successfully.")

    return redirect('vendors_details')






def location_page(request):
    return render(request, "location_page.html")
def location_save(request):
    if request.method=="POST":
        name=request.POST.get("name")
        obj=location(name=name)
        obj.save()
        return redirect(location_page)



def contact_table(request):
    data = contact_Db.objects.all()
    return render(request, "contact_query_table.html", {"data": data})

def contact_delete(req,c_id):
    data=contact_Db.objects.get(id=c_id)
    data.delete()
    return redirect(contact_table)


def view_vendor_reviews(request, signup_db_id):
    # Get the Signup_db entry
    signup = get_object_or_404(Signup_db, id=signup_db_id, user_type='vendor')
    # Use the email to get the corresponding Vendor
    vendor = get_object_or_404(Vendor, email=signup.email)

    # Fetch reviews associated with the vendor
    reviews = Vendor_review_Db.objects.filter(vendor=vendor).order_by('-created_at')

    context = {
        'vendor': vendor,
        'reviews': reviews,
    }
    return render(request, 'vendor_review_page.html', context)

def food_single_table(request, signup_db_id):
    # Get the Signup_db entry
    signup = get_object_or_404(Signup_db, id=signup_db_id, user_type='vendor')

    # Use the email (or another identifier) to get the corresponding Vendor
    vendor = get_object_or_404(Vendor, email=signup.email)

    # Retrieve all food items associated with this vendor
    food = Food_single.objects.filter(vendor=vendor)

    # Render the page with the food items and vendor profile
    return render(request, "food_single_table.html", {'food': food, 'vendor': vendor})

def vendor_food_reviews(request, food_id):
    # Assuming food_id is passed correctly from the URL
    food_item = get_object_or_404(Food_single, pk=food_id)
    reviews = Food_review_Db.objects.filter(food=food_item).order_by('-created_at')
    vendor = get_object_or_404(Vendor, id=food_item.vendor.id)

    return render(request, 'vendor_food_reviews.html',{
        'food_item': food_item,
        'reviews': reviews,
        'vendor':vendor})