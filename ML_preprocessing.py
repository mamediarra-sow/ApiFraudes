import pickle
import numpy as np
import pandas as pd
class ML_preprocessing:

    def __init__(self):
        pass
   
    #Encoder les heures
    def cos_encoding_hour(self,x):
        return np.cos((x/24)*2*np.pi)

    #Encoder les minutes
    def cos_encoding_min(self,x):
        return np.cos((x/60)*2*np.pi)
    
    #Fonction global
    def encode_time(self,dataset):
        dataset[['heure','min','sec']] = dataset.heure_trx.str.split(":",expand=True)
        dataset.drop(['heure_trx','sec'],1,inplace=True)
        dataset['heure'] = dataset['heure'].astype("int64").apply(self.cos_encoding_hour)
        dataset['min'] = dataset['min'].astype("int64").apply(self.cos_encoding_min)
        return dataset
    
    def preprocessingMl(self,transaction,encoders):
        transaction[['date_trx','heure_trx']] = transaction.date.str.split(" ",expand=True)
        transaction['montant'] = pd.to_numeric(transaction['montant'])
        transaction['montant_total']  = transaction[['montant','frais']].sum(axis=1)
        transaction.drop(['date','montant','frais'],1, inplace=True)
        transaction['loginAgent'].astype(str)
        df_ml = transaction[['codeNetwork','codePDA',	'codeSalePoint',	'codeService',	'loginAgent','type','network_groupe_code','spareOp4',	'montant_total','heure_trx']]
        for name in df_ml.columns:
            if df_ml[name].dtype == 'O' and name != "heure_trx":
                clf = encoders[name]
                df_ml[name] = clf.transform(df_ml[name])
        df_ml = self.encode_time(df_ml)
        return df_ml
