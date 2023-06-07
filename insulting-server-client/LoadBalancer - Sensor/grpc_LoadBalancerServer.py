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

    def sendMeteoData(self, RawMeteoData, context):
        # Contactar con server real
        print("a")
        response = sensorLoadBalancer_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response

    def sendPollutionData(self, RawPollutionData, context):
        # Contactar con server real
        print("a")
        response = sensorLoadBalancer_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response


