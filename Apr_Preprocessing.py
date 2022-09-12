import numpy as np
import pandas as pd

class AP_preprocessing():

    def __init__(self):
        pass
    #Transformer heure
    def transform_heure_rules(self,dataset):
        dataset['heure'] = dataset.heure_trx.str.split(":",expand=True)[0]
        dataset.drop('heure_trx',1,inplace=True) 
        dataset = dataset.astype({"heure": int}, errors='raise') 
        dataset['heure'] = np.where(dataset['heure']<8,'fermeture',np.where(dataset['heure']<16,'journee',
                                                                    np.where(dataset['heure']<20,'soir','nuit')))
        return dataset
    #Transformer montant
    def transform_montant(self,dataset):
        dataset['montant_total'] = np.where(dataset['montant_total']<70000.0,'faible',np.where(dataset['montant_total']<232300.0,'moyen',
                                                            np.where(dataset['montant_total']<2000000.0,'elevé','très elevé')))
        return dataset
    #Preprocessing pour l'algorithme apriori
    def apr_preprocessing(self, transaction):
        transaction[['date_trx','heure_trx']] = transaction.date.str.split(" ",expand=True)
        transaction['montant'] = pd.to_numeric(transaction['montant'])
        transaction['montant_total']  = transaction[['montant','frais']].sum(axis=1)
        transaction.drop(['date','montant','frais'],1, inplace=True)
        transaction['loginAgent'].astype(str)
        df_rules  = transaction[['codeService','loginAgent','network_groupe_code','spareOp4',	'montant_total','heure_trx']]
        df_rules = self.transform_heure_rules(df_rules)
        df_rules = self.transform_montant(df_rules)
        return df_rules