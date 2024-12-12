from django.urls import path
from products import views

urlpatterns = [
     path("",views.index),
     path("detail/<int:id>",views.productDetail,name="productDetail"),
     path("products",views.products)
]
