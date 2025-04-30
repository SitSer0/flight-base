/*
 Находит пассажиров, которые летали чаще 75% всех пассажиров
 */

select p.name,
       p.surname,
       p.flight_count
from fb.passengers p
where p.flight_count > (select percentile_cont(0.75) within group (order by flight_count)
                        from fb.passengers);