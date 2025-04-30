/*
 аэропорты с наименьшим количеством рейсов
 */

select a.city,
       a.country,
       count(f.iata_code) as flight_count
from fb.airports a
         left join
     fb.flights f on a.code_iata = f.departure_airport_iata
group by a.city, a.country
having count(f.iata_code) < 5
order by flight_count asc;