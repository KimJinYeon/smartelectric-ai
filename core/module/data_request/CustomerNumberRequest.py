from core.module.data_request import SecretKeyHolder
import json
import urllib3 as urllib3

url = "https://opm.kepco.co.kr:11080/OpenAPI/getCustNoList.do"


def get_customer_number_data():
    # urllib setting
    http = urllib3.PoolManager()

    # fields

    fields = {"serviceKey": SecretKeyHolder.service_key,
             "returnType": "02"}

    # send http request
    response = http.request(
        "GET", url=url, fields=fields
    )

    # JSON parse
    customer_number_json = json.loads(response.data.decode('utf-8'))
    customer_dict = dict()
    for customer in customer_number_json["custNoInfoList"]:
        customer_dict[customer["custNo"]] = customer
    return customer_dict
