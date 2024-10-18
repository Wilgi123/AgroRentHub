from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class Farmer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=255)
    status = models.CharField(max_length=10, default="active")
    last_login = models.DateTimeField(blank=True, null=True)
    reset_password_token = models.CharField(max_length=100, blank=True, null=True)
    token_expiry = models.DateTimeField(blank=True, null=True)
    reasontoblock = models.TextField(blank=True, null=True)

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=255)
    status = models.CharField(max_length=10, default="active")
    last_login = models.DateTimeField(blank=True, null=True)
    reset_password_token = models.CharField(max_length=100, blank=True, null=True)
    token_expiry = models.DateTimeField(blank=True, null=True)
    reasontoblock = models.TextField(blank=True, null=True)

class DeliveryBoy(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=255)
    status = models.CharField(max_length=10, default="active")
    last_login = models.DateTimeField(blank=True, null=True)
    reset_password_token = models.CharField(max_length=100, blank=True, null=True)
    token_expiry = models.DateTimeField(blank=True, null=True)
    reasontoblock = models.TextField(blank=True, null=True)

class ProductCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_disabled = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('rented', 'Rented'),
        ('maintenance', 'Maintenance'),
    ]

    product_name = models.CharField(max_length=255)
    product_image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    product_price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()
    product_description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    is_disabled = models.BooleanField(default=False)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.product_name


class CartItem(models.Model):
    user = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('rented', 'Rented'),
        ('collected', 'Collected'),
    ]

    user = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    ordered_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_id = models.CharField(max_length=255, blank=True, null=True)
    delivery_boy = models.ForeignKey(DeliveryBoy, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    otp = models.CharField(max_length=6, blank=True, null=True)
    
    # New fields
    shipping_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    delivery_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Order {self.id} - {self.user.name}"

# Signal handler to update order status when delivery_status is set to 'delivered'
@receiver(post_save, sender=Order)
def update_order_status(sender, instance, **kwargs):
    if instance.delivery_status == 'delivered' and instance.status == 'pending':
        instance.status = 'rented'
        instance.save()


class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"

class ProductDamage(models.Model):
    DAMAGE_LEVEL_CHOICES = [
        ('minor', 'Minor'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe'),
    ]

    DAMAGE_TYPE_CHOICES = [
        ('physical', 'Physical'),
        ('operational', 'Operational'),
        ('wear_and_tear', 'Wear and Tear'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='damages')
    damage_level = models.CharField(max_length=20, choices=DAMAGE_LEVEL_CHOICES)
    damage_type = models.CharField(max_length=20, choices=DAMAGE_TYPE_CHOICES)
    estimated_repair_cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Damage Report for Product {self.product.product_name} - {self.damage_level} Damage"


class ReturnRequest(models.Model):
    DAMAGE_LEVEL_CHOICES = [
        ('minor', 'Minor'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe'),
    ]

    DAMAGE_TYPE_CHOICES = [
        ('physical', 'Physical'),
        ('operational', 'Operational'),
        ('wear_and_tear', 'Wear and Tear'),
    ]

    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='return_requests')
    customer_name = models.CharField(max_length=100, editable=False)
    product_name = models.CharField(max_length=255, editable=False)
    quantity = models.PositiveIntegerField()
    damage_level = models.CharField(max_length=20, choices=DAMAGE_LEVEL_CHOICES)
    damage_type = models.CharField(max_length=20, choices=DAMAGE_TYPE_CHOICES)
    #damage_photos = models.FileField(upload_to='return_photos/', blank=True, null=True)
    estimated_repair_cost = models.DecimalField(max_digits=10, decimal_places=2)
    total_repair_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)  # Add this line
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Return Request for Order {self.order.id} - {self.damage_level} Damage"