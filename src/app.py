import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import DATE, UUID
from walrus import Database

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

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
