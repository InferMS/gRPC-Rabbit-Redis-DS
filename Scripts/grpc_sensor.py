import time
from enum import Enum

import grpc

# import the generated classes
import meteo_utils
import sensorLoadBalancer_pb2
import sensorLoadBalancer_pb2_grpc
from google.protobuf.timestamp_pb2 import Timestamp

class Sensor:
    def __init__(self, sensorId, sensorType):
        self.sensorId = sensorId
        self.sensorType = sensorType
        channel = grpc.insecure_channel('localhost:50051')
        self.stub = sensorLoadBalancer_pb2_grpc.LoadBalancerStub(channel)

    def sendData(self):
        timestamp = Timestamp()
        timestamp.GetCurrentTime()
        detector = meteo_utils.MeteoDataDetector()
        # MeteoData
        if self.sensorType == 0:
            self.__sendMeteoData(detector, timestamp)
        # PollutionData
        if self.sensorType == 1:
            self.__sendPollutionData(detector, timestamp)

    def __sendMeteoData(self, detector, timestamp):
        air = detector.analyze_air()
        SensorMeteoData = sensorLoadBalancer_pb2.SensorMeteoData(
            id=self.sensorId
        )

        SensorMeteoData.RawMeteoData.temperature=air['temperature']
        SensorMeteoData.RawMeteoData.humidity=air['humidity']
        SensorMeteoData.RawMeteoData.timestamp=timestamp

        self.stub.sendMeteoData(SensorMeteoData)

    def __sendPollutionData(self, detector, timestamp):
        pollution = detector.analyze_pollution()
        SensorPollutionData = sensorLoadBalancer_pb2.SensorPollutionData(
            id=self.sensorId,
        )

        SensorPollutionData.RawPollutionData.co2 = pollution['co2']
        SensorPollutionData.RawPollutionData.timestamp = timestamp

        self.stub.sendPollutionData(SensorPollutionData)

    def start(self):
        while True:
            time.sleep(5)
            self.sendData()
