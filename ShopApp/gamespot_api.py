import os
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from platform import release

from django.conf import settings
import requests

from ShopApp.models import Game
from ShopProject.settings import GAME_SPOT_API_KEY

API_URL = 'https://www.gamespot.com/api/games/'

def fetch_save_games(limits=10):
    params = {
        'api_key': settings.GAME_SPOT_API_KEY,
        'limit': limits,
        'format': 'json',
        'filter': 'name:Grand Theft Auto',
    }
    headers = {
        'User-agent' : 'Alexey121-GameShop/1.0 (+https://github.com/Alliaxei)'
    }
    try:
        response = requests.get(API_URL, params=params, headers=headers)
        response.raise_for_status()
        games = response.json().get('results', [])
        for game in games:
            name = game.get('name', 'Unknown')
            description = game.get('description', 'Unknown')
            release_date = game.get('release_date', None)
            genres = game.get('genres', [])
            genre_names = [genre ['name'] for genre in genres]
            genres_str = ', '.join(genre_names)

            image_url = game.get('image', {}).get('original', None)
            if Game.objects.filter(name=name).exists():
                print(f"Игра {name} уже существует в БД")
                continue

            game_instance = Game(
                name=name,
                description=description,
                release_date=release_date or 'Unknown',
                price=0.0,
                publisher='Unknown',
                developer='Unknown',
                genre=genres_str,
            )

            if image_url:
                img_response = requests.get(image_url)
                img_response.raise_for_status()

                image_name = os.path.basename(image_url)
                image_path = os.path.join(settings.MEDIA_ROOT, 'games_images', image_name)

                with open(image_path, 'wb') as img_file:
                    img_file.write(img_response.content)

                game_instance.image = os.path.join('games_images', image_name)  # Путь, который будет храниться в БД

            game_instance.save()
            print(f"Игра '{name}' успешно добавлена.")
    except ValueError as e:
        print(f"JSON decoding failed: {e}")
