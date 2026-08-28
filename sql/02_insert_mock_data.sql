-- Script de carga de datos
INSERT INTO ingredients (name, calories_per_100g, protein_g, carbs_g, fat_g) VALUES
('Avena en hojuelas', 389, 16.9, 66.3, 6.9),
('Mantequilla de maní', 588, 25.0, 20.0, 50.0),
('Semillas de chía', 486, 16.5, 42.1, 30.7);

INSERT INTO recipes (name, description) VALUES
('Barritas de Granola Fit', 'Snack rápido y alto en fibra, sin cocción.');

INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity_g) VALUES
(1, 1, 200.00), -- Relaciona con la Avena
(1, 2, 100.00), -- Relaciona con la Mantequilla de maní
(1, 3, 30.00);  -- Relaciona con las Semillas de chía

INSERT INTO ingredients (name, calories_per_100g, protein_g, carbs_g, fat_g) VALUES
('Arroz integral cocido', 112, 2.6, 23.5, 0.9),
('Bebida de almendras sin azúcar', 13, 0.4, 0.1, 1.1),
('Stevia en polvo', 0, 0.0, 0.0, 0.0),
('Canela molida', 247, 4.0, 80.6, 1.2);

INSERT INTO recipes (name, description) VALUES
('Arroz con Leche Fit', 'Postre tradicional adaptado, sin azúcar y con bebida vegetal.');

INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity_g) VALUES
(2, 4, 150.00), -- Arroz integral
(2, 5, 500.00), -- Bebida de almendras
(2, 6, 5.00),   -- Stevia
(2, 7, 2.00);   -- Canela