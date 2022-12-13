from typing import Dict

from pymongo import MongoClient
import bson
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import sys
import logging
import pathlib


class Database:
    db_url = "mongodb+srv://dali:dali2908@medicall.x4hyrxq.mongodb.net/?retryWrites=true&w=majority"
    cluster_name = "sensors"
    predictor_filepath = f'{pathlib.Path().resolve()}/server/data/qt_dataset.csv'
    db = 0
    collection = 0
    predictor = 0

    def __init__(self):
        try:
            cluster = MongoClient(self.db_url)
        except:
            logging.error(
                "Cannot connect to Mongo Database. Please check connection and retry. \n"
            )
            sys.exit(1)

        self.db = cluster[self.cluster_name]
        self.patients_collection = self.db["patients"]
        self.records_collection = self.db["records"]
        self.initPredictor()

    def insert_record(self, data: Dict, patient_id: str):
        self.records_collection.insert_one({
            "patient_id":
            patient_id,
            "prediction":
            self.predictSickness(data),
            **data
        })

    def insert_patient(self, data: Dict):
        patient_id = self.patients_collection.count_documents({}) + 1
        self.patients_collection.insert_one({"_id": patient_id, **data})
        print("patients inserted")
        return patient_id

    def find_patient(self, patient_id):
        return self.patients_collection.find_one({"_id": patient_id})

    def initPredictor(self):
        df = pd.read_csv(self.predictor_filepath)
        df.set_index('ID', inplace=True)
        df['Result'].replace(['Positive', 'Negative'], [1, 0], inplace=True)
        x = df.drop('Result', axis=1)
        y = df['Result']
        x_train, x_test, y_train, y_test = train_test_split(x,
                                                            y,
                                                            test_size=0.3)
        # We choose kernel='rbf'
        self.predictor = SVC(C=5, gamma='auto')
        self.predictor.fit(x_train, y_train)

    def predictSickness(self, data):
        d = {
            'Oxy': [data["spo2"]],
            'Pulse': [data["hr"]],
            'Temp': [data["temp"]]
        }
        df = pd.DataFrame(data=d)
        result = self.predictor.predict(df)[0]
        if (result):
            return "sick"
        else:
            return "healthy"
