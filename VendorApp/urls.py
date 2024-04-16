from django.urls import path
from VendorApp import views


urlpatterns=[
    path('vendor_index_page/', views.vendor_index_page, name='vendor_index_page'),
    path('vendor_profile_page/', views.vendor_profile_page, name='vendor_profile_page'),
    path('vendor_profile_add_details/', views.vendor_profile_add_details, name='vendor_profile_add_details'),
    path('vendor_profile_edit/', views.vendor_profile_edit, name='vendor_profile_edit'),
    path('vendor_save_profile/', views.vendor_save_profile, name='vendor_save_profile'),
    path('vendor_update_profile/<int:p_id>/', views.vendor_update_profile, name='vendor_update_profile'),
    path('vendor_delete_profile/', views.vendor_delete_profile, name='vendor_delete_profile'),
    path('vendor_delete_account/', views.vendor_delete_account, name='vendor_delete_account'),




    path('add_food_details/', views.add_food_details, name='add_food_details'),
    path('add_food_single_details/', views.add_food_single_details, name='add_food_single_details'),
    path('food_save/', views.food_save, name='food_save'),
    path('food_single_save/', views.food_single_save, name='food_single_save'),
    path('single_food_table/', views.single_food_table, name='single_food_table'),
    path('food_reviews/<int:food_id>/', views.food_reviews, name='food_reviews'),
    path('food_table/', views.food_table, name='food_table'),
    path('edit_food_details/<int:food_id>/', views.edit_food_details, name='edit_food_details'),
    path('update_food_details/<int:food_id>/', views.update_food_details, name='update_food_details'),
    path('food_delete/<int:food_id>/', views.food_delete, name='food_delete'),



    path('edit_food_single_details/<int:food_id>/', views.edit_food_single_details, name='edit_food_single_details'),
    path('update_food_single/<int:food_id>/', views.update_food_single, name='update_food_single'),
    path('single_food_delete/<int:food_id>/', views.single_food_delete, name='single_food_delete'),

    # path('food/update/<int:food_id>/', views.food_update, name='food_update'),
    path('food/delete/<int:food_id>/', views.food_delete, name='food_delete'),
    path('users_order_details/', views.users_order_details, name='users_order_details'),
    path('vendor_review/', views.vendor_review, name='vendor_review'),
    path('delete_review/<int:review_id>/', views.delete_review, name='delete_review'),





]