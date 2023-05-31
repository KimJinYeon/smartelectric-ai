import json

import pandas as pd
import numpy as np
from core.module import DataPreprocess
from core.module.PowerUsageBillCalculator import *


def analysis_reqeust_receiver(customer_number: str):
    df_hour, df_day = DataPreprocess.analysis_prepare_process(customer_number)
    section_list = sort_by_power_usage_with_section(df_hour)
    standby_power = calculate_standby_power(df_hour)
    weekday_list = calculate_weekday_power(df_day)
    day_stat_dict = calculate_day_stat(df_day)
    timezone, power_daytime, power_nighttime = day_night_power_usage_compare(df_hour)
    json_data = {
        "timePeriodIndex": list(map(int, section_list.index.values)),
        "timePeriodPowerUsage": list(map(float, section_list.values)),
        "standbyPower": float(standby_power),
        "weekdayIndex": list(map(int, weekday_list.index.values)),
        "weekdayPowerUsage": list(weekday_list.values),
        "dayOrNight": timezone,
        "dayTimePowerUsage": power_daytime,
        "nightTimePowerUsage": power_nighttime,
        "dayPowerUsageMean": float(day_stat_dict["mean"]),
        "dayPowerUsageMeanInWon": int(calculate_won_by_power_usage(customer_number, day_stat_dict["mean"])[0]),
        "dayPowerUsageMin": float(day_stat_dict["min"]),
        "dayPowerUsageMinInWon": int(calculate_won_by_power_usage(customer_number, day_stat_dict["min"])[0]),
        "dayPowerUsageMax": float(day_stat_dict["max"]),
        "dayPowerUsageMaxInWon": int(calculate_won_by_power_usage(customer_number, day_stat_dict["max"])[0])
    }
    return json_data


def sort_by_power_usage_with_section(df_hour):
    section = df_hour.groupby(by="section").sum()\
        .sort_values(by="powerUsageQuantity", ascending=False)

    return section["powerUsageQuantity"]


def calculate_standby_power(df_hour):
    hour_groupby_hour = df_hour.groupby(by="hour").mean().sort_values(by="powerUsageQuantity", ascending=False)
    return round(hour_groupby_hour.sort_values(by="powerUsageQuantity").head(5).mean()["powerUsageQuantity"], 3)


def calculate_weekday_power(df_day):
    day_groupby_weekday = df_day.groupby(by="weekday").mean().sort_values(by="powerUsageQuantity", ascending=False)
    return day_groupby_weekday["powerUsageQuantity"]


def calculate_day_stat(df_day):
    day_stat = df_day["powerUsageQuantity"].describe()

    return {"mean": day_stat["mean"],
            "min": day_stat["min"],
            "max": day_stat["max"]
            }


def day_night_power_usage_compare(df_hour):
    day_condition = (df_hour["hour"] > 6) | (df_hour["hour"] < 19)
    night_condition = (df_hour["hour"] <= 6) | (df_hour["hour"] >= 19)
    daytime_power_usage = df_hour[day_condition]["powerUsageQuantity"].sum()
    nighttime_power_usage = df_hour[night_condition]["powerUsageQuantity"].sum()
    if daytime_power_usage > nighttime_power_usage:
        return "daytime", daytime_power_usage, nighttime_power_usage
    else:
        return "nighttime", daytime_power_usage, nighttime_power_usage