--tabla de auditoría
CREATE TABLE ingredient_audit_log (
    audit_id SERIAL PRIMARY KEY,
    ingredient_id INT NOT NULL,
    old_calories NUMERIC(6, 2),
    new_calories NUMERIC(6, 2),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    changed_by VARCHAR(50) DEFAULT CURRENT_USER
);


CREATE OR REPLACE FUNCTION log_calorie_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.calories_per_100g <> OLD.calories_per_100g THEN
        INSERT INTO ingredient_audit_log (ingredient_id, old_calories, new_calories)
        VALUES (OLD.ingredient_id, OLD.calories_per_100g, NEW.calories_per_100g);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trg_audit_ingredient_calories
AFTER UPDATE ON ingredients
FOR EACH ROW
EXECUTE FUNCTION log_calorie_changes();