"""
server.py
"""

import os
import pandas as pd
from sklearn.externals import joblib
from flask import Flask, jsonify, request
import dill as pickle
import warnings
warnings.filterwarnings('ignore')
app = Flask(__name__)

@app.route('/predict',methods=['POST'])

def apicall():
	print 'entered apicall func'
	'''pandas dataframe sent as payload from api call'''
	try:
		test_json = request.get_json()
		test = pd.read_json(test_json, orient='records')

		#to resolve issues of type error cannot compare types ndarray and str
		test['Dependents'] = [str(x) for x in list(test['Dependents'])]

		#getting the loan_ids separated out
		loan_ids = test['Loan_ID']

	except Exception as e:
		raise e

	clf = 'model_v1.pk'

	if test.empty:
		return(bad_request())
	else:
		#load model
		print("loading the model")
		loaded_model = None
		with open('/Users/momori/Documents/GitHub/study_material/flask/'+clf, 'rb') as f:
			loaded_model = pickle.load(f)

		print("model is loaded, doing pedictions now")
		predictions = loaded_model.predict(test)

		prediction_series = list(pd.Series(predictions))

		final_predictions = pd.DataFrame(list(zip(loan_ids, prediction_series)))

		##response
		responses = jsonify(predictions=final_predictions.to_json(orient='records'))
		responses.status_code = 200

		return (responses)
