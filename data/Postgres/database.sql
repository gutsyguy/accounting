CREATE DATABASE accounting;

CREATE STABLE todo(
    todo_id SERIAL PRIMARY KEY, 
    description VARCHAR(255)
)