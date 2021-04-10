from flask import Flask, request, render_template,jsonify
import json
import numpy as np
from flask_cors import cross_origin
import sklearn
import pickle
import pandas as pd

def load_models():
    #file_name = "C:/Users/HP/Advanced Python/diabetes.pkl"
    #with open(file_name, 'rb') as pickled:
    #    data = pickle.load(pickled)
    #    model = data['model']
    model = pickle.load(open("models/diabetes.pkl", "rb"))
    return model

app = Flask(__name__)


def predict(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1,-1)
    # load model
    print(to_predict)
    model = load_models()
    prediction = model.predict(to_predict)
    response = json.dumps({'response': str(prediction)})
    print(int(prediction))
    return int(prediction)

@app.route("/")
@cross_origin()
def home():
    return render_template("index.html")

@app.route('/predict', methods = ['GET','POST'])
def result():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        to_predict_list = list(map(float, to_predict_list))
        result = predict(to_predict_list)
        if result == 0:
            response ='Congratulations! You donot have Diabetes.'
        else:
            response ='You are detected with Diabetes.'
        return render_template("result.html", prediction = response)
    else:
        return render_template("index.html")

