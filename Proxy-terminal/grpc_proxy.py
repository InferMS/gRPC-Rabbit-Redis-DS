import grpc, random, time, redis, pickle
from google.protobuf.timestamp_pb2 import Timestamp;
# import the generated classes
import terminal_pb2, terminal_pb2_grpc

# open a gRPC channel
channel = grpc.insecure_channel('localhost:50051')

# create a stub (client)
stub = terminal_pb2_grpc.send_resultsStub(channel)
r = redis.Redis(host='localhost', port=6379, decode_responses=False)
first = False
threshold = 0

# create a valid request message
while True:
    timer = Timestamp()
    timer.GetCurrentTime()

    # pollution_bytes = r.execute_command('GET', 'pollution')
    # wellness_bytes = r.execute_command('GET', 'wellness')

    pollution_bytes = r.get("pollution".encode())
    wellness_bytes = r.get("wellness".encode())

    pollution_dict = pickle.loads(pollution_bytes)
    wellness_dict = pickle.loads(wellness_bytes)

    if threshold==0 and first==False:
        first = True
    else:
        threshold+=1

    for x in pollution_dict.keys():
        for y in pollution_dict[x]:
            if threshold==0:
                y["timer_seconds"]= 0
            else:
                y["timer_seconds"]= threshold

    for x in wellness_dict.keys():
        for y in wellness_dict[x]:
            if threshold==0:
                y["timer_seconds"]= 0
            else:
                y["timer_seconds"]= threshold

    p1 = []
    w1 = []
    for x in pollution_dict.keys():
        for y in pollution_dict[x]:
            p1.append(terminal_pb2.pollutionData(id=y['id'], timestamp=timer.FromSeconds(y['timer_seconds']), coefficient=y['value']))

    for x in wellness_dict.keys():
        for y in wellness_dict[x]:
            w1.append(terminal_pb2.wellnessData(id=y['id'], timestamp=timer.FromSeconds(y['timer_seconds']), coefficient=y['value']))

    #data = terminal_pb2.airData(pollution=p1, wellness=w1)
    #stub.send_results(data)
    time.sleep(2)
