from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from ecart.views import admin_views

urlpatterns = [

    path('', admin_views.admin_login, name='Login'),
    path('dashboard/', admin_views.home, name='home'),
    path('new_product_list/', admin_views.new_product, name='new_product'),
    path('add_category/', admin_views.add_category, name='add_category'),
    path('add_subcategory/', admin_views.add_subcategory, name='add_subcategory'),
    path('manage_stock/', admin_views.manage_stock, name='Manage Stock'),
    path('update_stock/<id>', admin_views.update_stock, name='Update Stock'),
    path('manage_product/', admin_views.manage_product, name='Manage Product'),
    path('update_product/<id>', admin_views.update_product, name='Update Product'),
    path('delete_product/<id>', admin_views.delete_product, name='Delete Product'),
    path('orders/', admin_views.orders, name='Orders'),
    path('order_confirm/<order_num>/', admin_views.order_confirm, name='Order Confirm'),
    path('order_reject/<order_num>/', admin_views.order_reject, name='Order Confirm'),
    path('rejected_order/', admin_views.rejected_order, name='Rejected Order'),
    path('readytoship/', admin_views.readytoship, name='Ready to Ship'),
    path('update_courier/<order_num>/', admin_views.update_courier, name='Update Courier Name'),
    path('all_order/', admin_views.all_order, name='All Order'),
    path('get_shipping_label/', admin_views.get_shipping_label, name='Get Shipping Label'),
    path('get_label/<order_num>/', admin_views.get_label, name='Get Shipping Label'),
    path('banner/', admin_views.banner, name='Upadate Banner'),
    path('banner/delete/id=<id>/', admin_views.delete_banner, name='Delete Banner'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
