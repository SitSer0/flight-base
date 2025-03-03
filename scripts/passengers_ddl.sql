CREATE TABLE IF NOT EXISTS Passengers
(
    pass_id      SERIAL PRIMARY KEY,
    name varchar(20),
    surname varchar(20),
    date_of_birth date
);