import requests
import time
import re

# Token de acceso
TOKEN = "Bearer a31b6ff5-7941-4fbc-84d5-63f5c7146f3b"
HEADERS = {"Authorization": TOKEN}

# --- Obtener datos desde PokéAPI ---
def fetch_pokemon_data(name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"❌ Error al consultar PokéAPI ({name}):", e)
    return None

# --- Obtener datos desde SWAPI ---
def fetch_starwars_people(name):
    # Reemplazamos swapi.dev por el mirror funcional swapi.py4e.com
    base_url = "https://swapi.py4e.com/api/people/?search="
    url = f"{base_url}{name.lower()}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            results = response.json().get("results", [])
            if results:
                return results[0]
    except Exception as e:
        print(f"❌ Error al consultar SWAPI ({name}):", e)
    return None

def fetch_starwars_planets(name):
    # Reemplazamos swapi.dev por el mirror funcional swapi.py4e.com
    base_url = "https://swapi.py4e.com/api/planets/?search="
    url = f"{base_url}{name.lower()}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            results = response.json().get("results", [])
            if results:
                return results[0]
    except Exception as e:
        print(f"❌ Error al consultar SWAPI ({name}):", e)
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
                    "Convierte el enunciado en una fórmula matemática usando notación punto. "
                    "Por ejemplo: luke.mass * vulpix.weight + horsea.weight / spinarak.height"
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

# --- Clase normalizadora para evaluar fórmula ---
class Wrapper:
    def __init__(self, raw):
        for k, v in raw.items():
            try:
                self.__dict__[k.lower()] = float(v)
            except:
                self.__dict__[k.lower()] = v

# --- Detectar nombres de variables desde la fórmula ---
def extraer_nombres_objetos(formula):
    return list(set(re.findall(r'([a-zA-Z_]+)\.', formula)))

# --- Resolver un solo problema ---
def resolver_problema(problem):
    problem_id = problem["id"]
    description = problem["problem"]

    print(f"\n🧩 Problema: {description}")
    formula = interpretar_enunciado_con_ia(description)
    if not formula:
        return None, problem_id

    print(f"📐 Fórmula generada: {formula}")

    objetos = extraer_nombres_objetos(formula)
    print(f"🔍 Objetos detectados: {objetos}")

    data = {}
    for name in objetos:
        datos = fetch_pokemon_data(name)
        if not datos:
            datos = fetch_starwars_people(name)
        if not datos:
            datos = fetch_starwars_planets(name)
        if not datos:
            print(f"❌ No se pudo encontrar datos para: {name}")
            return None, problem_id
        data[name] = Wrapper(datos)

    try:
        resultado = eval(formula, {}, data)
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

    while time.time() < tiempo_limite:
        resultado, problem_id = resolver_problema(problem)
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