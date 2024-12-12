from django.db import models
from django.contrib.auth.models import User
from products.models import Product

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=255,blank=True)
    customer = models.ForeignKey(User,on_delete=models.CASCADE,default=None)

class Cartitem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.product.name + " : " + str(self.quantity)