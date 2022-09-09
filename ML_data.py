import imp
from pydantic import BaseModel

class if_data(BaseModel):
    codeNetwork:int
    codePDA:int
    codeSalePoint:int
    codeService:int
    loginAgent:int
    type:int
    network_groupe_code:int
    spareOp4:int
    montant_total:float
    heure: float
    min : float

class km_data(BaseModel):
    codeNetwork:int
    codePDA:int
    codeSalePoint:int
    codeService:int
    loginAgent:int
    type:int
    network_groupe_code:int
    spareOp4:int
    montant_total:float
    heure: float
    min : float
    score : float