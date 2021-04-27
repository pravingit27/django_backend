from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django import forms
from phone_field import PhoneField

class Category(models.Model):
    title = models.CharField(max_length=300)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Product(models.Model):
    #slug = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100,primary_key=True)
    category = models.ForeignKey(Category,related_name='products',on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.IntegerField(default=0, null=True, blank=True)
    image = models.ImageField(null=True,blank=True,upload_to ='post_images')
    owner = models.ForeignKey('Admin',related_name='products',on_delete=models.CASCADE, null=True)
    date_created = models.DateField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return '{} {}'.format(self.name, self.price)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super(Product, self).save(*args, **kwargs)


class Admin(AbstractUser):
    name = models.CharField(max_length=100,default='Anonymous')
    farm_name = models.CharField(max_length=100,blank=True,null=True)
    phone_number = models.CharField(max_length=20,blank=True,null=True)
    email = models.EmailField(max_length=40)
    username = models.CharField(max_length=50,unique=True,primary_key=True)
    product = models.ForeignKey('Product',related_name='products',on_delete=models.CASCADE,null=True,blank=True)
    password = models.CharField(max_length=20)
    session_token = models.CharField(max_length=10,default=0)
    created_at = models.DateField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

class cart(models.Model):
    cart_id = models.OneToOneField(Admin, on_delete=models.CASCADE, primary_key=True)
    created_at = models.DateField(auto_now_add=True)
    products = models.ManyToManyField(Product)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return '{}' .format(self.cart_id)

class order(models.Model):
    name = models.CharField(max_length=500,default=True)
    city = models.CharField(max_length=500,default=True)
    address = models.CharField(max_length=500,default=True)
    phone_num = PhoneField(blank=True,help_text='contact number')
    product_names = models.CharField(max_length=500)
    price = models.FloatField(default=True)
    product_quantity = models.IntegerField(default=0, null=True, blank=True)
    #order_id = models.CharField(max_length=150,default=0)
    sub_total = models.CharField(max_length=50,default=0)
    final_total = models.CharField(max_length=500,default=0)
    created_at = models.DateField(auto_now_add=True)

class calory(models.Model):
    name = models.CharField(max_length=200,primary_key=True)
    serving = models.CharField(max_length=500,null=True,blank=True)
    calories = models.CharField(max_length=500,null=True,blank=True)

    class Meta:
        verbose_name_plural = 'Calories'

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super(calory, self).save(*args, **kwargs)


