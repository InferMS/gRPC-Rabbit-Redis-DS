import random
import hashlib

class terminal_service():

    def __init__(self):
        self.dict_date = dict()
    def send_results(self,pollutionData,wellnessData):
        for x in pollutionData:
            self.dict_date[str(x.timestamp)] = pollutionData[0].coefficient
        for x in wellnessData:
            self.dict_date[str(x.timestamp)] = wellnessData[0].coefficient

        print(self.dict_date)
terminal_service = terminal_service()
