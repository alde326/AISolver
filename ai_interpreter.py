# ai_interpreter.py

import requests
from constants import HEADERS

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
                    "- Usa la notación \"nombre\".atributo, como \"Luke Skywalker\".mass o \"Vulpix\".weight.\n"
                    "- **Asegúrate de que el orden de los objetos sea el correcto**: la fórmula debe seguir la estructura **propiedad del primer objeto / propiedad del segundo objeto**. \n"
                    "- Usa paréntesis para asegurar el orden correcto de operaciones.\n"
                    "- **No pongas la fórmula entre comillas, ni simples ni dobles.**\n"
                    "- **Evita cualquier notación de LaTeX** como '\\frac{}', y usa la notación estándar de Python.\n"
                    "- Identifica solo las propiedades válidas de cada tipo:\n"
                    "  • StarWarsPlanet: rotation_period, orbital_period, diameter, surface_water, population\n"
                    "  • StarWarsCharacter: height, mass\n"
                    "  • Pokemon: base_experience, height, weight\n"
                )
            },
            {"role": "user", "content": enunciado}
        ]
    }

    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code == 200:
        formula = response.json()["choices"][0]["message"]["content"].strip()
        return formula
    print("❌ Error usando la IA:", response.text)
    return None
