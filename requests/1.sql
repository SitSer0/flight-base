/*
 авиакомпании с количеством рейсов больше среднего
*/

SELECT
    al.name AS airline_name,
    COUNT(f.iata_code) AS flight_count,
    ROUND((SELECT AVG(flight_count)
           FROM (SELECT COUNT(*) AS flight_count
                 FROM fb.flights
                 GROUP BY airline_iata) AS avg_flights), 2) AS avg_flight_count
FROM
    fb.airlines al
        LEFT JOIN
    fb.flights f ON al.iata_code = f.airline_iata
GROUP BY
    al.iata_code, al.name
HAVING
    COUNT(f.iata_code) < (SELECT AVG(flight_count)
                          FROM (SELECT COUNT(*) AS flight_count
                                FROM fb.flights
                                GROUP BY airline_iata) AS avg_flights)
ORDER BY
    flight_count DESC;