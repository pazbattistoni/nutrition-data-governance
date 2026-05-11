import requests
import pandas as pd

def fetch_usda_data(query="oats", limit=20):
    """Extrae datos crudos de la API de USDA."""
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    params = {
        "api_key": "DEMO_KEY", 
        "query": query,
        "pageSize": limit
    }
    
    print(f"1. Extrayendo {limit} registros para '{query}'...")
    response = requests.get(url, params=params)
    response.raise_for_status() 
    return response.json().get('foods', [])

def transform_and_govern_data(raw_foods):
    """Aplica reglas de gobernanza y limpieza usando Pandas."""
    print("2. Iniciando transformación y validación de datos...")
    
    procesados = []
    
    for item in raw_foods:
        marca = item.get('brandOwner', item.get('brandName', 'Genérico / Sin marca'))
        food_data = {
            "id_producto": item.get('fdcId'),
            "marca": marca,
            "nombre": item.get('description'),
            "proteinas_g": 0.0,
            "grasas_g": 0.0,
            "carbohidratos_g": 0.0
        }
        
        for nut in item.get('foodNutrients', []):
            name = nut.get('nutrientName', '').lower()
            if 'protein' in name:
                food_data["proteinas_g"] = nut.get('value', 0.0)
            elif 'total lipid (fat)' in name:
                food_data["grasas_g"] = nut.get('value', 0.0)
            elif 'carbohydrate' in name:
                food_data["carbohidratos_g"] = nut.get('value', 0.0)
                
        procesados.append(food_data)
        
    df = pd.DataFrame(procesados)
    
    total_inicial = len(df)
    
    df = df[(df['proteinas_g'] > 0) | (df['grasas_g'] > 0) | (df['carbohidratos_g'] > 0)]
    
    df['suma_macros'] = df['proteinas_g'] + df['grasas_g'] + df['carbohidratos_g']
    df_limpio = df[df['suma_macros'] <= 100.0].copy()
    df_limpio = df_limpio.drop(columns=['suma_macros'])
    
    total_final = len(df_limpio)
    descartados = total_inicial - total_final
    
    print(f"-> Gobernanza aplicada: Se descartaron {descartados} registros corruptos o incompletos.")
    print(f"-> Quedan {total_final} registros listos para la base de datos.\n")
    
    return df_limpio

if __name__ == "__main__":
    datos_crudos = fetch_usda_data("oats", 20)
    dataset_limpio = transform_and_govern_data(datos_crudos)
    
    print("Muestra de los primeros 5 registros validados:")
    print(dataset_limpio.head()) 
