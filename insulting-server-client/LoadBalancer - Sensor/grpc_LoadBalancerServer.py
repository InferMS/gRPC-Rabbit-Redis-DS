import grpc
from concurrent import futures
import time

# import the generated classes
import sensorLoadBalancer_pb2
import sensorLoadBalancer_pb2_grpc
import queue


# import the original insultingServer.py


# create a class to define the server functions, derived from
# insultingServer_pb2_grpc.InsultingServiceServicer
class LoadBalancerServicer(sensorLoadBalancer_pb2_grpc.LoadBalancerServicer):
    requests = queue.Queue()

    def __init__(self, servers_num):
        print("helou")
        self.servers_num = servers_num

    def sendMeteoData(self, SensorMeteoData, context):
        # Contactar con server real
        print(
            f"Meteo Data received from Sensor {SensorMeteoData.id} -> Temperature: {SensorMeteoData.RawMeteoData.temperature} Humidity: {SensorMeteoData.RawMeteoData.humidity}")
        response = sensorLoadBalancer_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response

    def sendPollutionData(self, SensorPollutionData, context):
        # Contactar con server real
        print(
            f"Pollution Data received from Sensor {SensorPollutionData.id} -> Co2: {SensorPollutionData.RawPollutionData.co2}")
        print(self.servers_num)
        response = sensorLoadBalancer_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response

    def start(servers_num):
        # create a gRPC server
        LB = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        # use the generated function `add_InsultingServiceServicer_to_server`
        # to add the defined class to the server
        sensorLoadBalancer_pb2_grpc.add_LoadBalancerServicer_to_server(
            LoadBalancerServicer(servers_num), LB)

        # listen on port 50051
        print('Starting LB. Listening on port 50051.')
        LB.add_insecure_port('0.0.0.0:50051')
        LB.start()

        try:
            while True:
                time.sleep(86400)
        except KeyboardInterrupt:
            pass
        LB.stop(0)

    # def __chooseServer(self):
        # print("hola")
