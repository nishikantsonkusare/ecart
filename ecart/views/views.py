from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password
from ecart.models import Product, Category, SubCategory, Order, Banner
from ecart.forms.UserForm import UserForm
from ecart.models import UserProfile
import json
from datetime import date
from django.contrib import messages
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string, get_template
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from ecart.forms.Profile_Update import UpdateUser, UpdateProfile
from ecart.forms.ChangePasswordForm import ChangePasswordForm
from ecart.views.admin_views import render_to_pdf
from django.db.models import Subquery
# Create your views here.

cat = Category.objects.all()
sub_cat = SubCategory.objects.all()

def home(request):
    print(settings.ALLOWED_HOSTS[0])
    banner = Banner.objects.all()
    data = Product.objects.all()[:20]
    allprod = []
    for i in cat:
        prod = Product.objects.filter(category_name_id = i.id)[:10]
        if prod:
            allprod.append(prod)

    return render(request, 'ecart/index.html', {'data': data, 'cat': cat, 'sub_cat': sub_cat, 'banner': banner, 'allprod':allprod})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        upass = request.POST.get('upass')

        user = authenticate(request, username=username, password=upass)
        if user is not None:
            if user.userprofile.is_verified == True:
                login(request, user)
                return redirect('/')
            else:
                messages.warning(request, 'Please verify account by link send on your email.')
                return redirect('/login/')
        else:
            messages.warning(request, 'Please enter valid username and password.')
            return redirect('/login/')
    else:
        return render(request, 'ecart/login.html', {'cat': cat, 'sub_cat': sub_cat})

def registration(request):
    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(user.password)
            token = uuid.uuid4()
            profile = UserProfile(user=user, token=token)
            url = f'{settings.ALLOWED_HOSTS[0]}/email/confirm_token={token}'    
            subject = 'E-cart account verification email'
            context = {
                'name': user.first_name,
                'url': url,
            }
            message = get_template('ecart/email_template.html').render(context)
            email_from = settings.EMAIL_HOST_USER
            recipient = [user.username,]
            if send_mail(subject,'', email_from, recipient, html_message=message):
                user.save()
                profile.save()
                messages.success(request, f'Account is successfully created and verification mail send on <strong>"{user.username}"</strong>.')
            else:
                messages.success(request, f'Please entered valid email address.')
            return redirect('/registration/')
        else:
            return render(request, 'ecart/registration.html', {'form': form, 'cat': cat, 'sub_cat': sub_cat})
    else:
        form = UserForm()
        return render(request, 'ecart/registration.html', {'form': form, 'cat': cat, 'sub_cat': sub_cat})

def email_verification(request, token):
    data = UserProfile.objects.get(token=token)
    data.is_verified = True
    data.save()
    messages.success(request, 'Your account successfully activate.')
    return redirect('/login/')

def product_view(request, id):
    data = Product.objects.get(pk=id)
    product = Product.objects.filter(category_name_id=data.category_name_id, sub_category_id=data.sub_category_id)
    context = {
        'product': data,
        'product_data': product,
        'cat': cat,
        'sub_cat': sub_cat
    }
    return render(request, 'ecart/product_view.html', context)

def category_wise(request, id, sub_name):
    product_filter = SubCategory.objects.filter(name=sub_name, category_id=id)
    products = Product.objects.filter(category_name_id=product_filter[0].category_id, sub_category_id=product_filter[0].id)
    context = {
        'products': products,
        'page_name': product_filter[0].name,
        'cat': cat,
        'sub_cat': sub_cat,
    }
    return render(request, 'ecart/category_wise_product.html', context)

def cart(request):
    return render(request, 'ecart/cart.html', {'cat': cat, 'sub_cat': sub_cat})

def checkout_status(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            if user.userprofile.address and user.userprofile.mobile:
                pro_id = []
                qty = {}
                amount = 0
                counter = int(request.POST['counter'])
                
                for i in range(1, counter+1):
                    pro_id.append(request.POST['id_'+str(i)])
                    qty[request.POST['id_'+str(i)]] = request.POST['qty_'+str(i)]
        
                pro_data = Product.objects.filter(id__in=pro_id)
                
                for i in pro_data:
                    amount += (int(qty[str(i.id)]) * int(i.selling_price))
                    print(amount)

                for item in pro_data:
                    if int(qty[str(item.id)]) > 3 or int(qty[str(item.id)]) == 0:
                        messages.warning(request, 'Please check valid product order quantity.')
                        return redirect('/cart/')
                
                # Create Razor Pay Client
                client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))
                # Checkout logic
                order_amount = amount * 100
                order_currency = 'INR'
                payment_order = client.order.create(dict(amount=order_amount, currency=order_currency, payment_capture=1))
                payment_order_id = payment_order['id']
                if payment_order['status'] == 'created':
                    for i in pro_data:
                        data = Order(user='nish.so007@gmail.com', product_id = i.id, product_name=i.product_name, price=i.selling_price, qty=int(qty[str(item.id)]), order_amount=amount, order_number=payment_order_id, order_status=payment_order['status'], img_url=i.thumbnail.url)
                        data.save()
                context = {
                    'amount' : amount,
                    'api_key' : settings.RAZORPAY_KEY_ID,
                    'order_id' : payment_order_id,
                    'product': pro_data,
                    'qty': qty,
                    'cat': cat,
                    'sub_cat': sub_cat
                }
                return render(request, 'ecart/checkout.html', context)
            else:
                messages.warning(request, 'Kindly update address and mobile in profile.')
                return redirect('checkout/status=review/')
        else:
            return redirect('/cart/')
    else:
        messages.warning(request, 'Please login before checkout.')
        return redirect('/login/')

@csrf_exempt
def order_confirmation(request):
    if request.user.is_authenticated:
        response = request.POST
        params_dict = {
            'razorpay_payment_id': response['razorpay_payment_id'],
            'razorpay_order_id': response['razorpay_order_id'],
            'razorpay_signature': response['razorpay_signature'],
        }

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))
        check = client.utility.verify_payment_signature(params_dict)
        if check == None:
            user = request.user
            data = Order.objects.filter(order_number=response['razorpay_order_id'])
            data.update(transaction_id=response['razorpay_payment_id'], payment_signature=response['razorpay_signature'], order_status='pending', name=(request.user.first_name + ' ' + request.user.last_name), address=user.userprofile.address, mobile=user.userprofile.mobile, user=request.user.username)
            Order.objects.filter(user='nish.so007@gmail.com', order_status='created').delete()
            return render(request, 'ecart/order_confirmation.html', {'cat': cat, 'sub_cat': sub_cat})
        else:
            messages.warning(request, 'Payment is not completed for your order.')
            return redirect('/cart/')
        
        return render(request, 'ecart/order_confirmation.html', {'cat': cat, 'sub_cat': sub_cat})

    else:
        return redirect('/')

def my_order(request):
    if request.user.is_authenticated:
        # values('order_number', 'order_date', 'courier_name', 'tracking_id', 'order_amount')
        # order_num = Order.objects.filter(user = request.user.username).order_by('-order_date').order_by('order_number').distinct('order_number').values('order_number', 'order_date', 'courier_name', 'tracking_id', 'order_amount')
        order_num = Order.objects.filter(
            pk__in = Subquery (
                Order.objects.values('id').distinct('order_number')
            )
        ).values('order_number', 'order_date', 'courier_name', 'tracking_id', 'order_amount').order_by('-order_date')
        orders = Order.objects.filter(user = request.user.username)
        context = {
            'cat': cat,
            'sub_cat': sub_cat,
            'order_num': order_num,
            'orders': orders,
        }
        return render(request, 'ecart/order.html', context)
    else:
        return redirect('/')

def profile(request):

    if request.user.is_authenticated:
        user = request.user
        data = {
            'first_name' : request.user.first_name,
            'last_name': request.user.last_name,
            'username' : request.user.username,
            'mobile' : user.userprofile.mobile,
            'address' : user.userprofile.address,
        }

        if request.method == 'POST':
            form1 = UpdateUser(data = request.POST, instance = request.user)
            form2 = UpdateProfile(request.POST, request.FILES, instance = request.user)
            if (form1.is_valid() and form2.is_valid()) or form.is_valid():
                user = form1.save(commit=False)
                profile = UserProfile.objects.get(user_id=request.user.id)
                profile.address = form2.cleaned_data['address']
                profile.mobile = form2.cleaned_data['mobile']
                profile.profile_image = form2.cleaned_data['profile_image']
                user.save()
                profile.save()
                return redirect('/profile/')
            else:
                return render(request, 'ecart/profile.html', {'form1': form1, 'form2': form2, 'cat': cat, 'sub_cat': sub_cat})    
        else:
            form1 = UpdateUser(initial = data)
            form2 = UpdateProfile(initial = data)
            return render(request, 'ecart/profile.html', {'form1': form1, 'form2': form2, 'cat': cat, 'sub_cat': sub_cat})
    else:    
        return redirect('/')

def change_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ChangePasswordForm(user = request.user, data = request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, 'Password is successfully changed.')
                return redirect('/changepassword/')
            else:
                return render(request, 'ecart/changepassword.html', {'form': form, 'cat': cat, 'sub_cat': sub_cat})    
        else:
            form = ChangePasswordForm(user = request.user)
            return render(request, 'ecart/changepassword.html', {'form': form, 'cat': cat, 'sub_cat': sub_cat   })
    else:
        return redirect('/')

def get_invoice(request, order_num):
    if request.user.is_authenticated:
        check_data = Order.objects.values('courier_name').filter(order_number=order_num).distinct('order_number')
        if check_data[0]['courier_name']:
            data = Order.objects.values('product_name', 'qty','price').filter(order_number = order_num)
            data1 = Order.objects.values('order_number', 'order_amount', 'tracking_id', 'user', 'name', 'address', 'mobile').filter(order_number = order_num).distinct('order_number')
            total_selling_price = 0
            total_tax_amount = 0
            for i in data:
                total_selling_price += i['price']/100 * 82
                total_tax_amount += i['price']/100 * 18
            context = {
                'order_number' : data1[0]['order_number'],
                'order_amount' : data1[0]['order_amount'],
                'name' : data1[0]['name'],
                'address' : data1[0]['address'],
                'mobile' : data1[0]['mobile'],
                'email' : data1[0]['user'],
                'tracking_id': data1[0]['tracking_id'],
                'data' : data,
                'gst_rate' : '18%',
                'total_selling_price' : total_selling_price,
                'total_tax_amount' : total_tax_amount,
                'date' : date.today(),
                'seller_name': settings.COMPANY_NAME,
                'seller_address': settings.COMPANY_ADDRESS,
                'gst_no': settings.GST_NO,
            }

            pdf = render_to_pdf('ecart/invoice.html', context)
            return HttpResponse(pdf, content_type='application/pdf')
        else:
            messages.warning(request, f'Order number <b>{order_num}</b> not yet shipped.')
            return redirect('/my_order/')
    else:
        return redirect('/')

def user_logout(request):
    logout(request)
    return redirect('/')

