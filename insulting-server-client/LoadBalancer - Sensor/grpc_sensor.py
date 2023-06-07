import time
from enum import Enum

import grpc

# import the generated classes
import meteo_utils
import sensorLoadBalancer_pb2
import sensorLoadBalancer_pb2_grpc


class Sensor:
    def __init__(self, sensorId, sensorType):
        self.sensorId = sensorId
        self.sensorType = sensorType
        channel = grpc.insecure_channel('localhost:50051')
        self.stub = sensorLoadBalancer_pb2_grpc.LoadBalancerStub(channel)

    def sendData(self):
        detector = meteo_utils.MeteoDataDetector()
        # MeteoData
        if self.sensorType == 0:
            self.__sendMeteoData(detector)
        # PollutionData
        if self.sensorType == 1:
            self.__sendPollutionData(detector)

    def __sendMeteoData(self, detector):
        air = detector.analyze_air()
        RawMeteoData = sensorLoadBalancer_pb2.RawMeteoData(temperature=air["temperature"], humidity=air["humidity"])
        print(f"Sensor {self.sensorId} sending MeteoData")
        self.stub.sendMeteoData(RawMeteoData)

    def __sendPollutionData(self, detector):
        pollution = detector.analyze_pollution()
        pollutionData = sensorLoadBalancer_pb2.RawPollutionData(co2=pollution["co2"])
        print(f"Sensor {self.sensorId} sending PollutionData")
        self.stub.sendPollutionData(pollutionData)

    def start(self):
        while True:
            time.sleep(5)
            self.sendData()
