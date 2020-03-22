import os

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from sqlalchemy.dialects.postgresql import DATE, UUID
from walrus import Database

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)
redis_db = Database(host=os.environ.get('CACHE_REDIS_HOST'), port=os.environ.get('CACHE_REDIS_PORT'),
                    db=os.environ.get('CACHE_REDIS_DB'), password=os.environ.get('CACHE_REDIS_PASSWORD'))
cache = redis_db.cache()


class Records(db.Model):
    __tablename__ = 'records'
    __table_args__ = {'extend_existing': True}

    uuid = db.Column(UUID(as_uuid=True), primary_key=True)
    country_iso = db.Column(db.String(100), index=True)
    country_name = db.Column(db.String(100))
    date = db.Column(DATE)
    confirmed = db.Column(db.INTEGER)
    deaths = db.Column(db.INTEGER)
    recovered = db.Column(db.INTEGER)

    def __repr__(self):
        return f'<Record ID: {self.uuid}, ISO: {self.country_iso}, Country: {self.country_name}, Date: {self.date}, {self.confirmed, self.deaths, self.deaths}>'


@app.route('/')
def home():
    return 'It works!!!'


@app.route('/api/v1/country/<country_iso>')
@cache.cached(timeout=86400)
def country(country_iso):
    result = Records.query.filter_by(country_iso=country_iso).all()
    data = {
        'count': len(result),
        'result': {}
    }
    for record in result:
        data['result'][record.date.strftime('%Y-%m-%d')] = {"confirmed": record.confirmed, "deaths": record.deaths,
                                                            "recovered": record.recovered}
    return data


@app.route('/api/v1/country/<country_iso>/<date>')
@cache.cached(timeout=86400)
def country_date(country_iso, date):
    result = Records.query.filter(Records.country_iso == country_iso).filter(Records.date == date).first()
    data = {
        'count': 1,
        'result': {}
    }
    data['result'][result.date.strftime('%Y-%m-%d')] = {"confirmed": result.confirmed, "deaths": result.deaths,
                                                        "recovered": result.recovered}
    return data


@app.route('/api/v1/global')
@cache.cached(timeout=86400)
def world():
    date = Records.query.filter(Records.country_iso == "IND").order_by(desc(Records.date)).first().date
    results = Records.query.filter(Records.date == date).all()
    global_confirmed_count, global_death_count, global_recovered_count = 0, 0, 0
    for result in results:
        global_confirmed_count += result.confirmed
        global_death_count += result.deaths
        global_recovered_count += result.recovered
    data = {
        'count': 1,
        'date': date,
        'result': {"confirmed": global_confirmed_count, "deaths": global_death_count,
                   "recovered": global_recovered_count}
    }
    return data


@app.route('/api/v1/global/<date>')
@cache.cached(timeout=86400)
def world_date(date):
    results = Records.query.filter(Records.date == date).all()
    global_confirmed_count, global_death_count, global_recovered_count = 0, 0, 0
    for result in results:
        global_confirmed_count += result.confirmed
        global_death_count += result.deaths
        global_recovered_count += result.recovered
    data = {
        'count': 1,
        'date': date,
        'result': {"confirmed": global_confirmed_count, "deaths": global_death_count,
                   "recovered": global_recovered_count}
    }
    return data


@app.route('/api/v1/global/<from_date>/<to_date>')
@cache.cached(timeout=86400)
def world_date_window(from_date, to_date):
    from_date_result = Records.query.filter(Records.date == from_date).all()
    to_date_result = Records.query.filter(Records.date == to_date).all()
    from_date_confirmed_count, from_date_death_count, from_date_recovered_count = 0, 0, 0
    to_date_confirmed_count, to_date_death_count, to_date_recovered_count = 0, 0, 0

    for result in from_date_result:
        from_date_confirmed_count += result.confirmed
        from_date_death_count += result.deaths
        from_date_recovered_count += result.recovered

    for result in to_date_result:
        to_date_confirmed_count += result.confirmed
        to_date_death_count += result.deaths
        to_date_recovered_count += result.recovered

    data = {
        'count': 1,
        'from_date': from_date,
        'to_date': to_date,
        'result': {
            "confirmed": abs(from_date_confirmed_count - to_date_confirmed_count),
            "deaths": abs(from_date_death_count - to_date_death_count),
            "recovered": abs(from_date_recovered_count - to_date_recovered_count)}
    }
    return data
