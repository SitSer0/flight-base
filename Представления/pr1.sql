drop view if exists fb.flight_details;

create view fb.flight_details as
select
    f.iata_code as flight_code,
    f.departure_time,
    f.arrival_time,
    a.name as airline_name,
    dep_airport.city as departure_city,
    arr_airport.city as arrival_city,
    f.passengers_count
from fb.flights f
         join fb.airlines a on f.airline_iata = a.iata_code
         join fb.airports dep_airport on f.departure_airport_iata = dep_airport.code_iata
         join fb.airports arr_airport on f.arrival_airport_iata = arr_airport.code_iata;


-- Информация о рейсах с деталями авиакомпаний и аэропортов.
-- Объединяет данные из таблиц Рейсы, Авиакомпании, Аэропорты.

select * from fb.flight_details
where departure_city = 'West Michael';