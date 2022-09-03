from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.conf import settings

CATEGORY_CHOICES = (
    ('S', 'Staples'),
    ('SB', 'Snacks and Branded Food'),
    ('B', 'Beverages'),
    ('PC', 'Personal Care'),
    ('HC', 'Home Care'),
    ('BC', 'Baby Care')
)


class Product(models.Model):
    #     products_id = models.AutoField
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_name = models.CharField(max_length=100)
    mrp = models.FloatField()
    consumer_price = models.FloatField()
    wholesaler_price = models.FloatField()
    desc = models.TextField(max_length=400)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to="shop/images", default="")
    large_image = models.ImageField(upload_to="shop/images", default="")

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return reverse("Product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("addToCart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("removeFromCart", kwargs={
            'slug': self.slug
        })


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.product.product_name}"

    def get_total_mrp(self):
        return round(self.quantity * self.product.mrp, 2)

    def get_total_item_price(self):
        account_type = Profile.objects.filter(user=self.user)[0].account_type
        if account_type == 'P':
            return round(self.quantity * self.product.consumer_price, 2)
        else:
            return round(self.quantity * self.product.wholesaler_price, 2)

    def get_total_you_save(self):
        account_type = Profile.objects.filter(user=self.user)[0].account_type
        if account_type == 'P':
            return round(self.quantity * (self.product.mrp - self.product.consumer_price), 2)
        else:
            return round(self.quantity * (self.product.mrp - self.product.wholesaler_price), 2)


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(Order)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email
    
    def get_billed_amount(self):
        billed = 0
        for item in self.items.all():
            billed += item.get_total_item_price()
        return round(billed, 2)
    
    def get_total_amount(self):
        total = 0
        for item in self.items.all():
            total += item.get_total_item_price()
        total += 25
        return round(total, 2)

    def get_total_savings(self):
        savings = 0
        for item in self.items.all():
            savings += item.get_total_you_save()
        return round(savings, 2)


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=1)
    address_line_1 = models.CharField(max_length=50, default=None, null=True)
    address_line_2 = models.CharField(max_length=50, default=None, null=True)
    city = models.CharField(max_length=50, default=None, null=True)
    state = models.CharField(max_length=50, default=None, null=True)
    zip_code = models.IntegerField(default=1, null=True)

    # address

    def __str__(self):
        return self.user.email

    def get_account_type(self):
        return self.account_type

    def get_address_line_1(self):
        return self.address_line_1

    def get_address_line_2(self):
        return self.address_line_2

    def get_city(self):
        return self.city

    def get_state(self):
        return self.state

    def get_zip_code(self):
        return self.zip_code


class Product_Request(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    request = models.CharField(max_length=500, default=None)
    product_request_time = models.DateTimeField()

    def __str__(self):
        return self.user.email


class Received_Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    total_amount = models.FloatField()
    items = models.TextField(default=None)
    address = models.TextField(default=None)
    receiving_time = models.DateTimeField(default=None)
    delivered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email
