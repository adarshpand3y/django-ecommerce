from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils.timezone import now

# states = [
#     ("AP", "Andhra Pradesh"),
#     ("", "Arunachal Pradesh"),
#     ("", "Assam"),
#     ("", "Bihar"),
#     ("", "Chhattisgarh"),
#     ("", "Goa"),
#     ("", "Gujarat"),
#     ("", "Haryana"),
#     ("", "Himachal Pradesh"),
#     ("", "Jharkhand"),
#     ("", "Karnataka"),
#     ("", "Kerala"),
#     ("", "Madhya Pradesh"),
#     ("", "Maharashtra"),
#     ("", "Manipur"),
#     ("", "Meghalaya"),
#     ("", "Mizoram"),
#     ("", "Nagaland"),
#     ("", "Odisha"),
#     ("", "Punjab"),
#     ("", "Rajasthan"),
#     ("", "Sikkim"),
#     ("", "Tamil Nadu"),
#     ("", "Telangana"),
#     ("", "Tripura"),
#     ("", "Uttar Pradesh"),
#     ("", "Uttarakhand"),
#     ("", "West Bengal)"
# ]

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class SubCategory(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Subcategories"

class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default='1')
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_DEFAULT, default='2')
    price = models.IntegerField(default=0)
    stock = models.IntegerField(default=0)
    desc = models.TextField()
    pub_date = models.DateField()
    avg_rating = models.IntegerField(default=0)
    avg_rating_float = models.FloatField(default=0.0)
    number_of_ratings = models.IntegerField(default=0)
    image1 = models.ImageField(upload_to="images", default="")
    image2 = models.ImageField(upload_to="images", default="")
    image3 = models.ImageField(upload_to="images", default="")
    slug = models.SlugField(blank=True, help_text=('Leave this parameter empty, it will get generated automatically.'))

    def save(self, *args, **kwargs):
        self.slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_name

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.TextField()
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.review)[0:15]

class Order(models.Model):
    order_choices = [
        ("OPS", 'Order Placed Successfully'),
        ("S", 'Shipped'),
        ("OFD", 'Out For Delivery'),
        ("D", 'Delivered'),
        ]
    items = models.TextField(help_text=(f"Customer's Orders"))
    total_cost = models.IntegerField(default=0)
    code_applied = models.CharField(default="", max_length=20)
    discounted_cost = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text=(f"User who placed this order."))
    first_name = models.CharField(max_length=50, default="")
    last_name = models.CharField(max_length=50, default="")
    address1 = models.CharField(max_length=100, default="")
    address2 = models.CharField(max_length=100, default="")
    email = models.CharField(max_length=50, default="")
    phone = models.CharField(max_length=50, default="")
    city = models.CharField(max_length=50, default="")
    state = models.CharField(max_length=50, default="")
    pincode = models.CharField(max_length=50, default="")
    landmark = models.CharField(max_length=50, default="")
    ordered_at = models.DateTimeField(auto_now_add=True, help_text=(f"Do NOT change this date and time field."))
    last_changed_at = models.DateTimeField(auto_now=True, help_text=(f"Do NOT change this date and time field."))
    status = models.CharField(max_length=5, choices=order_choices, default="Order Placed Successfully", help_text=(f"Change this only when you are sure. This sends an email to the user regarding the update."))

    def __str__(self):
        return f"Order Id: {self.id}"

class Coupon(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=20)
    discount_percentage = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    description = models.CharField(max_length=100)
    val = models.FloatField(blank=True, help_text="Do NOT change this field. It gets updated automatically.")

    def save(self, *args, **kwargs):
        self.val = self.discount_percentage/100
        super(Coupon, self).save(*args, **kwargs)

    def __str__(self):
        return f"Coupon: {self.name}"

class UserDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=50)
    pincode = models.IntegerField()
    landmark = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = "User Details"

class FeaturedCategory(models.Model):
    category = models.CharField(max_length=100)
    help_text_to_display = models.CharField(max_length=200, default="")

    def __str__(self):
        return self.category
    
    class Meta:
        verbose_name_plural = "Featured Categories"

class FeaturedProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    featured_category = models.ForeignKey(FeaturedCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.product_name
    
    class Meta:
        verbose_name_plural = "Featured Products"

class OTP(models.Model):
    value = models.CharField(max_length=10)

    def __str__(self):
        return self.value
    
    class Meta:
        verbose_name_plural = "OTPs"