from django.urls import path
from Admin import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin_index_page/', views.admin_index_page, name='admin_index_page'),
    path('add_food_items/', views.add_food_items, name='add_food_items'),
    path('food_items_save/', views.food_items_save, name='food_items_save'),
    path('admin_food_table/', views.admin_food_table, name='admin_food_table'),
path('edit_food_items/<int:food_id>/', views.edit_food_items, name='edit_food_items'),
    path('update_food_item/<int:food_id>/', views.update_food_item, name='update_food_item'),

    path('food_item_delete/<int:food_id>/', views.food_item_delete, name='food_item_delete'),
    path('vendors_details/', views.vendors_details, name='vendors_details'),
    path('vendors_food_history/', views.vendors_food_history, name='vendors_food_history'),

    path('users_orders_page/', views.users_orders_page, name='users_orders_page'),
    path('users_orders_status/<str:username>/', views.users_orders_status, name='users_orders_status'),

    path('approve_vendor/<int:user_id>/', views.approve_vendor, name='approve_vendor'),
    path('reject_vendor/<int:user_id>/', views.reject_vendor, name='reject_vendor'),
    path('delete_vendor/<int:user_id>/', views.delete_vendor, name='delete_vendor'),

    path('location_save/', views.location_save, name='location_save'),
    path('location_page', views.location_page, name='location_page'),
    path('contact_table/', views.contact_table, name='contact_table'),
    path('contact_delete/<int:c_id>/', views.contact_delete, name='contact_delete'),
    path('view_vendor_reviews/<int:signup_db_id>/', views.view_vendor_reviews, name='view_vendor_reviews'),
    path('food_single_table/<int:signup_db_id>/', views.food_single_table, name='food_single_table'),
    path('vendor_food_reviews/<int:food_id>/', views.vendor_food_reviews, name='vendor_food_reviews'),





    




  
    
]