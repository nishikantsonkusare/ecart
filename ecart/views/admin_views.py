from django.shortcuts import render, HttpResponse, redirect
from ecart.forms.create_product import Create_Product_Form
from ecart.forms.UpdateProductForm import UpdateProductForm
from ecart.forms.BannerForm import BannerForm
from ecart.models import Product, Category, SubCategory, Order, Banner
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import date
from io import BytesIO
from django.conf import settings
# Create your views here.

# Home Page Data
received_order = Order.objects.filter(order_status='pending').distinct('order_number').count()
pending_order = Order.objects.filter(order_status='received').distinct('order_number').count()
complete_order = Order.objects.filter(order_status='shipped').distinct('order_number').count()
cancel_order = Order.objects.filter(order_status='rejected').distinct('order_number').count()


def admin_login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser == True:
            return redirect('/admin/dashboard/')
    if request.method == 'POST':
        user = request.POST.get('user')
        upass = request.POST.get('pass')

        user = authenticate(request, username=user, password=upass)
        if user is not None:
            if user.is_superuser == True:
                login(request, user)
                return redirect('/admin/dashboard/')
            else:
                messages.warning(request, 'You are not allow to login in administrator account.')
                return redirect('/admin/')    
        else:
            messages.warning(request, 'Please entered valid username and password')
            return redirect('/admin/')
    return render(request, 'ecart/admin/login.html')

def home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser == True:
            context = {
                'received_order': received_order,
                'pending_order': pending_order,
                'complete_order': complete_order,
                'cancel_order'  : cancel_order,
            }            
            return render(request, 'ecart/admin/home.html', context)
        else:
            return redirect('/admin/')
    else:
            return redirect('/admin/')

def new_product(request):
    if request.user.is_authenticated:
        if request.user.is_superuser == True:
            if request.method == 'POST':
                form = Create_Product_Form(request.POST, request.FILES)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Product is successfully save.')
                    return redirect('/admin/new_product_list/')
                else:
                    return render(request, 'ecart/admin/new_product.html', {'form': form})

            else:
                form = Create_Product_Form()
                return render(request, 'ecart/admin/new_product.html', {'form': form})
        else:
            return redirect('/admin/')
    else:
            return redirect('/admin/')

def add_category(request):
    if request.user.is_authenticated:
        if request.user.is_superuser == True:
            if request.method == 'POST':
                cat = request.POST['category']
                if cat:
                    data = Category(name=cat)
                    data.save()
                    messages.success(request, 'Category successfully Added.')
                    return redirect('/admin/add_category')
            else:
                data = Category.objects.all()
                return render(request, 'ecart/admin/add_category.html', {'data': data})
        else:
            return redirect('/admin/')
    else:
            return redirect('/admin/')

def add_subcategory(request):
    if request.user.is_authenticated:
        if request.user.is_superuser == True:
            if request.method == 'POST':
                cat = request.POST['category']
                sub_cat = request.POST['subcat']

                data = SubCategory(name=sub_cat, category_id=cat)
                data.save()
                messages.success(request, 'Sub-Category is updated.')
                return redirect('/admin/add_category')
        else:
            return redirect('/admin/')
    else:
            return redirect('/admin/')

def manage_stock(request):
    if request.user.is_authenticated:
        if request.user.is_superuser == True:
            data = Product.objects.values('id','product_name', 'stock').all()
            return render(request, 'ecart/admin/product_stock.html', {'data': data})
    else:
        return redirect('/admin/')

def update_stock(request, id):
    if request.user.is_authenticated:
        if request.user.is_superuser == True:
            if request.method == 'POST':
                stock = request.POST.get('stock')
                data = Product.objects.get(id=id)
                data.stock = stock
                data.save()
                messages.success(request, f'Stock is successfully update for <b>{data.product_name}</b>.')
                return redirect('/admin/manage_stock/')
        else:
            return HttpResponse('this is not working')
    else:
        return redirect('/admin/')

def manage_product(request):
    if request.user.is_authenticated:
        if request.user.is_superuser == True:
            data = Product.objects.values('id','product_name', 'stock').all()
            return render(request, 'ecart/admin/manage_product.html', {'data': data})
        else:
            return redirect('/admin/')
    else:
            return redirect('/admin/')

def update_product(request, id):
    if request.user.is_authenticated:
        if request.user.is_superuser == True:
            data = Product.objects.get(id=id)
            pro_data = {
                'product_name': data.product_name,
                'product_description': data.product_description,
                'mrp': data.mrp,
                'selling_price': data.selling_price,
                'stock': data.stock,
                'category_name': data.category_name,
                'sub_category': data.sub_category,
                'thumbnail': data.thumbnail,
                'img1': data.img1,
                'img2': data.img2,
                'img3':data.img3,
            }

            if request.method == 'POST':
                form = UpdateProductForm(request.POST, request.FILES)
                if form.is_valid():
                    form.save(commit=False)
                    product = Product.objects.get(id=id)
                    product.product_name = form.cleaned_data['product_name']
                    product.product_description = form.cleaned_data['product_description']
                    product.mrp = form.cleaned_data['mrp']
                    product.selling_price = form.cleaned_data['selling_price']
                    product.stock = form.cleaned_data['stock']
                    product.category_name = form.cleaned_data['category_name']
                    product.sub_category = form.cleaned_data['sub_category']
                    if form.cleaned_data['thumbnail'] != None:
                        product.thumbnail = form.cleaned_data['thumbnail']
                    if form.cleaned_data['img1'] != None:
                        product.img1 = form.cleaned_data['img1']
                    if form.cleaned_data['img2'] != None:
                        product.img2 = form.cleaned_data['img2']
                    if form.cleaned_data['img3'] != None:
                        product.img3 = form.cleaned_data['img3']
                    product.save()
                    messages.success(request, 'Product details successfully updated.')
                    return redirect('/admin/manage_product/')
                else:
                    return render(request, 'ecart/admin/update_product.html', {'form': form, 'id': id})    
            else:
                form = UpdateProductForm(initial=pro_data)
                return render(request, 'ecart/admin/update_product.html', {'form': form, 'id': id})
        else:
            return redirect('/admin/')
    else:
            return redirect('/admin/')

def delete_product(request, id):
    if request.user.is_authenticated:
        if request.user.is_superuser == True:
            data = Product.objects.get(id=id)
            data.delete()
            messages.success(request, f'"<b>{data.product_name}</b>" is successfully deleted.')
            return redirect('/admin/manage_product/')
        else:
            return redirect('/admin/')
    else:
        return redirect('/admin/')

def orders(request):
    if request.user.is_authenticated:
        if request.user.is_superuser == True:
            data = Order.objects.values('order_date', 'order_amount', 'order_number', 'order_status').filter(order_status='pending').distinct('order_number')
            return render(request, 'ecart/admin/orders.html', {'data': data})
        else:
            return redirect('/admin/')
    else:
            return redirect('/admin/')

def order_confirm(request, order_num):
    if request.user.is_authenticated:
        if request.user.is_superuser == True:
            data = Order.objects.filter(order_number = order_num)
            data.update(order_status='received')
            messages.success(request, f'Order No. <b>{order_num}</b> is received.')
            return redirect('/admin/orders/')
        else:
            return redirect('/admin/')
    else:
            return redirect('/admin/')

def order_reject(request, order_num):
    if request.user.is_authenticated:
        if request.user.is_superuser == True:
            data = Order.objects.filter(order_number = order_num)
            data.update(order_status='rejected')
            messages.success(request, f'Order No. <b>{order_num}</b> is rejected.')
            return redirect('/admin/orders/')
        else:
            return redirect('/admin/')
    else:
            return redirect('/admin/')

def rejected_order(request):
    if request.user.is_authenticated:
        if request.user.is_superuser == True:
            data = Order.objects.values('order_date', 'order_amount', 'order_number', 'order_status').filter(order_status='rejected').distinct('order_number')
            return render(request, 'ecart/admin/rejected_order.html', {'data': data})
        else:
            return redirect('/admin/')
    else:
            return redirect('/admin/') 

def readytoship(request):
    if request.user.is_authenticated:
        if request.user.is_superuser == True:
            data = Order.objects.values('order_date', 'order_number').filter(order_status='received').distinct('order_number')
            return render(request, 'ecart/admin/readytoshipped.html', {'data': data})
        else:
            return redirect('/admin/')
    else:
        return redirect('/admin/') 

def update_courier(request, order_num):
    if request.user.is_authenticated:
        if request.user.is_superuser == True:
            if request.method == 'POST':
                courier_name = request.POST.get('courier_name')
                tracking_id = request.POST.get('tracking_id')

                data = Order.objects.filter(order_number=order_num)
                data.update(courier_name=courier_name, tracking_id=tracking_id, order_status='shipped')
                messages.success(request, f'Order No. {order_num} shipping details updated.')
                return redirect('/admin/readytoship/')
        else:
            return redirect('/admin/')
    else:
        return redirect('/admin/') 

def all_order(request):
    if request.user.is_authenticated:
        if request.user.is_superuser == True:
            if request.method == 'POST':
                search_by = request.POST.get('search_by')
                data = Order.objects.filter(order_status=search_by).distinct('order_number')
                return render(request, 'ecart/admin/all_order.html', {'data': data})
            else:
                data = Order.objects.values('order_number', 'order_date', 'order_amount', 'order_status').all().distinct('order_number')
                return render(request, 'ecart/admin/all_order.html', {'data': data})
        else:
            return redirect('/admin/')
    else:
        return redirect('/admin/') 

def get_shipping_label(request):
    if request.user.is_authenticated:
        if request.user.is_superuser == True:
            data = Order.objects.values('order_number', 'order_date', 'order_amount', 'order_status').filter(order_status='shipped').distinct('order_number')
            return render(request, 'ecart/admin/shipping_details.html', {'data': data})
        else:
            return redirect('/admin/')
    else:
        return redirect('/admin/') 

def render_to_pdf(template_src, context_dict={}):
     template = get_template(template_src)
     html  = template.render(context_dict)
     result = BytesIO()
 
     #This part will create the pdf.
     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
     if not pdf.err:
         return HttpResponse(result.getvalue(), content_type='application/pdf')
     return None

def get_label(request, order_num):
    if request.user.is_authenticated:
        if request.user.is_superuser == True:
            data = Order.objects.values('product_name', 'qty','price').filter(order_number = order_num)
            data1 = Order.objects.values('order_number', 'order_amount', 'tracking_id', 'user', 'name', 'address', 'mobile').filter(order_number = order_num).distinct('order_number')
            context = {
                'order_number' : data1[0]['order_number'],
                'order_amount' : data1[0]['order_amount'],
                'name' : data1[0]['name'],
                'address' : data1[0]['address'],
                'mobile' : data1[0]['mobile'],
                'email' : data1[0]['user'],
                'tracking_id': data1[0]['tracking_id'],
                'data' : data,
                'date' : date.today(),
                'seller_name': settings.COMPANY_NAME,
                'seller_address': settings.COMPANY_ADDRESS,
                'gst_no': settings.GST_NO,
            }

            pdf = render_to_pdf('ecart/admin/shipping_slip.html', context)
            return HttpResponse(pdf, content_type='application/pdf')
        else:
            return redirect('/admin/')
    else:
        return redirect('/admin/')    

def banner(request):
    if request.user.is_authenticated:
        if request.user.is_superuser == True:
            if request.method == 'POST':
                form = BannerForm(request.POST, request.FILES)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Banner is successfully uploaded.')
                    return redirect('/admin/banner/')
                else:
                    return render(request, 'ecart/admin/banner.html', {'form': form})  
            data = Banner.objects.all()      
            form = BannerForm()
            return render(request, 'ecart/admin/banner.html', {'form': form, 'data' : data})
        else:
            return redirect('/admin/')
    else:
        return redirect('/admin/')

def delete_banner(request, id):
    if request.user.is_authenticated:
        if request.user.is_superuser == True:
            Banner.objects.filter(id=id).delete()
            messages.success(request, 'Banner is successfully deleted.')
            return redirect('/admin/banner/')
        else:
            return redirect('/admin/')
    else:
        return redirect('/admin/')