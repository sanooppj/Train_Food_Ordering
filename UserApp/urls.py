from django.urls import path
from UserApp import views

urlpatterns = [
    path('login_page/', views.login_page, name='login_page'),
    path('signup_page/', views.signup_page, name='signup_page'),
    path('register_user/', views.register_user, name='register_user'),
    path('login_user/', views.login_user, name='login_user'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('Forgot_page/', views.Forgot_page, name="Forgot_page"),
    path('forgot_password/', views.forgot_password, name="forgot_password"),
    path('verification_page/', views.verification_page, name="verification_page"),
    path('change_password/<str:token>/', views.change_password, name="change_password"),



    path('Home_page/', views.Home_page, name='Home_page'),
    path('view_food_restaurant/<str:name>/', views.view_food_restaurant, name='view_food_restaurant'),

    path('search_foods/', views.search_foods, name='search_foods'),


    path('profile_page/', views.profile_page, name='profile_page'),
    path('profile_edit/', views.profile_edit, name='profile_edit'),
    path('save_profile/', views.save_profile, name='save_profile'),
    path('order_view/', views.order_view, name='order_view'),
    path('update_profile/<int:p_id>/', views.update_profile, name='update_profile'),
    path('delete_profile/', views.delete_profile, name='delete_profile'),
    path('delete_account/', views.delete_account, name='delete_account'),



    path('profile_orders/', views.profile_orders, name='profile_orders'),
    path('cancel_order/<int:order_id>', views.cancel_order, name='cancel_order'),
    path('order_view/<int:order_id>', views.order_view, name='order_view'),
    path('update_order_status/', views.update_order_status, name='update_order_status'),
    path('delete_selected_orders', views.delete_selected_orders, name='delete_selected_orders'),



    path('profile_change_password/', views.profile_change_password, name='profile_change_password'),
    path('profile_add_details/', views.profile_add_details, name='profile_add_details'),
    


    path('menu_page/', views.menu_page, name='menu_page'),
    path('cart_page/', views.cart_page, name='cart_page'),
    path('save_cart/', views.save_cart, name='save_cart'),
    path('Update_cart/', views.Update_cart, name='Update_cart'),
    path('delete_cart/', views.delete_cart, name='delete_cart'),
    path('Checkout_page/', views.Checkout_page, name='Checkout_page'),
    path('payment_section/', views.payment_section, name='payment_section'),
    path('save_booking_details/', views.save_booking_details, name='save_booking_details'),
    path('place_order/', views.place_order, name='place_order'),
    path('order_confirmed/<str:order_id>/', views.order_confirmed, name='order_confirmed'),







    path('about_page/', views.about_page, name='about_page'),
    path('contact_page/', views.contact_page, name='contact_page'),
    path('contact_save/', views.contact_save, name='contact_save'),
    path('view_food_restaurant/', views.view_food_restaurant, name='view_food_restaurant'),
    path('food_inner_page/<int:vendor_id>/<str:name>/', views.food_inner_page, name='food_inner_page'),
    path('vendor_single_page/<int:vendor_id>/', views.vendor_single_page, name='vendor_single_page'),
    path('save_review/<int:vendor_id>/', views.save_review, name="save_review"),
    path('single_product/<int:food_id>/', views.single_product, name='single_product'),
    path('save_food_review/<int:food_id>/', views.save_food_review, name='save_food_review'),





]

