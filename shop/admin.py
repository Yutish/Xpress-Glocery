from django.contrib import admin

from .models import Product, Cart, Order, Profile, Product_Request, Received_Order

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Profile)
admin.site.register(Product_Request)
admin.site.register(Received_Order)
