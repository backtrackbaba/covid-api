from app import cache
from app.api.v1 import bp
from app.api.v1.services.common_service import CommonService
from app.api.v1.services.country_service import CountryService
from app.api.v1.services.world_service import WorldService


@bp.route('/global')
@cache.cached()
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


@cache.cached()
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


@bp.route('/global/latest')
def global_latest():
    common_service = CommonService()
    world_service = WorldService()
    latest_date = common_service.get_latest_date()
    results = world_service.get_global_count_on_date(str(latest_date))
    data = {
        'count': len(results),
        'result': [],
        'date': str(latest_date)
    }
    for result in results:
        country_data = {}
        country_data[result.country_iso] = {"confirmed": result.confirmed, "deaths": result.deaths,
                                            "recovered": result.recovered}
        data['result'].append(country_data)
    return data


@bp.route('/global/<date>')
@cache.cached()
def world_date(date):
    world_service = WorldService()
    results = world_service.get_global_count_on_date(date)
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
@cache.cached()
def world_date_window(from_date, to_date):
    world_service = WorldService()
    from_date_result = world_service.get_global_count_on_date(from_date)
    to_date_result = world_service.get_global_count_on_date(to_date)
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
@cache.cached()
def global_timeseries(from_date, to_date):
    country_service = CountryService()
    result = {}
    country_list = country_service.get_all_countries()
    data = {
        'count': len(country_list),
        'result': result
    }
    for country in country_list:
        country_result = country_service.get_country_timeseries(country.country_iso, from_date, to_date)
        data_list = []
        for entry in country_result:
            data_list.append({"date": str(entry.date), "confirmed": entry.confirmed, "deaths": entry.deaths,
                              "recovered": entry.recovered})
        result[country.country_iso] = data_list
    return data
