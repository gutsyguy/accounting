CREATE DATABASE data;

CREATE STABLE todo(
    todo_id SERIAL PRIMARY KEY, 
    description VARCHAR(255)
)