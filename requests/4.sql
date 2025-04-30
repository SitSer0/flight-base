/*
 пассажиры, которые летали чаще среднего
*/


select p.name,
       p.surname,
       p.flight_count,
       (select avg(flight_count) from fb.passengers) as avg_flight_count
from fb.passengers p
where p.flight_count > (select avg(flight_count) from fb.passengers)
order by p.flight_count desc;