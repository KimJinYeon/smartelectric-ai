import math


def calculate_base_bills(power_usage: float, factors: dict):
    if power_usage <= factors["power_accumulate_threshold_first"]:
        basic_bill = factors["base_bill_first"]
        power_bill = (power_usage * factors["power_bill_first"]) // 1
        accumulate = 0
    elif factors["power_accumulate_threshold_first"] < power_usage <= factors["power_accumulate_threshold_second"]:
        basic_bill = factors["base_bill_second"]
        power_bill = (factors["power_accumulate_threshold_first"] * factors["power_bill_first"]
                      + (power_usage - factors["power_accumulate_threshold_first"])
                      * factors["power_bill_second"]) // 1
        accumulate = 1
    elif factors["power_accumulate_threshold_second"] < power_usage <= factors["power_accumulate_threshold_super"]:
        basic_bill = factors["base_bill_third"]
        power_bill = (factors["power_accumulate_threshold_first"] * factors["power_bill_first"]
                      + (factors["power_accumulate_threshold_second"] - factors["power_accumulate_threshold_first"]) * factors["power_bill_second"]
                      + (power_usage - factors["power_accumulate_threshold_second"]) * factors["power_bill_third"]) // 1
        accumulate = 2
    else:
        basic_bill = factors["base_bill_third"]
        power_bill = (factors["power_accumulate_threshold_first"] * factors["power_bill_first"]
                      + (factors["power_accumulate_threshold_second"] - factors["power_accumulate_threshold_first"]) * factors["power_bill_second"]
                      + (factors["power_accumulate_threshold_super"] - factors["power_accumulate_threshold_second"]) * factors["power_bill_third"]
                      + (power_usage - factors["power_accumulate_threshold_super"]) * factors["power_bill_super"]) // 1
        accumulate = 3
    return basic_bill, power_bill, accumulate


def calculate_common_bills(basic_bill: float, power_bill: float, power_usage: float):
    environment_bill = power_usage * 7.3 // 1
    fuel_bill = power_usage * 5
    power_bill_total = basic_bill + power_bill + environment_bill + fuel_bill
    value_added_tax = round(power_bill_total * 0.1)
    foundation_bill_rate = power_bill_total * 0.037 // 10 * 10
    bill_total = (power_bill_total + value_added_tax + foundation_bill_rate) // 10 * 10
    return bill_total


def residence_low_voltage_other_season(power_usage: float):
    power_usage_factors = {
        "power_accumulate_threshold_first": 200,
        "power_accumulate_threshold_second": 400,
        "power_accumulate_threshold_super": 1000,
        "base_bill_first": 910,
        "base_bill_second": 1600,
        "base_bill_third": 7300,
        "power_bill_first": 100.6,
        "power_bill_second": 195.2,
        "power_bill_third": 287.9,
        "power_bill_super": 716.8
    }
    basic_bill, power_bill, accumulate = calculate_base_bills(power_usage, power_usage_factors)

    bill_total = calculate_common_bills(basic_bill, power_bill, power_usage)
    if power_usage == 0:
        bill_total = 0

    return bill_total, accumulate, power_usage_factors


def residence_low_voltage_summer_season(power_usage: float):
    power_usage_factors = {
        "power_accumulate_threshold_first": 300,
        "power_accumulate_threshold_second": 450,
        "power_accumulate_threshold_super": 1000,
        "base_bill_first": 910,
        "base_bill_second": 1600,
        "base_bill_third": 7300,
        "power_bill_first": 100.6,
        "power_bill_second": 195.2,
        "power_bill_third": 287.9,
        "power_bill_super": 716.8
    }
    basic_bill, power_bill, accumulate = calculate_base_bills(power_usage, power_usage_factors)

    bill_total = calculate_common_bills(basic_bill, power_bill, power_usage)
    if power_usage == 0:
        bill_total = 0

    return bill_total, accumulate, power_usage_factors


def residence_high_voltage_other_season(power_usage: float):
    power_usage_factors = {
        "power_accumulate_threshold_first": 200,
        "power_accumulate_threshold_second": 400,
        "power_accumulate_threshold_super": 1000,
        "base_bill_first": 730,
        "base_bill_second": 1260,
        "base_bill_third": 6060,
        "power_bill_first": 85.6,
        "power_bill_second": 154.6,
        "power_bill_third": 222.9,
        "power_bill_super": 581.9
    }
    basic_bill, power_bill, accumulate = calculate_base_bills(power_usage, power_usage_factors)

    bill_total = calculate_common_bills(basic_bill, power_bill, power_usage)
    if power_usage == 0:
        bill_total = 0

    return bill_total, accumulate, power_usage_factors


def residence_high_voltage_summer_season(power_usage: float):
    power_usage_factors = {
        "power_accumulate_threshold_first": 300,
        "power_accumulate_threshold_second": 450,
        "power_accumulate_threshold_super": 1000,
        "base_bill_first": 730,
        "base_bill_second": 1260,
        "base_bill_third": 6060,
        "power_bill_first": 85.6,
        "power_bill_second": 154.6,
        "power_bill_third": 222.9,
        "power_bill_super": 581.9
    }
    basic_bill, power_bill, accumulate = calculate_base_bills(power_usage, power_usage_factors)

    bill_total = calculate_common_bills(basic_bill, power_bill, power_usage)
    if power_usage == 0:
        bill_total = 0

    return bill_total, accumulate, power_usage_factors
