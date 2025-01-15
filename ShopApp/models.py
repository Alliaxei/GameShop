from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.conf import settings

class Game(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    release_date = models.DateTimeField(blank=False, null=False)
    price = models.IntegerField(blank=True, null=True)
    genre = models.CharField(max_length=255, blank=False, null=False)
    metacritic = models.CharField(max_length=255, blank=True, null=True)
    playtime = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='games_images/', blank=True, null=True)

class Screenshot(models.Model):
    game = models.ForeignKey(Game, related_name='screenshots', on_delete=models.CASCADE)
    url = models.URLField(blank=False, null=False)

class Cart(models.Model):
    user = models.ForeignKey(
       User,
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    session_key = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_price(self):
        sum = 0
        for item in self.items.all():
            sum +=item.price
        return sum

    def total_items(self):
        return sum(item.quantity for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(
                Cart,
                on_delete=models.CASCADE,
                related_name='items')
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.game.price * self.quantity