import os
from dotenv import load_dotenv

load_dotenv()


def get_token():
    return os.getenv('TOKEN')


def get_steam_key():
    return os.getenv('STEAM_API_KEY')


def get_google():
    return os.getenv('GOOGLE_API_KEY')


def get_cse():
    return os.getenv('SEARCH_ENGINE_ID')


def get_rezi():
    return os.getenv('REZI_API_KEY')
