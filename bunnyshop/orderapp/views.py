from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from cartapp.models import Cart,Cartitem
from orderapp.models import Order,OrderDetail
from products.models import Product
from cartapp.views import create_cart_id
# Create your views here.

@login_required(login_url='/login')
def orderHistory(request):
    orders=Order.objects.filter(customer=request.user)
    return render(request,"orderhistory.html",{"order":orders})

@login_required(login_url='/login')
def OrderDetails(request,order_id):
    orders=Order.objects.get(pk=order_id)
    if orders.customer==request.user:
        order_item=OrderDetail.objects.filter(order=orders)
        return render(request,"orderdetails.html",{"order":orders,"order_items":order_item})
    else:
        return redirect("/orderHistory")

@login_required(login_url="/login")
def order(request):
    if request.method=="POST":
        fullname=request.POST["fullname"]
        phone=request.POST["phone"]
        address=request.POST["address"]
        cart=Cart.objects.get(cart_id=create_cart_id(request),customer=request.user)
        cartItem=Cartitem.objects.filter(cart=cart)
        total=0
        for item in cartItem:
            total+=(item.product.price * item.quantity)

        order=Order.objects.create(
            fillname=fullname,
            phone=phone,
            address=address,
            total=total,
            customer=request.user
        )
        order.save()
        #บันทึกรายการสั่งซื้อและตัด Stock
        for item in cartItem:
            order_detail=OrderDetail.objects.create(
                product=item.product.name,
                quantity=item.quantity,
                price=item.product.price,
                order=order
            )
            order_detail.save()
            #ตัดStock
            product=Product.objects.get(pk=item.product.id)
            product.stock = int(item.product.stock - order_detail.quantity)
            product.save()
            item.delete()
        cart.delete()
        return render(request,"ordercomplete.html")
    else:
        return render(request,"order.html")