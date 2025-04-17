import requests
import time
import re
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Token de acceso
TOKEN = "Bearer a31b6ff5-7941-4fbc-84d5-63f5c7146f3b"
HEADERS = {"Authorization": TOKEN}

# --- Obtener listas de nombres posibles ---
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

# --- Fuzzy Match ---
def fuzzy_match(nombre, opciones):
    mejor, score = process.extractOne(nombre, opciones)
    if score > 80:
        return mejor
    return None

# --- Obtener datos desde PokéAPI ---
def fetch_pokemon_data(name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

# --- Obtener datos desde SWAPI ---
def fetch_starwars_people(name):
    base_url = "https://swapi.py4e.com/api/people/?search="
    url = f"{base_url}{name.lower()}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            results = response.json().get("results", [])
            if results:
                return results[0]
    except:
        pass
    return None

def fetch_starwars_planets(name):
    base_url = "https://swapi.py4e.com/api/planets/?search="
    url = f"{base_url}{name.lower()}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            results = response.json().get("results", [])
            if results:
                return results[0]
    except:
        pass
    return None

# --- IA: Convertir enunciado a fórmula ---
def interpretar_enunciado_con_ia(enunciado):
    url = "https://recruiting.adere.so/chat_completion"
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "developer",
                "content": (
                    "Convierte el siguiente enunciado en una fórmula matemática usando notación punto.\n"
                    "- **Usa exactamente los mismos nombres de los personajes, Pokémon y planetas tal como aparecen en el enunciado original**, sin traducirlos, corregirlos, ni cambiarlos. Deben ir entre **comillas dobles** (\" \").\n"
                    "- Usa la notación '\"nombre\".atributo', como '\"Luke Skywalker\".mass' o '\"Vulpix\".weight'.\n"
                    "- Usa paréntesis para asegurar el orden correcto de operaciones.\n"
                    "- Identifica solo las propiedades válidas de cada tipo:\n"
                    "  • StarWarsPlanet: rotation_period, orbital_period, diameter, surface_water, population\n"
                    "  • StarWarsCharacter: height, mass\n"
                    "  • Pokemon: base_experience, height, weight\n"
                    "- No expliques nada, no inventes nombres ni traduzcas.\n"
                )
            },
            {"role": "user", "content": enunciado}
        ]
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        print("❌ Error usando la IA:", response.text)
        return None

# --- Clase normalizadora ---
class Wrapper:
    def __init__(self, raw):
        for k, v in raw.items():
            try:
                self.__dict__[k.lower()] = float(v)
            except:
                self.__dict__[k.lower()] = v

# --- Extraer nombres desde fórmula ---
def extraer_nombres_objetos(formula):
    return list(set(re.findall(r'"([^"]+)"\.', formula)))

# --- Transformar fórmula para evaluación ---
def transformar_formula(formula):
    return re.sub(r'"([^"]+)"\.(\w+)', r'objects["\1"].\2', formula)

# --- Resolver un problema ---
def resolver_problema(problem, nombres_pokemon, nombres_starwars, nombres_planetas):
    problem_id = problem["id"]
    description = problem["problem"]

    print(f"\n🧩 Problema: {description}")
    formula = interpretar_enunciado_con_ia(description)
    if not formula:
        return None, problem_id

    print(f"📐 Fórmula generada: {formula}")
    print(f"📐 Fórmula esperada: {problem.get('expression', 'desconocida')}" )

    objetos = extraer_nombres_objetos(formula)
    print(f"🔍 Objetos detectados: {objetos}")

    data = {}
    for name in objetos:
        datos = fetch_pokemon_data(name)
        if not datos:
            datos = fetch_starwars_people(name)
        if not datos:
            datos = fetch_starwars_planets(name)

        # Si aún no se encuentran, aplicar fuzzy matching
        if not datos:
            sugerencia = fuzzy_match(name, nombres_pokemon)
            if sugerencia:
                datos = fetch_pokemon_data(sugerencia)

        if not datos:
            sugerencia = fuzzy_match(name, nombres_starwars)
            if sugerencia:
                datos = fetch_starwars_people(sugerencia)

        if not datos:
            sugerencia = fuzzy_match(name, nombres_planetas)
            if sugerencia:
                datos = fetch_starwars_planets(sugerencia)

        if not datos:
            print(f"❌ No se pudo encontrar datos para: {name}")
            return None, problem_id

        data[name] = Wrapper(datos)

    try:
        formula_transformada = transformar_formula(formula)
        resultado = eval(formula_transformada, {"objects": data})
        resultado = round(resultado, 10)
        print(f"✅ Resultado: {resultado}")
        return resultado, problem_id
    except Exception as e:
        print("❌ Error al evaluar la fórmula:", e)
        return None, problem_id

# --- Flujo principal ---
def correr_prueba(real=False):
    url_start = "" if real else "https://recruiting.adere.so/challenge/test"
    url_solution = "https://recruiting.adere.so/challenge/solution"

    response = requests.get(url_start, headers=HEADERS)
    if response.status_code != 200:
        print("❌ No se pudo iniciar el desafío:", response.text)
        return

    problem = response.json()
    tiempo_limite = time.time() + (180 if real else 9999)

    # Precarga para fuzzy matching
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

# --- Iniciar ---
if __name__ == "__main__":
    correr_prueba(real=False)
