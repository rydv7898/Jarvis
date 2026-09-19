import json
import webbrowser
import os


def load_favorites():

    file_path = os.path.join(
        os.path.dirname(__file__),
        "favorites.json"
    )

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def play_favorite_song():

    favorites = load_favorites()

    song_url = favorites["favorite_song"]

    webbrowser.open(song_url)

    return "Playing your favorite song."


def play_favorite_playlist():

    favorites = load_favorites()

    playlist_url = favorites["favorite_playlist"]

    webbrowser.open(playlist_url)

    return "Playing your favorite playlist."