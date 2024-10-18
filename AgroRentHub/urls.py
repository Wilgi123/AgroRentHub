# urls.py (main project file)
from agroapp import views  # Import views from your app
from django.contrib import admin
from django.urls import include, path
from django.conf import settings 
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # Home page
    path('about_us/', views.about_us, name='about_us'),  # About Us page
    path('services/', views.services, name='services'),  # Services page
    path('contact/', views.contact, name='contact'),  # Contact page
    path('rental-items/', views.rental_items, name='rental_items'),
    path('register/', views.register, name='register'),  # Register page
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('check_email/', views.check_email, name='check_email'),
    path('login/', views.login_view, name='login'),  # Login page
    path('forgotpassword/', views.forgotpassword, name='forgotpassword'),
    path('resetpassword/<uidb64>/<token>/', views.resetpassword, name='resetpassword'),
    path('logout/', views.logout_view, name='logout'), 
    path('social-auth/', include('social_django.urls', namespace='social')),
    
    path("customer_index/", views.customer_index, name="customer_index"),
    path('customer/customer_profile/', views.customer_profile, name='customer_profile'),
    path('customer/customer_about/', views.customer_about, name='customer_about'),
    path('customer/customer_service/', views.customer_service, name='customer_service'),
    path('customer/customer_profile/edit/', views.edit_details, name='edit_details'),
    path('customer/customer_profile/change_password/', views.change_password, name='change_password'),
    path('customer/products/', views.products, name='products'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('productcart/', views.productcart, name='productcart'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('delete_cart_item/<int:item_id>/', views.delete_cart_item, name='delete_cart_item'),
    path('place_order/', views.place_order, name='place_order'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('payment_cancel/', views.payment_cancel, name='payment_cancel'),
    path('orderdetails/', views.order_details, name='orderdetails'),
    path('delete_order/<int:order_id>/', views.delete_order, name='delete_order'),
    path('orderdetails/',views.order_details, name='order_details'),
    path('download_receipt/<int:order_id>/', views.download_receipt, name='download_receipt'),
      path('orderproductview/<int:order_id>/', views.orderproductview, name='orderproductview'),
    
      path('schedule_return/', views.schedule_return, name='schedule_return'),


    path("supplier_index/", views.supplier_index, name="supplier_index"),
    path('supplier_add_pro/', views.supplier_add_pro, name='supplier_add_pro'),
    path('supplier_add_pro/supplier_view_pro/', views.supplier_view_pro, name='supplier_view_pro'),
    path('supplier_view_pro/', views.supplier_view_pro, name='supplier_view_pro'),
    path('update_product/<int:product_id>/', views.update_product, name='update_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('supplier_add_cat/', views.supplier_add_cat, name='supplier_add_cat'),
    path('supplier_add_cat/supplier_view_cat/', views.supplier_view_cat, name='supplier_view_cat'),
    path('supplier_view_cat/', views.supplier_view_cat, name='supplier_view_cat'),
    path('update_category/<int:category_id>/', views.update_category, name='update_category'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('supplier_add_del/', views.supplier_add_del, name='supplier_add_del'),
    #path('supplier/supplier_view_del/', views.supplier_view_del, name='supplier_view_del'),
    path('supplier_view_del/', views.supplier_view_del, name='supplier_view_del'),
    path('delete_delivery_boy/<int:delivery_boy_id>/', views.delete_delivery_boy, name='delete_delivery_boy'),

    path('add_product_damage/', views.add_product_damage, name='add_product_damage'),
path('view_product_damage/', views.view_product_damage, name='view_product_damage'),
    path('supplier/supplier_add_worker/', views.supplier_add_worker, name='supplier_add_worker'),
    path('supplier/supplier_view_worker/', views.supplier_view_worker, name='supplier_view_worker'),
    path('supplier/supplier_view_order/', views.supplier_view_order, name='supplier_view_order'),
    path('supplier/supplier_profile/', views.supplier_profile, name='supplier_profile'),
    path('supplier/edit-details/', views.supplier_edit_details, name='supplier_edit_details'),
    path('supplier/change-password/', views.supplier_change_password, name='supplier_change_password'),
    
    path("admin_index/", views.admin_index, name="admin_index"),
    path('admin_view_farmer/', views.admin_view_farmer, name='admin_view_farmer'),
    path('admin_view_supplier/', views.admin_view_supplier, name='admin_view_supplier'),
    path('admin_view_deliveryboy/', views.admin_view_deliveryboy, name='admin_view_deliveryboy'),
    path('block_user/', views.block_user, name='block_user'),
    path('admin_view_pro/', views.admin_view_pro, name='admin_view_pro'),
    path('admin/admin_view_pro/toggle/<int:product_id>/', views.toggle_product_status, name='toggle_product_status'),
    path('toggle-product-status/<int:product_id>/', views.toggle_product_status, name='toggle_product_status'),
    path('admin_view_cat/', views.admin_view_cat, name='admin_view_cat'),
    path('toggle-category-status/', views.toggle_category_status, name='toggle_category_status'),
    path('toggle_user_status/<str:user_type>/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
    #path('admin_view_worker/', views.admin_view_worker, name='admin_view_worker'),
    path('admin_view_order/', views.admin_view_order, name='admin_view_order'),
    path('admin/admin_view_order/assign/', views.assign_order, name='assign_order'),
    path('assign-order/', views.assign_order, name='assign_order'),
    path('cancel_assignment/', views.cancel_assignment, name='cancel_assignment'),
    path('assign-order-page/<int:order_id>/', views.assign_order_page, name='assign_order_page'),
    path('admin_view_damagedpro/', views.admin_view_damagedpro, name='admin_view_damagedpro'),
    
    #path('admin/admin_view_worker/', views.admin_view_worker, name='admin_view_worker'),
    #path('admin/admin_view_order/', views.admin_view_order, name='admin_view_order'),

    path("deliveryboy/deliveryboy_index/", views.deliveryboy_index, name="deliveryboy_index"),
    path("deliveryboy/deliveryboy_profile/", views.deliveryboy_profile, name="deliveryboy_profile"),
    path('edit-details/', views.deliveryboy_edit_details, name='deliveryboy_edit_details'),
    path('change-password/', views.deliveryboy_change_password, name='deliveryboy_change_password'),
    path('deliveryboy/deliveryboy_view_order/', views.deliveryboy_view_order, name='deliveryboy_view_order'),
    path('deliveryboy/ship_order/', views.ship_order, name='deliveryboy_ship_order'),
    path('generate-otp-delivery/', views.generate_otp_delivery, name='generate_otp_delivery'),
    path('verify-otp-delivery/', views.verify_otp_delivery, name='verify_otp_delivery'),
    path('ship-order/', views.ship_order, name='ship_order'),

    path('deliveryboy/deliveryboy_return_management/', views.deliveryboy_return_management, name='deliveryboy_return_management'),
   path('process-return/<int:order_id>/', views.process_return, name='process_return'),
    path('return-product/<int:order_id>/', views.return_product, name='return_product'),  # Add this line
    path('process-return/<int:order_id>/', views.process_return, name='process_return'),  # Add this line
     path('damaged-products/', views.deliveryboy_view_damages, name='deliveryboy_view_damages'),
 path('damaged-products-chart/', views.deliveryboy_view_damages_chart, name='deliveryboy_view_damages_chart'),
  path('get-estimated-repair-cost/', views.get_estimated_repair_cost, name='get_estimated_repair_cost'),
   path('process-return-payment/<int:order_id>/', views.process_return_payment, name='process_return_payment'),



    path('deliveryboy/deliveryboy_deliveries/', views.deliveryboy_deliveries, name='deliveryboy_deliveries'),
    path('deliveryboy/deliveryboy_earnings/', views.deliveryboy_earnings, name='deliveryboy_earnings'),
    path('deliveryboy/deliveryboy_support/', views.deliveryboy_support, name='deliveryboy_support'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
