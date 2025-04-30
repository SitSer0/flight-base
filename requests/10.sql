/*
 топ 5 самых популярных авиарейсов
 */
select
    f.iata_code as flight_number,
    al.name as airline,
    a1.city as departure_city,
    a2.city as arrival_city,
    count(t.id) as tickets_sold
from
    fb.flights f
        join
    fb.airlines al on f.airline_iata = al.iata_code
        join
    fb.airports a1 on f.departure_airport_iata = a1.code_iata
        join
    fb.airports a2 on f.arrival_airport_iata = a2.code_iata
        left join
    fb.tickets t on f.aircraft_iata = t.aircraft_id
        and f.departure_time = t.departure_time
        and f.arrival_time = t.arrival_time
group by
    f.iata_code, al.name, a1.city, a2.city
order by
    tickets_sold desc
limit 5;