import requests
import pandas as pd

def fetch_nutrition_data(query="oats", limit=20):
    """Extrae datos de la la API oficial de la USDA."""
    url= "https://api.nal.usda.gov/fdc/v1/foods/search"

    params = {
        "api_key": "DEMO_KEY",
        "query": query,
        "page_size": limit
    }

    print(f"1. Extrayendo {limit} registros para  '{query}'...")
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    foods = data.get('foods', [])

def transform_and_govern_data(raw_foods):
    """Aplica reglas de gobernanza y limpieza usando Pandas."""
    print("2. Transformando y validando los datos...")

    procesados = []
    for item in raw_foods:
        food_data = {
            "id_producto": item.get('fdcId'),
            "nombre": item.get('description'),
            "proteinas_g": 0.0,
            "grasas_g": 0.0,
            "carbohidratos_g": 0.0
        }


    print(f"Extraccion exitosa. Se encontraron {len(foods)} productos./n")

        for item in foods:
            nombre = item.get('description', 'Sin nombre registrado')
            nutrientes = item.get('foodNutrients', [])
            proteina = 'Valor nulo o no reportado'
            for nut in nutrientes:
                if nut.get('nutrientName') == 'Protein':
                    proteina = nut.get('value')
                    break
            print(f"Producto: {nombre}")
            print(f"Proteína cada 100g: {proteina}g")
            print("-" * 30)

    except requests.exceptions.RequestException as e:
        print(f"Error durante la extraccion: {e}")

if __name__ == "__main__":
    fetch_nutrition_data("oats")