from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import Cart

@receiver(user_logged_out)
def logged_out(sender, request, user, **kwargs):
    session_key = request.session.session_key
    if session_key:
        try:
            cart = Cart.objects.get(session_key=session_key, user=None)
            cart.delete()
        except Cart.DoesNotExist:
            pass

@receiver(user_logged_in)
def logged_in(sender, request, user, **kwargs):
    session_key = request.session.session_key
    Cart.objects.filter(user_id=None).delete()
    if session_key:
        try:
            cart = Cart.objects.get(session_key=session_key)
            if cart.user is None:
                cart.user = user
                cart.save()
            else:
                print(f"Корзина уже привязана к пользователю {cart.user}")
        except Cart.DoesNotExist:
            cart = Cart.objects.filter(user = user).first()
            if cart is None:
                cart = Cart.objects.create(user = user)
                cart.save()