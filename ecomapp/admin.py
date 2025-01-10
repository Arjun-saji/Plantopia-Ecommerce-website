from django.contrib import admin
from .models import *
from django.contrib.auth.admin import *

admin.site.register(Category),
#admin.site.register(Product),
admin.site.register(Productimage),
admin.site.register(Cart),
admin.site.register(Cartitem),
admin.site.register(Payment),
# admin.site.register(Order),
admin.site.register(Blogs),
admin.site.unregister(Group)
admin.site.register(Whishlist)
admin.site.register(Coupon)
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
	list_display =['name','price','in_stock']


@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
	list_display=['user',"total_amount","is_paid"]