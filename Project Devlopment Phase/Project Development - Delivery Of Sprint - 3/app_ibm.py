

import numpy as np
from flask import Flask, request, jsonify, render_template
import json
from json import JSONEncoder

import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "VRPKD1qVgUgqtLpDzESBUnBSykdvOGmUNou5Z065rfbq"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__)
#model = pickle.load(open('model0.pkl','rb'))

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/predict', methods=['POST'])
def predict():
    int_features = [float(x) for x in request.form.values()]
    final_features = np.array(int_features)
    #prediction = model.predict(final_features)
    t = {"array": final_features}
    t = json.dumps(t, cls=NumpyArrayEncoder)
    payload_scoring = {"input_data": [
{
  "fields" : [ "f0", "f1", "f2", "f3" ],
  "values" : t
}]}
    


    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/8e9bcf3c-adf0-4865-b14e-6c02c3b7550c/predictions?version=2022-06-02', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
#print(response_scoring.json())
    pred= response_scoring.json()
    output=pred['predictions'][0]['values'][0]
#print(output)
    return render_template('index.html', prediction_text='Predicted Energy output of the Wind Turbine is {} kWh'.format(output))
@app.route('/predict_api',methods=['POST'])
def predict_api():
    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])
    
    output = prediction[0]
    return jsonify(output)
class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)
if __name__=="__main__":
    app.run(debug=True)
