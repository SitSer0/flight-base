/*
 статусы рейсов за последние 24 часа
 */

select f.iata_code,
       fsh.status,
       fsh.status_time,
       lag(fsh.status) over (partition by f.iata_code order by fsh.status_time) as prev_status
from fb.flight_status_history fsh
         join
     fb.flights f on fsh.iata_code = f.iata_code
where fsh.status_time >= now() - interval '24 hours'
order by f.iata_code, fsh.status_time;


