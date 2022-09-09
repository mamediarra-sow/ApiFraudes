import sklearn
from fastapi import FastAPI
import numpy as np
from typing import Any, Dict, List, Union
import pickle
from ML_data import *
from ML_preprocessing import *
import pandas as pd
app = FastAPI()

df_ml : if_data
preprocessing = ML_preprocessing()

#load models with pickle
models =pickle.load(open('data/classifers.pkl', 'rb'))
IForest = models[0]
Kmeans = models[1]
#Load encoders
with open("data/encoders.pkl","rb") as f:
    encoders =pickle.load(f)
#Index page just to say hello
@app.get('/')
def index():
    return "hello"
#Ml prediction page
@app.post('/predict')
def predict(data : dict):
    try:

        df = pd.DataFrame(data,index=[0])
        df_ml = preprocessing.preprocessingMl(df,encoders)
        df_km = df_ml.copy()
        X_if = df_ml.to_numpy()
        score = IForest.decision_function(X_if)[0].reshape(-1,1)
        s = score[0,0]
        prob  = -s+0.5
        y_pred = Kmeans.predict(score)
        if(y_pred==0):
            return { "classe" : "normal" , "probabilité" : 1-prob }
        else : 
            return { "classe" : "anormal" , "probabilité" : prob}
    except:
        return 'new data'


