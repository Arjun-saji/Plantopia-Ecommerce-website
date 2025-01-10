from django.db import models
from django.contrib.auth.models import User
from ecomapp.models import *
from django.utils import timezone


class Category(models.Model):
	name=models.CharField(max_length=20)

	class Meta:
		verbose_name = 'Category'
		verbose_name_plural = 'Categories'

	def __str__(self):
		return self.name

class Product(models.Model):
	category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="products")
	name=models.CharField(max_length=100)
	scientific_name=models.CharField(max_length=50)
	soil=models.CharField(max_length=100)
	height=models.DecimalField(max_digits=5,decimal_places=2)
	weight=models.DecimalField(max_digits=5,decimal_places=2)
	about_plant=models.CharField(max_length=100)
	description=models.TextField(blank=True)
	price=models.DecimalField(max_digits=10,decimal_places=2)
	created_date=models.DateTimeField(auto_now_add=True)
	in_stock=models.BooleanField(default=True)



	def __str__(self):
		return self.name


class Productimage(models.Model):
	product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="images")
	image=models.ImageField(upload_to="Product_img/",blank=True)

	class Meta:
		verbose_name_plural = 'Product Images'

	def __str__(self):
		return f"image for {self.product.name}"

class Cart(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
	session_id=models.CharField(max_length=250,null=False)
	created_date=models.DateTimeField(auto_now_add=True)
	updated_time=models.DateTimeField(auto_now=True)


	def __str__(self):
		return f"cart- {self.id} for session ID {self.session_id}"



class Cartitem(models.Model):
	cart=models.ForeignKey(Cart,related_name="items",on_delete=models.CASCADE)
	product=models.ForeignKey(Product,on_delete=models.CASCADE)
	quantity=models.PositiveIntegerField(default=0)

	def __str__(self):
		return f"{self.product.name}-{self.quantity}"

	def get_price(self):
		return self.product.price * slef.quantity


class Order(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	first_name = models.CharField(max_length=100,null=True)
	last_name = models.CharField(max_length=100,null=True)
	email = models.EmailField(null=True)
	phone = models.CharField(max_length=15,null=True)
	address = models.CharField(max_length=255,null=True)
	city = models.CharField(max_length=100,null=True)
	state = models.CharField(max_length=100,null=True)
	zip_code = models.CharField(max_length=10, blank=True,null=True)
	total_amount = models.DecimalField(max_digits=10, decimal_places=2)
	order_date = models.DateTimeField(default=timezone.now)
	is_paid = models.BooleanField(default=False)


	def __str__(self):
		return f"Order {self.id} - {self.user.username if self.user else 'Anonymous'}"


class Payment(models.Model):
	order = models.OneToOneField(Order, on_delete=models.CASCADE)
	razorpay_order_id = models.CharField(max_length=100,null=True)
	razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
	razorpay_signature = models.CharField(max_length=100, blank=True, null=True)
	is_successful = models.BooleanField(default=False)
	payment_date = models.DateTimeField(default=timezone.now)


	def __str__(self):
		return f"Payment for order {self.order.id}"

class Blogs(models.Model):
	title=models.CharField(max_length=250)
	description=models.TextField()
	created_date=models.DateTimeField(default=timezone.now)
	image=models.ImageField()

	class Meta:
		verbose_name_plural = 'Blogs'

class Whishlist(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
	product=models.ForeignKey(Product,on_delete=models.CASCADE)
	date_on=models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together=('user','product')
		# Prevent duplicate entries for the same user/product

	def __str__(self):
		return f"whishlist- {self.user.username}'s wishlist: {self.product.name}"


class Coupon(models.Model):

	code =models.CharField(max_length=20,unique=True)
	discount=models.DecimalField(max_digits=5,decimal_places=2)
	valid_from=models.DateTimeField()
	valid_to=models.DateTimeField()
	active=models.BooleanField(default=True)


	def is_vaild(self):
		now=timezone.now()
		return self.active and self.valid_from <= now <= self.valid_to

	def __str__(self):
		return self.code





















