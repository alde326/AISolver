# utils.py

import re
from fuzzywuzzy import process, fuzz
import unidecode

# Diccionario de sinónimos
SYNONYMS = {
    "Emperor Palpatine": "Emperador Palpatine",
}

# Función para normalizar los nombres antes de hacer el fuzzy match
def normalize_name(name):
    # Normalizar para eliminar acentos y convertir a minúsculas
    return unidecode.unidecode(name).lower()

# Función para hacer fuzzy matching con ajustes
def fuzzy_match(nombre, opciones, umbral=80):
    # Normalizar el nombre de entrada
    nombre_normalizado = normalize_name(nombre)
    
    # Normalizar todas las opciones
    opciones_normalizadas = [normalize_name(opcion) for opcion in opciones]
    
    # Realizar el fuzzy matching con el mejor algoritmo
    mejor, score = process.extractOne(nombre_normalizado, opciones_normalizadas, scorer=fuzz.token_sort_ratio)
    
    # Si el score es mayor o igual al umbral, devolver la mejor coincidencia
    if score >= umbral:
        return opciones[opciones_normalizadas.index(mejor)]
    else:
        print(f"No se encontró una coincidencia aceptable para {nombre}")
        return None


# Función para extraer nombres de objetos de una fórmula
def extraer_nombres_objetos(formula):
    return list(set(re.findall(r'"([^"]+)"\.', formula)))

# Función para transformar la fórmula
def transformar_formula(formula):
    return re.sub(r'"([^"]+)"\.(\w+)', r'objects["\1"].\2', formula)

# Clase Wrapper para convertir datos en atributos de objeto
class Wrapper:
    def __init__(self, raw):
        for k, v in raw.items():
            if isinstance(v, str) and v.replace('.', '', 1).isdigit():
                try:
                    self.__dict__[k.lower()] = float(v)
                except:
                    self.__dict__[k.lower()] = v
            else:
                self.__dict__[k.lower()] = v

