import json
import paypalrestsdk
import razorpay
import string
from django.http import JsonResponse, HttpResponseBadRequest
from decimal import Decimal
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from uuid import uuid4
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.exceptions import ValidationError
from social_django.models import UserSocialAuth
from django.utils.html import strip_tags
import random
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.template import Context
from io import BytesIO
from xhtml2pdf import pisa  # Install xhtml2pdf using pip
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import logging
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from .models import (
    DeliveryBoy,
    Farmer,
    ContactUs,
    Supplier,
    Product,
    ProductCategory,
    CartItem,
    Order,
    ReturnRequest,ProductDamage,
)


def index(request):
    return render(request, "index.html")


def about_us(request):
    return render(request, "about_us.html")


def services(request):
    return render(request, "services.html")


def contact(request):
    return render(request, "contact.html")


def rental_items(request):
    products = Product.objects.all()
    return render(request, "rental_items.html", {"products": products})


"""def login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        # Check Google Sign-In
        try:
            social_user = UserSocialAuth.objects.get(provider='google-oauth2', uid=email)
            user = social_user.user
            login(request, user, backend='social_core.backends.google.GoogleOAuth2')
            return redirect('customer_index')  # Adjust this to your actual redirect URL after Google Sign-In
        except UserSocialAuth.DoesNotExist:
            pass

        # Check Farmer
        try:
            user = Farmer.objects.get(email=email)
            if user.status == 'blocked':
                messages.error(request, "Your account has been blocked.")
                return render(request, "login.html")
            if check_password(password, user.password):
                update_last_login(user)
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                set_session_variables(request, user, "farmer")
                return redirect("customer_index")
            else:
                raise Farmer.DoesNotExist  # Invalid password
        except Farmer.DoesNotExist:
            pass

        # Check Supplier
        try:
            user = Supplier.objects.get(email=email)
            if user.status == 'blocked':
                messages.error(request, "Your account has been blocked.")
                return render(request, "login.html")
            if check_password(password, user.password):
                update_last_login(user)
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                set_session_variables(request, user, "supplier")
                return redirect("supplier_index")
            else:
                raise Supplier.DoesNotExist  # Invalid password
        except Supplier.DoesNotExist:
            pass

        # Check DeliveryBoy
        try:
            user = DeliveryBoy.objects.get(email=email)
            if user.status == 'blocked':
                messages.error(request, "Your account has been blocked.")
                return render(request, "login.html")
            if check_password(password, user.password):
                update_last_login(user)
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                set_session_variables(request, user, "delivery_boy")
                return redirect("deliveryboy_index")
            else:
                raise DeliveryBoy.DoesNotExist  # Invalid password
        except DeliveryBoy.DoesNotExist:
            pass

        # Check Admin
        if email == "admin@gmail.com" and password == "admin@123":
            request.session["user_id"] = "admin"
            request.session["user_type"] = "admin"
            request.session["user_name"] = "Admin"
            request.session["user_email"] = "admin@gmail.com"
            return redirect("admin_index")

        # Invalid credentials
        messages.error(request, "Invalid email or password")
        return render(request, "login.html")

    return render(request, "login.html")"""


def login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        # Check Google Sign-In
        try:
            social_user = UserSocialAuth.objects.get(
                provider="google-oauth2", uid=email
            )
            user = social_user.user
            login(request, user, backend="social_core.backends.google.GoogleOAuth2")
            return redirect(
                "customer_index"
            )  # Adjust this to your actual redirect URL after Google Sign-In
        except UserSocialAuth.DoesNotExist:
            pass

        # Check Farmer
        try:
            user = Farmer.objects.get(email=email)
            if user.status == "blocked":
                messages.error(request, "Your account has been blocked.")
                return render(request, "login.html")
            if check_password(password, user.password):
                update_last_login(user)
                login(
                    request, user, backend="django.contrib.auth.backends.ModelBackend"
                )
                set_session_variables(request, user, "farmer")
                return redirect("customer_index")
            else:
                raise Farmer.DoesNotExist  # Invalid password
        except Farmer.DoesNotExist:
            pass

        # Check Supplier
        try:
            user = Supplier.objects.get(email=email)
            if user.status == "blocked":
                messages.error(request, "Your account has been blocked.")
                return render(request, "login.html")
            if check_password(password, user.password):
                update_last_login(user)
                login(
                    request, user, backend="django.contrib.auth.backends.ModelBackend"
                )
                set_session_variables(request, user, "supplier")
                return redirect("supplier_index")
            else:
                raise Supplier.DoesNotExist  # Invalid password
        except Supplier.DoesNotExist:
            pass

        # Check DeliveryBoy
        try:
            user = DeliveryBoy.objects.get(email=email)
            if user.status == "blocked":
                messages.error(request, "Your account has been blocked.")
                return render(request, "login.html")
            if check_password(password, user.password):
                update_last_login(user)
                login(
                    request, user, backend="django.contrib.auth.backends.ModelBackend"
                )
                set_session_variables(request, user, "delivery_boy")
                return redirect("deliveryboy_index")
            else:
                raise DeliveryBoy.DoesNotExist  # Invalid password
        except DeliveryBoy.DoesNotExist:
            pass

        # Check Admin
        if email == "admin@gmail.com" and password == "admin@123":
            request.session["user_id"] = "admin"
            request.session["user_type"] = "admin"
            request.session["user_name"] = "Admin"
            request.session["user_email"] = "admin@gmail.com"
            return redirect("admin_index")

        # Invalid credentials
        messages.error(request, "Invalid email or password")
        return render(request, "login.html")

    return render(request, "login.html")


def update_last_login(user):
    user.last_login = timezone.now()
    user.save()


def set_session_variables(request, user, user_type):
    request.session["user_id"] = user.id
    request.session["user_type"] = user_type
    request.session["user_name"] = user.name
    request.session["user_email"] = user.email
    request.session["user_address"] = user.address
    request.session["user_phone"] = user.phone


"""def set_session_variables(request, user, user_type):
    request.session["user_id"] = user.id
    request.session["user_type"] = user_type
    request.session["user_name"] = user.name
    request.session["user_email"] = user.email
    request.session["user_address"] = user.address
    request.session["user_phone"] = user.phone"""


def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp(email, otp):
    subject = "Your OTP for AgroRent Hub"
    html_message = render_to_string("otp_email.html", {"otp": otp})
    plain_message = strip_tags(html_message)
    email_from = "agrorenthub@gmail.com"
    recipient_list = [email]
    send_mail(
        subject, plain_message, email_from, recipient_list, html_message=html_message
    )


def register(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        address = request.POST["address"]
        phone = request.POST["phone"]
        password = make_password(request.POST["password"])
        user_type = request.POST["user_type"]

        # Check if email already exists
        if (
            Farmer.objects.filter(email=email).exists()
            or Supplier.objects.filter(email=email).exists()
            or DeliveryBoy.objects.filter(email=email).exists()
        ):
            messages.error(request, "Email is already registered.")
            return render(request, "register.html")

        # Generate OTP
        otp = generate_otp()

        # Save user information and OTP in session
        request.session["registration_data"] = {
            "name": name,
            "email": email,
            "address": address,
            "phone": phone,
            "password": password,
            "user_type": user_type,
            "otp": otp,
        }

        # Send OTP to user's email
        send_otp(email, otp)
        return redirect("verify_otp")

    return render(request, "register.html")


def verify_otp(request):
    if request.method == "POST":
        otp = request.POST["otp"]
        session_data = request.session.get("registration_data")

        if session_data and otp == session_data["otp"]:
            # Register the user based on user_type
            if session_data["user_type"] == "farmer":
                Farmer.objects.create(
                    name=session_data["name"],
                    email=session_data["email"],
                    address=session_data["address"],
                    phone=session_data["phone"],
                    password=session_data["password"],
                    status="active",
                )
            elif session_data["user_type"] == "supplier":
                Supplier.objects.create(
                    name=session_data["name"],
                    email=session_data["email"],
                    address=session_data["address"],
                    phone=session_data["phone"],
                    password=session_data["password"],
                    status="active",
                )
            elif session_data["user_type"] == "delivery_boy":
                DeliveryBoy.objects.create(
                    name=session_data["name"],
                    email=session_data["email"],
                    address=session_data["address"],
                    phone=session_data["phone"],
                    password=session_data["password"],
                    status="active",
                )

            # Clear session data
            del request.session["registration_data"]
            return redirect("login")
        else:
            messages.error(request, "Invalid OTP")

    return render(request, "verify_otp.html")


"""def register(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        address = request.POST["address"]
        phone = request.POST["phone"]
        password = make_password(request.POST["password"])
        user_type = request.POST["user_type"]

        # Check if email already exists
        if (
            Farmer.objects.filter(email=email).exists()
            or Supplier.objects.filter(email=email).exists()
            or DeliveryBoy.objects.filter(email=email).exists()
            or User.objects.filter(email=email).exists()
        ):
            messages.error(request, "Email is already registered.")
            return render(request, "register.html")

        # Register the user based on user_type
        if user_type == "farmer":
            Farmer.objects.create(
                name=name,
                email=email,
                address=address,
                phone=phone,
                password=password,
                status="active",
            )
        elif user_type == "supplier":
            Supplier.objects.create(
                name=name,
                email=email,
                address=address,
                phone=phone,
                password=password,
                status="active",
            )
        elif user_type == "delivery_boy":
            DeliveryBoy.objects.create(
                name=name,
                email=email,
                address=address,
                phone=phone,
                password=password,
                status="active",
            )

        return redirect("login")
    return render(request, "register.html")"""


def check_email(request):
    email = request.GET.get("email", None)
    response = {
        "exists": Farmer.objects.filter(email=email).exists()
        or Supplier.objects.filter(email=email).exists()
        or DeliveryBoy.objects.filter(email=email).exists()
        or User.objects.filter(email=email).exists()
    }
    return JsonResponse(response)


def forgotpassword(request):
    if request.method == "POST":
        email = request.POST["email"]
        user = None

        try:
            user = Farmer.objects.get(email=email)
        except Farmer.DoesNotExist:
            try:
                user = Supplier.objects.get(email=email)
            except Supplier.DoesNotExist:
                try:
                    user = DeliveryBoy.objects.get(email=email)
                except DeliveryBoy.DoesNotExist:
                    pass

        if user:
            token = str(uuid4())
            user.reset_password_token = token
            user.token_expiry = timezone.now() + timezone.timedelta(hours=1)
            user.save()

            reset_url = request.build_absolute_uri(
                reverse(
                    "resetpassword",
                    args=[urlsafe_base64_encode(force_bytes(user.pk)), token],
                )
            )

            html_content = render_to_string(
                "password_reset_email.html", {"user": user, "reset_url": reset_url}
            )
            text_content = strip_tags(html_content)

            email_message = EmailMultiAlternatives(
                "Reset Your Password", text_content, "admin@agrorenthub.com", [email]
            )
            email_message.attach_alternative(html_content, "text/html")
            email_message.send()

            messages.success(
                request, "A password reset link has been sent to your email."
            )
        else:
            messages.error(request, "Email not found.")

    return render(request, "forgotpassword.html")


"""def forgotpassword(request):
    if request.method == "POST":
        email = request.POST["email"]
        user = None

        try:
            user = Farmer.objects.get(email=email)
        except Farmer.DoesNotExist:
            try:
                user = Supplier.objects.get(email=email)
            except Supplier.DoesNotExist:
                try:
                    user = DeliveryBoy.objects.get(email=email)
                except DeliveryBoy.DoesNotExist:
                    pass

        if user:
            token = str(uuid4())
            user.reset_password_token = token
            user.token_expiry = timezone.now() + timezone.timedelta(hours=1)
            user.save()

            reset_url = request.build_absolute_uri(
                reverse(
                    "resetpassword",
                    args=[urlsafe_base64_encode(force_bytes(user.pk)), token],
                )
            )
            send_mail(
                "Reset Your Password",
                f"Hi {user.name},\n\nClick the link below to reset your password:\n\n{reset_url}\n\nIf you did not request a password reset, please ignore this email.",
                "admin@agrorenthub.com",
                [email],
                fail_silently=False,
            )
            messages.success(
                request, "A password reset link has been sent to your email."
            )
        else:
            messages.error(request, "Email not found.")

    return render(request, "forgotpassword.html")

"""


def resetpassword(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = (
            Farmer.objects.get(pk=uid)
            or Supplier.objects.get(pk=uid)
            or DeliveryBoy.objects.get(pk=uid)
        )
    except (
        TypeError,
        ValueError,
        OverflowError,
        Farmer.DoesNotExist,
        Supplier.DoesNotExist,
        DeliveryBoy.DoesNotExist,
    ):
        user = None

    if (
        user is not None
        and user.reset_password_token == token
        and timezone.now() < user.token_expiry
    ):
        if request.method == "POST":
            password = request.POST["password"]
            confirm_password = request.POST["confirm_password"]

            if password == confirm_password:
                user.password = make_password(password)
                user.reset_password_token = None
                user.token_expiry = None
                user.save()
                messages.success(request, "Password has been reset successfully.")
                return redirect("login")
            else:
                messages.error(request, "Passwords do not match.")

        return render(request, "resetpassword.html", {"uidb64": uidb64, "token": token})
    else:
        messages.error(request, "The reset link is invalid or has expired.")
        return redirect("forgotpassword")


def supplier_index(request):
    if request.session.get("user_type") == "supplier":
        # Fetch additional user details based on user_id if needed
        user_id = request.session.get("user_id")
        user = Supplier.objects.get(id=user_id)
        context = {
            "user_name": user.name,
            "user_email": user.email,
        }
        return render(request, "supplier/supplier_index.html", context)
    else:
        return render(request, "access_denied.html")


"""
def admin_index(request):
    if request.session.get("user_type") == "admin":
        farmers = Farmer.objects.all()
        suppliers = Supplier.objects.all()
        delivery_boys = DeliveryBoy.objects.all()
        context = {
            "user_name": request.session.get("user_name"),
            "user_email": request.session.get("user_email"),
            # Add other fields as needed
            "farmers": farmers,
            "suppliers": suppliers,
            "delivery_boys": delivery_boys,
        }
        return render(request, "admin/admin_index.html", context)
    else:
        return render(request, "access_denied.html")
"""


@never_cache
def logout_view(request):
    # Clear session data
    request.session.flush()

    # Redirect to the login page
    return redirect("login")


"""def customer_index(request):
    if request.session.get("user_type") == "farmer":
        user_id = request.session.get("user_id")
        user = Farmer.objects.get(id=user_id)
        context = {
            "user_name": user.name,
            "user_email": user.email,
            "user_phone": user.phone,
            "user_address": user.address,
        }
        return render(request, "customer/customer_index.html", context)
    else:
        return render(request, "access_denied.html")"""


def customer_index(request):
    if request.session.get("user_type") == "farmer":
        user_id = request.session.get("user_id")
        user = Farmer.objects.get(id=user_id)
        context = {
            "user_name": user.name,
            "user_email": user.email,
            "user_phone": user.phone,
            "user_address": user.address,
            "success_message": None,
        }

        if request.method == "POST":
            # Handle form submission
            name = request.POST.get("name")
            email = request.POST.get("email")
            message = request.POST.get("message")

            # Save to ContactUs model
            contact = ContactUs(name=name, email=email, message=message)
            contact.save()

            # Send email using EmailMessage to ensure correct from_email
            email_message = EmailMessage(
                subject=f"New Contact Message from {name}",
                body=message,
                from_email=email,  # User's email as sender
                to=["agrorenthub@gmail.com"],  # Recipient's email
                reply_to=[email],  # This ensures replies go to the user's email
            )
            email_message.send(fail_silently=False)

            # Display success message
            context["success_message"] = (
                "Thank you for contacting us! We will get back to you soon."
            )

        return render(request, "customer/customer_index.html", context)
    else:
        return render(request, "access_denied.html")


def customer_about(request):
    if request.session.get("user_type") == "farmer":
        user_id = request.session.get("user_id")
        user = Farmer.objects.get(id=user_id)
        context = {
            "user_name": user.name,
            "user_email": user.email,
        }
        return render(request, "customer/customer_about.html", context)
    else:
        return render(request, "access_denied.html")


def customer_service(request):
    if request.session.get("user_type") == "farmer":
        user_id = request.session.get("user_id")
        user = Farmer.objects.get(id=user_id)
        context = {
            "user_name": user.name,
            "user_email": user.email,
        }
        return render(request, "customer/customer_service.html", context)
    else:
        return render(request, "access_denied.html")


def customer_profile(request):
    if request.session.get("user_type") == "farmer":
        user_id = request.session.get("user_id")
        user = get_object_or_404(Farmer, id=user_id)
        context = {"user": user}
        return render(request, "customer/customer_profile.html", context)
    else:
        return render(request, "access_denied.html")


def edit_details(request):
    if request.method == "POST":
        user_id = request.session.get("user_id")
        user = get_object_or_404(Farmer, id=user_id)

        user.name = request.POST["name"]
        """ user.email = request.POST["email"]"""
        user.phone = request.POST["phone"]
        user.address = request.POST["address"]
        user.save()
        """ messages.success(request, "Details updated successfully.")"""
        return redirect("customer_profile")
    else:
        return redirect("customer_index")


def change_password(request):
    if request.method == "POST":
        user_id = request.session.get("user_id")
        user = get_object_or_404(Farmer, id=user_id)

        current_password = request.POST["current-password"]
        new_password = request.POST["new-password"]
        confirm_password = request.POST["confirm-password"]

        if check_password(current_password, user.password):
            if new_password == confirm_password:
                user.password = make_password(new_password)
                user.save()
                return redirect("login")
            """else:
                messages.error(request, "New passwords do not match.")
        else:
            messages.error(request, "Current password is incorrect.")"""

        return redirect("customer_index")


"""def products(request):
    if request.method == 'GET':
        products = Product.objects.all()  # Fetch all products
        return render(request, 'customer/products.html', {
            'products': products,
        })
    else:
        return redirect('some_error_page') """

"""def products(request):
    products = Product.objects.all()
    categories = ProductCategory.objects.all()
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'customer/products.html', context)"""


def products(request):
    # products = Product.objects.filter(is_disabled=False)
    # categories = ProductCategory.objects.all()
    # Filter out disabled categories
    active_categories = ProductCategory.objects.filter(is_disabled=False)

    # Get products that belong to active categories
    products = Product.objects.filter(category__in=active_categories, is_disabled=False)

    # Include all categories, including disabled ones if needed for display purposes
    categories = ProductCategory.objects.all()
    context = {
        "products": products,
        "categories": categories,
    }
    return render(request, "customer/products.html", context)


"""
def add_to_cart(request, product_id):
    user_id = request.session.get("user_id")
    user = get_object_or_404(Farmer, id=user_id)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    # Handle start_date
    start_date_str = request.POST.get('start_date', None)
    if start_date_str:
        try:
            start_date = timezone.datetime.strptime(start_date_str, '%Y-%m-%d').date()
        except ValueError:
            start_date = timezone.now().date()
    else:
        start_date = timezone.now().date()
    
    # Handle end_date
    end_date_str = request.POST.get('end_date', None)
    if end_date_str:
        try:
            end_date = timezone.datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            end_date = timezone.now().date()
    else:
        end_date = timezone.now().date()

    # Calculate number of days between start and end dates
    number_of_days = (end_date - start_date).days # Include both start and end dates

    price = product.product_price_per_day * quantity * number_of_days
    
    cart_item, created = CartItem.objects.get_or_create(
        user=user,
        product=product,
        defaults={'quantity': quantity, 'start_date': start_date, 'end_date': end_date, 'price': price}
    )
    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    return redirect('productcart')  # URL name for your cart view
"""


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user_id = request.session.get("user_id")
    cart_item = None

    if user_id:
        user = get_object_or_404(Farmer, id=user_id)
        try:
            cart_item = CartItem.objects.get(user=user, product=product)
        except CartItem.DoesNotExist:
            cart_item = None

    context = {
        "product": product,
        "cart_item": cart_item,
    }

    return render(request, "customer/product_detail.html", context)


def add_to_cart(request, product_id):
    user_id = request.session.get("user_id")
    user = get_object_or_404(Farmer, id=user_id)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get("quantity", 1))

    start_date_str = request.POST.get("start_date", None)
    end_date_str = request.POST.get("end_date", None)

    if start_date_str:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    else:
        start_date = None

    if end_date_str:
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    else:
        end_date = None

    if not start_date or not end_date or end_date <= start_date:
        messages.error(request, "Invalid start or end date.")
        return redirect("product_detail", product_id=product_id)

    if product.stock_quantity < quantity:
        messages.error(request, "Not enough stock available.")
        return redirect("product_detail", product_id=product_id)

    if product.stock_quantity <= 5:
        messages.error(request, "Product is out of stock.")
        return redirect("product_detail", product_id=product_id)

    number_of_days = (end_date - start_date).days
    price = product.product_price_per_day * quantity * number_of_days

    cart_item, created = CartItem.objects.get_or_create(
        user=user,
        product=product,
        defaults={
            "quantity": quantity,
            "start_date": start_date,
            "end_date": end_date,
            "price": price,
        },
    )
    if not created:
        cart_item.quantity = quantity
        cart_item.price = (
            product.product_price_per_day * cart_item.quantity * number_of_days
        )
        cart_item.start_date = start_date
        cart_item.end_date = end_date
        cart_item.save()

    return redirect("productcart")


def productcart(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")  # Redirect to login if no user_id in session

    user = get_object_or_404(Farmer, id=user_id)
    cart_items = CartItem.objects.filter(user=user)
    return render(request, "customer/productcart.html", {"cart_items": cart_items})


def delete_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect("productcart")


# Configure PayPal SDK
# Configure PayPal SDK
"""paypalrestsdk.configure({
    "mode": "sandbox",  # sandbox or live
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_SECRET_KEY
})

def place_order(request):
    if request.method == 'POST':
        user_id = request.session.get("user_id")
        user = get_object_or_404(Farmer, id=user_id)
        cart_items = CartItem.objects.filter(user=user)

        if cart_items.exists():
            total_price = sum(item.price for item in cart_items)
            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal"
                },
                "redirect_urls": {
                    "return_url": request.build_absolute_uri(reverse('payment_success')),
                    "cancel_url": request.build_absolute_uri(reverse('payment_cancel'))
                },
                "transactions": [{
                    "amount": {
                        "total": str(total_price),
                        "currency": "USD"
                    },
                    "description": "Agriculture Rental Hub Order",
                    "item_list": {
                        "items": [{
                            "name": item.product.product_name,
                            "sku": item.product.id,
                            "price": str(item.price),
                            "currency": "USD",
                            "quantity": item.quantity
                        } for item in cart_items]
                    }
                }]
            })

            if payment.create():
                for link in payment.links:
                    if link.rel == "approval_url":
                        approval_url = link.href
                        return redirect(approval_url)
            else:
                return JsonResponse({'error': payment.error}, status=400)
        else:
            return redirect('productcart')
    return redirect('productcart')

def payment_success(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        user_id = request.session.get("user_id")
        user = get_object_or_404(Farmer, id=user_id)
        cart_items = CartItem.objects.filter(user=user)

        for item in cart_items:
            Order.objects.create(
                user=user,
                product=item.product,
                quantity=item.quantity,
                start_date=item.start_date,
                end_date=item.end_date,
                price=item.price,
                payment_status='completed'
            )
            item.product.stock_quantity -= item.quantity
            item.product.save()

        cart_items.delete()
        return redirect('orderdetails')
    else:
        return JsonResponse({'error': payment.error}, status=400)

def payment_cancel(request):
    return render(request, 'payment_cancel.html')

def order_details(request):
    user_id = request.session.get("user_id")
    user = get_object_or_404(Farmer, id=user_id)
    orders = Order.objects.filter(user=user)

    return render(request, 'orderdetails.html', {'orders': orders})"""
# Initialize Razorpay client with your credentials

logger = logging.getLogger(__name__)

# Initialize Razorpay client with your credentials
client = razorpay.Client(auth=("rzp_test_IHsYiv67CqdAaf", "xP9T994L6wieFJYHjb1wfPNO"))

'''
def place_order(request):
    if request.method == "POST":
        user_id = request.session.get("user_id")
        user = get_object_or_404(Farmer, id=user_id)
        cart_items = CartItem.objects.filter(user=user)

        if cart_items.exists():
            total_price = sum(
                float(item.price) for item in cart_items
            )  # Convert Decimal to float
            amount_in_paise = int(total_price * 100)  # Razorpay expects amount in paise
            currency = "INR"

            try:
                # Create order in Razorpay
                razorpay_order = client.order.create(
                    {
                        "amount": amount_in_paise,
                        "currency": currency,
                        "payment_capture": "1",
                    }
                )

                # Save the Razorpay order ID in session or database if needed
                request.session["razorpay_order_id"] = razorpay_order["id"]

                # Pass the required details to the frontend
                context = {
                    "razorpay_order_id": razorpay_order["id"],
                    "razorpay_key": "rzp_test_IHsYiv67CqdAaf",
                    "amount": total_price,
                    "amount_in_paise": amount_in_paise,
                    "currency": currency,
                }

                return render(request, "customer/payment_checkout.html", context)
            except Exception as e:
                logger.error("Error creating Razorpay order: %s", e)
                return JsonResponse(
                    {"error": "Failed to create Razorpay order"}, status=500
                )
        else:
            return redirect("productcart")
    return redirect("productcart")
'''
def place_order(request):
    if request.method == "POST":
        user_id = request.session.get("user_id")
        user = get_object_or_404(Farmer, id=user_id)
        cart_items = CartItem.objects.filter(user=user)

        if cart_items.exists():
            total_price = sum(
                float(item.price) for item in cart_items
            )  # Convert Decimal to float

            # Set your upper limit (e.g., ₹100,000)
            upper_limit = 100000

            if total_price > upper_limit:
                messages.error(request, f"The total amount exceeds the limit of ₹{upper_limit}. Please adjust your cart.")
                return redirect("productcart")

            amount_in_paise = int(total_price * 100)  # Razorpay expects amount in paise
            currency = "INR"

            try:
                # Create order in Razorpay
                razorpay_order = client.order.create(
                    {
                        "amount": amount_in_paise,
                        "currency": currency,
                        "payment_capture": "1",
                    }
                )

                # Save the Razorpay order ID in session or database if needed
                request.session["razorpay_order_id"] = razorpay_order["id"]

                # Pass the required details to the frontend
                context = {
                    "razorpay_order_id": razorpay_order["id"],
                    "razorpay_key": "rzp_test_IHsYiv67CqdAaf",
                    "amount": total_price,
                    "amount_in_paise": amount_in_paise,
                    "currency": currency,
                }

                return render(request, "customer/payment_checkout.html", context)
            except Exception as e:
                logger.error("Error creating Razorpay order: %s", e)
                return JsonResponse(
                    {"error": "Failed to create Razorpay order"}, status=500
                )
        else:
            return redirect("productcart")
    return redirect("productcart")


@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        razorpay_payment_id = request.POST.get("razorpay_payment_id")
        razorpay_order_id = request.POST.get("razorpay_order_id")
        razorpay_signature = request.POST.get("razorpay_signature")

        # Verify the payment signature
        params_dict = {
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_signature": razorpay_signature,
        }

        try:
            client.utility.verify_payment_signature(params_dict)
        except Exception as e:
            logger.error("Signature verification failed: %s", e)
            return JsonResponse({"error": "Signature verification failed"}, status=400)

        # Payment successful, create order and clear cart
        user_id = request.session.get("user_id")
        user = get_object_or_404(Farmer, id=user_id)
        cart_items = CartItem.objects.filter(user=user)

        for item in cart_items:
            Order.objects.create(
                user=user,
                product=item.product,
                quantity=item.quantity,
                start_date=item.start_date,
                end_date=item.end_date,
                price=item.price,
                payment_status="completed",
                payment_id=razorpay_payment_id,  # Save payment ID
            )
            item.product.stock_quantity -= item.quantity
            item.product.save()

        cart_items.delete()
        return redirect("orderdetails")
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)


def payment_cancel(request):
    return render(request, "payment_cancel.html")


def order_details(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")  # Redirect to login if user_id is not in session

    user = get_object_or_404(Farmer, id=user_id)
    orders = Order.objects.filter(user=user).select_related("product")  # Adjusted here

    return render(request, "customer/orderdetails.html", {"orders": orders})


def delete_order(request, order_id):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")
    order = get_object_or_404(Order, id=order_id)
    if order.user.id == user_id:
        order.delete()
    return redirect("order_details")


def download_receipt(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.user.id != request.session.get("user_id"):
        return HttpResponse("Unauthorized", status=401)

    # Render the receipt HTML
    context = {"order": order}
    html_string = render_to_string("receipts/order_receipt.html", context)

    # Convert HTML to PDF
    result = BytesIO()
    pdf = pisa.CreatePDF(BytesIO(html_string.encode("UTF-8")), dest=result)

    if pdf.err:
        return HttpResponse("Error generating PDF", status=500)

    response = HttpResponse(result.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="receipt_{order_id}.pdf"'
    return response


def orderproductview(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    product = order.product

    context = {"product": product, "order": order}
    return render(request, "customer/orderproductview.html", context)


@csrf_exempt
def schedule_return(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        order_id = data.get('order_id')
        
        try:
            order = Order.objects.get(id=order_id)
            if order.status == 'rented':
                # Logic to mark return as scheduled (if needed)
                order.status = 'return_scheduled'  # Add this status to Order model if needed
                order.save()
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Order status invalid for return'})
        except Order.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Order not found'})


def supplier_index(request):
    if request.session.get("user_type") == "supplier":
        # Fetch additional user details based on user_id if needed
        user_id = request.session.get("user_id")
        user = Supplier.objects.get(id=user_id)
        context = {
            "user_name": user.name,
            "user_email": user.email,
        }
        return render(request, "supplier/supplier_index.html", context)
    else:
        return render(request, "access_denied.html")


def supplier_profile(request):
    if not request.session.get("user_id"):
        return redirect("login")

    supplier_id = request.session["user_id"]
    try:
        supplier = Supplier.objects.get(id=supplier_id)
    except Supplier.DoesNotExist:
        return redirect("login")

    context = {
        "supplier": supplier,
    }

    return render(request, "supplier/supplier_profile.html", context)


def supplier_edit_details(request):
    if request.method == "POST":
        supplier_id = request.session["user_id"]
        try:
            supplier = Supplier.objects.get(id=supplier_id)
        except Supplier.DoesNotExist:
            return redirect("login")

        supplier.name = request.POST["name"]
        # supplier.email = request.POST['email']
        supplier.address = request.POST["address"]
        supplier.phone = request.POST["phone"]
        supplier.save()

        return redirect("supplier_profile")


def supplier_change_password(request):
    if request.method == "POST":
        supplier_id = request.session.get("user_id")
        if supplier_id is None:
            return redirect("login")

        try:
            supplier = Supplier.objects.get(id=supplier_id)
        except Supplier.DoesNotExist:
            return redirect("login")

        current_password = request.POST.get("current-password", "")
        new_password = request.POST.get(
            "password", ""
        )  # Adjusted to match input name 'password'
        confirm_password = request.POST.get(
            "confirm_password", ""
        )  # Adjusted to match input name 'confirm_password'

        if not check_password(current_password, supplier.password):
            # Handle incorrect current password scenario
            # You may want to show an error message or redirect appropriately
            return redirect("supplier_profile")

        if new_password != confirm_password:
            # Handle passwords not matching scenario
            # You may want to show an error message or redirect appropriately
            return redirect("supplier_profile")

        supplier.password = make_password(new_password)
        supplier.save()
        return redirect(
            "login"
        )  # Redirect to login or profile page after successful password change

    return redirect("supplier_profile")  # Handle GET requests or other scenarios


def supplier_add_pro(request):
    if request.method == "POST":
        user_id = request.session.get("user_id")
        supplier = get_object_or_404(Supplier, id=user_id)
        name = request.POST["product_name"]
        price_per_day = request.POST["product_price_per_day"]
        stock_quantity = request.POST["stock_quantity"]
        description = request.POST["product_description"]
        status = request.POST["status"]
        image = request.FILES["product_image"]

        # Retrieve category ID from POST data
        category_id = request.POST["category"]
        category = get_object_or_404(ProductCategory, id=category_id)

        product = Product.objects.create(
            product_name=name,
            product_price_per_day=price_per_day,
            stock_quantity=stock_quantity,
            product_description=description,
            status=status,
            product_image=image,
            supplier=supplier,
            category=category,  # Assign the category object to the product
        )

        return redirect("supplier_view_pro")

    else:
        # Get all categories for initial render of the form
        categories = ProductCategory.objects.all()

        return render(
            request, "supplier/supplier_add_pro.html", {"categories": categories}
        )


def supplier_view_pro(request):
    if request.session.get("user_type") == "supplier":
        user_id = request.session.get("user_id")
        products = Product.objects.filter(supplier=user_id)
        return render(
            request, "supplier/supplier_view_pro.html", {"products": products}
        )
    else:
        return render(request, "access_denied.html")


def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        product.product_name = request.POST["product_name"]
        product.product_price_per_day = request.POST["product_price_per_day"]
        product.stock_quantity = request.POST["stock_quantity"]
        product.product_description = request.POST["product_description"]
        product.status = request.POST["status"]

        if "product_image" in request.FILES:
            product.product_image = request.FILES["product_image"]

        product.save()
        return redirect("supplier_view_pro")  # Redirect to view all products

    return render(request, "supplier/update_product.html", {"product": product})


"""
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        product.delete()
        return redirect('supplier_view_pro')  # Redirect to view all products
    
    return render(request, 'supplier/delete_product.html', {'product': product})"""


@csrf_exempt
def delete_product(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        product.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})


def supplier_add_cat(request):
    if request.method == "POST":
        name = request.POST.get("name")
        
        if name:
            # Check if the category name already exists
            if ProductCategory.objects.filter(name=name).exists():
                return render(request, "supplier/supplier_add_cat.html", {"error": "Category name already exists"})
            
            category = ProductCategory(name=name)
            category.save()

            return redirect("supplier_view_cat")

    # Get existing categories to send to the template for validation
    categories = ProductCategory.objects.values_list('name', flat=True)
    
    return render(request, "supplier/supplier_add_cat.html", {"categories": list(categories)})


def supplier_view_cat(request):
    categories = ProductCategory.objects.all()
    context = {"categories": categories}
    return render(request, "supplier/supplier_view_cat.html", context)


def update_category(request, category_id):
    category = get_object_or_404(ProductCategory, id=category_id)
    if request.method == "POST":
        new_name = request.POST.get("name")
        if new_name:
            category.name = new_name
            category.save()
            return redirect("supplier_view_cat")  # Redirect to the category list view
    context = {"category": category}
    return render(request, "supplier/update_category.html", context)


"""def delete_category(request, category_id):
    category = get_object_or_404(ProductCategory, id=category_id)
    if request.method == 'POST':
        category.delete()
        return redirect('supplier_view_cat')  # Redirect to the category list view
    context = {
        'category': category
    }
    return render(request, 'supplier/delete_category.html', context)
"""


@csrf_exempt
@require_POST
def delete_category(request, category_id):
    category = get_object_or_404(ProductCategory, id=category_id)
    category.delete()
    return JsonResponse({"success": True})


"""def supplier_add_del(request):
    return render(request, 'supplier/supplier_add_del.html')"""
"""def supplier_add_del(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        address = request.POST['address']
        phone = request.POST['phone']
        password = make_password(request.POST['password'])
        status = request.POST['status']
        
        # Check if the email already exists
        if DeliveryBoy.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
        else:
            delivery_boy = DeliveryBoy(name=name, email=email, address=address, phone=phone, password=password, status=status)
            delivery_boy.save()
            messages.success(request, "Delivery Boy added successfully.")
        
        return redirect('supplier_add_del')
    return render(request, 'supplier/supplier_add_del.html')"""
"""def supplier_add_del(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        address = request.POST['address']
        phone = request.POST['phone']
        password = make_password(request.POST['password'])
        status = request.POST['status']
        
        # Check if the email already exists
        if DeliveryBoy.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
        else:
            delivery_boy = DeliveryBoy(
                name=name,
                email=email,
                address=address,
                phone=phone,
                password=password,
                status=status,
                supplier=request.user  # Save the currently logged-in supplier
            )
            delivery_boy.save()
        
        return redirect('supplier_add_del')
    return render(request, 'supplier/supplier_add_del.html')"""
"""def supplier_add_del(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        address = request.POST['address']
        phone = request.POST['phone']
        password = request.POST['password']
        status = request.POST['status']

        # Get the supplier from the session or request (assuming the user is a supplier)
        supplier = Supplier.objects.get(id=request.session['supplier_id'])

        # Create the DeliveryBoy instance
        delivery_boy = DeliveryBoy(
            name=name,
            email=email,
            address=address,
            phone=phone,
            password=password,
            status=status,
            supplier=supplier
        )
        delivery_boy.save()

        return redirect('supplier/supplier_view_del')

    return render(request, 'supplier/supplier_add_del.html')"""


def supplier_add_del(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        address = request.POST["address"]
        phone = request.POST["phone"]
        password = request.POST["password"]
        status = request.POST["status"]

        # Get the supplier from the session
        supplier_id = request.session.get("user_id")
        if supplier_id:
            try:
                supplier = Supplier.objects.get(id=supplier_id)
            except Supplier.DoesNotExist:
                return redirect("login")  # Redirect to login if supplier is not found

            # Create the DeliveryBoy instance
            delivery_boy = DeliveryBoy(
                name=name,
                email=email,
                address=address,
                phone=phone,
                password=password,
                status=status,
                supplier=supplier,
            )
            delivery_boy.save()

            return redirect("supplier_view_del")
        else:
            return redirect(
                "login"
            )  # Redirect to login if supplier_id is not found in session

    return render(request, "supplier/supplier_add_del.html")


"""def supplier_view_del(request):
    return render(request, 'supplier/supplier_view_del.html')"""
"""def view_delivery_boys(request):
    delivery_boys = DeliveryBoy.objects.filter(supplier=request.user)
    return render(request, 'supplier/view_delivery_boys.html', {'delivery_boys': delivery_boys})"""


def supplier_view_del(request):
    if request.session.get("user_type") == "supplier":
        user_id = request.session.get("user_id")
        try:
            supplier = Supplier.objects.get(id=user_id)
            delivery_boys = DeliveryBoy.objects.filter(supplier=supplier)
            return render(
                request,
                "supplier/supplier_view_del.html",
                {"delivery_boys": delivery_boys},
            )
        except Supplier.DoesNotExist:
            return redirect("login")  # Handle case where supplier does not exist
    else:
        return redirect("login")  # Redirect to login if user is not authenticated


def delete_delivery_boy(request, delivery_boy_id):
    if request.session.get("user_id"):
        delivery_boy = DeliveryBoy.objects.get(id=delivery_boy_id)
        delivery_boy.delete()
        messages.success(request, "Delivery Boy deleted successfully.")
        return redirect("view_delivery_boys")
    else:
        return redirect("login")


def supplier_add_worker(request):
    return render(request, "supplier/supplier_add_worker.html")


def supplier_view_worker(request):
    return render(request, "supplier/supplier_view_worker.html")


def supplier_view_order(request):
    supplier = Supplier.objects.get(id=request.session["user_id"])
    orders = Order.objects.filter(product__supplier=supplier)
    return render(request, "supplier/supplier_view_order.html", {"orders": orders})
def add_product_damage(request):
    if request.method == 'POST':
        product_id = request.POST.get('product')
        damage_level = request.POST.get('damage_level')
        damage_types = request.POST.getlist('damage_types')
        estimated_repair_cost = request.POST.get('estimated_repair_cost')

        # Get the product object
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({"error": "Product not found"}, status=404)

        # Check for existing records
        existing_damages = ProductDamage.objects.filter(
            product=product,
            damage_level=damage_level,
            damage_type__in=damage_types
        )

        # If any existing damage record is found, return a JSON response
        if existing_damages.exists():
            return JsonResponse({"error": "Damage record already exists for the selected product and damage level/type."}, status=400)

        # Create a new ProductDamage record for each selected damage type
        for damage_type in damage_types:
            ProductDamage.objects.create(
                product=product,
                damage_level=damage_level,
                damage_type=damage_type,
                estimated_repair_cost=estimated_repair_cost
            )

        # Return a success response
        return JsonResponse({"message": "Damage report added successfully"}, status=200)

    # If the request is GET, render the page with the form
    if not request.session.get("user_id"):
        return HttpResponse("Access Denied", status=403)
    
    user_id = request.session.get("user_id")
    products = Product.objects.filter(supplier=user_id)
    damage_level_choices = ProductDamage.DAMAGE_LEVEL_CHOICES
    damage_type_choices = ProductDamage.DAMAGE_TYPE_CHOICES

    return render(request, 'supplier/add_product_damage.html', {
        'products': products,
        'damage_level_choices': damage_level_choices,
        'damage_type_choices': damage_type_choices
    })

def view_product_damage(request):
    if not request.session.get('user_id'):
        return HttpResponse("Access Denied", status=403)

    user_id = request.session.get("user_id")

    # Get all products added by the supplier
    products = Product.objects.filter(supplier=user_id)
    
    # Get damage reports for those products
    damages = ProductDamage.objects.filter(product__in=products).order_by('-created_at')
    
    return render(request, 'supplier/view_product_damage.html', {
        'damages': damages
    })
# Admin Functions
"""
def admin_index(request):
    if request.session.get("user_type") == "admin":
        farmers = Farmer.objects.all()
        suppliers = Supplier.objects.all()
        delivery_boys = DeliveryBoy.objects.all()
        context = {
            "user_name": request.session.get("user_name"),
            "user_email": request.session.get("user_email"),
            # Add other fields as needed
            "farmers": farmers,
            "suppliers": suppliers,
            "delivery_boys": delivery_boys,
        }
        return render(request, "admin/admin_index.html", context)
    else:
        return render(request, "access_denied.html")
    """


def admin_index(request):
    if not request.session.get("user_id"):
        return redirect("login")

    # Fetch statistics data
    num_farmers = Farmer.objects.count()
    num_suppliers = Supplier.objects.count()
    num_delivery_boys = DeliveryBoy.objects.count()
    num_products = Product.objects.count()
    # overall_sales = Order.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    # profit = overall_sales * 0.2  # Assuming a 20% profit margin for simplicity

    context = {
        "num_farmers": num_farmers,
        "num_suppliers": num_suppliers,
        "num_delivery_boys": num_delivery_boys,
        "num_products": num_products,
        #'overall_sales': overall_sales,
        #'profit': profit,
    }

    return render(request, "admin/admin_index.html", context)


def admin_view_farmer(request):
    if not request.session.get("user_id"):
        return redirect("login")

    farmers = Farmer.objects.all()
    context = {"farmers": farmers}
    return render(request, "admin/admin_view_farmer.html", context)


def admin_view_supplier(request):
    if not request.session.get("user_id"):
        return redirect("login")

    suppliers = Supplier.objects.all()
    context = {"suppliers": suppliers}
    return render(request, "admin/admin_view_supplier.html", context)


"""def admin_view_pro(request):
    if not request.session.get('user_id'):
        return redirect('login')

    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'admin/admin_view_pro.html', context)"""


def admin_view_pro(request):
    if not request.session.get("user_id"):
        return redirect("login")

    products = Product.objects.all()
    context = {"products": products}
    return render(request, "admin/admin_view_pro.html", context)


@csrf_exempt
def toggle_product_status(request, product_id):
    if request.method == "POST":
        try:
            product = Product.objects.get(id=product_id)
            product.is_disabled = not product.is_disabled  # Toggle the status
            product.save()

            return JsonResponse(
                {"status": "success", "new_status": product.is_disabled}
            )
        except Product.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Product not found."})
    return JsonResponse({"status": "error", "message": "Invalid request method."})


def admin_view_cat(request):
    if not request.session.get("user_id"):
        return redirect("login")

    categories = ProductCategory.objects.all()
    context = {"categories": categories}
    return render(request, "admin/admin_view_cat.html", context)


def toggle_category_status(request):
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        category_id = request.GET.get("id")
        action = request.GET.get("action")

        if category_id and action in ["enable", "disable"]:
            category = get_object_or_404(ProductCategory, id=category_id)
            if action == "disable":
                category.is_disabled = True
            elif action == "enable":
                category.is_disabled = False
            category.save()
            new_status = not category.is_disabled
            return JsonResponse({"success": True, "new_status": new_status})

    return JsonResponse({"success": False})


def admin_view_deliveryboy(request):
    if not request.session.get("user_id"):
        return redirect("login")

    delivery_boys = DeliveryBoy.objects.all()
    context = {"delivery_boys": delivery_boys}
    return render(request, "admin/admin_view_deliveryboy.html", context)

def toggle_user_status(request, user_type, user_id):
    # Determine the model based on user_type
    if user_type == "farmer":
        model = Farmer
    elif user_type == "supplier":
        model = Supplier
    elif user_type == "deliveryboy":
        model = DeliveryBoy
    else:
        return JsonResponse({"error": "Invalid user type"}, status=400)

    # Fetch the user object
    user = get_object_or_404(model, id=user_id)

    # Toggle status
    if user.status == "active":
        user.status = "blocked"
        # Send email notification to the user
        send_mail(
            'Account Blocked',
            'Your account has been blocked as you have not been active on our website for 1 year. If you believe this is a mistake, please contact support.',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
    else:
        user.status = "active"

    user.save()

    # Return JSON response with updated status
    return JsonResponse({"status": user.status})
def block_user(request):
    if request.method == "POST":
            data = json.loads(request.body)
            user_type = data.get("user_type")
            user_id = data.get("user_id")
            reason = data.get("reason")

            if user_type == "farmer":
                model = Farmer
            elif user_type == "supplier":
                model = Supplier
            elif user_type == "deliveryboy":
                model = DeliveryBoy
            else:
                return JsonResponse({'success': False, 'message': 'Invalid user type'})

            try:
                user = model.objects.get(id=user_id)
                user.status = 'blocked'
                user.reasontoblock = reason
                user.save()


                send_mail(
                    'Account Blocked',
                    f'Your account has been blocked for the following reason: {reason}. If you believe this is a mistake, please contact support.',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )

                return JsonResponse({'success': True})
            except model.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'User not found'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


'''def toggle_user_status(request, user_type, user_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            reason = data.get('reason')
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON")

        if not reason:
            return JsonResponse({"error": "Reason is required"}, status=400)

        if user_type == "farmer":
            model = Farmer
        elif user_type == "supplier":
            model = Supplier
        elif user_type == "deliveryboy":
            model = DeliveryBoy
        else:
            return JsonResponse({"error": "Invalid user type"}, status=400)

        user = get_object_or_404(model, id=user_id)

        if user.status == "active":
            user.status = "blocked"
            # Send email with reason
            send_mail(
                'Account Blocked',
                f'Your account has been blocked due to the following reason: {reason}',
                'admin@agrorenthub.com',
                [user.email],
                fail_silently=False,
            )
        else:
            user.status = "active"

        user.save()
        return JsonResponse({"status": user.status})'''
"""def admin_view_worker(request):
    if not request.session.get('user_id'):
        return redirect('login')

    # Logic to retrieve and display worker information
    workers = Worker.objects.all()
    context = {
        'workers': workers
    }
    return render(request, 'admin/admin_view_worker.html', context)

"""
"""def admin_view_order(request):
    if not request.session.get('user_id'):
        return redirect('login')

    orders = Order.objects.select_related('user', 'product').all()  # Ensure related fields are fetched
    context = {
        'orders': orders
    }
    return render(request, 'admin/admin_view_order.html', context)"""


def admin_view_order(request):
    if not request.session.get("user_id"):
        return redirect("login")

    orders = Order.objects.all()
    delivery_boys = DeliveryBoy.objects.all()

    context = {
        "orders": orders,
        "delivery_boys": delivery_boys,
    }
    return render(request, "admin/admin_view_order.html", context)


"""@csrf_exempt
def assign_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        order_id = data.get('order_id')
        delivery_boy_id = data.get('delivery_boy')

        order = get_object_or_404(Order, id=order_id)
        delivery_boy = get_object_or_404(DeliveryBoy, id=delivery_boy_id)

        # Check if the delivery boy has no conflicting orders except for the same user and supplier
        conflicting_orders = Order.objects.filter(
            delivery_boy=delivery_boy,
            start_date__lte=order.end_date,
            end_date__gte=order.start_date
        ).exclude(
            user=order.user,
            product__supplier=order.product.supplier
        )

        if not conflicting_orders.exists():
            order.delivery_boy = delivery_boy
            order.save()
            return JsonResponse({'status': 'success'})

        return JsonResponse({'status': 'error', 'message': 'Delivery boy has conflicting orders.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@csrf_exempt
def cancel_assignment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        order_id = data.get('order_id')

        try:
            order = Order.objects.get(id=order_id)
            order.delivery_boy = None
            order.save()

            return JsonResponse({'status': 'success'})
        except Order.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Order not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
"""


@csrf_exempt
def assign_order_page(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Filter only active delivery boys
    available_delivery_boys = DeliveryBoy.objects.filter(status="active")

    for delivery_boy in available_delivery_boys:
        conflicting_orders = Order.objects.filter(
            delivery_boy=delivery_boy,
            start_date__lte=order.end_date,
            end_date__gte=order.start_date,
        ).exclude(user=order.user, product__supplier=order.product.supplier)

        if (
            not conflicting_orders.exists()
            or conflicting_orders.filter(
                user=order.user, product__supplier=order.product.supplier
            ).exists()
        ):
            delivery_boy.availability = "Available"
        else:
            delivery_boy.availability = "Not Available"

    return render(
        request,
        "admin/assign_order.html",
        {
            "order": order,
            "delivery_boys": available_delivery_boys,
        },
    )


@csrf_exempt
def assign_order(request):
    if request.method == "POST":
        data = json.loads(request.body)
        order_id = data.get("order_id")
        delivery_boy_id = data.get("delivery_boy")

        order = get_object_or_404(Order, id=order_id)
        delivery_boy = get_object_or_404(DeliveryBoy, id=delivery_boy_id)

        conflicting_orders = Order.objects.filter(
            delivery_boy=delivery_boy,
            start_date__lte=order.end_date,
            end_date__gte=order.start_date,
        ).exclude(user=order.user, product__supplier=order.product.supplier)

        if (
            not conflicting_orders.exists()
            or conflicting_orders.filter(
                user=order.user, product__supplier=order.product.supplier
            ).exists()
        ):
            order.delivery_boy = delivery_boy
            order.save()
            return JsonResponse(
                {
                    "status": "success",
                    "delivery_boy_name": delivery_boy.name,
                    "redirect_url": reverse("admin_view_order"),
                }
            )

        return JsonResponse(
            {"status": "error", "message": "Delivery boy has conflicting orders."}
        )
    return JsonResponse({"status": "error", "message": "Invalid request method."})


@csrf_exempt
def cancel_assignment(request):
    if request.method == "POST":
        data = json.loads(request.body)
        order_id = data.get("order_id")

        try:
            order = Order.objects.get(id=order_id)
            order.delivery_boy = None

            # Update the status fields
            order.delivery_status = 'pending'
            order.shipping_status = 'pending'
            order.status = 'pending'
            
            order.save()

            return JsonResponse(
                {"status": "success", "redirect_url": reverse("admin_view_order")}
            )
        except Order.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Order not found"})
    return JsonResponse({"status": "error", "message": "Invalid request method"})


def admin_view_damagedpro(request):
    if not request.session.get("user_id"):
        return redirect("login")

    # Fetch all return requests
    return_requests = ReturnRequest.objects.all()

    context = {
        'return_requests': return_requests,
    }
    return render(request, 'admin/admin_view_damagedpro.html', context)


def deliveryboy_index(request):
    if request.session.get("user_type") == "delivery_boy":
        user_id = request.session.get("user_id")
        user = DeliveryBoy.objects.get(id=user_id)
        context = {
            "user_name": user.name,
            "user_email": user.email,
            # Add other fields as needed
        }
        return render(request, "deliveryboy/deliveryboy_index.html", context)
    else:
        return render(request, "access_denied.html")


def deliveryboy_profile(request):
    # Check if the user is authenticated
    if not request.session.get("user_id"):
        # messages.error(request, "You need to log in to access this page.")
        return redirect("login")

    user_id = request.session["user_id"]

    # Retrieve the DeliveryBoy object
    try:
        deliveryboy = DeliveryBoy.objects.get(id=user_id)
    except DeliveryBoy.DoesNotExist:
        messages.error(request, "Delivery Boy not found.")
        return redirect("login")

    # Pass the DeliveryBoy object to the template
    context = {
        "deliveryboy": deliveryboy,
    }

    return render(request, "deliveryboy/deliveryboy_profile.html", context)


def deliveryboy_edit_details(request):
    if request.method == "POST":
        user_id = request.session.get("user_id")

        deliveryboy = get_object_or_404(DeliveryBoy, id=user_id)

        deliveryboy.name = request.POST.get("name", deliveryboy.name)
        deliveryboy.address = request.POST.get("address", deliveryboy.address)
        deliveryboy.phone = request.POST.get("phone", deliveryboy.phone)

        deliveryboy.save()

        return redirect("deliveryboy_profile")

    else:
        return redirect(
            "deliveryboy_index"
        )  # Redirect to a default page if method is not POST


def deliveryboy_change_password(request):
    if request.method == "POST":
        deliveryboy = DeliveryBoy.objects.get(id=request.session["user_id"])
        current_password = request.POST["current-password"]
        if deliveryboy.password == current_password:
            new_password = request.POST["password"]
            confirm_password = request.POST["confirm_password"]
            if new_password == confirm_password:
                deliveryboy.password = new_password
                deliveryboy.save()
                return redirect("deliveryboy/deliveryboy_profile")

    return redirect("deliveryboy/deliveryboy_profile")


def deliveryboy_view_order(request):
    if not request.session.get("user_id"):
        return redirect("login")

    user_id = request.session["user_id"]

    # Retrieve the DeliveryBoy object
    try:
        delivery_boy = DeliveryBoy.objects.get(id=user_id)
    except DeliveryBoy.DoesNotExist:
        return redirect("login")  # Replace 'login' with the name of your login URL

    orders = Order.objects.filter(delivery_boy=delivery_boy)
    context = {"orders": orders}
    return render(request, "deliveryboy/deliveryboy_view_order.html", context)


@csrf_exempt
def ship_order(request):
    if request.method == "POST":
        data = json.loads(request.body)
        order_id = data.get("order_id")

        try:
            order = Order.objects.get(id=order_id)
            order.shipping_status = "shipped"
            order.save()
            return JsonResponse({"status": "success"})
        except Order.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Order not found"})
    return JsonResponse({"status": "error", "message": "Invalid request method"})


def generate_otp_delivery(request):
    if request.method == "POST":
        data = json.loads(request.body)
        order_id = data.get("order_id")
        order = get_object_or_404(Order, id=order_id)

        # Generate OTP
        otp = "".join(random.choices(string.digits, k=6))

        # Save OTP to the order (or a separate OTP model)
        order.otp = otp
        order.save()

        # Send OTP via email
        send_mail(
            "Your OTP for Order Delivery",
            f"Your OTP is {otp}.",
            settings.DEFAULT_FROM_EMAIL,
            [order.user.email],
        )
        return JsonResponse(
            {"status": "success", "message": "OTP sent to customer email."}
        )

    return JsonResponse({"status": "error", "message": "Invalid request method."})


def verify_otp_delivery(request):
    if request.method == "POST":
        data = json.loads(request.body)
        order_id = data.get("order_id")
        otp_entered = data.get("otp")
        order = get_object_or_404(Order, id=order_id)

        if order.otp == otp_entered:
            order.delivery_status = "delivered"
            order.save()
            return JsonResponse(
                {"status": "success", "message": "Order marked as delivered."}
            )
        else:
            return JsonResponse({"status": "error", "message": "Incorrect OTP."})

    return JsonResponse({"status": "error", "message": "Invalid request method."})


def deliveryboy_view_damages(request):
    if not request.session.get("user_id"):
        return redirect("login")

    # Fetching all products with damage reports
    damaged_products = ProductDamage.objects.all()

    context = {
        'damaged_products': damaged_products,
    }
    return render(request, "deliveryboy/deliveryboy_view_damages.html", context)
'''def deliveryboy_view_damages_chart(request):
    if not request.session.get("user_id"):
        return redirect("login")

    user_id = request.session["user_id"]
    delivery_boy = DeliveryBoy.objects.get(id=user_id)

    # Fetching all products with damage reports
    damaged_products = ProductDamage.objects.all()

    # Prepare data for chart
    labels = [damage.product.product_name for damage in damaged_products]
    data = [damage.estimated_repair_cost for damage in damaged_products]

    context = {
        'labels': labels,
        'data': data,
    }
    return render(request, "deliveryboy/deliveryboy_view_damages_chart.html", context)'''
def deliveryboy_view_damages_chart(request):
    if not request.session.get("user_id"):
        return redirect("login")

    user_id = request.session["user_id"]
    delivery_boy = DeliveryBoy.objects.get(id=user_id)

    # Fetching all products with damage reports
    damaged_products = ProductDamage.objects.all()

    # Apply filters if provided
    selected_product = request.GET.get('product')
    selected_damage_level = request.GET.get('damage_level')
    selected_damage_type = request.GET.get('damage_type')

    if selected_product:
        damaged_products = damaged_products.filter(product__id=selected_product)
    if selected_damage_level:
        damaged_products = damaged_products.filter(damage_level=selected_damage_level)
    if selected_damage_type:
        damaged_products = damaged_products.filter(damage_type=selected_damage_type)

    # Pagination
    damaged_products = damaged_products.order_by('product__product_name')
    paginator = Paginator(damaged_products, 10)  # Show 10 damages per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Fetch distinct values for dropdowns
    products = Product.objects.all().values_list('id', 'product_name').distinct()
    damage_levels = ProductDamage.DAMAGE_LEVEL_CHOICES
    damage_types = ProductDamage.DAMAGE_TYPE_CHOICES

    context = {
        'page_obj': page_obj,
        'products': products,
        'damage_levels': damage_levels,
        'damage_types': damage_types,
        'selected_product': selected_product,
        'selected_damage_level': selected_damage_level,
        'selected_damage_type': selected_damage_type,
    }
    return render(request, "deliveryboy/deliveryboy_view_damages_chart.html", context)




'''
def return_product(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        customer_name = order.user.name
        product_name = order.product.product_name
        quantity = order.quantity
        damage_level = request.POST.get('damage_level')
        damage_type = request.POST.get('damage_type')
        damage_photos = request.FILES.get('damage_photos')
        estimated_repair_cost = request.POST.get('estimated_repair_cost')

        ReturnRequest.objects.create(
            order=order,
            customer_name=customer_name,
            product_name=product_name,
            quantity=quantity,
            damage_level=damage_level,
            damage_type=damage_type,
            damage_photos=damage_photos,
            estimated_repair_cost=estimated_repair_cost
        )

        # Change order status or any other business logic
        order.delivery_status = 'collected'
        order.save()

        return redirect('deliveryboy_view_order')

    return render(request, 'deliveryboy/return_product.html', {'order': order})
'''
'''def return_product(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        customer_name = request.POST['customer_name']
        product_name = request.POST['product_name']
        quantity = request.POST['quantity']
        damage_level = request.POST['damage_level']
        damage_type = request.POST['damage_type']
        #damage_photos = request.FILES.get('damage_photos')
        estimated_repair_cost = request.POST['estimated_repair_cost']

        # Create a new ReturnRequest object and save it to the database
        return_request = ReturnRequest.objects.create(
            order=order,
            customer_name=customer_name,
            product_name=product_name,
            quantity=quantity,
            damage_level=damage_level,
            damage_type=damage_type,
           # damage_photos=damage_photos,
            estimated_repair_cost=estimated_repair_cost,
        )

        return render('deliveryboy_return_management')

    return render(request, 'deliveryboy/return_product.html', {'order': order})


@csrf_exempt
def process_return(request, order_id):
    if request.method == 'POST':
        action = request.GET.get('action')

        order = get_object_or_404(Order, id=order_id)

        if action == 'no_damages':
            order.status = 'collected'
            order.save()
            return JsonResponse({'status': 'collected'})

    return JsonResponse({'status': 'error'})

def get_estimated_repair_cost(request):
    product_name = request.GET.get('product_name')
    damage_level = request.GET.get('damage_level')
    damage_type = request.GET.get('damage_type')

    # Fetch the estimated repair cost based on the criteria
    try:
        damage_report = ProductDamage.objects.get(
            product__product_name=product_name,
            damage_level=damage_level,
            damage_type=damage_type
        )
        estimated_repair_cost = damage_report.estimated_repair_cost
    except ProductDamage.DoesNotExist:
        estimated_repair_cost = 0.0  # Default value if no matching record is found

    return JsonResponse({'estimated_repair_cost': estimated_repair_cost})
'''

def deliveryboy_return_management(request):
    if not request.session.get("user_id"):
        return redirect("login")

    user_id = request.session["user_id"]

    try:
        delivery_boy = DeliveryBoy.objects.get(id=user_id)
    except DeliveryBoy.DoesNotExist:
        return redirect("login")  # Replace 'login' with your login URL

    # Get orders delivered by this delivery boy
    delivered_orders = Order.objects.filter(delivery_status='delivered', delivery_boy=delivery_boy)
    
    context = {
        'orders': delivered_orders
    }
    return render(request, "deliveryboy/deliveryboy_return_management.html", context)

# Return Product View
def return_product(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        customer_name = request.POST['customer_name']
        product_name = request.POST['product_name']
        quantity = request.POST['quantity']
        damage_level = request.POST['damage_level']
        damage_type = request.POST['damage_type']
        estimated_repair_cost = request.POST['estimated_repair_cost']
        total_repair_cost = request.POST['total_repair_cost']
        razorpay_payment_id = request.POST.get('razorpay_payment_id', '')
        
        # Create a new ReturnRequest object
        ReturnRequest.objects.create(
            order=order,
            customer_name=customer_name,
            product_name=product_name,
            quantity=quantity,
            damage_level=damage_level,
            damage_type=damage_type,
            estimated_repair_cost=estimated_repair_cost,
            total_repair_cost=total_repair_cost,
            razorpay_payment_id=razorpay_payment_id,
        )

        # Redirect to the payment processing view
        return redirect('process_return_payment', order_id=order.id)

    return render(request, 'deliveryboy/return_product.html', {'order': order})

# Payment Processing View
def process_return_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    # Replace this with actual payment verification logic
    payment_successful = check_payment_status()
    
    if payment_successful:
        # Update the order status to 'collected'
        order.status = 'collected'
        order.save()
        
        # Update the product stock quantity
        product = order.product
        product.stock_quantity += order.quantity  # Add the quantity of the returned product
        product.save()
        
        return redirect('deliveryboy_return_management')  # Redirect back to the management page
    else:
        return HttpResponse("Payment failed. Please try again.")

def check_payment_status():
    # Replace this with your payment verification logic (e.g., Razorpay or another payment gateway)
    return True  # Placeholder for successful payment


@csrf_exempt
def process_return(request, order_id):
    if request.method == 'POST':
        action = request.GET.get('action')
        order = get_object_or_404(Order, id=order_id)
        
        if action == 'no_damages':
            # Update the order status to 'collected'
            order.status = 'collected'
            order.save()
            
            # Update the product stock quantity
            product = order.product
            product.stock_quantity += order.quantity  # Add the quantity of the returned product
            product.save()
            
            return JsonResponse({'status': 'collected'})
    
    return JsonResponse({'status': 'error'})


def get_estimated_repair_cost(request):
    product_name = request.GET.get('product_name')
    damage_level = request.GET.get('damage_level')
    damage_type = request.GET.get('damage_type')

    try:
        damage_report = ProductDamage.objects.get(
            product__product_name=product_name,
            damage_level=damage_level,
            damage_type=damage_type
        )
        estimated_repair_cost = damage_report.estimated_repair_cost
    except ProductDamage.DoesNotExist:
        estimated_repair_cost = 0.0

    return JsonResponse({'estimated_repair_cost': estimated_repair_cost})


def deliveryboy_deliveries(request):
    return render(request, "deliveryboy/deliveryboy_deliveries.html")


def deliveryboy_earnings(request):
    return render(request, "deliveryboy/deliveryboy_earnings.html")


def deliveryboy_support(request):
    return render(request, "deliveryboy/deliveryboy_support.html")
