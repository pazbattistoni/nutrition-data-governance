CREATE TABLE ingredients (
    ingredient_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    calories_per_100g NUMERIC(6, 2) NOT NULL CHECK (calories_per_100g >= 0),
    protein_g NUMERIC(5, 2) NOT NULL CHECK (protein_g >= 0),
    carbs_g NUMERIC(5, 2) NOT NULL CHECK (carbs_g >= 0),
    fat_g NUMERIC(5, 2) NOT NULL CHECK (fat_g >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE ingredients IS 'Catálogo maestro de ingredientes y sus macronutrientes por cada 100 gramos.';

CREATE TABLE recipes (
    recipe_id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE recipe_ingredients (
    recipe_id INT NOT NULL REFERENCES recipes(recipe_id) ON DELETE CASCADE,
    ingredient_id INT NOT NULL REFERENCES ingredients(ingredient_id) ON DELETE RESTRICT,
    quantity_g NUMERIC(7, 2) NOT NULL CHECK (quantity_g > 0),
    PRIMARY KEY (recipe_id, ingredient_id)
);

COMMENT ON TABLE recipe_ingredients IS 'Tabla puente que define qué cantidad de cada ingrediente lleva una receta.';

CREATE TABLE daily_logs (
    log_id SERIAL PRIMARY KEY,
    log_date DATE NOT NULL DEFAULT CURRENT_DATE,
    recipe_id INT NOT NULL REFERENCES recipes(recipe_id),
    servings_consumed NUMERIC(4, 2) NOT NULL DEFAULT 1.0 CHECK (servings_consumed > 0),
    notes VARCHAR(255)
);