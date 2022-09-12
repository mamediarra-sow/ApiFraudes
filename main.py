import sklearn
from fastapi import FastAPI
import numpy as np
from typing import Any, Dict, List, Union
import pickle
from ML_data import *
from ML_preprocessing import *
from Apr_Preprocessing import *
import pandas as pd
from mongoengine import connect
from models import Regles
import json
import ast

#Initiate an APP
app = FastAPI()

#Connection to mongo
connect(db ='rules', host='localhost', port=27017)

#Variable Initiation
df_ml : if_data
preprocessing_ml = ML_preprocessing()
preprocessing_rl = AP_preprocessing()

#Load models
models = pickle.load(open('data/classifers.pkl', 'rb'))
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
        """try : """
        score_ap = 0
        cons = []
        df = pd.DataFrame(data,index=[0])
        df_1 = df.copy()
        df_2 = df.copy()
        #Dataset machine learning
        df_ml = preprocessing_ml.preprocessingMl(df_1,encoders)
        #Dataset apriori
        df_rl = preprocessing_rl.apr_preprocessing(df_2)
        #################################################
        #Traitement ML
        df_km = df_ml.copy()
        X_if = df_ml.to_numpy()
        score_ml = IForest.decision_function(X_if)[0].reshape(-1,1)
        s = score_ml[0,0]
        prob_ml = -s+0.5
        y_pred = Kmeans.predict(score_ml)
        ###############################################
        #Traitement Apriori
        agent = df_rl['loginAgent'][0]
        col = df_rl.columns
        rules  = json.loads(Regles.objects(antecedents = agent).to_json())
        for r in rules:
            cons.append(ast.literal_eval((r['consequents'])))
        cons = np.array(cons)
        for c in col:
            if c!='loginAgent':
                el = df_rl[c][0]
                if(el in cons):
                    score_ap +=1 
        prob_ap = score_ap/5
        print(prob_ap)

        ##############################################
        if(y_pred==0 and prob_ap<0.6):
            return [    {"ml_predict" : "normal" , "probabilité de fraude" : prob_ml},
                        {"ap_predict" : "anormal" , "probabilité de fraude" : 1-prob_ap} ]
        elif(y_pred==0 and prob_ap>0.6):
            return [  {"ml_predict" : "normal" , "probabilité de fraude" : prob_ml},
                        {"ap_predict" : "normal" , "probabilité de fraude" : 1-prob_ap} ]
        elif(y_pred==1 and prob_ap<0.6):
            return [    {"ml_predict" : "anormal" , "probabilité de fraude" : prob_ml},
                        {"ap_predict" : "anormal" , "probabilité de fraude" : 1-prob_ap} ]

        else : 
            return [    {"ml_predict" : "anormal" , "probabilité de fraude" : prob_ml},
                        {"ap_predict" : "normal" ,  "probabilité de fraude" : 1-prob_ap} ]
        #Traitement apriori"""
        """except:
        return "new data"""

#get from mongodb
@app.get('/rules')
def get_all():
    rules  = json.loads(Regles.objects(antecedents = "776084616").to_json())
    return {"rules":rules}