import datetime
import json

import matplotlib
import pandas as pd
from matplotlib import pyplot as plt
from sqlalchemy import and_, func, text

from entity.dashboard import Dashboard
from entity.log import Log
from entity.user import User
from repository.db import session


def get_log_by_id(log_id: int) -> str:
    query = session.query(Log).filter(Log.id == log_id).first().as_dict()
    query['json'] = json.loads(query['json'])
    return json.dumps(query, indent=4, default=str, ensure_ascii=False).encode('utf8').decode()


def get_all_logs() -> pd.DataFrame:
    query = session.query(Log).order_by(Log.id)
    return pd.read_sql(query.statement, query.session.bind).set_index(['id'])


def get_last_n_logs(n: int) -> pd.DataFrame:
    query = session.query(Log).order_by(Log.id.desc()).limit(n)
    return pd.read_sql(query.statement, query.session.bind).set_index(['id'])


def get_logs_between_datetimes(start_dttm: datetime.datetime, end_dttm: datetime.datetime) -> pd.DataFrame:
    query = session.query(Log).filter(and_(Log.dttm >= start_dttm, Log.dttm <= end_dttm)).order_by(Log.id.desc())
    return pd.read_sql(query.statement, query.session.bind).set_index(['id'])


def get_dashboard_logs(dashboard_id: int, start_dttm: datetime.datetime = None, end_dttm: datetime.datetime = None) -> pd.DataFrame:
    query = session.query(Log.id, Log.dttm, Log.user_id, User.email, Log.action, Log.slice_id, Log.referrer, Log.json) \
        .join(User) \
        .filter(Log.dashboard_id == dashboard_id)
    if start_dttm is not None:
        query = query.filter(Log.dttm >= start_dttm)
    if end_dttm is not None:
        query = query.filter(Log.dttm <= end_dttm)
    query = query.order_by(Log.id.desc())
    return pd.read_sql(query.statement, query.session.bind).set_index(['id'])


def count_dashboards_usage(start_dttm: datetime.datetime = None, end_dttm: datetime.datetime = None) -> pd.DataFrame:
    query = session.query(Log.dashboard_id, Dashboard.dashboard_title, Dashboard.published,
                          func.count(Log.dashboard_id).label('count')).join(Dashboard) \
        .filter(Log.dashboard_id.isnot(None)) \
        .group_by(Log.dashboard_id, Dashboard.dashboard_title, Dashboard.published)
    if start_dttm is not None:
        query = query.filter(Log.dttm >= start_dttm)
    if end_dttm is not None:
        query = query.filter(Log.dttm <= end_dttm)
    query = query.order_by(text('count DESC'))
    result = pd.read_sql(query.statement, query.session.bind)
    result.index = result.index + 1
    return result


def get_last_dashboards_usage(last_date: datetime.datetime = None) -> pd.DataFrame:
    query = session.query(Log.dashboard_id, Dashboard.dashboard_title, Dashboard.published,
                          func.max(Log.dttm).label('last_usage')).join(
        Dashboard) \
        .filter(Log.dashboard_id.isnot(None)) \
        .group_by(Log.dashboard_id, Dashboard.dashboard_title, Dashboard.published)
    if last_date is not None:
        query = query.having(func.max(Log.dttm) <= last_date)
    query = query.order_by(text('last_usage DESC'))
    result = pd.read_sql(query.statement, query.session.bind)
    result.index = result.index + 1
    return result


def get_user_actions(user_id: int) -> pd.DataFrame:
    query = session.query(Log).filter(Log.user_id == user_id).order_by(Log.id.desc())
    return pd.read_sql(query.statement, query.session.bind).set_index(['id'])


def count_users_using_each_dashboard() -> pd.DataFrame:
    query = session.query(Log.dashboard_id, Dashboard.dashboard_title, Dashboard.published,
                          func.count(func.distinct(Log.user_id)).label('users_count')).join(Dashboard) \
        .filter(Log.dashboard_id.isnot(None)) \
        .group_by(Log.dashboard_id, Dashboard.dashboard_title, Dashboard.published) \
        .order_by(text('users_count DESC')) \
        .order_by(Log.dashboard_id.desc())
    result = pd.read_sql(query.statement, query.session.bind)
    result.index = result.index + 1
    return result


def get_duration_stats_by_action() -> pd.DataFrame:
    query = session.query(Log.action, func.avg(Log.duration_ms).label('avg_execution_time'),
                          func.max(Log.duration_ms).label('max_execution_time'),
                          func.count(Log.action).label('usage_count')).group_by(Log.action).order_by(
        text('usage_count DESC'))
    result = pd.read_sql(query.statement, query.session.bind)
    result.index = result.index + 1
    return result


def plot_dashboard_usage_by_weekday(dashboard_id: int) -> matplotlib.figure:
    usage_by_weekday = session.query(func.date_trunc('day', Log.dttm), func.count(Log.id)).filter(
        Log.dashboard_id == dashboard_id).group_by(func.date_trunc('day', Log.dttm)).all()

    usage_by_weekday_dict = {}
    for usage in usage_by_weekday:
        weekday = usage[0].strftime('%A')
        count = usage[1]
        usage_by_weekday_dict[weekday] = count

    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    counts = [usage_by_weekday_dict.get(weekday, 0) for weekday in weekdays]
    plt.figure(figsize=(10, 6))
    plt.bar(weekdays, counts)
    plt.title(f"Dashboard {dashboard_id} usage by weekday")
    plt.xlabel("Weekday")
    plt.ylabel("Usage count")
    plt.show()

    return plt.gcf()


def plot_dashboard_usage_by_hour(dashboard_id: int) -> matplotlib.figure:
    usage_by_hour = session.query(func.date_trunc('hour', Log.dttm), func.count(Log.id)).filter(
        Log.dashboard_id == dashboard_id).group_by(func.date_trunc('hour', Log.dttm)).all()

    usage_by_hour_dict = {}
    for usage in usage_by_hour:
        hour = usage[0].strftime('%H')
        count = usage[1]
        usage_by_hour_dict[hour] = count

    hours = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17',
             '18', '19', '20', '21', '22', '23']
    counts = [usage_by_hour_dict.get(hour, 0) for hour in hours]
    plt.bar(hours, counts)
    plt.title(f"Dashboard {dashboard_id} usage by hour")
    plt.xlabel("Hour")
    plt.ylabel("Usage count")
    plt.show()


def json_len_by_dashboard() -> pd.DataFrame:
    query = session.query(Log.dashboard_id, Dashboard.dashboard_title,
                          func.avg(func.length(Log.json)).label('avg_json_length')).join(Dashboard).filter(
        Log.dashboard_id.isnot(None)) \
        .group_by(Log.dashboard_id, Dashboard.dashboard_title).order_by(text('avg_json_length DESC'))
    result = pd.read_sql(query.statement, query.session.bind)
    result.index = result.index + 1
    return result


def get_popular_actions() -> pd.DataFrame:
    query = session.query(Log.dashboard_id, Log.action, func.count(Log.id).label('count')).group_by(Log.dashboard_id,
                                                                                                    Log.action).order_by(
        text('count DESC'))
    result = pd.read_sql(query.statement, query.session.bind)
    result.index = result.index + 1
    result['dashboard_id'] = result['dashboard_id'].astype('Int64')
    return result


def get_popular_dashboards_by_users() -> pd.DataFrame:
    query = session.query(Log.user_id, Log.dashboard_id, User.email, Dashboard.dashboard_title,
                          func.count(Log.id).label('count')) \
        .join(User).join(Dashboard) \
        .filter(and_(Log.user_id.isnot(None), Log.dashboard_id.isnot(None))) \
        .group_by(Log.user_id, User.email, Log.dashboard_id, Dashboard.dashboard_title) \
        .order_by(text('count DESC'))
    result = pd.read_sql(query.statement, query.session.bind)
    result.index = result.index + 1
    return result
