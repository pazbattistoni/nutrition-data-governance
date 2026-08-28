# Nutrition Data Governance

Este repositorio es un proyecto de portfolio enfocado en el diseño, administración y gobernanza de una base de datos relacional para información nutricional, utilizando **PostgreSQL**.

El objetivo principal es demostrar la aplicación de reglas de negocio a nivel de motor de base de datos para garantizar la calidad, integridad y precisión de los datos.

## Diccionario de Datos (Data Dictionary)

El modelo normalizado consta de las siguientes entidades principales:

### 1. `ingredients` (Catálogo Maestro)
Almacena la información nutricional base por cada 100 gramos.
* `ingredient_id`: Identificador único (PK).
* `name`: Nombre del ingrediente (UNIQUE, NOT NULL).
* `calories_per_100g`, `protein_g`, `carbs_g`, `fat_g`: Valores nutricionales. Se utiliza el tipo de dato `NUMERIC` en lugar de `FLOAT` o `REAL` para evitar errores de redondeo en punto flotante y mantener la precisión estricta. Todos cuentan con un `CHECK (>= 0)` para evitar anomalías en los datos.

### 2. `recipes` (Preparaciones)
Agrupa ingredientes en platos específicos.
* `recipe_id`: Identificador único (PK).
* `name`: Nombre de la receta.
* `description`: Breve detalle de la preparación.

### 3. `recipe_ingredients` (Tabla Intermedia)
Resuelve la relación muchos a muchos entre recetas e ingredientes, definiendo las proporciones exactas.
* `recipe_id` / `ingredient_id`: Llaves foráneas compuestas (PK, FK). 
* `quantity_g`: Cantidad en gramos utilizada en la receta. Utiliza un `CHECK (> 0)`.
* *Regla de integridad:* Si se elimina una receta (`ON DELETE CASCADE`), se eliminan sus proporciones. Si se intenta eliminar un ingrediente que está en uso, la base de datos lo impide (`ON DELETE RESTRICT`).

### 4. `vw_recipe_macros` (Vista de Cálculo Automático)
Una vista (`VIEW`) que centraliza la lógica de negocio. Calcula de forma automática los macronutrientes totales de cada receta, cruzando las tablas y aplicando la matemática necesaria sin tener que escribir `JOINs` complejos en cada consulta.

## Tecnologías y Prácticas Aplicadas
* **PostgreSQL:** Motor de base de datos.
* **SQL (DDL y DML):** Creación de tablas, inserción de *mock data* y consultas relacionales.
* **Data Governance:** Restricciones de integridad (`Constraints`, `Foreign Keys`, `Check`).