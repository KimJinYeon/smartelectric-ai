import math
from core.module.data_request import CustomerNumberRequest
from core.module.CalculatorStrategyPattern import *
from datetime import date


def calculate_won_by_power_usage(customer_number: str, power_usage: float):

    power_usage = round(power_usage)
    customer_contract_data = CustomerNumberRequest.get_customer_number_data()
    today = date.today()

    if customer_contract_data.get(customer_number):
        contract_type: str = customer_contract_data[customer_number]["ictg"]
        voltage_type: str = customer_contract_data[customer_number]["lv_hv_val"]

    if today.month in (7, 8):
        if contract_type == "주택용" and voltage_type == "저압":
            return residence_low_voltage_summer_season(power_usage)
        elif contract_type == "주택용" and voltage_type == "고압":
            return residence_high_voltage_summer_season(power_usage)
    else:
        if contract_type == "주택용" and voltage_type == "저압":
            return residence_low_voltage_other_season(power_usage)
        elif contract_type == "주택용" and voltage_type == "고압":
            return residence_high_voltage_other_season(power_usage)
