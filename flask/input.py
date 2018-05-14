"""
setting the headers to send and accept json responses
"""
import json
import requests
import pandas as pd
header = {"Content-Type":"application/json", \
                "Accept":"application/json"}

#Reading test batch

df = pd.read_csv('/Users/momori/data/loan_prediction_test.csv', encoding='utf-8-sig')

#convert to json
data = df.to_json(orient='records')

#post
resp = requests.post("http://0.0.0.0:8000/predict", \
		data = json.dumps(data), \
		headers = header)

print resp.status_code
resp.json() 
