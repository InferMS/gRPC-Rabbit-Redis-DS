import random
import hashlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class terminal_service():

    def __init__(self):
        self.dict_pollution = dict()
        self.dict_wellness = dict()
    def send_results(self,pollutionData,wellnessData):

        timestamps1 = []
        timestamps2 = []
        values_pollution = dict()
        values_wellness = dict()
        fig, ax = plt.subplots()

        for x in pollutionData:
            timestamps1.append(str(x.timestamp))
            values_pollution[str(x.timestamp)] = x.coefficient
            self.dict_pollution[x.id] = values_pollution
            #print(timestamps1)
            #print(self.dict_pullution[x.id][str(x.timestamp)])
            for y in timestamps1:
                ax.plot(y, self.dict_pollution[x.id][str(x.timestamp)], marker='o')
        plt.show()
        plt.close()
        for x in wellnessData:
            timestamps2.append(str(x.timestamp))
            values_wellness[str(x.timestamp)] = x.coefficient
            self.dict_wellness[x.id] = values_wellness
            for y in timestamps2:
                ax.plot(y, self.dict_wellness[x.id][str(x.timestamp)], marker='^')
        plt.show()
        plt.close()

terminal_service = terminal_service()
