import pandas as pd
import json
from core.module.data_request import PowerUsageRequest


def model_train_prepare_process():
    df_day = pd.json_normalize(PowerUsageRequest.power_data_request_train_data())
    df_day["dateTimeKr"] = pd.to_datetime(df_day["dateTimeKr"])  # str -> pandas datetime
    df_day["year"] = df_day["dateTimeKr"].dt.year
    df_day["month"] = df_day["dateTimeKr"].dt.month
    df_day["day"] = df_day["dateTimeKr"].dt.day
    df_day["weekday"] = df_day["dateTimeKr"].dt.weekday
    df_day.drop(columns=["ID", "custNo", "dateTimeKr"], inplace=True)
    return df_day


def analysis_prepare_process(customer_number_requested: str):
    date_dict = find_right_timerange(customer_number_requested)
    df_day = make_dataframe(customer_number_requested,
                            date_dict["start_date_latest_month"],
                            date_dict["end_date_latest_month"])
    df_hour = make_dataframe(customer_number_requested,
                             date_dict["start_date_latest_month"]+"00",
                             date_dict["end_date_latest_month"]+"23")
    df_hour, df_day = datetime(df_hour, df_day)

    return df_hour, df_day


def datetime(df_hour, df_day):
    df_hour["dateTimeKr"] = pd.to_datetime(df_hour["dateTimeKr"])  # str -> pandas datetime
    df_hour["year"] = df_hour["dateTimeKr"].dt.year
    df_hour["month"] = df_hour["dateTimeKr"].dt.month
    df_hour["day"] = df_hour["dateTimeKr"].dt.day
    df_hour["hour"] = df_hour["dateTimeKr"].dt.hour
    df_hour["weekday"] = df_hour["dateTimeKr"].dt.weekday
    df_hour["section"] = df_hour["hour"].apply(lambda x: time_series_discrete(x))
    df_day["dateTimeKr"] = pd.to_datetime(df_day["dateTimeKr"])  # str -> pandas datetime
    df_day["year"] = df_day["dateTimeKr"].dt.year
    df_day["month"] = df_day["dateTimeKr"].dt.month
    df_day["day"] = df_day["dateTimeKr"].dt.day
    df_day["weekday"] = df_day["dateTimeKr"].dt.weekday
    return df_hour, df_day




def make_dataframe(customer_number_requested: str, start_date_by_latest_bill: str, end_date_by_closest_date: str):

    rawdata = PowerUsageRequest.time_range_router(customer_number_requested,
                                                  start_date_by_latest_bill,
                                                  end_date_by_closest_date)

    return pd.DataFrame(rawdata)


def find_right_timerange(customer_number_requested: str):

    month = PowerUsageRequest.most_recent_router(customer_number_requested)
    start_date_latest_month = month["startDateKr"].replace("-", "")
    end_date_latest_month = month["endDateKr"].replace("-", "")
    datetime_kr_latest_month = month["dateTimeKr"].replace("-", "")

    data_binding = {
        "start_date_latest_month": start_date_latest_month,
        "end_date_latest_month": end_date_latest_month,
        "datetime_kr_latest_month": datetime_kr_latest_month
    }

    return data_binding


def time_series_discrete(hour):
    if 0<=hour<=3:
        return 0
    elif 4<=hour<=7:
        return 1
    elif 8<=hour<=11:
        return 2
    elif 12<=hour<=15:
        return 3
    elif 16<=hour<=19:
        return 4
    elif 20<=hour<=23:
        return 5

# customer_number, start_date, end_date = find_right_timerange("0130392270")
# print(customer_number, start_date, end_date)
# df = make_dataframe(customer_number, start_date, end_date)
# print(df)
# df_hour, df_day = prepare_process("0130392270")
# print(df_hour)
# print(df_day)
