import getopt
import random
import signal
import sys
import threading
import time
import grpc
from concurrent import futures
import grpc_sensor
import sensorLoadBalancer_pb2
import grpc_LoadBalancerServer
import sensorLoadBalancer_pb2_grpc

import loadBalancerServer_pb2_grpc
import loadBalancerServer_pb2



def main():
    pollutionSensors = 1
    qualitySensors = 1
    servers_num = 2

    argv = sys.argv[1:]

    opts, args = getopt.getopt(argv, "p:q:s:",
                               ["pollution_sensor=",
                                "quality_sensor=",
                                "servers="])

    for opt, arg in opts:
        if opt in ['-p', '--pollution_sensor']:
            pollutionSensors = arg
        elif opt in ['-q', '--quality_sensor']:
            qualitySensors = arg
        elif opt in ['-s', '--servers']:
            servers_num = arg

    servers = []
    index = 0
    for index in range(int(servers_num)):
        servers[index] = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        index+=1
    loadBalancerServer_pb2_grpc.add_ServerServicer_to_server()
    # create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # use the generated function `add_InsultingServiceServicer_to_server`
    # to add the defined class to the server
    sensorLoadBalancer_pb2_grpc.add_LoadBalancerServicer_to_server(
        grpc_LoadBalancerServer.LoadBalancerServicer(), server)

    # listen on port 50051
    print('Starting LB. Listening on port 50051.')
    server.add_insecure_port('0.0.0.0:50051')
    server.start()

    randomList = []
    clients = []

    for index in range(int(qualitySensors)):
        success = False
        while not success:
            sensorId = random.randint(1, 999)
            if sensorId not in randomList:
                randomList.append(sensorId)
                clients.append(grpc_sensor.Sensor(sensorId=sensorId, sensorType=0))
                success = True

    for index in range(int(pollutionSensors)):
        success = False
        while not success:
            sensorId = random.randint(1, 999)
            if sensorId not in randomList:
                randomList.append(sensorId)
                clients.append(grpc_sensor.Sensor(sensorId=sensorId, sensorType=1))
                success = True

    threads = []
    for client in clients:
        print(f"Creating thread for sensor {client.sensorId}")
        thread = threading.Thread(target=client.start)
        thread.start()
        threads.append(thread)
    for server in servers
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        pass

    server.stop(0)
    for thread in threads:
        thread.join()


main()
