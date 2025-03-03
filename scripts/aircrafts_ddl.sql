CREATE TABLE IF NOT EXISTS Aircrafts
(
    id      SERIAL PRIMARY KEY,
    company varchar(20),
    airline varchar(20),
    model   varchar(20)
);
