from django.contrib import admin
from .models import Product,Cart,CartItem,Transaction
# Register your models here.

admin.site.register([Product,Cart,CartItem,Transaction])
