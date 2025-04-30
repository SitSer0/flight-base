DROP TABLE IF EXISTS fb.baggage CASCADE;
DROP TABLE IF EXISTS fb.tickets CASCADE;
DROP TABLE IF EXISTS fb.flight_status_history CASCADE;
DROP TABLE IF EXISTS fb.flights CASCADE;
DROP TABLE IF EXISTS fb.passengers CASCADE;
DROP TABLE IF EXISTS fb.airports CASCADE;
DROP TABLE IF EXISTS fb.aircrafts CASCADE;
DROP TABLE IF EXISTS fb.airlines CASCADE;

CREATE SCHEMA IF NOT EXISTS fb;

-- Таблица airlines
CREATE TABLE fb.airlines
(
    name         VARCHAR(255) NOT NULL,
    iata_code    CHAR(2)      NOT NULL PRIMARY KEY,
    base_country VARCHAR(255) NULL,
    count_planes BIGINT       NULL
);

-- Таблица aircrafts
CREATE TABLE fb.aircrafts
(
    iata                CHAR(3)      NOT NULL PRIMARY KEY,
    registration        VARCHAR(255) NOT NULL,
    type                VARCHAR(255) NULL,
    owning_airline_iata CHAR(2)      NULL REFERENCES fb.airlines (iata_code)
);

-- Таблица airports
CREATE TABLE fb.airports
(
    country      VARCHAR(255) NULL,
    city         VARCHAR(255) NULL,
    runway_count BIGINT       NULL,
    code_iata    CHAR(3)      NOT NULL PRIMARY KEY
);

-- Таблица passengers
CREATE TABLE fb.passengers
(
    id           BIGSERIAL    NOT NULL PRIMARY KEY,
    name         VARCHAR(255) NOT NULL,
    surname      VARCHAR(255) NOT NULL,
    flight_count BIGINT       NULL,
    age          BIGINT       NULL,
    nation       VARCHAR(255) NULL
);

-- Таблица flights
CREATE TABLE fb.flights
(
    iata_code              CHAR(3)                        NOT NULL PRIMARY KEY,
    aircraft_iata          CHAR(3)                        NOT NULL REFERENCES fb.aircrafts (iata),
    airline_iata           CHAR(2)                        NOT NULL REFERENCES fb.airlines (iata_code),
    departure_airport_iata CHAR(3)                        NOT NULL REFERENCES fb.airports (code_iata),
    arrival_airport_iata   CHAR(3)                        NOT NULL REFERENCES fb.airports (code_iata),
    passengers_count       BIGINT                         NULL,
    departure_time         TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    arrival_time           TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL
);

-- Таблица flight_status_history
CREATE TABLE fb.flight_status_history
(
    id          BIGSERIAL PRIMARY KEY,
    iata_code   VARCHAR(10) NOT NULL,
    status      VARCHAR(50) NOT NULL,
    status_time TIMESTAMP   NOT NULL DEFAULT NOW(),
    FOREIGN KEY (iata_code) REFERENCES fb.flights (iata_code)
);

-- Таблица tickets
CREATE TABLE fb.tickets
(
    id             BIGSERIAL                      NOT NULL PRIMARY KEY,
    passenger_id   BIGINT                         NOT NULL REFERENCES fb.passengers (id),
    time           TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    aircraft_id    CHAR(3)                        NOT NULL REFERENCES fb.aircrafts (iata),
    departure_time TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    arrival_time   TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    status         VARCHAR(255)                   NULL
);

-- Таблица baggage
CREATE TABLE fb.baggage
(
    id           BIGSERIAL    NOT NULL PRIMARY KEY,
    passenger_id BIGINT       NOT NULL REFERENCES fb.passengers (id),
    weight       FLOAT(53)    NOT NULL,
    type         VARCHAR(255) NULL,
    flight_iata  CHAR(3)      NOT NULL REFERENCES fb.flights (iata_code)
);

-- Добавление индексов.

create index idx_flights_airports
    on fb.flights (departure_airport_iata, arrival_airport_iata);