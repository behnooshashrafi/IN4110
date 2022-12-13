#!/usr/bin/env python3
"""
Fetch data from https://www.hvakosterstrommen.no/strompris-api
and visualize it.

Assignment 5
"""

import datetime

import altair as alt
import pandas as pd
import requests
import requests_cache
from typing import Optional

# install an HTTP request cache
# to avoid unnecessary repeat requests for the same data
# this will create the file http_cache.sqlite
requests_cache.install_cache()


# task 5.1:


def fetch_day_prices(date: datetime.date = None, location: str = "NO1") -> pd.DataFrame:
    """Fetch one day of data for one location from hvakosterstrommen.no API

    arguments:
    date(datetime): date format (year-month-day without 0-padding). Today if no argument was given.
    returns:
    df(DataFrame): DataFrame containing information with two columns (NOK_per_kWh (float), time_start (datetime))
    """
    if date is None:
        date = datetime.date.today()
    assert date >= datetime.date(2022,10,2)
    year = date.year
    # the month needs to be zero padded
    month = zero_pad(str(date.month))
    # the day needs to be zero padded
    day = zero_pad(str(date.day))

    url = f"https://www.hvakosterstrommen.no/api/v1/prices/{year}/{month}-{day}_{location}.json"
    r = requests.get(url)
    #dataframe
    df = pd.DataFrame(r.json())
    df["time_start"] = pd.to_datetime(df["time_start"], utc=True).dt.tz_convert("Europe/Oslo")
    return pd.DataFrame(data = df, columns = ["NOK_per_kWh", "time_start"])

def zero_pad(n: str):
    """zero-pad a number string

    turns '2' into '02'

    You don't need to use this function,
    but you may find it useful.
    """
    if len(n)==1:
        return str('0' + n)
    elif len(n)<1 or len(n)>2:
        raise ValueError("Incorrect day format")
    else:
        return n


# LOCATION_CODES maps codes ("NO1") to names ("Oslo")
LOCATION_CODES = {
    "NO1" : "Oslo",
    "NO2" : "Kristiansand",
    "NO3" : "Trondheim",
    "NO4" : "Tromsø",
    "NO5" : "Bergen",
}

# task 1:


def fetch_prices(
    end_date: datetime.date = None,
    days: int = 7,
    locations=tuple(LOCATION_CODES.keys()),
) -> pd.DataFrame:
    """Fetch prices for multiple days and locations into a single DataFrame
    
    arguments:
    date(datetime): date format (year-month-day without 0-padding). Today if no argument was given.
    days(int): number of days including the end_date
    returns:
    df(DataFrame): DataFrame containing information with four columns (NOK_per_kWh (float), time_start (datetime), location_code: The location code (NO2 or similar), location: The location name (Oslo, Trondheim, etc.))
    """
    if end_date is None:
        end_date = datetime.date.today()
        
    dates = []
    
    for i in range(days):
        date = end_date - datetime.timedelta(i)
        dates.append(date)
    # creating the data frame
    df = pd.DataFrame()
    # retrieves the data for all locations
    for loc in locations:
        for i in dates:
            df = df.append(fetch_day_prices(i, loc))
            df["location_code"] = loc
            df["location"] = LOCATION_CODES[loc]
    df["delta_pre_hour"] = df["NOK_per_kWh"].diff()
    df["delta_pre_day"] = df["NOK_per_kWh"].diff(24)
    df["delta_pre_week"] = df["NOK_per_kWh"].diff(24*7)
    return df

# task 5.1:


def plot_prices(df: pd.DataFrame) -> alt.Chart:
    """Plot energy prices over time

    x-axis should be time_start
    y-axis should be price in NOK
    each location should get its own line

    Make sure to document arguments and return value
    arguments:
    df(DataFrame): DataFrame containing information with four columns (NOK_per_kWh (float), time_start (datetime), location_code: The location code (NO2 or similar), location: The location name (Oslo, Trondheim, etc.))
    return:
    alt.Chart: a plot of price over time
    """
    chart = alt.Chart(df).mark_line().encode(
    x="time_start:T",
    y="NOK_per_kWh:Q",
    color="location:N",
    tooltip=[
    "delta_pre_hour",
    "delta_pre_day",
    "delta_pre_week"
    ]
    )
    return chart


# Task 5.4


def plot_daily_prices(df: pd.DataFrame) -> alt.Chart:
    """Plot the daily average price

    x-axis should be time_start (day resolution)
    y-axis should be price in NOK

    You may use any mark.

    Make sure to document arguments and return value...
    """
    chart = alt.Chart(df).mark_line().encode(
        x="day(time_start):T",
        y="mean(NOK_per_kWh):Q",
        color="location:N"
    )
    return chart
   


# Task 5.6

ACTIVITIES = {
    # activity name: energy cost in kW
    ...
}


def plot_activity_prices(
    df: pd.DataFrame, activity: str = "shower", minutes: float = 10
) -> alt.Chart:
    """
    Plot price for one activity by name,
    given a data frame of prices, and its duration in minutes.

    Make sure to document arguments and return value...
    """

    ...


def main():
    """Allow running this module as a script for testing."""
    df = fetch_prices()
    chart = plot_prices(df)
    # showing the chart without requiring jupyter notebook or vs code for example
    # requires altair viewer: `pip install altair_viewer`
    chart.show()
    print(df.to_string())


if __name__ == "__main__":
    main()
