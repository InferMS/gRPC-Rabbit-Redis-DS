import pickle, redis, grpc, time
import terminal_pb2, terminal_pb2_grpc
from google.protobuf.timestamp_pb2 import Timestamp

'''# open a gRPC channel
channel = grpc.insecure_channel('localhost:50051')
# create a stub (client)
stub = terminal_pb2_grpc.send_resultsStub(channel)'''
# creat a stub (redis)
r = redis.Redis(host='localhost', port=6379, decode_responses=False)

p_last = dict()
w_last = dict()
first_2 = False
timestamp = 1
timesleep = 2

def create_timestamp(seconds):
    timestamp = Timestamp()
    timestamp.FromSeconds(seconds)
    return timestamp

def generate_pollution_data():
    timer = Timestamp()
    timer.GetCurrentTime()
    pollution_bytes = r.get("pollution".encode())
    pollution_dict = pickle.loads(pollution_bytes)
    for x in pollution_dict.keys():
        for y in pollution_dict[x]:
            z = pickle.loads(y["timer_seconds"])
            y["timer_seconds"] = z
    return pollution_dict


def generate_wellness_data():
    timer = Timestamp()
    timer.GetCurrentTime()
    wellness_bytes = r.get("wellness".encode())
    wellness_dict = pickle.loads(wellness_bytes)
    for x in wellness_dict.keys():
        for y in wellness_dict[x]:
            z = pickle.loads(y["timer_seconds"])
            y["timer_seconds"] = z
    return wellness_dict

def run_client(terminals,servers):
    timestamp = 1
    # Configurar la conexión con el servidor
    stubs = []
    for index in range(int(terminals)):
        print(50051 + int(servers) + int(index) + 1)
        channel = grpc.insecure_channel(f'localhost:{50051 + int(servers) + int(index) + 1}')
        stubs.append(terminal_pb2_grpc.send_resultsStub(channel))

    while True:
        # Generate new data
        pollution_dict = generate_pollution_data()
        wellness_dict = generate_wellness_data()
        p1 = []
        w1 = []

        for x in pollution_dict.keys():
            for y in pollution_dict[x]:
                timer = create_timestamp(timestamp)
                y['timer_seconds'] = timer
                if p_last.get(y['id']) == None:
                    p1.append(terminal_pb2.pollutionData(id=y['id'], timestamp=y['timer_seconds'], coefficient=float(y['value'])))
                else:
                    if y['timer_seconds'].seconds == timestamp and (p_last.get(y['id'])['timer_seconds'].seconds != (y['timer_seconds'].seconds - timesleep) and p_last.get(y['id'])['value'] != y['value']):
                        p1.append(terminal_pb2.pollutionData(id=y['id'], timestamp=y['timer_seconds'], coefficient=float(y['value'])))
                p_last[y['id']] = y

        for x in wellness_dict.keys():
            for y in wellness_dict[x]:
                timer = create_timestamp(timestamp)
                y['timer_seconds'] = timer
                if w_last.get(y['id']) == None:
                    w1.append(terminal_pb2.wellnessData(id=y['id'], timestamp=y['timer_seconds'], coefficient=float(y['value'])))
                else:
                    if y['timer_seconds'].seconds == timestamp and (w_last.get(y['id'])['timer_seconds'].seconds != (y['timer_seconds'].seconds - timesleep) and w_last.get(y['id'])['value'] != y['value']):
                        w1.append(terminal_pb2.wellnessData(id=y['id'], timestamp=y['timer_seconds'], coefficient=float(y['value'])))
                w_last[y['id']] = y

        for x in stubs:
            data = terminal_pb2.airData(pollution=p1, wellness=w1)
            x.send_results(data)

        time.sleep(timesleep)
        timestamp += 1

if __name__ == '__main__':
    run_client()
