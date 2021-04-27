from django.contrib import admin
from .models import Category,Product,cart,Admin,order,calory
from django.contrib.auth.admin import UserAdmin
# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(cart)
admin.site.register(Admin)
admin.site.register(order)
admin.site.register(calory)
