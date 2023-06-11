import grpc
import random
import time
import terminal_pb2
import terminal_pb2_grpc

# open a gRPC channel
channel = grpc.insecure_channel('localhost:50051')

# create a stub (client)
stub = terminal_pb2_grpc.send_resultsStub(channel)

#r = redis.Redis(host='localhost', port=6379, decode_responses=False)

pollution_dict = dict()
wellness_dict = dict()
p_last = dict()
w_last = dict()
first_2 = False
timestamp = 1

def generate_pollution_data():
    data1 = {"id": 111, "timer_seconds": random.randrange(100, 200), "value": random.randrange(0, 100)}
    data2 = {"id": 222, "timer_seconds": random.randrange(100, 200), "value": random.randrange(0, 100)}
    #pollution_bytes = r.get("pollution".encode())
    pollution_dict['111'] = [data1]
    pollution_dict['222'] = [data2]

def generate_wellness_data():
    data3 = {"id": 111, "timer_seconds": random.randrange(0, 100), "value": random.randrange(0, 100)}
    data4 = {"id": 222, "timer_seconds": random.randrange(0, 100), "value": random.randrange(0, 100)}
    #wellness_bytes = r.get("wellness".encode())
    wellness_dict['111'] = [data3]
    wellness_dict['222'] = [data4]
def run_client():
    timestamp = 1
    # Configurar la conexión con el servidor
    channel = grpc.insecure_channel('localhost:50051')
    stub = terminal_pb2_grpc.send_resultsStub(channel)
    while True:
        # Generate new data
        generate_pollution_data()
        generate_wellness_data()

        p1 = []
        w1 = []

        for x in pollution_dict.keys():
            for y in pollution_dict[x]:
                y['timer_seconds'] = timestamp
                p_last[y['id']] = y
                if y['timer_seconds'] == timestamp:
                    p1.append(terminal_pb2.pollutionData(id=y['id'], timestamp=y['timer_seconds'], coefficient=y['value']))

        for x in wellness_dict.keys():
            for y in wellness_dict[x]:
                y['timer_seconds'] = timestamp
                w_last[y['id']] = y
                if y['timer_seconds'] == timestamp:
                    w1.append(terminal_pb2.wellnessData(id=y['id'], timestamp=y['timer_seconds'], coefficient=y['value']))

        first_2 = True
        data = terminal_pb2.airData(pollution=p1, wellness=w1)
        stub.send_results(data)

        time.sleep(2)
        timestamp += 1

if __name__ == '__main__':
    run_client()
