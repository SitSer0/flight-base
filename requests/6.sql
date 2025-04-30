/*
 5 самых старых пассажиров
*/

select id,
       name,
       surname,
       age
from fb.passengers
order by age desc limit 5
offset 0;