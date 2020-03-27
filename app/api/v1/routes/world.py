from operator import and_

from sqlalchemy import asc

from app import cache
from app.api.v1 import bp
from app.api.v1.services.common_service import CommonService
from app.api.v1.services.world_service import WorldService
from app.models import Records


@bp.route('/global')
@cache.cached(timeout=86400, metrics=True)
def world():
    world_service = WorldService()
    common_service = CommonService()
    date = common_service.get_latest_date()
    results = world_service.get_global_count()
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


@cache.cached(timeout=86400, metrics=True)
@bp.route('/global/count')
def global_count():
    common_service = CommonService()
    world_service = WorldService()
    dates = common_service.get_all_dates()
    date_result = {}
    for entry in dates:
        date = entry.date
        results = world_service.get_global_count_on_date(date)
        global_confirmed_count, global_death_count, global_recovered_count = 0, 0, 0
        for result in results:
            global_confirmed_count += result.confirmed
            global_death_count += result.deaths
            global_recovered_count += result.recovered
        date_result[str(date)] = {
            "confirmed": global_confirmed_count,
            "deaths": global_death_count,
            "recovered": global_recovered_count
        }
    data = {
        "count": len(date_result),
        "result": date_result
    }
    return data


@bp.route('/global/<date>')
@cache.cached(timeout=86400, metrics=True)
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


@bp.route('/global/<from_date>/<to_date>')
@cache.cached(timeout=86400, metrics=True)
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


@bp.route('/global/timeseries/<from_date>/<to_date>')
@cache.cached(timeout=86400, metrics=True)
def global_timeseries(from_date, to_date):
    result = {}
    country_list = Records.query.distinct(Records.country_iso).all()
    data = {
        'count': len(country_list),
        'result': result
    }
    for country in country_list:
        country_result = get_country_time_series(country.country_iso, from_date, to_date)
        data_list = []
        for entry in country_result:
            data_list.append({"date": str(entry.date), "confirmed": entry.confirmed, "deaths": entry.deaths,
                              "recovered": entry.recovered})
        result[country.country_iso] = data_list
    return data


########################################################################################################################

# Internal Functions to be taken out into utils

########################################################################################################################
@cache.cached(timeout=86400, metrics=True)
def get_country_time_series(country_iso, from_date, to_date):
    result = Records.query.filter(Records.country_iso == country_iso).filter(
        and_(Records.date >= from_date, Records.date < to_date)).order_by(asc(Records.date)).all()
    return result


@cache.cached(timeout=86400, metrics=True)
def global_count_on_date(date):
    result = Records.query.filter(Records.date == date).all()
    return result
