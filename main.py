# main.py

import time
import requests
from constants import HEADERS
from data_fetchers import (
    obtener_todos_los_nombres_pokemon,
    obtener_todos_los_personajes_swapi,
    obtener_todos_los_planetas_swapi
)
from resolver import resolver_problema

def correr_prueba(real=False):
    url_start = "" if real else "https://recruiting.adere.so/challenge/test"
    url_solution = "https://recruiting.adere.so/challenge/solution"

    response = requests.get(url_start, headers=HEADERS)
    if response.status_code != 200:
        print("❌ No se pudo iniciar el desafío:", response.text)
        return

    problem = response.json()
    tiempo_limite = time.time() + (180 if real else 9999)

    print("🔃 Cargando listas para fuzzy matching...")
    nombres_pokemon = obtener_todos_los_nombres_pokemon()
    nombres_starwars = obtener_todos_los_personajes_swapi()
    nombres_planetas = obtener_todos_los_planetas_swapi()
    print("✅ Listas cargadas.")

    while time.time() < tiempo_limite:
        resultado, problem_id = resolver_problema(problem, nombres_pokemon, nombres_starwars, nombres_planetas)
        if resultado is None:
            print("❌ No se pudo resolver el problema.")
            break

        if real:
            payload = {"problem_id": problem_id, "answer": resultado}
            response = requests.post(url_solution, headers=HEADERS, json=payload)
            if response.status_code == 200:
                problem = response.json()
                print("➡️  Siguiente problema recibido.")
            else:
                print("❌ Error al enviar la respuesta:", response.text)
                break
        else:
            print(f"✅ Respuesta esperada: {problem.get('solution', 'desconocida')}")
            break

if __name__ == "__main__":
    correr_prueba(real=False)
