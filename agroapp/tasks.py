from celery import shared_task
from django.utils import timezone
from agroapp.models import CartItem

@shared_task
def remove_expired_cart_items():
    now = timezone.now()
    expired_items = CartItem.objects.filter(start_date__lt=now)
    count, _ = expired_items.delete()
    return f'Deleted {count} expired cart items'
