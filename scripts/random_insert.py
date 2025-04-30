import random
from faker import Faker
from sqlalchemy import create_engine, MetaData, Table, insert, text
from datetime import datetime, time, timedelta
from collections import defaultdict

count_data = 500

fake = Faker()
engine = create_engine('postgresql://serafim:@localhost/serafim')
metadata = MetaData()
metadata.reflect(bind=engine, schema='fb')

def random_time():
    return time(random.randint(0, 23), random.randint(0, 59))


def safe_insert(table_name, data, pk_column='id'):
    """Безопасная вставка с проверкой существования записей"""
    table = Table(table_name, metadata, schema='fb', autoload_with=engine)
    inserted = 0

    with engine.connect() as conn:
        for record in data:
            check = conn.execute(
                text(f"SELECT 1 FROM fb.{table_name} WHERE {pk_column} = :val"),
                {'val': record[pk_column]}
            ).fetchone()

            if not check:
                conn.execute(insert(table), record)
                inserted += 1
        conn.commit()

    print(f"Вставлено {inserted}/{len(data)} записей в {table_name}")
    return inserted


# 1. Генерация авиакомпаний
airlines_data = []
used_codes = set()

for _ in range(count_data):
    while True:
        code = fake.unique.bothify(text='??').upper()
        if code not in used_codes:
            used_codes.add(code)
            break

    airlines_data.append({
        'iata_code': code,
        'name': fake.company() + ' Airlines',
        'base_country': fake.country(),
        'count_planes': random.randint(10, 500)
    })

safe_insert('airlines', airlines_data, 'iata_code')

# 2. Генерация самолетов
aircrafts_data = []
aircraft_types = ['Boeing 737', 'Airbus A320', 'Boeing 787', 'Airbus A350',
                  'Embraer E190', 'Bombardier CRJ900', 'ATR 72', 'Sukhoi Superjet']

for _ in range(15):
    aircrafts_data.append({
        'iata': fake.unique.bothify(text='???').upper(),
        'registration': fake.unique.bothify(text='?##??').upper(),
        'type': random.choice(aircraft_types),
        'owning_airline_iata': random.choice(airlines_data)['iata_code'],
        'capacity': random.choice([100, 150, 200, 250, 300])
    })

safe_insert('aircrafts', aircrafts_data, 'iata')

# 3. Генерация аэропортов
airports_data = []
for _ in range(count_data):
    airports_data.append({
        'code_iata': fake.unique.bothify(text='???').upper(),
        'country': fake.country(),
        'city': fake.city(),
        'runway_count': random.randint(1, 4)
    })

safe_insert('airports', airports_data, 'code_iata')

# 4. Генерация пассажиров
passengers_data = []
for i in range(count_data):
    passengers_data.append({
        'id': 1000 + i,
        'name': fake.first_name(),
        'surname': fake.last_name(),
        'flight_count': random.randint(0, 100),
        'age': random.randint(18, 80),
        'nation': fake.country()
    })

safe_insert('passengers', passengers_data)

# 5. Генерация рейсов
flights_data = []
for i in range(count_data):
    airline = random.choice(airlines_data)
    aircraft = random.choice(
        [ac for ac in aircrafts_data if ac['owning_airline_iata'] == airline['iata_code']] or aircrafts_data)
    dep_airport, arr_airport = random.sample(airports_data, 2)

    dep_time = random_time()
    arr_time = (datetime.combine(datetime.today(), dep_time) +
                timedelta(hours=random.randint(1, 12), minutes=random.randint(0, 59))).time()

    flights_data.append({
        'iata_code': f"{airline['iata_code'][0]}{random.randint(10, 99)}",  # 3 символа
        'aircraft_iata': aircraft['iata'],
        'airline_iata': airline['iata_code'],
        'departure_airport_iata': dep_airport['code_iata'],
        'arrival_airport_iata': arr_airport['code_iata'],
        'passengers_count': random.randint(50, aircraft['capacity']),
        'departure_time': dep_time,
        'arrival_time': arr_time
    })

safe_insert('flights', flights_data, 'iata_code')

# 6. Генерация истории статусов рейсов
status_history_data = []
statuses = ['SCHEDULED', 'BOARDING', 'DEPARTED', 'IN_FLIGHT', 'LANDED', 'ARRIVED']


ind = 0
for flight in flights_data:
    for status in random.sample(statuses, random.randint(3, 5)):
        status_history_data.append({
            'id': ind,
            'iata_code': flight['iata_code'],
            'status': status,
            'status_time': datetime.now() - timedelta(days=random.randint(1, 30))
        })
        ind += 1

safe_insert('flight_status_history', status_history_data)

# 7. Генерация билетов
tickets_data = []
for i in range(count_data):
    flight = random.choice(flights_data)
    tickets_data.append({
        'id': 5000 + i,
        'passenger_id': random.choice(passengers_data)['id'],
        'aircraft_id': flight['aircraft_iata'],
        'departure_time': flight['departure_time'],
        'arrival_time': flight['arrival_time'],
        'time': datetime.now() - timedelta(days=random.randint(1, 30)),
        'status': random.choice(['CONFIRMED', 'CHECKED_IN', 'BOARDED', 'CANCELLED'])
    })

safe_insert('tickets', tickets_data)

# 8. Генерация багажа
baggage_data = []
for i in range(count_data):
    ticket = random.choice(tickets_data)
    baggage_data.append({
        'id': 7000 + i,
        'passenger_id': ticket['passenger_id'],
        'flight_iata': next(f['iata_code'] for f in flights_data if f['aircraft_iata'] == ticket['aircraft_id']),
        'weight': round(random.uniform(5.0, 30.0), 2),
        'type': random.choice(['Hand', 'Checked', 'Oversized'])
    })

safe_insert('baggage', baggage_data)

print("Все данные успешно загружены!")
engine.dispose()