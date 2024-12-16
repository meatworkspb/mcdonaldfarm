CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  type INTEGER NOT NULL
);

CREATE TABLE animal_type (
  id SERIAL PRIMARY KEY,
  name TEXT UNIQUE NOT NULL
);

CREATE TABLE animal (
  id SERIAL PRIMARY KEY,
  name TEXT UNIQUE NOT NULL,
  type_id INTEGER NOT NULL,
  weight REAL,
  dob DATE,
  sex CHAR(1) CHECK (sex IN ('M', 'F')),
  CONSTRAINT fk_type FOREIGN KEY (type_id) REFERENCES animal_type(id) ON DELETE CASCADE
);