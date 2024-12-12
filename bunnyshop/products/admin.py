from django.contrib import admin
from products.models import Product

class ManageProduct(admin.ModelAdmin):
    list_display=["name","price","stock","isTrending","image"]
    list_editable=["price","stock","isTrending"]
    list_per_page=5
    search_fields=["name"]


# Register your models here.
admin.site.register(Product,ManageProduct)