import signal
import threading
import time
import grpc
from concurrent import futures
import grpc_sensor
import sensorLoadBalancer_pb2
import grpc_LoadBalancerServer
import sensorLoadBalancer_pb2_grpc

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

time.sleep(5)

clients = [
    grpc_sensor.Sensor(sensorId=1, sensorType=0),
    grpc_sensor.Sensor(sensorId=2, sensorType=1),
    grpc_sensor.Sensor(sensorId=3, sensorType=0),
    grpc_sensor.Sensor(sensorId=4, sensorType=1),
]

threads = []
for client in clients:
    print(f"Creating thread for sensor {client.sensorId}")
    thread = threading.Thread(target=client.start)
    thread.start()
    threads.append(thread)
print("AllDone")
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    pass

server.stop(0)
for thread in threads:
    thread.join()
