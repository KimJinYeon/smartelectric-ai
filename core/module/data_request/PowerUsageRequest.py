import urllib3
import json
from core.module.data_request.SecretKeyHolder import create_refresh_token


def time_range_router(customer_number: str, start_date: str, end_date: str):
    """
    route data request to head to right function
    :param customer_number: KEPCO customer number - str with 10 letters long
    :param start_date: datetime in Java LocalDate and LocalDateTime format - able to handle from "yyyyMMddkk" to "yyyy"
    :param end_date: datetime in Java LacalDate and LocalDateTime format - able to handle from "yyyyMMddkk" to "yyyy"
    :return: power_data_request_with_time_range with date considered
    """

    url_routed: str = "https://api.smartelectric.kr/power-usage/specific-user/period"  # root url
    fields: dict[str:str] = \
        {"custNo": customer_number, "startDate": start_date, "endDate": end_date}  # http request query parameter
    headers: dict[str:str] = \
        {'Authorization': 'Bearer ' + create_refresh_token("123")}  # header for JWT authentication

    if len(start_date) == len(end_date) == 10:  # yyyyMMddkk
        url_routed += "/hour"
    elif len(start_date) == len(end_date) == 8:  # yyyyMMdd
        url_routed += "/day"
    elif len(start_date) == len(end_date) == 6:  # yyyyMM
        url_routed += "/month"
    else:
        url_routed += "/year"  # yyyy

    # power data request
    return power_data_request_with_time_range(url_routed, headers, fields)


def whole_data_router(customer_number: str, time_unit: str):
    """
    route data request for whole data to head to right function
    :param customer_number: KEPCO customer number - str with 10 letters long
    :param time_unit: datetime in Java LocalDate and LocalDateTime format - able to handle from "yyyyMMddkk" to "yyyy"
    :return:
    """

    # set parameters for power_data_request_whole_data
    url_routed: str = "https://api.smartelectric.kr/power-usage/specific-user/whole/" + time_unit
    fields: dict[str:str] = {"custNo": customer_number}
    headers: dict[str:str] = {'Authorization': 'Bearer ' + create_refresh_token("123")}

    # power data reqeust
    return power_data_request_whole_data(url_routed, headers, fields)


def most_recent_router(customer_number: str):
    url_routed: str = "https://api.smartelectric.kr/power-usage/specific-user/period/month/most-recent"
    fields: dict[str:str] = {"custNo": customer_number}
    headers: dict[str:str] = {'Authorization': 'Bearer ' + create_refresh_token("123")}

    # power data reqeust
    return power_data_request_whole_data(url_routed, headers, fields)


def power_data_request_with_time_range(url_routed: str, headers: dict, fields: dict):
    """
    makes request for smartelectric main server with following data:
    1. KEPCO customer number - str with 10 letters long
    2. start date with format "yyyyMMddkk" - kk means hour with 24 hour time system(01~24)
    3. end date with format "yyyyMMddkk" - kk means hour with 24 hour time system(01~24)

    requirements should be wrapped into "fields" parameter(dict)

    :param url_routed: finalized request url toward "api.smartelectric.kr"
    :param headers: http request header for providing jwt to authenticate
    :param fields: http request query parameter that holds KEPCO customer number, start date, end date
    :return: electric power usage data of target customer in JSON
    """
    # urllib setting
    http = urllib3.PoolManager()

    # send http request
    response = http.request(
        "GET", url=url_routed, headers=headers, fields=fields
    )

    # JSON parse
    power_usage = json.loads(response.data.decode('utf-8'))
    return power_usage


def power_data_request_whole_data(url_routed: str, headers: dict, fields: dict):
    """
    makes request for smartelectric main server with following data:
    1. KEPCO customer number - str with 10 letters long

    requirements should be wrapped into "fields" parameter(dict)

    :param url_routed: finalized request url toward "api.smartelectric.kr"
    :param headers: http request header for providing jwt to authenticate
    :param fields: http request query parameter that holds KEPCO customer number, start date, end date
    :return: whole electric power usage data of specific user by request power unit(embedded in url_routed)
    """

    # urllib setting
    http = urllib3.PoolManager()

    # send http request
    response = http.request(
        "GET", url=url_routed, headers=headers, fields=fields
    )

    # JSON parse
    power_usage_whole = json.loads(response.data.decode('utf-8'))

    return power_usage_whole


def power_data_request_train_data():

    url_routed: str = "https://api.smartelectric.kr/power-usage/special/whole"
    headers: dict[str:str] = \
        {'Authorization': 'Bearer ' + create_refresh_token("123")}  # header for JWT authentication

    # urllib setting
    http = urllib3.PoolManager()

    # send http request
    response = http.request(
        "GET", url=url_routed, headers=headers
    )

    # JSON parse
    power_usage_whole = json.loads(response.data.decode('utf-8'))

    return power_usage_whole
