
import pandas as pd
from sqlalchemy import create_engine, BigInteger, String, CHAR
from sqlalchemy.dialects.postgresql import BIGINT

DB_CONFIG = {
    'user': 'serafim',
    'password': '',
    'host': 'localhost',
    'port': '5432',
    'database': 'serafim',
    'schema': 'fb'
}

try:
    df = pd.read_csv('apinfo.csv', sep=None, engine='python')
    df = df.iloc[:, 2:-1]
    print(df)

    print("Первые 5 строк из CSV:")
    print(df.head())

    engine = create_engine(
        f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    )

    dtype = {
        'country': String(255),  # VARCHAR(255)
        'city': String(255),  # VARCHAR(255)
        'runway_count': BIGINT,  # BIGINT
        'code_iata': CHAR(3),  # CHAR(3)
    }

    if 'id' in df.columns:
        df = df.drop(columns=['id'])

    df.to_sql(
        'airports',
        engine,
        schema=DB_CONFIG['schema'],
        if_exists='append',
        index=False,
        dtype=dtype
    )
    print(f"Успешно загружено {len(df)} записей в {DB_CONFIG['schema']}.airports")

except Exception as e:
    print(f"Ошибка: {str(e)}")
finally:
    if 'engine' in locals():
        engine.dispose()
