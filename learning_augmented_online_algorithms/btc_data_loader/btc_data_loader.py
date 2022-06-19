"""
Module for loading BTC data from csv files.
"""
from __future__ import annotations

from datetime import datetime, timedelta
import pandas as pd


BASE_URL = 'https://raw.githubusercontent.com/jrrhuang/data/main/BTCUSD/'
DT_FORMAT = '%Y-%m-%d'
DATA_PATHS = []
for year in range(2022, 2014, -1):
    DATA_PATHS.append(BASE_URL + f'gemini_BTCUSD_{year}_1min.csv')
START_DATE_2015 = datetime.strptime('2015-10-08', DT_FORMAT)
END_DATE_2022 = datetime.strptime('2022-03-20', DT_FORMAT)


class BTCDataLoader:
    """
    Iterator for BTCData.

    Interface for loading Bitcoin data sequentially from csv files. Loads
    one-week of data starting on the Monday of each week.
    """

    def __init__(self, start_date_str: str = '2015-10-07',
                 end_date_str: str = None, interval: int = 5) -> None:
        """
        Initialize BTCDaetaLoader iterator object.

        Arguments:
        start_date_str (str) - start date of BTC data trace
        end_date_str (str) - end date of BTC data trace
        interval (int) - number of minutes per timestep

        Notes:
        Both `start_date_str` and `end_date_str` should be in YYYY-MM-DD format
        """
        # find start and end date in data, starting on Monday of the week
        if end_date_str is None:
            end_date_str = datetime.now().strftime(DT_FORMAT)

        start_date = datetime.strptime(start_date_str, DT_FORMAT)
        end_date = datetime.strptime(end_date_str, DT_FORMAT)
        # bound start and end date
        if start_date < START_DATE_2015:
            start_date = START_DATE_2015
        if end_date > END_DATE_2022:
            end_date = END_DATE_2022
        # find first Sunday - dataframe starts reading on Monday
        weekday = start_date.weekday()
        days_to_sunday = 6 - weekday
        self.start_date = start_date + timedelta(days=days_to_sunday)
        # find cutoff of last day
        self.end_date = end_date + timedelta(days=1)

        # load in data
        start_date_str = self.start_date.strftime(DT_FORMAT)
        end_date_str = self.end_date.strftime(DT_FORMAT)
        self.df = pd.concat([pd.read_csv(data, skiprows=1, parse_dates=['Date'], index_col=['Date'])
                            for data in DATA_PATHS])['Close']

        # slice from start to finish and reverse direction
        self.df = self.df.sort_index().loc[start_date_str: end_date_str]

        # store interval of each timestep
        self.interval = interval

    def __iter__(self):
        """Iterate through data by week."""
        self.curweek = self.start_date
        self.nextweek = self.curweek + timedelta(days=6)
        return self

    def __next__(self):
        """Get next week's data until end of data set."""
        if self.nextweek > self.end_date:
            raise StopIteration

        curweekstr = self.curweek.strftime(DT_FORMAT)
        nextweekstr = self.nextweek.strftime(DT_FORMAT)
        data = self.df.loc[curweekstr: nextweekstr]

        self.curweek = self.curweek + timedelta(days=7)
        self.nextweek = self.nextweek + timedelta(days=7)

        return data[::self.interval]
