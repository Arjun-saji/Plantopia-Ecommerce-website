from .models import *
from .views import *


def cart_items(request):
	cart=getcart(request)
	cart_items=cart.items.all()
	total_amount=sum(items.product.price*items.quantity for items in cart_items)

	coupon_id=request.session.get("coupon_id")
	discount=0

	if coupon_id:
		coupon=get_object_or_404(Coupon,id=coupon_id)
		discount=(coupon.discount)
		total_amount-=discount
		
	else:
		total_amount=sum(item.product.price * item.quantity for item in cart_items)
		

	context={"cart":cart,"cart_items":cart_items,"total_amount":total_amount,"discount":discount}


	return {"cart_items":cart_items,"total_amount":total_amount,"discount":discount}






# cart/context_processors.py


def cart_length(request):
	# Ensure that the user is authenticated before attempting to get their cart
	if request.user.is_authenticated:
		try:
			cart = Cart.objects.get(user=request.user)
			cart_length = cart.items.count()  # Count the number of items in the cart
		except Cart.DoesNotExist:
			cart_length = 0
	else:
		cart_length = 0

	return {'cart_length': cart_length}




def wishlist_length(request):

	if request.user.is_authenticated:

		wishlist_items=Whishlist.objects.filter(user=request.user).select_related("product")
		wishlist_length = wishlist_items.count()  # Count the number of items in the cart
	else:

		wishlist_items=[]
		wishlist_length = 0 # Count the number of items in the cart


	return {'wishlist_length':wishlist_length,"wishlist_items":wishlist_items}








	 