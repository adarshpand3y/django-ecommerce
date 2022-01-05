from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('product/<slug:slug>', views.product, name="product"),
    path('category', views.category, name="category"),
    path('subcategory', views.subcategory, name="subcategory"),
    path('search', views.search, name="search"),
    path('checkCoupon', views.isValid, name="check"),
    path('about', views.about, name="about"),
    path('contact', views.contact, name="contact"),
    path('postReview', views.postReview, name="postReview"),
    path('checkout', views.checkout, name="checkout"),
    path('handleRegister', views.handleRegister),
    path('handleLogin', views.handleLogin),
    path('handleLogout', views.handleLogout),
    path('account', views.accountSettings),
    path('updateProfile', views.updateProfile),
    path('updateAddress', views.updateAddress),
    path('updatePassword', views.updatePassword),
    path('sendOTP', views.sendOTP),
    path('forgotpassword', views.forgotpassword),
    path('orders', views.orders),
]