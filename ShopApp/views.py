from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from ShopApp.models import Game, Cart, CartItem
import json
def index(request):
    return render(request, 'index.html')

def main_window(request):
    games = Game.objects.all()
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None

    cart_queryset = Cart.objects.filter(user=user)
    cart = cart_queryset.first()

    cart_items_ids = []
    if cart:
        for item in cart.items.all():
            cart_items_ids.append(item.game.id)
    context = {"games": games,
               "cart_items_ids": cart_items_ids,}
    return render(request, "partials/main.html", context)

def cart_view(request):
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    cart_queryset = Cart.objects.filter(user=user)
    cart = cart_queryset.first()
    context = {"cart": cart,
               "items": cart.items.all() if cart else [],}
    return render(request, "partials/cart.html", context)

def about(request):
    return render(request, "partials/about.html")
def catalog(request):
    return render(request, "partials/catalog.html")
def contacts(request):
    return render(request, "partials/contacts.html")

def remove_from_cart(request):
    if request.method == "DELETE":
        body = json.loads(request.body)
        game_id = body.get("game_id")
        game = get_object_or_404(Game, pk=game_id)

        cart = Cart.objects.filter(user=request.user, session_key=request.session.session_key).first()
        if not cart:
            return JsonResponse({"error": "Корзина не найдена"}, status=404)
        cart_item = CartItem.objects.filter(cart=cart, game=game).first()
        if cart_item:
            cart_item.delete()
            updated_cart_items = CartItem.objects.filter(cart=cart)
            cart_data = [
                {
                    "game_id": item.game.id,
                    "game_name": item.game.name,
                    "game_price": item.game.price,
                    "remove_url": reverse('remove_from_cart'),
                }
                for item in updated_cart_items
            ]
            return JsonResponse({"message": "Игра успешно удалена из корзины", "cart_items": cart_data})
        return JsonResponse({"error": "Игра не найдена в корзине"}, status=404)

    return JsonResponse({"error": "Недопустимый метод запроса"}, status=400)

def add_to_cart(request):
    game_id = request.POST.get("game_id")
    game = get_object_or_404(Game, pk=game_id)

    cart, created = Cart.objects.get_or_create(user=request.user, session_key=request.session.session_key)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, game=game)

    if created:
        message = "Игра успешно добавлена в корзину"
    else:
        message = "Игра уже есть в корзине"

    return JsonResponse({"message": message})

