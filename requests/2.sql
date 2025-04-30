/*
 пассажиры, у которых багаж тяжелее 20 кг
 */

select p.name,
       p.surname,
       b.weight
from fb.passengers p
         join
     fb.baggage b on p.id = b.passenger_id
where b.weight > 20
order by b.weight desc;