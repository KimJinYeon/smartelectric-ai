from fastapi import FastAPI
from core.module.data_request import PowerUsageRequest
from core.module import PowerUsageBillCalculator
from core.module import DataPreprocess
from core.module import DataAnalysis
from core.module import Model
import json

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/report/issue")
def ai_report_generate(custNo: str):
    json_data = DataAnalysis.analysis_reqeust_receiver(custNo)
    return json_data


@app.get("/prediction")
def predict(custNo: str):
    return Model.predict(custNo)


@app.get("/calculator")
def power_bill_calculate(custNo: str, powerUsageQuantity: float):
    power_won_converted, accumulate, power_bill_info = PowerUsageBillCalculator.calculate_won_by_power_usage(custNo, powerUsageQuantity)
    return {"result": power_won_converted,
            "accumulate": accumulate,
            "powerBillInfo": power_bill_info}
