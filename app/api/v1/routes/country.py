from app import cache
from app.api.v1 import bp
from app.api.v1.services.country_service import CountryService


@bp.route('/country/<country_iso>')
@cache.cached()
def country(country_iso):
    country_service = CountryService()
    results = country_service.get_country_historic_data(country_iso)
    data = {
        'count': len(results),
        'result': {}
    }
    for result in results:
        data['result'][result.date.strftime('%Y-%m-%d')] = {"confirmed": result.confirmed, "deaths": result.deaths,
                                                            "recovered": result.recovered}
    return data


@bp.route('/country/<country_iso>/<date>')
@cache.cached()
def country_date(country_iso, date):
    country_service = CountryService()
    result = country_service.get_country_record_on_date(country_iso.upper(), date)
    data = {
        'count': 1,
        'result': {}
    }
    data['result'][result.date.strftime('%Y-%m-%d')] = {"confirmed": result.confirmed, "deaths": result.deaths,
                                                        "recovered": result.recovered}
    return data


@bp.route('/country/<country_iso>/latest')
@cache.cached()
def country_latest(country_iso):
    country_service = CountryService()
    result = country_service.get_latest_country_record(country_iso)
    data = {
        'count': 1,
        'result': {}
    }
    data['result'][result.date.strftime('%Y-%m-%d')] = {"confirmed": result.confirmed, "deaths": result.deaths,
                                                        "recovered": result.recovered}
    return data


@bp.route('/country/<country_iso>/timeseries/<from_date>/<to_date>')
@cache.cached()
def country_timeseries(country_iso, from_date, to_date):
    country_service = CountryService()
    results = country_service.get_country_timeseries(country_iso, from_date, to_date)
    data_list = []
    for result in results:
        data_list.append({"date": str(result.date), "confirmed": result.confirmed, "deaths": result.deaths,
                          "recovered": result.recovered})
    data = {
        'count': len(results),
        'result': data_list
    }
    return data


@bp.route('/latest-date')
@cache.cached()
def latest_date():
    country_service = CountryService()
    date = country_service.get_latest_record_date()
    return str(date)
