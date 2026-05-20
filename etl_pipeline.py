import os
import requests
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

def fetch_usda_data(query="oats", limit=20):
    """Extrae datos crudos de la API de USDA."""
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    params = {"api_key": "DEMO_KEY", "query": query, "pageSize": limit}
    
    print(f"1. Extrayendo {limit} registros para '{query}'...")
    response = requests.get(url, params=params)
    response.raise_for_status() 
    return response.json().get('foods', [])

def transform_and_govern_data(raw_foods):
    """Aplica reglas de gobernanza y limpieza usando Pandas."""
    print("2. Iniciando transformación y validación de datos...")
    
    procesados = []
    
    for item in raw_foods:
        marca = item.get('brandOwner', item.get('brandName', 'Genérico'))
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
    
    descartados = total_inicial - len(df_limpio)
    print(f"-> Se descartaron {descartados} registros sin macronutrientes o con valores no realistas.")
    

    return df_limpio

def load_data_to_postgres(df, table_name="ingredientes_nutricionales"):
    """Fase 3: Carga a Base de Datos (Load)"""
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("Error crítico: No se encontró DATABASE_URL en el archivo .env")
        return


    print(f"Conectando a Neon PostgreSQL y cargando {len(df)} registros limpios...")
    try:
        engine = create_engine(db_url)
        df.to_sql(table_name, engine, if_exists="append", index=False)

        print(f"¡Éxito! Datos guardados en la tabla '{table_name}'.")
    except Exception as e:
        print(f"Error al guardar en la base de datos: {e}")
    

if __name__ == "__main__":
    print("===Iniciando pipeline de gobernan===")
    datos_crudos = fetch_usda_data("oats", 20)
    dataset_limpio = transform_and_govern_data(datos_crudos)
    
    if not dataset_limpio.empty:
        load_data_to_postgres(dataset_limpio)
    else:
        print("No se encontraron datos limpios para cargar.")

print("/n===pipeline finalizado===")