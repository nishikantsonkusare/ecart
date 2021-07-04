from django.db import models
import uuid
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_name = models.CharField(max_length=100, null=False, blank=False)
    product_description = RichTextField(null=False, blank=False)
    mrp = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    stock = models.PositiveIntegerField(null=False, blank=False)
    category_name = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True)
    thumbnail = models.ImageField(null=False, blank=True, upload_to='product/', default='')
    img1 = models.ImageField(null=True, blank=True, upload_to='product/')
    img2 = models.ImageField(null=True, blank=True, upload_to='product/')
    img3 = models.ImageField(null=True, blank=True, upload_to='product/')
    publish_date = models.DateField(default=timezone.now, blank=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=256, null=True, blank=True)
    mobile = models.CharField(max_length=10, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile/', default='', blank=True)
    token = models.CharField(max_length=256, null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Order(models.Model):
    user = models.CharField(max_length=256, null=False, blank=False)
    name = models.CharField(max_length=256, null=False, blank=False)
    address = models.CharField(max_length=256, null=False, blank=False)
    mobile = models.CharField(max_length=10, null=False, blank=False)
    product_id = models.CharField(max_length=256, null=False, blank=False)
    product_name = models.CharField(max_length=256, null=False, blank=False)
    price = models.IntegerField(default=0)
    img_url = models.CharField(max_length=500, blank=True)
    qty = models.IntegerField()
    order_date = models.DateField(default=timezone.now)
    order_amount = models.PositiveIntegerField(null=True)
    order_number = models.CharField(max_length=256, null=False, blank=True)
    transaction_id = models.CharField(max_length=256, null=False, blank=True)
    payment_signature = models.CharField(max_length=256, null=False, blank=True)
    order_status = models.CharField(max_length=50, null=False, blank=True)
    courier_name = models.CharField(max_length=100, null=False, blank=True)
    tracking_id = models.CharField(max_length=100, null=False, blank=True)

class Banner(models.Model):
    image = models.ImageField(upload_to='banner/', null=True, blank=False)