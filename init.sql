CREATE DATABASE test_db;

\c test_db

CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS event (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    start TIMESTAMP NOT NULL,
    end TIMESTAMP NOT NULL,
    location VARCHAR(255),
    color VARCHAR(20) DEFAULT '#3788d8',
    created_by INTEGER REFERENCES "user"(id) NOT NULL
);

CREATE TABLE IF NOT EXISTS participant (
    id SERIAL PRIMARY KEY,
    event_id INTEGER REFERENCES event(id) NOT NULL,
    user_id INTEGER REFERENCES "user"(id) NOT NULL,
    status VARCHAR(20) DEFAULT '未定'
);