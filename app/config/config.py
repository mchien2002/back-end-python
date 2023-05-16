from pymongo import MongoClient


client = MongoClient("mongodb+srv://dbAPIDashboard:dbAPIDashboard@cluster0.5iliejt.mongodb.net/?retryWrites=true&w=majority")
conn = client.api_dashboard_application
db=conn["api_dashboard"]

SECRET_KEY = "adminhashtoken"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 64*24*7
