import grpc
from concurrent import futures
import time

# import the generated classes
import sensorLoadBalancer_pb2
import sensorLoadBalancer_pb2_grpc

# import the original insultingServer.py


# create a class to define the server functions, derived from
# insultingServer_pb2_grpc.InsultingServiceServicer
class LoadBalancerServicer(sensorLoadBalancer_pb2_grpc.LoadBalancerServicer):

    def sendMeteoData(self, SensorMeteoData, context):
        # Contactar con server real
        print(f"Meteo Data received from Sensor {SensorMeteoData.id} -> Temperature: {SensorMeteoData.RawMeteoData.temperature} Humidity: {SensorMeteoData.RawMeteoData.humidity}")
        response = sensorLoadBalancer_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response

    def sendPollutionData(self, SensorPollutionData, context):
        # Contactar con server real
        print(f"Pollution Data received from Sensor {SensorPollutionData.id} -> Co2: {SensorPollutionData.RawPollutionData.co2}")
        response = sensorLoadBalancer_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response


