/*
 Сравнивает количество рейсов из каждого аэропорта со средним значением
 */

select airport,
       flight_count,
       ROUND(flight_count / avg_flight, 2) * 100 as div_from_avg_in_procent
from (select a.code_iata                     as airport,
             count(f.iata_code)              as flight_count,
             avg(count(f.iata_code)) over () as avg_flight
      from fb.airports a
               left join
           fb.flights f on a.code_iata = f.departure_airport_iata
      group by a.code_iata) as airport_stats;