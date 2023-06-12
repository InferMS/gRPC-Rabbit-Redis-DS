import grpc
from concurrent import futures
import time

# import the generated classes
import sensorLoadBalancer_pb2
import sensorLoadBalancer_pb2_grpc
import loadBalancerServer_pb2_grpc
import loadBalancerServer_pb2
import queue
from google.protobuf.timestamp_pb2 import Timestamp


# import the original insultingServer.py


# create a class to define the server functions, derived from
# insultingServer_pb2_grpc.InsultingServiceServicer
class LoadBalancerServicer(sensorLoadBalancer_pb2_grpc.LoadBalancerServicer):
    requests = queue.Queue()

    def __init__(self, servers_num):
        self.servers_num = servers_num
        sechannels = []
        self.stubs = []
        for index in range(int(servers_num)):
            print("caca")
            channel = grpc.insecure_channel(f"localhost:{50051+index+1}")
            print("culo")
            self.stubs.append(loadBalancerServer_pb2_grpc.ServerStub(channel))


    def sendMeteoData(self, SensorMeteoData, context):
        # Contactar con server real
        print(
            f"Meteo Data received from Sensor {SensorMeteoData.id} -> Temperature: {SensorMeteoData.RawMeteoData.temperature} Humidity: {SensorMeteoData.RawMeteoData.humidity}")
        response = sensorLoadBalancer_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        self.__forwardMeteoData(SensorMeteoData)
        return response

    def sendPollutionData(self, SensorPollutionData, context):
        # Contactar con server real
        print(
            f"Pollution Data received from Sensor {SensorPollutionData.id} -> Co2: {SensorPollutionData.RawPollutionData.co2}")
        response = sensorLoadBalancer_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        self.__forwardPollutionData(SensorPollutionData)
        return response

    def __forwardPollutionData(self, SensorPollutionData):
        print("aki llego")
        ForwardSensorPollutionData = loadBalancerServer_pb2.ForwardSensorPollutionData(
            id=SensorPollutionData.id
        )
        ForwardSensorPollutionData.RawPollutionData.co2 = SensorPollutionData.RawPollutionData.co2
        ForwardSensorPollutionData.RawPollutionData.timestamp = SensorPollutionData.RawPollutionData.timestamp

        self.__chooseServer(SensorPollutionData.id).processPollutionData(ForwardSensorPollutionData)

    def __forwardMeteoData(self, SensorMeteoData):
        print("aki llego")
        ForwardSensorMeteoData = loadBalancerServer_pb2.ForwardSensorMeteoData(
            id=SensorMeteoData.id
        )
        ForwardSensorMeteoData.RawMeteoData.temperature = SensorMeteoData.RawMeteoData.temperature
        ForwardSensorMeteoData.RawMeteoData.humidity = SensorMeteoData.RawMeteoData.humidity
        ForwardSensorMeteoData.RawMeteoData.timestamp = SensorMeteoData.RawMeteoData.timestamp
        self.__chooseServer(SensorMeteoData.id).processMeteoData(ForwardSensorMeteoData)

    def __chooseServer(self, sensorId):
        print(f"mandando a {sensorId % int(self.servers_num)}")
        return self.stubs[sensorId % int(self.servers_num)]

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
