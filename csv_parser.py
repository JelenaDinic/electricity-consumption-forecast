from datetime import datetime
import pandas as pd
import numpy as np
from backend.weather_model import Weather, store_to_database


class CSVParser:

    def __init__(self):
        self.weather_data = [
            # "Training Data/NYS Weather Data/New York City, NY/New York City, ... 2018-01-01 to 2018-12-31.csv",
            # "Training Data/NYS Weather Data/New York City, NY/New York City, ... 2019-01-01 to 2019-12-31.csv",
            # "Training Data/NYS Weather Data/New York City, NY/New York City, ... 2020-01-01 to 2020-12-31.csv",
            # "Training Data/NYS Weather Data/New York City, NY/New York City, ... 2021-01-01 to 2021-12-11.csv",
            "Training Data/NYS Weather Data/New York City, NY/test.csv"
        ]
        self.load_data = "Training Data/NYS Load  Data"

    def process_data(self):
        holidays = self.retrieve_holidays_data()
        weather = self.retrieve_weather_data()

        weather['datetime'] = pd.to_datetime(weather['datetime'])
        weather['date'] = weather['datetime'].apply(lambda x: x.strftime('%Y-%m-%d'))
        joined = pd.merge(weather, holidays, how='left', on='date', indicator=True)
        processed = joined[joined['_merge'] == 'left_only'].drop('_merge', axis=1)
        processed.set_index("datetime", inplace=True)
        processed = processed.reset_index()
        processed = self.clear_extrems(processed, "temp", 108)
        columns_to_process = ['humidity', 'windspeed', 'winddir', 'visibility', 'cloudcover']
        for column in columns_to_process:
            processed = self.custom_impute(processed, column)
            processed = self.fill_rest(processed, column)
        processed['load'] = 0
        self.store_to_db(processed)


    def retrieve_holidays_data(self):
        holiday_frame = pd.read_excel("Training Data/US Holidays 2018-2021.xlsx")
        holiday_frame['date'] = pd.to_datetime(holiday_frame['date'])
        holiday_frame["date"] = holiday_frame["date"].astype(str)

        return holiday_frame[['date']]

    def retrieve_weather_data(self):
        data_frames = []

        for file in self.weather_data:
            df = pd.read_csv(file)
            data_frames.append(df)

        merged = pd.concat(data_frames, ignore_index=True)
        selected_columns = ['datetime', 'temp', 'humidity', 'windspeed', 'winddir', 'visibility', 'cloudcover']
        merged = merged[selected_columns]

        return merged
    
    def fill_rest(self,data_frame,column):
        data_frame[column] = data_frame[column].fillna(
            data_frame[column].rolling(15, min_periods=1).mean())
        return data_frame

    def custom_impute(self, data_frame, column: str):

        row_index = data_frame[data_frame[column].isnull()].index.tolist()

        for row in row_index:
            average = self.average(data_frame, column, row)
            data_frame.loc[row, column] = average

        return data_frame

    def average(self, data_frame, column, row):

        next_row = self.get_working_index(data_frame, row, column)
        first_row = data_frame.iloc[row - 1][column]
        second_row = data_frame.iloc[row - 2][column]
        next_first = data_frame.iloc[next_row + 1][column]
        next_second = data_frame.iloc[next_row + 2][column]
        average = (first_row + second_row + next_first + next_second) / 4

        return round(average, 2)

    def get_working_index(self, data_frame, row, column):
        while True:
            if not np.isnan(data_frame.loc[row, column]):
                return row
            row += 1

    def clear_extrems(self, data_frame,
                           column: str,
                           min_value: int):
        extrems_mask = data_frame[column] > min_value

        # Replace values exceeding the threshold with 0
        data_frame.loc[extrems_mask, column] = 0

        # Find row indices with replaced values
        row_indices = data_frame.index[extrems_mask]

        # Iterate through row indices and replace 0 values with the average of adjacent values
        for row in row_indices:
            # Use iloc with -1 and +1 to get adjacent row values
            average = (data_frame.iloc[row - 1][column] + data_frame.iloc[row + 1][column]) / 2
            data_frame.loc[row, column] = average

        return data_frame

    # def combine_loads_data(self):
    #     pd.set_option('mode.chained_assignment', None)
    #     merged = None
    #     for (root, dirs, files) in os.walk(self.load_data):
    #         for file in files:
    #             if ".csv" in file:
    #                 df = pd.read_csv(f"{root}/{file}")
    #                 new_york = df[df["Name"] == "N.Y.C."]
    #                 new_york['Time Stamp'] = pd.to_datetime(
    #                     new_york['Time Stamp'])

    #                 new_york = new_york[new_york["Time Stamp"].dt.minute == 0]
    #                 new_york["date"] = new_york["Time Stamp"].dt.strftime(
    #                     '%Y-%m-%d')
    #                 new_york["Time Stamp"] = new_york[
    #                     "Time Stamp"].dt.strftime('%Y-%m-%dT%H:%M:%S')

    #                 merged = pd.concat([merged, new_york], ignore_index=True)
    #     pd.set_option('mode.chained_assignment', 'warn')
    #     merged.rename(columns={"Time Stamp": "datetime", "Load": "load"},
    #                   inplace=True)

    #     return merged[['datetime', 'load', 'date']]

    def store_to_db(self, processed):
        list_hours = {0, 1, 2, 3, 4, 5, 6, 7, 22, 23}

        processed['day_part'] = processed['datetime'].dt.hour.isin(list_hours).astype(int)
        processed['day_part'] = processed['day_part'].apply(lambda x: 0 if x else 1)

        processed.apply(lambda row: store_to_database(Weather(**row)), axis=1)

cs= CSVParser()
cs.process_data()