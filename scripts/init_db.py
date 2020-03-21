import json
import uuid

import requests
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import Config
from models import Records

MASTER_DATA_URL = "https://pomber.github.io/covid19/timeseries.json"

master_data_json = requests.get(MASTER_DATA_URL).json()

POSTGRESQL_URL = Config.POSTGRESQL_URL
POSTGRESQL_USERNAME = Config.POSTGRESQL_USERNAME
POSTGRESQL_PASSWORD = Config.POSTGRESQL_PASSWORD
POSTGRESQL_DATABASE = Config.POSTGRESQL_DATABASE

db_string = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRESQL_USERNAME,
                                                                  pw=POSTGRESQL_PASSWORD,
                                                                  url=POSTGRESQL_URL,
                                                                  db=POSTGRESQL_DATABASE)
db = create_engine(db_string)
base = declarative_base()
print("db_string", db_string)
Session = sessionmaker(db)
session = Session()

countries = list(master_data_json.keys())

with open('/Users/sai/workspace/work/covid-api/data/country_name_to_iso.json', 'r') as fp:
    country_name_to_code = json.loads(fp.read())

for country in countries:
    for everyday in master_data_json[country]:
        record = Records()
        record.uuid = uuid.uuid4()
        record.country_name = country
        record.country_iso = country_name_to_code.get(country)
        record.date = everyday["date"]
        record.confirmed = everyday["confirmed"]
        record.deaths = everyday["deaths"]
        record.recovered = everyday["recovered"]
        session.add(record)
        print("Record Object", record)
        session.commit()
        print(record)
        print(f"Successfully added record for {country}")
