from mongoengine import Document,StringField,IntField,ListField

class Regles(Document):
    antecedents = StringField(max_length = 100)
    consequents = ListField()
    support = IntField()
    confidence = IntField()