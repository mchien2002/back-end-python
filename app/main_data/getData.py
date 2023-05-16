import requests
import json
from app.main_data.getToken import token
from datetime import datetime, date
from array import array

url = "http://cads-api.fpt.vn/fiber-detection/v2/using_json_inf/2022/12"

payload = "angle_id"
headers = {"Content-Type": "application/json", "Authorization": token}


response = requests.request("POST", url, headers=headers)
data = json.loads(response.text)


times = [0 for i in range(0, 7)]  # 7 angle_id
stateOk = [0 for i in range(0, 7)]  # 7 angle_id
inspection = []

for lv1 in data:
    status_ok = 0  # get model ok
    dates = []
    for lv2 in data[lv1]:
        temp = data[lv1][lv2]
        num = int(temp["angle_id"])
        status = temp["status"]
        times[num - 1] += 1

        if status == "ok":
            status_ok += 1
            stateOk[num - 1] += 1

        time = datetime.fromisoformat(temp["date"]).date()
        dates.append(time.strftime("%Y/%m/%d"))

    inspection.append(
        {
            "id": lv1,
            "state_ok": round((100 * status_ok / len(data[lv1])), 2),
            "begin": str(min(dates)),
            "end": str(max(dates)),
        }
    )

