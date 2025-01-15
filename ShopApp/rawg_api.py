import os
import random

import requests
from django.utils.termcolors import background
from .models import *
from django.conf import settings

API_Key = '2450f3356fd74c9db3e7b3d431e390e1'
API_URL = 'https://api.rawg.io/api/games'

def fetch_save_games(limit=10):
    params = {
        'key': API_Key,
        'page_size': limit,
        'platforms': '4',
    }
    headers = {
        'User-Agent': 'Alexey-GameShop/1.0 (+https://github.com/Alliaxei)'
    }
    try:
        response = requests.get(API_URL, params=params, headers=headers)
        response.raise_for_status()
        games = response.json().get('results', [])

        for game in games:
            name = game.get('name')
            if Game.objects.filter(name=name).exists():
                continue
            release_date = game.get('released')
            genres = ', '.join(genre.get('name') for genre in game.get('genres', []))
            background_image = game.get('background_image', None)
            playtime = game.get('playtime')
            metacritic = game.get('metacritic')
            platforms = ', '.join(platf.get('name') for platf in game.get('platform', []))

            game_instance = Game(
                name= name,
                release_date= release_date,
                genre= genres,
                price = random.randint(5, 100),
                metacritic= metacritic,
                playtime= playtime,
                platforms= platforms,
            )
            if background_image:
                try:
                    image_response = requests.get(background_image)
                    image_response.raise_for_status()

                    image_name = os.path.basename(background_image)
                    image_dir = os.path.join(settings.MEDIA_ROOT, 'games_images')
                    os.makedirs(image_dir, exist_ok=True)

                    image_path = os.path.join(image_dir, image_name)

                    with open(image_path, 'wb') as image_file:
                        image_file.write(image_response.content)

                    game_instance.image = f'games_images/{image_name}'
                except requests.RequestException as e:
                    print(f"Error downloading image for '{name}': {e}")
                game_instance.save()
                print(f"Игра '{name}' успешно добавлена.")

                short_screenshots = game.get('short_screenshots', [])
                for screenshot in short_screenshots:
                    url = screenshot.get('image') #Берётся значение по ключу
                    if url:
                        Screenshot.objects.create(game=game_instance, url=url)
    except Exception as e:
        print(e)

def get_url_info():
    params = {
        'key': API_Key,
        'page_size': 1,
    }
    headers = {
        'User-agent': 'Alexey-GameShop/1.0 (+https://github.com/Alliaxei)'
    }
    response = requests.get(API_URL, params=params, headers=headers)
    response.raise_for_status()
    games = response.json()
    print(games)

PLATFORM_URL = 'https://api.rawg.io/api/platforms'
def fetch_platforms():
    params = {
        'key': API_Key,
    }
    try:
        response = requests.get(PLATFORM_URL, params=params)
        response.raise_for_status()
        platforms = response.json().get('results', [])
        for platform in platforms:
            print(f'ID: {platform["id"]} Name: {platform["name"]}')
    except Exception as e:
        print(e)