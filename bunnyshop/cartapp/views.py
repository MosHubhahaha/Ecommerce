from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from products.models import Product
from cartapp.models import Cart,Cartitem

def create_cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart
# Create your views here.
@login_required(login_url="/login")

def removecart(request,product_id):
    cart=Cart.objects.get(cart_id=create_cart_id(request),customer=request.user)
    product=Product.objects.get(pk=product_id)
    cartitem=Cartitem.objects.get(product=product,cart=cart)
    cartitem.delete()
    return redirect("/cart")

@login_required(login_url="/login")
def cart(request):
    counter=0
    total=0
    try:
        #ดีงตะกร้าสินค้า
        cart=Cart.objects.get(cart_id=create_cart_id(request),customer=request.user)
        #ดึงข้อมูลสินค้าในตะกร้า
        cartItem=Cartitem.objects.filter(cart=cart)
        for item in cartItem:
            counter+=item.quantity
            total+=(item.product.price * item.quantity)

    except (Cart.DoesNotExist,Cartitem.DoesNotExist):
        cart=None
        cartItem=None
    return render(request,"cart.html",{"cartitem":cartItem,"total":total,"counter":counter})


@login_required(login_url="/login")
def add_product_to_cart(request,product_id):
    add_product = Product.objects.get(pk=product_id)
    try:
        #มีตะกร้าสินค้า
        cart=Cart.objects.get(cart_id=create_cart_id(request))
    except Cart.DoesNotExist:
        #ไม่มีตะกร้าสินค้า
        cart=Cart.objects.create(
            cart_id=create_cart_id(request),
            customer=request.user
        )

        cart.save()
    
    #บันทึกรายการสินค้าในตะกร้า
    try:
        #ซื้อสินค้าตัวเดิม
        cartitem=Cartitem.objects.get(product=add_product,cart=cart)
        if cartitem.quantity<cartitem.product.stock:
            cartitem.quantity+=1
            cartitem.save()
    except Cartitem.DoesNotExist:
        #ซื้อสินค้า
        cartitem=Cartitem.objects.create(
            product=add_product,
            cart=cart,
            quantity=1
        )

        cartitem.save()
    print(cartitem)

    return redirect("/cart")

