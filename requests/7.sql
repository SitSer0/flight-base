
/*
 Показывает время следующего рейса той же авиакомпании
*/

select f.iata_code,
       f.departure_time,
       lead(f.departure_time, 1) over (partition by f.airline_iata order by f.departure_time) as next_flight_time
from fb.flights f
where f.aircraft_iata in (select iata from fb.aircrafts where type = 'Boeing 737');