from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="Login"),
    path('registration/', views.registration, name="Registration"),
    path("home/", views.home, name="Home"),
    path("home/search", views.search, name="Search"),
    path("track-order/", views.track_order, name="TrackingStatus"),
    path("cart/", views.cart, name="Cart"),
    path("product/<slug>/", views.product, name="Product"),
    path("add-to-cart/<slug>/", views.add_to_cart, name="addToCart"),
    path("remove-from-cart/<slug>/", views.remove_from_cart, name="removeFromCart"),
    path("remove-item-from-cart/<slug>/",
         views.remove_single_item_from_cart, name="removeItemFromCart"),
    path("cart/add/<slug>/",
         views.add_single_item_from_cart, name="addItemToCart"),
    path("all-products/<category>/", views.product_list, name="ProductList"),
    path("about-us/", views.about, name="AboutUs"),
    path("checkout/", views.checkout, name="Checkout"),
    path("request/", views.request_product, name="RequestProduct"),
    path("address/", views.address, name="Address"),
    path('logout/', views.logout, name="Logout"),
]
