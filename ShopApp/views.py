from turtledemo.sorting_animate import enable_keys

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from ShopApp.models import Game, Cart, CartItem, Screenshot
from django.db.models import Q

import json
def index(request):
    return render(request, 'index.html')

def get_cart_info(request):
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None

    cart_queryset = Cart.objects.filter(user=user)
    cart = cart_queryset.first()

    cart_items_ids = []
    if cart:
        for cart_item in cart.items.all():
            cart_items_ids.append(cart_item.game.id)
    return cart_items_ids

def main_window(request):
    games = Game.objects.all()
    cart_items_ids = get_cart_info(request)
    context = {"games": games,
               "cart_items_ids": cart_items_ids,
               }
    return render(request, "partials/main.html", context)

def about(request):
    return render(request, "partials/about.html")
def catalog(request):
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
               "cart_items_ids": cart_items_ids,
               }
    return render(request, "partials/catalog.html", context)
def contacts(request):
    return render(request, "partials/contacts.html")

def cart_view(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart = Cart.objects.filter(session_key=session_key).first()

    context = {"cart": cart,
               "items": cart.items.all() if cart else [],}
    return render(request, "partials/cart.html", context)

def remove_from_cart(request):
    if request.method == "DELETE":
        if not request.user.is_authenticated and not request.session.session_key:
            return JsonResponse({"error": "Пользователь не аутентифицирован или сессия не найдена"}, status=401)

        body = json.loads(request.body) # json loads преобразует объект json в объект питон
        game_id = body.get("game_id")
        if not game_id:
            return JsonResponse({"error": "ID игры не предоставлен"}, status=400)
        game = get_object_or_404(Game, pk=game_id)

        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
        else:
            cart = Cart.objects.filter(session_key=request.session.session_key).first()

        if not cart:
            return JsonResponse({"error": "Корзина не найдена"}, status=404)

        cart_item = cart.items.filter(game=game).first()
        if not cart_item:
            return JsonResponse({"error": "Игра не найдена в корзине"}, status=404)
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

    return JsonResponse({"error": "Недопустимый метод запроса"}, status=400)

def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
        cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart

def add_to_cart(request):
    game_id = request.POST.get("game_id")
    game = get_object_or_404(Game, pk=game_id)
    print("Добавление в корзину товара с индексом " + str(game_id))

    cart = get_or_create_cart(request)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, game=game)
    message = "Игра успешно добавлена в корзину" if created else "Игра уже есть в корзине"

    return JsonResponse(
        {"message": message}
    )

def add_to_cart_form(request):
    if request.method == "POST":
        game_id = request.POST.get("game_id")
        game = get_object_or_404(Game, pk=game_id)

        cart = get_or_create_cart(request)
        CartItem.objects.get_or_create(cart=cart, game=game)
        return redirect(reverse("extended_info", args=[game_id]))
    return JsonResponse({"error": "Invalid request method"}, status=400)

def extended_view(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    screenshots = game.screenshots.all()
    cart_items_ids = get_cart_info(request)
    context = {
        "game": game,
        "screenshots": screenshots,
        "cart_items_ids": cart_items_ids,
        }
    return render(request, "partials/extended_info.html", context)

def ajax_search_games(request):
    query = request.GET.get("search", "").strip()
    if query:
        filters = Q()

        filters &= Q(name__istartswith=query)

        games = Game.objects.filter(filters)
    else:
        games = Game.objects.all()

    games_data = [
        {
            'id': game.id,
            'name': game.name,
            'price': game.price,
            'image': game.image.url if game.image else None,
            'in_cart': game.id in request.session.get('cart_items', [])
        }
        for game in games
    ]
    return JsonResponse({"games": games_data})

def apply_filters(request):
    if request.method == "POST":
        try:
            filters = json.loads(request.body)
            price_max = filters.get("price_max")

            games = Game.objects.filter(price__lte=price_max)

            games_data = [
                {
                    "id": game.id,
                    "name": game.name,
                    "price": game.price,
                    "image":game.image.url,
                    "in_cart": game.id in request.session.get("cart_items", []),
                }
                for game in games
            ]
            return JsonResponse({"games": games_data}, status=200)
        except json.decoder.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)