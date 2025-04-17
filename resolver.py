# resolver.py

from ai_interpreter import interpretar_enunciado_con_ia
from data_fetchers import (
    fetch_pokemon_data,
    fetch_starwars_people,
    fetch_starwars_planets
)
from utils import fuzzy_match, extraer_nombres_objetos, transformar_formula, Wrapper

def resolver_problema(problem, nombres_pokemon, nombres_starwars, nombres_planetas):
    problem_id = problem["id"]
    description = problem["problem"]

    print(f"\n🧩 Problema: {description}")
    formula = interpretar_enunciado_con_ia(description)
    if not formula:
        return None, problem_id

    print(f"📐 Fórmula generada: {formula}")
    print(f"📐 Fórmula esperada: {problem.get('expression', 'desconocida')}")
    objetos = extraer_nombres_objetos(formula)
    print(f"🧸 Objetos detectados: {objetos}")

    data = {}
    for name in objetos:
        datos = fetch_pokemon_data(name) or fetch_starwars_people(name) or fetch_starwars_planets(name)

        if not datos:
            datos = (
                fetch_pokemon_data(fuzzy_match(name, nombres_pokemon)) or
                fetch_starwars_people(fuzzy_match(name, nombres_starwars)) or
                fetch_starwars_planets(fuzzy_match(name, nombres_planetas))
            )

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
