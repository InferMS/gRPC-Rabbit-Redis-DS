import grpc
import random, time
from google.protobuf.timestamp_pb2 import Timestamp ;
# import the generated classes
import terminal_pb2
import terminal_pb2_grpc

# open a gRPC channel
channel = grpc.insecure_channel('localhost:50051')

# create a stub (client)
stub = terminal_pb2_grpc.send_resultsStub(channel)

# create a valid request message
while True:
    p1 = []
    w1 = []
    timer = Timestamp()
    timer.GetCurrentTime()
    p1.append(terminal_pb2.pollutionData(coefficient=random.randrange(0,5),timestamp=timer))
    w1.append(terminal_pb2.wellnessData(coefficient=random.randrange(6,10),timestamp=timer))

    data = terminal_pb2.airData(pollution=p1, wellness=w1)
    stub.send_results(data)
    time.sleep(5)


