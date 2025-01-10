from django.urls import path
from . import views
from django.contrib.auth.admin import *


urlpatterns=[path("",views.index,name="index"),
path("contact/",views.contact,name="contact"),
path("faq/",views.faq,name="faq"),
path("about/",views.about,name="about"),
path("product/<int:object_id>/",views.singleproduct,name="product"),
path("shop/",views.shop,name="shop"),
path("indoor/",views.indoorplant,name="indoor"),
path("outdoor/",views.outdoorplant,name="outdoor"),
path("succi/",views.succiplant,name="succi"),

path("signup/",views.register,name="signup"),
path("login/",views.login,name="login"),
path("logout/",views.logout,name="logout"),
path("cartdetails/",views.cartdetail,name="cartdetails"),
path("addcart/<int:object_id>/",views.addtocart,name="addcart"),
path("cartupdate/",views.cartupdate,name="cartupdate"),
path('update_quantity/<int:item_id>/', views.update_quantity, name='update_quantity'),
path("checkout/",views.checkout,name="checkout"),
path("placeorder/",views.placeorder,name="placeorder"),
path("success_order/",views.order_success,name="order_success"),
path("order_failed/",views.order_failed,name="order_failed"),
path("blogs/",views.blogs,name="blogs"),
path("blogdetails/<int:object_id>/",views.blogdetails,name="blogdetails"),
path("search/",views.product_search,name="search"),
path("addwishlist/<int:product_id>/",views.add_wishlist,name="addwishlist"),
path("viewwishlist/",views.view_wishlist,name="viewwishlist"),
path("removewishlist/<int:product_id>/",views.remove_wishlist,name="removewishlist"),
path("applycoupon/",views.applycoupon,name="applycoupon"),






]


admin.site.site_header="Plantopia Admin Panel"
admin.site.site_title ="Plantopia"
admin.site.site_index_title="Plantopia index"