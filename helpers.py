import os
import requests

from flask import redirect, session
from functools import wraps


def login_required(f):

    # Login required function
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def get_game_description(name):

    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        url = f"https://api.rawg.io/api/games/{name}?key={api_key}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        return response.json()
    except (KeyError, TypeError, ValueError):
        return None


def search_game(name):

    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        url = f"https://api.rawg.io/api/games?key={api_key}&search={name}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        return response.json()
    except (KeyError, TypeError, ValueError):
        return None


def get_game_screenshots(name):

    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        url = f"https://api.rawg.io/api/games/{name}/screenshots?key={api_key}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        return response.json()
    except (KeyError, TypeError, ValueError):
        return None
