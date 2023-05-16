import requests
import json
from types import SimpleNamespace


url = "https://cads-api.fpt.vn/fiber-detection/v2/getToken"

payload = json.dumps({
  "clientId": "H8J1NKema4LrrUu6TYq6kH5if1JX6UyQ",
  "clientSecret": "RimknsnMuXAzi6gzWqinaUyLMgS95tbp"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)
x = json.loads(response.text, object_hook=lambda d: SimpleNamespace(**d))

token = x.access_token


