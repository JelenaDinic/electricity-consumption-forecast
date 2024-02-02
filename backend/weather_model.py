import datetime
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import enum

db_string = "postgresql://postgres:39007466@localhost:5432/isis"

db = create_engine(db_string)
base = declarative_base()

Session = sessionmaker(db)
session = Session()



class WeatherType(enum.Enum):
    Rain = 0
    Rain_Overcast = 0.12
    Rain_Partially_cloudy = 0.24
    Partially_cloudy = 0.36
    Clear = 0.48
    Snow = 0.6
    Snow_Partially_cloudy = 0.72
    Snow_Overcast = 0.84
    Overcast = 0.96


class Weather(base):
    __tablename__ = 'prognoza'

    id = Column(Integer, autoincrement=True, primary_key=True)
    datetime = Column(DateTime, nullable=False)
    temp = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    wind_speed = Column(Float, nullable=False)
    wind_dir = Column(Float, nullable=False)
    visibility = Column(Float, nullable=False)
    cloud_cover = Column(Float, nullable=False)
    day_part = Column(Integer, nullable=False)
    load = Column(Float, nullable=False)

    def __init__(self, **kwargs):
        self.datetime = kwargs.get('datetime')
        self.temp = kwargs.get('temp')
        self.humidity = kwargs.get('humidity')
        self.wind_speed = kwargs.get('windspeed')
        self.wind_dir = kwargs.get('winddir')
        self.visibility = kwargs.get('visibility')
        self.cloud_cover = kwargs.get('cloudcover')
        self.day_part = kwargs.get('day_part')
        self.load = kwargs.get('load')

def impute(df, col_name):
    import numpy as np
    for ind in df.index:
        if np.isnan(df[col_name][ind]):
            temp = df[col_name].iloc[ind - 15:ind + 15].dropna()
            df[col_name][ind] = temp.mean()

def return_all_elements():
    res = pd.read_sql_table('prognoza',db).drop(['id','datetime'], axis=1)
    return res


def return_elements_from_database_in_range(start_date,end_date):
    res = pd.read_sql_table('prognoza', db)
    impute(res, 'wind_gust')
    impute(res, 'load')
    impute(res, 'humidity')
    res['date'] = pd.to_datetime(res['time_stamp']).dt.date
    res = res[(res['date'] >= start_date) & (res['date'] <= end_date)]
    res = res.drop(['id', 'time_stamp','date'], axis=1)
    return res

def return_elements_from_database_in_range_predict(start_date,end_date):
    res = pd.read_sql_table('prognoza', db)
    impute(res, 'humidity')
    res['date'] = pd.to_datetime(res['datetime']).dt.date
    res = res[(res['date'] >= start_date) & (res['date'] <= end_date)]
    res = res.drop(['id', 'date', 'datetime'], axis=1)
    return res

def store_to_database(weather : Weather):
    session.add(weather)
    session.commit()

def return_min_max_load():
    res = pd.read_sql_table('prognoza', db)
    data = res['load']
    return min(data) , max(data)



if __name__ == "__main__":
    base.metadata.create_all(db)