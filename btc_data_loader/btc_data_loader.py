from datetime import datetime, timedelta

import pandas as pd

class BTCDataLoader:
  """
  Interface for loading Bitcoin data sequentially from csv files. Loads one-week
  of data starting on the Monday of each week.
  """
  base_url = 'https://raw.githubusercontent.com/jrrhuang/data/main/BTCUSD/'
  data_paths = []
  for year in range(2022, 2014, -1):
    data_paths.append(base_url + f'gemini_BTCUSD_{year}_1min.csv')

  dt_format = '%Y-%m-%d'
  start_date_2015 = datetime.strptime('2015-10-08', '%Y-%m-%d')
  end_date_2022 = datetime.strptime('2022-03-20', '%Y-%m-%d')

  def __init__(self, start_date_str='2015-10-07', end_date_str=None, interval=5):
    """
    Arguments:
    start_date_str (str) - default beginning of data
    end_date_str (str) - default end of data
    interval (int) - number of minutes per timestep
    """
    # find start and end date in data, starting on Monday of the week
    if end_date_str is None:
      end_date_str = datetime.now().strftime(BTCDataLoader.dt_format)
    
    start_date = datetime.strptime(start_date_str, BTCDataLoader.dt_format)
    end_date = datetime.strptime(end_date_str, BTCDataLoader.dt_format)
    # bound start and end date
    if start_date < BTCDataLoader.start_date_2015:
      start_date = BTCDataLoader.start_date_2015
    if end_date > BTCDataLoader.end_date_2022:
      end_date = BTCDataLoader.end_date_2022
    # find first Sunday - dataframe starts reading on Monday
    weekday = start_date.weekday()
    days_to_sunday = 6 - weekday
    self.start_date = start_date + timedelta(days=days_to_sunday)
    # find cutoff of last day
    self.end_date = end_date + timedelta(days=1)

    # load in data
    start_date_str = self.start_date.strftime(BTCDataLoader.dt_format)
    end_date_str = self.end_date.strftime(BTCDataLoader.dt_format)
    self.df = pd.concat([pd.read_csv(data, skiprows=1, parse_dates=['Date'], index_col=['Date'])
                         for data in BTCDataLoader.data_paths])['Close']
    # slice from start to finish and reverse direction
    self.df = self.df.sort_index().loc[start_date_str: end_date_str]

    # store interval of each timestep
    self.interval = interval

  def __iter__(self):
    self.curweek = self.start_date
    self.nextweek = self.curweek + timedelta(days=8)
    return self
  
  def __next__(self):
    if self.nextweek > self.end_date:
      print(self.nextweek, self.end_date)
      raise StopIteration

    curweekstr = self.curweek.strftime(BTCDataLoader.dt_format)
    nextweekstr = self.nextweek.strftime(BTCDataLoader.dt_format)
    data = self.df.loc[curweekstr: nextweekstr]

    self.curweek = self.curweek + timedelta(days=7)
    self.nextweek = self.nextweek + timedelta(days=7)

    return data[::self.interval]