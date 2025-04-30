drop view if exists fb.passenger_flight_stats;

create view fb.passenger_flight_stats as
select
    p.id as passenger_id,
    p.name as first_name,
    p.surname as last_name,
    p.age,
    COUNT(t.id) AS total_tickets,
    SUM(CASE WHEN t.status = 'CONFIRMED' THEN 1 ELSE 0 END) AS completed_flights
FROM fb.passengers p
         LEFT JOIN fb.tickets t ON p.id = t.passenger_id
GROUP BY p.id, p.name, p.surname, p.age;

-- Статистика пассажиров по количеству полетов.
-- Объединяет данные из таблиц Пассажиры и Билеты.

select * from fb.passenger_flight_stats