from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Product, Review, Order, Coupon, UserDetails, FeaturedProduct, FeaturedCategory, OTP
from django.core.paginator import Paginator, EmptyPage
import json
import random
import string



# Set PRODUCTS_PER_PAGE = 1 only for testing pagination.
# Set it to some reasonable value in production.
PRODUCTS_PER_PAGE = 1

# Create your views here.
def index(request):
    allProds = []
    cats = FeaturedCategory.objects.all()
    for cat in cats:
        ob = FeaturedProduct.objects.filter(featured_category=cat)
        allProds.append([ob[0].featured_category.category, ob[0].featured_category.help_text_to_display, ob])
    context = {'categories': allProds}
    return render(request, 'index.html', context)

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def product(request, slug):
    product = Product.objects.get(slug=slug)
    reviews = Review.objects.filter(product=product)
    context = {
        'product': product,
        'reviews': reviews
        }
    return render(request, 'product.html', context)

def category(request):
    cat = request.GET.get('category', "")
    page_num = request.GET.get('page', 1)
    # if cat == "":
    #     print("No category query found")
    #     messages.error(request, "No such category found.")
    #     return redirect("/")
    products = Product.objects.filter(category__name__contains=cat).order_by('pub_date')
    p = Paginator(products, PRODUCTS_PER_PAGE)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
    context = {"products": page, "this_page_num": page_num, "num_of_pages": p.num_pages, "category": cat}
    return render(request, 'category.html', context)

def subcategory(request):
    sub = request.GET.get('subcategory', "")
    page_num = request.GET.get('page', 1)
    # if sub == "":
    #     print("No subcategory query found")
    #     messages.error(request, "No such subcategory found.")
    #     return redirect("/")
    products = Product.objects.filter(sub_category__name__contains=sub).order_by('pub_date')
    p = Paginator(products, PRODUCTS_PER_PAGE)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
    context = {"products": page, "this_page_num": page_num, "num_of_pages": p.num_pages, "subcategory": sub}
    return render(request, 'subcategory.html', context)

def search(request):
    query = request.GET.get('query', "")
    page_num = request.GET.get('page', 1)
    if query == "":
        print("No search query found")
        messages.error(request, "No items match your search. Please refine your search.")
        return redirect("/")
    products = Product.objects.filter(product_name__icontains=query).order_by('pub_date')
    p = Paginator(products, PRODUCTS_PER_PAGE)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
    context = {"products": page, "this_page_num": page_num, "num_of_pages": p.num_pages, "query": query}
    return render(request, 'search.html', context)

def postReview(request):
    if request.method == "POST":
        # Getting the post parameters
        productSlug = request.POST.get("productSlug")
        rating = int(request.POST.get("rating"))
        review = request.POST.get("review")
        # Getting Product and updating its rating
        product = Product.objects.get(slug=productSlug)
        old_avg_rating = product.avg_rating_float
        prev_no_of_ratings = product.number_of_ratings
        old_full_rating = old_avg_rating * prev_no_of_ratings
        new_full_rating = old_full_rating + rating
        new_number_of_ratings = prev_no_of_ratings + 1
        new_avg_rating = new_full_rating / new_number_of_ratings
        product.avg_rating = new_avg_rating
        product.avg_rating_float = float(new_avg_rating)
        product.number_of_ratings = int(new_number_of_ratings)
        product.save()
        # Creating new Review object
        review = Review(
            user = request.user,
            product = product,
            rating = rating,
            review = review
            )
        review.save()
        return redirect(f"/product/{productSlug}")
    
    return redirect(f"/")

def isValid(request):
    if request.method == "POST":
        couponcode = request.POST.get('couponcode')
        try:
            coupon = Coupon.objects.filter(code=couponcode)
            if len(coupon) > 0 and coupon[0].quantity > 0:
                return JsonResponse({'val': 1})
            else:
                return JsonResponse({'val': 0})
        except Exception as e:
            print("\n\nEXCEPTION\n\n")
            print(e)
    return redirect("/")

def checkout(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            items = json.loads(request.POST.get('items'))
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            address1 = request.POST.get('address1')
            address2 = request.POST.get('address2')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            coupon = request.POST.get('coupon')
            city = request.POST.get('city')
            state = request.POST.get('state')
            pincode = request.POST.get('pincode')
            landmark = request.POST.get('landmark')
            final_order = ""
            total_price = 0
            # discounted_price = 0
            for item in items:
                qty = int(items[item][2])
                name = items[item][0]
                item_obj = Product.objects.get(product_name=name)
                price = item_obj.price
                total_price = total_price + (price*qty)
                final_order = final_order + f"{name} - X{qty} - Rs.{price}\n"
            coupon_obj = Coupon.objects.get(code=coupon)
            dis_factor = coupon_obj.val
            discounted_price = total_price - (total_price*dis_factor)
            final_order += f"Total Price: {total_price}\n"
            final_order += f"Coupon Applied: {coupon}\n"
            final_order += f"Discounted Price: {discounted_price}"
            order = Order(
                items=final_order,
                total_cost=total_price,
                user=request.user,
                first_name=firstname,
                last_name=lastname,
                address1=address1,
                address2=address2,
                email=email,
                phone=phone,
                city=city,
                state=state,
                pincode=pincode,
                landmark=landmark,
                discounted_cost=discounted_price,
                code_applied=coupon
                )
            order.save()
            context = {
                'thank': True,
                'id': order.id
            }
            messages.success(request, f"Your order has been placed successfully. Your Order Id is '{order.id}'.")
            return redirect("/")
        return render(request, 'checkout.html')
    else:
        p = request.GET.get('p', "/")
        page = request.GET.get('page', "/")
        messages.error(request, "You must be logged in to checkout!")
        if p == "/" and page == "/":
            return redirect("/")
        elif page != "/":
            return redirect(f"{p}&page={page}")
        else:
            return redirect(f"{p}&page={page}")

def handleRegister(request):
    if request.method == "POST":
        # Get the post parameters
        firstname = request.POST.get("register_firstname")
        lastname = request.POST.get("register_lastname")
        username = request.POST.get("register_username")
        email = request.POST.get("register_email")
        password = request.POST.get("register_password")
        conf_password = request.POST.get("register_conf_password")
        add1 = request.POST.get("add_line_1")
        add2 = request.POST.get("add_line_2")
        city = request.POST.get("city")
        state = request.POST.get("state")
        pincode = request.POST.get("pincode")
        landmark = request.POST.get("landmark")
        otp = request.POST.get("otp")
        otpid = request.POST.get("otpid")
        slug = request.POST.get("slug")

        print(add1, add2, city, state, pincode, landmark, otp, otpid)

        # check for errorneous input
        if len(firstname) <= 3:
            messages.error(request, "Firstname length is too short.")
            return redirect(slug)
        if len(firstname) >= 15:
            messages.error(request, "Firstname length is too long.")
            return redirect(slug)
        if len(lastname) <= 3:
            messages.error(request, "Lastname length is too short.")
            return redirect(slug)
        if len(lastname) >= 15:
            messages.error(request, "Lastname length is too long.")
            return redirect(slug)
        if len(username) <= 3:
            messages.error(request, "Username length is too short.")
            return redirect(slug)
        if len(username) >= 15:
            messages.error(request, "Username length is too long.")
            return redirect(slug)
        if password != conf_password:
            messages.error(request, "Passwords do not match.")
            return redirect(slug)
        if User.objects.filter(username=username).exists():
            messages.error(request, "The username you have taken already exists.")
            return redirect(slug)
        if User.objects.filter(email=email).exists():
            messages.error(request, "The email you have taken already exists.")
            return redirect(slug)
        if OTP.objects.get(id=int(otpid)).value != otp:
            messages.error(request, "The OTP is either expired or invalid.")
            return redirect(slug)
        

        # Create the user
        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = firstname
        myuser.last_name = lastname
        myuser.save()
        details = UserDetails(
            user=myuser,
            address1=add1,
            address2=add2,
            city=city,
            state=state,
            pincode=pincode,
            landmark=landmark
        )
        details.save()
        messages.success(request, "User created successfully. Now log in with the details provided.")
    return redirect(slug)

def handleLogin(request):
    if request.method == "POST":
        # Get the post parameters
        loginusername = request.POST.get("login_username")
        loginpassword = request.POST.get("login_password")
        slug = request.POST.get("slug")

        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, f"Logged in successfully as @{user}.")
            return redirect(slug)
        else:
            messages.error(request, "Invalid credentials, please try again.")
            return redirect(slug)

    return HttpResponse("404- Not found")

def handleLogout(request):
    slug = request.GET.get("slug")
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect(f"{slug}")

def accountSettings(request):
    found = 1
    if request.user.is_authenticated:
        myuser = User.objects.get(username=request.user)
        try:
            details = UserDetails.objects.get(user__username=myuser.username)
        except:
            messages.error(request, "No records found for your account. Update your details.")
            found = 0
        if found:
            context = {
                "first": myuser.first_name,
                "last": myuser.last_name,
                "email": myuser.email,
                "add1": details.address1,
                "add2": details.address2,
                "city": details.city,
                "state": details.state,
                "pincode": details.pincode,
                "landmark": details.landmark
                }
        else:
            context = {
                "first": myuser.first_name,
                "last": myuser.last_name,
                "email": myuser.email,
                }
        return render(request, 'account.html', context)
    else:
        messages.error(request, "The requested page was not found.")
        return redirect("/")

def updateProfile(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            # Getting Parameters to update
            firstname = request.POST.get("firstname", "")
            lastname = request.POST.get("lastname", "")
            email = request.POST.get("useremail", "")
            otp_id = request.POST.get("update-profile-otp-id", "")
            otp_val = request.POST.get("update-profile-otp-input", "")
            print("OTP ID AND VAL:", otp_id, otp_val)
            print(firstname, lastname, email)
            # Updating User Instance
            myuser = User.objects.get(username=request.user.username)
            myuser.first_name = firstname
            myuser.last_name = lastname
            if myuser.email != email:
                o = OTP.objects.get(id=otp_id)
                print(o)
                if o.value == otp_val:
                    myuser.email = email
                    o.delete()
                else:
                    messages.error(request, "OTP is either invalid or incorrect.")
                    return redirect("/account")
            myuser.save()
            messages.success(request, "Account details updated successfully.")
            return redirect("/account")
        else:
            messages.error(request, "Please log in to access that page.")
            return redirect("/")
    else:
        messages.error(request, "Page Not Found.")
        return redirect("/")

def updateAddress(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            # Getting Parameters to update
            add1 = request.POST.get("add1", "")
            add2 = request.POST.get("add2", "")
            city = request.POST.get("city", "")
            state = request.POST.get("state", "")
            pincode = request.POST.get("pincode", "")
            landmark = request.POST.get("landmark", "")
            # Updating Details
            details = UserDetails.objects.get(user__username=request.user)
            details.address1 = add1
            details.address2 = add2
            details.city = city
            details.state = state
            details.pincode = pincode
            details.landmark = landmark
            details.save()
            messages.success(request, "Address updated successfully.")
            return redirect("/account")
        else:
            messages.error(request, "Please log in to access that page.")
            return redirect("/")
    else:
        messages.error(request, "Page Not Found.")
        return redirect("/")

def updatePassword(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            # Getting Parameters to update
            oldpass = request.POST.get("oldpass", "")
            newpass = request.POST.get("newpass", "")
            confpass = request.POST.get("confpass", "")
            print(oldpass, newpass, confpass)
            # Updating Details
            if newpass == confpass:
                myuser = User.objects.get(username=request.user.username)
                if myuser.check_password(oldpass):
                    myuser.set_password(newpass)
                    messages.success(request, "Address updated successfully.")
                else:
                    messages.error(request, "Wrong old password. Password NOT updated.")
                return redirect("/account")
            else:
                messages.error(request, "Passwords do not match.")
                return redirect("/account")
        else:
            messages.error(request, "Please log in to access that page.")
            return redirect("/")
    else:
        messages.error(request, "Page Not Found.")
        return redirect("/")

def generateOTP(length):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def sendOTP(request):
    if request.method == "POST":
        toEmail = request.POST.get('emailid')
        otp = generateOTP(6)
        existing = OTP.objects.filter(value=otp).first()
        if existing is not None:
            while existing.value == otp:
                otp = generateOTP(6)
        otp_ob = OTP(value=otp)
        otp_ob.save()
        otp_ob_id = otp_ob.id
        send_mail(
                f"Your OTP for Fusion Store", # subject
                f"Your OTP is {otp}.\nDo NOT share this OTP with anyone.", # message
                '', # from email
                [toEmail], # to email, must be an iterable
                )
        return JsonResponse({'id': otp_ob_id})

def forgotpassword(request):
    if request.method == "POST":
        oldpass = request.POST.get("oldpass", "")
        newpass = request.POST.get("newpass", "")
        confpass = request.POST.get("confpass", "")
        otp = request.POST.get("confpass", "otp")
        otpid = request.POST.get("confpass", "otpid")
        print(oldpass, newpass, confpass, otp, otpid)
        return render("/")
    return render(request, 'forgotpassword.html')

def orders(request):
    pass

# TODO: make no search results if result length == 0
# TODO for otp: add a counter variable