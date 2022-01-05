from django.contrib import admin
from .models import Product, Category, SubCategory, Review, Order, Coupon, UserDetails, FeaturedProduct, FeaturedCategory, OTP

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    class Media(admin.ModelAdmin):
        js = ('tiny.js',)

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(Coupon)
admin.site.register(UserDetails)
admin.site.register(FeaturedProduct)
admin.site.register(FeaturedCategory)
admin.site.register(OTP)