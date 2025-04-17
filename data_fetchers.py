# data_fetchers.py

import requests

def obtener_todos_los_nombres_pokemon():
    url = "https://pokeapi.co/api/v2/pokemon?limit=10000"
    response = requests.get(url)
    if response.status_code == 200:
        return [p["name"] for p in response.json()["results"]]
    return []

def obtener_todos_los_personajes_swapi():
    nombres = []
    url = "https://swapi.py4e.com/api/people/"
    while url:
        response = requests.get(url)
        if response.status_code != 200:
            break
        data = response.json()
        nombres.extend([person["name"] for person in data["results"]])
        url = data["next"]
    return nombres

def obtener_todos_los_planetas_swapi():
    nombres = []
    url = "https://swapi.py4e.com/api/planets/"
    while url:
        response = requests.get(url)
        if response.status_code != 200:
            break
        data = response.json()
        nombres.extend([planet["name"] for planet in data["results"]])
        url = data["next"]
    return nombres

def fetch_pokemon_data(name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def fetch_starwars_people(name):
    url = f"https://swapi.py4e.com/api/people/?search={name.lower()}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            results = response.json().get("results", [])
            return results[0] if results else None
    except:
        pass
    return None

def fetch_starwars_planets(name):
    url = f"https://swapi.py4e.com/api/planets/?search={name.lower()}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            results = response.json().get("results", [])
            return results[0] if results else None
    except:
        pass
    return None
