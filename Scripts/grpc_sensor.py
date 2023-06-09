import time

import grpc

# import the generated classes
import meteo_utils
import sensorLoadBalancer_pb2
import sensorLoadBalancer_pb2_grpc
from google.protobuf.timestamp_pb2 import Timestamp


def sendMeteoData(sensorId):
    timestamp = Timestamp()

    detector = meteo_utils.MeteoDataDetector()
    channel = grpc.insecure_channel('localhost:50051')
    stub = sensorLoadBalancer_pb2_grpc.LoadBalancerStub(channel)
    while True:
        timestamp.GetCurrentTime()
        air = detector.analyze_air()
        SensorMeteoData = sensorLoadBalancer_pb2.SensorMeteoData(
            id=sensorId
        )

        SensorMeteoData.RawMeteoData.temperature = air['temperature']
        SensorMeteoData.RawMeteoData.humidity = air['humidity']
        SensorMeteoData.RawMeteoData.timestamp = timestamp

        stub.sendMeteoData(SensorMeteoData)

        time.sleep(1)


def sendPollutionData(sensorId):
    timestamp = Timestamp()

    detector = meteo_utils.MeteoDataDetector()
    channel = grpc.insecure_channel('localhost:50051')
    stub = sensorLoadBalancer_pb2_grpc.LoadBalancerStub(channel)
    while True:
        timestamp.GetCurrentTime()

        pollution = detector.analyze_pollution()
        SensorPollutionData = sensorLoadBalancer_pb2.SensorPollutionData(
            id=sensorId,
        )

        SensorPollutionData.RawPollutionData.co2 = pollution['co2']
        SensorPollutionData.RawPollutionData.timestamp = timestamp

        stub.sendPollutionData(SensorPollutionData)
        time.sleep(1)
