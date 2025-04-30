import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://user:password@localhost:5432/db')
df = pd.read_csv('employees.csv')
df.to_sql('employees', engine, if_exists='append', index=False)