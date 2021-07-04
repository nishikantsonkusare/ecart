from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from ecart.views import views

urlpatterns = [

    path('', views.home, name='home'),
    path('product_view=<id>/', views.product_view, name='product_view'),
    path('cart/', views.cart, name='cart'),
    path('checkout/status=review/', views.checkout_status, name='checkout'),
    path('order_confirmation/', views.order_confirmation, name='order confirmation'),
    path('login/', views.user_login, name='Login'),
    path('registration/', views.registration, name='Registration'),
    path('my_order/', views.my_order, name='My Order'),
    path('email/confirm_token=<token>/', views.email_verification, name='verification email' ),
    path('category_id=<id>/sub_category=<sub_name>/', views.category_wise, name='category wise product list'),
    path('profile/', views.profile, name='Profile View'),
    path('changepassword/', views.change_password, name='Change Password'),
    path('get_invoice/<order_num>', views.get_invoice, name='Get Invoice'),
    path('logout/', views.user_logout, name='logout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
