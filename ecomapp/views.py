from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import *
from django.contrib.auth import authenticate, login as auth_login,logout as auth_logout
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
import razorpay
from django.contrib import messages
from razorpay import Client
from django.contrib.auth.decorators import login_required
from .forms import * 


def index(request):

	categories=Category.objects.all()
	productimages=Productimage.objects.all()
	indoor_plants=Product.objects.filter(category=1)
	outdoor_plants=Product.objects.filter(category=2)
	blogs=Blogs.objects.all()
	recent=Blogs.objects.latest('created_date')

	recent_blogs = Blogs.objects.exclude(pk=recent.pk).order_by('created_date')[:3]

	context={"categories":categories,
	"productimages":productimages,
	"indoor_plants":indoor_plants,
	"outdoor_plants":outdoor_plants,
	"blogs":blogs,"recent_blogs":recent_blogs
	}

	return render(request,"index.html",context)


def singleproduct(request,object_id):

	single=Product.objects.get(pk=object_id)
	related=Product.objects.exclude(pk=object_id)
	images = Productimage.objects.filter(product=single)
	context={"single":single,"images":images,"related":related}

	return render(request,"product.html",context)


def shop(request):

	products = Product.objects.all()
	productimages = Productimage.objects.all()
	min_price = request.GET.get("min_price", 0)
	max_price = request.GET.get("max_price", 10000)

	try:
		min_price = float(min_price)
		max_price = float(max_price)

	except ValueError:
		min_price = 0
		max_price = 10000
		print("Invalid input; using default min_price and max_price.")

	new_product = Product.objects.filter(price__gte=min_price, price__lte=max_price)

	context = {
		"products": products,
		"productimages": productimages,
		"new_product": new_product,
		"min_price": min_price,
		"max_price": max_price
	}

	return render(request, "shop.html", context)





def indoorplant(request,):

	indoor_plants=Product.objects.filter(category=1)
	productimages=Productimage.objects.all()

	context={"indoor_plants":indoor_plants,
	"productimages":productimages
	}

	return render(request,"indoor.html",context)


def outdoorplant(request):

	outdoor_plants=Product.objects.filter(category=2)
	productimages=Productimage.objects.all()

	context={"outdoor_plants":outdoor_plants,"productimages":productimages
	}

	return render(request,"outdoor.html",context)


def succiplant(request,):

	succicacti_plants=Product.objects.filter(category=3)
	productimages=Productimage.objects.all()

	context={"succicacti_plants":succicacti_plants,
	"productimages":productimages}

	return render(request,"succi.html",context)

def register(request):

	if request.method=="POST":
		username=request.POST.get("username")
		password=request.POST.get("password")
		User.objects.create_user(username=username,password=password)
		
		return redirect("index")
	return render(request,"auth/signup.html")


def login(request):

	if request.method == "POST":
		username=request.POST.get("username")
		password=request.POST.get("password")
		
		user=authenticate(request,username=username,password=password)
		
		if user is not None:
			print("none")
			auth_login(request,user)
			return redirect("index")

	return render(request,"auth/login.html")


def logout(request):

	auth_logout(request)

	return redirect("index")
	



def getcart(request):

	# Ensure a session key is created if not authenticated
	if not request.session.session_key:
		request.session.create()  # Create a new session if it doesn't exist
	
	# Try to get the cart associated with the user, if authenticated
	if request.user.is_authenticated:

		cart, created = Cart.objects.get_or_create(user=request.user)
	else:

		# Use the session_id for unauthenticated users
		session_id = request.session.session_key
		cart, created = Cart.objects.get_or_create(session_id=session_id)
	
	return cart

def addtocart(request,object_id):

	product=get_object_or_404(Product,id=object_id)
	cart=getcart(request)
	cart_item,created=Cartitem.objects.get_or_create(cart=cart,product=product)

	if created:
		cart_item.quantity +=1
	cart_item.save()
	return redirect('index')




def cartdetail(request):

	cart=getcart(request)
	cart_items=cart.items.all()
	total_amount=sum(item.product.price * item.quantity for item in cart_items)
	coupon_id=request.session.get("coupon_id")
	discount=0
	if coupon_id:
		coupon=get_object_or_404(Coupon,id=coupon_id)
		discount=(coupon.discount)
		total_amount-=discount
	else:
		total_amount=sum(item.product.price * item.quantity for item in cart_items)
		
	context={"cart":cart,"cart_items":cart_items,"total_amount":total_amount,"discount":discount}

	return render(request,"cartdetails.html",context)



def cartupdate(request):

	cart = getcart(request)  # Assuming you have a function to get the current cart
	
	if request.method == "POST":
		# Check if the "remove" button was clicked

		if 'remove' in request.POST:
			item_id = request.POST.get('remove')
			cart_item = Cartitem.objects.filter(id=item_id, cart=cart).first()
			if cart_item:
				cart_item.delete()

	return redirect('cartdetails')  # Redirect to the cart details page after update



def update_quantity(request, item_id):


	cart = Cart.objects.get(user=request.user)  # Assuming cart is user-specific
	cart_item = get_object_or_404(Cartitem, id=item_id, cart=cart)


	# Check what action was sent
	if request.method == 'POST':
		action = request.POST.get('action')

		if action == 'increment':
			cart_item.quantity += 1
		elif action == 'decrement' and cart_item.quantity > 1:
			cart_item.quantity -= 1
		elif action == 'decrement' and cart_item.quantity == 1:
			# Optionally, if the quantity reaches 0, you may delete the item
			cart_item.delete()
			return redirect('cartdetails')

		cart_item.save()

	return redirect('cartdetails')


# Razorpay client initialization
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


def checkout(request):

	cart=Cart.objects.get(user=request.user)
	cart_item=cart.items.all()
	total_amount=sum(item.product.price * item.quantity for item in cart_item)

	if request.method=="POST":


		order = Order.objects.create(
			user=request.user,
			first_name=request.POST["first_name"],
			last_name=request.POST["last_name"],
			email=request.POST["email"],
			phone=request.POST["phone"],
			address=request.POST["address"],
			city=request.POST["city"],
			state=request.POST["state"],
			zip_code=request.POST["zip_code"],
			total_amount=total_amount,
			# total_amount=request.POST["total_amount"],
			)

		razorpay_order = razorpay_client.order.create({
			"amount": int(total_amount * 100),  # amount in paise
			"currency": "INR",
			"payment_capture": "1"
		})


		razorpay_order_id = razorpay_order["id"]

		payment=Payment.objects.create(
			order=order,
			razorpay_order_id=razorpay_order_id

		)

		context={
		 "cart_item":cart_item,
		 "total_amount":total_amount,
		 "razorpay_order_id":razorpay_order_id,
		 "razorpay_key":settings.RAZORPAY_KEY_ID,
		 "order":order
		}


		return render(request,"checkout.html",context)


	return render(request,"checkout.html", {
		'cart_items': cart_item,
		'total_amount': total_amount
	})


def placeorder(request):
	if request.method=="POST":
		razorpay_order_id=request.POST.get("razorpay_order_id")
		razorpay_payment_id=request.POST.get("razorpay_payment_id")
		razorpay_signature=request.POST.get("razorpay_signature")

	payment=get_object_or_404(Payment,razorpay_order_id=razorpay_order_id)

	params={
	"razorpay_order_id":razorpay_order_id,
	"razorpay_payment_id":razorpay_payment_id,
	"razorpay_signature":razorpay_signature
	}

	try:
		
		razorpay_client.utility.verify_payment_signature(params)
		payment.is_successful=True
		payment.razorpay_payment_id=razorpay_payment_id
		payment.razorpay_signature=razorpay_signature
		payment.save()

		order=payment.order
		order.is_paid=True
		order.save()

		#---To clear the cart after successful payment---

		cart=getcart(request)
		cart.items.all().delete()
		cart.save()

		return redirect(reverse("order_success"))

	except razorpay.errors.SignatureVerificationError:

		payment.is_successful=False
		payment.save()

		return redirect(reverse("order_failed"))


def blogs(request):

	blogs=Blogs.objects.all()
	recent=Blogs.objects.latest('created_date')
	recent_blogs = Blogs.objects.exclude(pk=recent.pk).order_by('created_date')[:2]

	context={"blogs":blogs,"recent_blogs":recent_blogs}

	return render(request,"blogs.html",context)


def blogdetails(request,object_id):

	blogs=get_object_or_404(Blogs,pk=object_id)
	prev= get_object_or_404(Blogs,pk=object_id-1)
	ne_xt = get_object_or_404(Blogs,pk=object_id+1)

	context={"blogs":blogs,"prev":prev,"ne_xt":ne_xt}

	return render(request,"blogdetails.html",context)

def product_search(request):

	query=request.GET.get("query",'')
	search_result=[]
	if query:
		search_result=Product.objects.filter(name__icontains=query)
	
	context={"query":query,"search_result":search_result}

	return render(request,"search_result.html",context)

@login_required
def add_wishlist(request,product_id):

	if not request.session.session_key:
		request.session.create() 
		
	if request.user.is_authenticated:
		product=get_object_or_404(Product,id=product_id)
		wishlist,created=Whishlist.objects.get_or_create(user=request.user,product=product)
	else:
		session_id = request.session.session_key
		wishlist,created=Whishlist.objects.get_or_create(session_id=session_id)

	return redirect("index")

@login_required
def view_wishlist(request):

	wishlist_items=Whishlist.objects.filter(user=request.user).select_related("product")
	context={"wishlist_items":wishlist_items}
	return render(request,"wishlist.html",context)
	
@login_required
def remove_wishlist(request,product_id):

	product=get_object_or_404(Product,id=product_id)
	Whishlist.objects.filter(user=request.user,product=product).delete()
	messages.success(request,"This product is removed from your wishlist")

	return redirect('viewwishlist')


def applycoupon(request):

	form=Applycouponform(request.POST or None)

	if request.method=="POST" and form.is_valid():
		code = form.cleaned_data['code']
		print("coupon--",code)
		now =timezone.now()

		try:
			coupon=Coupon.objects.get(code=code,valid_from__lte=now,valid_to__gte=now,active=True)
			request.session['coupon_id']=coupon.id
			print("coupon-id",coupon.id)
			messages.success(request,f"coupon '{code}' successfully appiled..! You get {coupon.discount}")

		except Coupon.DoesNotExist:
			messages.errors(request,"The coupon is invalid..")

		return redirect("cartdetails")

	return render(request,"cartdetails.html",{"form":form})
































def order_success(request):
	return render(request,"order_success.html")

def order_failed(request):
	return render(request,"order_failed.html")

def contact(request):
	return render(request,"contact.html")

def faq(request):
	return render(request,"faq.html")

def about(request):
	return render(request,"about.html")

