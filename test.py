import requests

def obtener_problema():
    url = "https://recruiting.adere.so/challenge/test"
    headers = {
        "Authorization": "Bearer a31b6ff5-7941-4fbc-84d5-63f5c7146f3b"
    }
    response = requests.get(url, headers=headers)
    
    # Imprimir la respuesta completa para ver cómo está estructurada
    problema = response.json()
    print(problema)  # Aquí puedes ver todo el JSON que se devuelve
    
    return problema

if __name__ == "__main__":
    obtener_problema() 