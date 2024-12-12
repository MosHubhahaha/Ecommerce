from django.urls import path
from cartapp import views

urlpatterns = [
    path("cart",views.cart),
    path("cart/add/<int:product_id>",views.add_product_to_cart,name="addcart"),
    path("cart/remove/<int:product_id>",views.removecart,name="removeCart")
]
