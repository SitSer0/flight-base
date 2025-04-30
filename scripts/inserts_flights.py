import requests
import pandas as pd
from sqlalchemy import create_engine, CHAR, BigInteger, Time, Integer, String
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.dialects.postgresql import insert

# Настройки API
params = {
    'access_key': 'e7a955e18abe99b19447f01e7ceaae23',
    'offset': 64000
}

# Получение данных из API
api_result = requests.get('https://api.aviationstack.com/v1/flights', params)
api_response = api_result.json()

# Настройки подключения к БД
DB_CONFIG = {
    'user': 'serafim',
    'password': '',
    'host': 'localhost',
    'port': '5432',
    'database': 'serafim',
    'schema': 'fb'
}

# Создание подключения
engine = create_engine(
    f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
)

# Словари для хранения данных
data_airports_keys = {
    'country': [],
    'city': [],
    'runway_count': [],
    'code_iata': []
}

data_aircrafts_keys = {
    'iata': [],
    'registration': [],
    'type': [],
    'owning_airline_iata': [],
}

data_airlines_keys = {
    'name': [],
    'iata_code': [],
    'base_country': [],
    'count_planes': []
}

data_flights_keys = {
    'iata_code': [],
    'aircraft_iata': [],
    'airline_iata': [],
    'departure_airport_iata': [],
    'arrival_airport_iata': [],
    'passengers_count': [],
    'departure_time': [],
    'arrival_time': []
}

# Обработка данных из API
for flight in api_response['data']:
    try:
        # Проверка и обрезка данных до нужной длины
        def validate_code(code, max_length):
            if code is None:
                return None
            code = str(code).strip().upper()
            return code[:max_length] if code else None


        # Получение данных с проверкой на None
        flight_data = flight.get('flight', {}) or {}
        aircraft_data = flight.get('aircraft', {}) or {}
        airline_data = flight.get('airline', {}) or {}
        departure_data = flight.get('departure', {}) or {}
        arrival_data = flight.get('arrival', {}) or {}

        flight_iata = validate_code(flight_data.get('iata'), 3)
        aircraft_iata = validate_code(aircraft_data.get('iata'), 3)
        airline_iata = validate_code(airline_data.get('iata'), 2)
        departure_iata = validate_code(departure_data.get('iata'), 3)
        arrival_iata = validate_code(arrival_data.get('iata'), 3)
        dep_time = departure_data.get('scheduled')
        arr_time = arrival_data.get('scheduled')

        # Проверка обязательных полей
        if None in [flight_iata, aircraft_iata, airline_iata, departure_iata, arrival_iata, dep_time, arr_time]:
            continue

        # Сначала добавляем данные в справочники
        # Авиакомпании
        data_airlines_keys['name'].append(airline_data.get('name', 'Unknown'))
        data_airlines_keys['iata_code'].append(airline_iata)
        data_airlines_keys['base_country'].append(airline_data.get('country', 'Unknown'))
        data_airlines_keys['count_planes'].append(0)

        # Самолеты
        data_aircrafts_keys['iata'].append(aircraft_iata)
        data_aircrafts_keys['registration'].append(aircraft_data.get('registration', 0))
        data_aircrafts_keys['type'].append(aircraft_data.get('type', 'plane'))
        data_aircrafts_keys['owning_airline_iata'].append(airline_iata)

        # Аэропорты (вылет)
        data_airports_keys['country'].append(departure_data.get('country', 'Unknown'))
        data_airports_keys['city'].append(departure_data.get('city', 'Unknown'))
        data_airports_keys['runway_count'].append(1)
        data_airports_keys['code_iata'].append(departure_iata)

        # Аэропорты (прилет)
        data_airports_keys['country'].append(arrival_data.get('country', 'Unknown'))
        data_airports_keys['city'].append(arrival_data.get('city', 'Unknown'))
        data_airports_keys['runway_count'].append(1)
        data_airports_keys['code_iata'].append(arrival_iata)

        # Затем добавляем данные рейса
        data_flights_keys['iata_code'].append(flight_iata)
        data_flights_keys['aircraft_iata'].append(aircraft_iata)
        data_flights_keys['airline_iata'].append(airline_iata)
        data_flights_keys['departure_airport_iata'].append(departure_iata)
        data_flights_keys['arrival_airport_iata'].append(arrival_iata)
        data_flights_keys['passengers_count'].append(0)
        data_flights_keys['departure_time'].append(dep_time)
        data_flights_keys['arrival_time'].append(arr_time)

    except Exception as e:
        print(f"Ошибка обработки рейса: {str(e)}")
        continue


# Функция для вставки данных с обработкой ошибок
def safe_insert(df, table_name, conflict_column, dtype=None):
    if df.empty:
        print(f"Нет данных для вставки в {table_name}")
        return

    try:
        # Удаляем дубликаты
        df = df.drop_duplicates(subset=[conflict_column])

        if df.empty:
            print(f"Нет уникальных данных для вставки в {table_name}")
            return

        # Вставляем построчно с обработкой ошибок
        inserted = 0
        with engine.begin() as connection:
            for _, row in df.iterrows():
                try:
                    row.to_frame().T.to_sql(
                        table_name,
                        connection,
                        schema=DB_CONFIG['schema'],
                        if_exists='append',
                        index=False,
                        dtype=dtype
                    )
                    inserted += 1
                except SQLAlchemyError as e:
                    # Пропускаем дубликаты и ошибки внешних ключей
                    if "duplicate key" not in str(e) and "foreign key" not in str(e):
                        print(f"Ошибка при вставке в {table_name}: {str(e)}")
                        continue

        print(f"Успешно вставлено {inserted} из {len(df)} записей в {table_name}")
    except Exception as e:
        print(f"Ошибка при вставке в {table_name}: {str(e)}")


# Преобразование в DataFrame
df_airlines = pd.DataFrame(data_airlines_keys)
df_aircrafts = pd.DataFrame(data_aircrafts_keys)
df_airports = pd.DataFrame(data_airports_keys)
df_flights = pd.DataFrame(data_flights_keys)

# Конвертация времени для рейсов
if not df_flights.empty:
    df_flights['departure_time'] = pd.to_datetime(df_flights['departure_time']).dt.time
    df_flights['arrival_time'] = pd.to_datetime(df_flights['arrival_time']).dt.time

# Вставка данных в правильном порядке
print("\nНачало вставки данных...")

# 1. Сначала авиакомпании
print("\nВставка авиакомпаний...")
safe_insert(
    df_airlines,
    'airlines',
    'iata_code',
    dtype={
        'name': String(255),
        'iata_code': CHAR(2),
        'base_country': String(255),
        'count_planes': BigInteger()
    }
)

# 2. Затем самолеты
print("\nВставка самолетов...")
safe_insert(
    df_aircrafts,
    'aircrafts',
    'iata',
    dtype={
        'iata': CHAR(3),
        'registration': String(255),
        'type': String(255),
        'owning_airline_iata': CHAR(2)
    }
)

# 3. Затем аэропорты
print("\nВставка аэропортов...")
safe_insert(
    df_airports,
    'airports',
    'code_iata',
    dtype={
        'country': String(255),
        'city': String(255),
        'runway_count': BigInteger(),
        'code_iata': CHAR(3)
    }
)




# 4. И только потом рейсы
print("\nВставка рейсов...")
safe_insert(
    df_flights,
    'flights',
    'iata_code',
    dtype={
        'iata_code': CHAR(3),
        'aircraft_iata': CHAR(3),
        'airline_iata': CHAR(2),
        'departure_airport_iata': CHAR(3),
        'arrival_airport_iata': CHAR(3),
        'passengers_count': BigInteger(),
        'departure_time': Time(),
        'arrival_time': Time()
    }
)

print("\nЗавершение работы...")
engine.dispose()