import datetime
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from core.module.DataPreprocess import model_train_prepare_process, find_right_timerange
from dateutil.relativedelta import relativedelta
from core.module.data_request import PowerUsageRequest


def split_train_data():
    df_day = model_train_prepare_process()
    df_day_train = df_day.drop(columns=["powerUsageQuantity"])
    df_day_label = df_day["powerUsageQuantity"]
    return df_day_train, df_day_label


def train_model(df_day_train, df_day_label):
    model_rf = RandomForestRegressor()
    model_rf.fit(df_day_train, df_day_label)
    joblib.dump(model_rf, "core/module/model_rf_day.pkl")
    return


def predict(customer_number_requested: str):
    date_binding = find_right_timerange(customer_number_requested)
    model_loaded = joblib.load("core/module/model_rf_day.pkl")
    start_date = datetime.datetime.strptime(date_binding.get("start_date_latest_month"), "%Y%m%d")
    end_date = datetime.datetime.strptime(date_binding.get("datetime_kr_latest_month"), "%Y%m%d")
    # if end_date < datetime.datetime.today():
    #     start_date = start_date + relativedelta(months=1)
    #     end_date = end_date + relativedelta(months=1)

    predict_df = pd.DataFrame()
    date_list = []
    while start_date < end_date:
        date_list.append(start_date)
        start_date += timedelta(days=1)

    predict_df["dateTimeKr"] = date_list
    predict_df["dateTimeKr"] = pd.to_datetime(predict_df["dateTimeKr"])  # str -> pandas datetime
    predict_df["year"] = predict_df["dateTimeKr"].dt.year
    predict_df["month"] = predict_df["dateTimeKr"].dt.month
    predict_df["day"] = predict_df["dateTimeKr"].dt.day
    predict_df["weekday"] = predict_df["dateTimeKr"].dt.weekday
    predict_df.drop(columns=["dateTimeKr"], inplace=True)

    prediction = model_loaded.predict(predict_df)
    predicted_df = pd.DataFrame()
    predicted_df["dateTimeKr"] = date_list
    predicted_df["dateTimeKr"] = predicted_df["dateTimeKr"].astype("str")
    predicted_df["dateTimeKr"] = predicted_df["dateTimeKr"].apply(lambda x: x.replace("-", ""))
    predicted_df["powerUsageQuantity"] = prediction
    return {"prediction": predicted_df.to_dict('records')}
