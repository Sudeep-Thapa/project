from django.shortcuts import render,redirect
from .models import *
from home.views import *
from django.core.mail import EmailMessage
def add_to_cart(request,slug):
    username = request.user.username
    price = Item.objects.get(slug=slug).price
    discounted_price=Item.objects.get(slug=slug).price
    if discounted_price > 0:
        original_price=discounted_price
    else:
        original_price=price
    if Cart.objects.filter(username=username,slug=slug,checkout=False).exists():
        quantity=Cart.objects.get(username=username,slug=slug,checkout=False).quantity
        quantity=quantity+1
        total=original_price*quantity
        Cart.objects.filter(username=username, slug=slug, checkout=False).update(quantity=quantity,total=total)
        return redirect('cart:my_cart')

    else:
        quantity=1
    total=original_price*quantity
    data=Cart.objects.create(
        username=username,
        items=Item.objects.filter(slug=slug)[0],
        slug=slug,
        quantity=quantity,
        total=total
    )
    data.save()
    return redirect('cart:my_cart')

class CartView(BaseView):
    def get(self,request):
        username=request.user.username
        self.views['my_cart']=Cart.objects.filter(username=username,checkout=False)
        return render(request,'cart.html',self.views)
class WishlistView(BaseView):
    def get(self,request):
        username=request.user.username
        self.views['my_wishlist']=WishList.objects.filter(username=username,add_to_cart=False)
        return render(request,'wishlist.html',self.views)
def add_wish_list(request,slug):
    username = request.user.username
    price = Item.objects.get(slug=slug).price
    discounted_price = Item.objects.get(slug=slug).discounted_price
    if WishList.objects.filter(username=username, slug=slug, add_to_cart=False).exists():
        quantity = WishList.objects.get(username=username, slug=slug, add_to_cart=False).quantity
        quantity = quantity + 1
        WishList.objects.filter(username=username, slug=slug, add_to_cart=False).update(quantity=quantity)
        return redirect('cart:my_cart')

    else:
        quantity = 1
    data = WishList.objects.create(
        username=username,
        items=Item.objects.filter(slug=slug)[0],
        slug=slug,
        quantity=quantity,
    )
    data.save()
    return redirect('cart:my_wishlist')
def add_wish(request,slug):
    username = request.user.username
    price = Item.objects.get(slug=slug).price
    discounted_price = Item.objects.get(slug=slug).price
    if WishList.objects.filter(username=username, slug=slug, add_to_cart=False).exists():
        quantity = WishList.objects.get(username=username, slug=slug,add_to_cart=False).quantity
        quantity = quantity + 1
        WishList.objects.filter(username=username, slug=slug, add_to_cart=False).update(quantity=quantity)
        return redirect('cart:my_wishlist')
def subtract_wish(request,slug):
    username = request.user.username
    price = Item.objects.get(slug=slug).price
    discounted_price = Item.objects.get(slug=slug).price
    if WishList.objects.filter(username=username, slug=slug, add_to_cart=False).exists():
        quantity = WishList.objects.get(username=username, slug=slug, add_to_cart=False).quantity
        if quantity >0 :
         quantity = quantity - 1
         WishList.objects.filter(username=username, slug=slug, add_to_cart=False).update(quantity=quantity)
         return redirect('cart:my_wishlist')
        else:
         return redirect('cart:my_wishlist')



def delete_wishlist(request,slug):
    username=request.user.username
    WishList.objects.filter(username=username,add_to_cart=False,slug=slug).delete()
    return redirect('cart:my_wishlist')

def delete_cart(request,slug):
    username=request.user.username
    Cart.objects.filter(username=username,checkout=False,slug=slug).delete()
    return redirect('cart:my_cart')
def add(request,slug):
    username = request.user.username
    price = Item.objects.get(slug=slug).price
    discounted_price = Item.objects.get(slug=slug).price
    if discounted_price > 0:
        original_price = discounted_price
    else:
        original_price = price
    if Cart.objects.filter(username=username, slug=slug, checkout=False).exists():
        quantity = Cart.objects.get(username=username, slug=slug, checkout=False).quantity
        quantity = quantity + 1
        total = original_price * quantity
        Cart.objects.filter(username=username, slug=slug, checkout=False).update(quantity=quantity, total=total)
        return redirect('cart:my_cart')


def subtract(request,slug):
    username = request.user.username
    price = Item.objects.get(slug=slug).price
    discounted_price = Item.objects.get(slug=slug).price
    if discounted_price > 0:
        original_price = discounted_price
    else:
        original_price = price
    if Cart.objects.filter(username=username, slug=slug, checkout=False).exists():
        quantity = Cart.objects.get(username=username, slug=slug, checkout=False).quantity
        if quantity >0 :
         quantity = quantity - 1
         total = original_price * quantity
         Cart.objects.filter(username=username, slug=slug, checkout=False).update(quantity=quantity, total=total)
         return redirect('cart:my_cart')
        else:
         return redirect('cart:my_cart')