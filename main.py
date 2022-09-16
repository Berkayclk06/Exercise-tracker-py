import requests
from datetime import datetime
import os


APP_ID = os.environ["APP_ID"]
API_KEY = os.environ["API_KEY"]

TODAY = datetime.today().strftime("%d/%m/%Y")
TIME_NOW = datetime.now().strftime("%X")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
    "Content-Type": "application/json",

}

req_body = {
    "query": input("Tell me which exercise you did: "),
    "gender": "male",
    "weight_kg": 101,
    "height_cm": 174,
    "age": 26
}

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

nutri_response = requests.post(url=exercise_endpoint, json=req_body, headers=headers)
exercise_data = nutri_response.json()["exercises"]

sheet_endpoint = os.environ["SHEET_ENDPOINT"]

for exercise in exercise_data:

    excel_body = {
        "workout": {
            "date": TODAY,
            "time": TIME_NOW,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"],
        }
    }

    sheet_response = requests.post(url=sheet_endpoint, json=excel_body,
                                   headers=headers, auth=(os.environ["USERNAME"], os.environ["PASSWORD"]))
    print(sheet_response.text)