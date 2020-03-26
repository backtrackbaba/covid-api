import json
import time
import uuid

import requests
from flask import current_app

from app import basic_auth, db, redis_db
from app.models import Records
from app.protected import bp


@bp.route('/update-db')
@basic_auth.required
def update_db():
    t1 = time.time()
    # Fetch the latest dataset
    master_data_url = "https://pomber.github.io/covid19/timeseries.json"
    country_name_to_iso_file = current_app.config['DATA_DIR'] + '/country_name_to_iso.json'
    master_data_json = requests.get(master_data_url).json()
    countries = list(master_data_json.keys())

    with open(country_name_to_iso_file, 'r') as fp:
        country_name_to_code = json.loads(fp.read())

    db.session.query(Records).delete()
    db.session.commit()

    for country in countries:
        for everyday in master_data_json[country]:
            record = Records()
            record.uuid = uuid.uuid4()
            record.country_name = country
            record.country_iso = country_name_to_code.get(country)
            record.date = everyday["date"]
            record.confirmed = everyday["confirmed"]
            record.deaths = everyday["deaths"]
            if not record.recovered:
                record.recovered = 0
            else:
                record.recovered = everyday["recovered"]
            db.session.add(record)
            print("Record Object", record)
            db.session.commit()
            print(record)
            print(f"Successfully added record for {country}")

    redis_db.flushdb()
    print(f"Added records for {len(countries)} countries!")
    return f"Added records in {time.time() - t1} seconds!"


@bp.route('/clear-redis')
@basic_auth.required
def clear_redis():
    redis_db.flushdb()
    return "Cleared Redis!!!"
