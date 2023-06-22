import pickle, redis, grpc
import terminal_pb2, terminal_pb2_grpc
from google.protobuf.timestamp_pb2 import Timestamp


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
    for id in pollution_dict.keys():
        for pollution_data in pollution_dict[id]:
            timer_deserialized = pickle.loads(pollution_data["timer_seconds"])
            pollution_data["timer_seconds"] = timer_deserialized
    return pollution_dict


def generate_wellness_data():
    timer = Timestamp()
    timer.GetCurrentTime()
    wellness_bytes = r.get("wellness".encode())
    wellness_dict = pickle.loads(wellness_bytes)
    for id in wellness_dict.keys():
        for wellness_data in wellness_dict[id]:
            timer_deserialized = pickle.loads(wellness_data["timer_seconds"])
            wellness_data["timer_seconds"] = timer_deserialized
    return wellness_dict

def run_client(terminals,servers):
    timestamp = 1
    # Configurar la conexión con el servidor
    stubs = []
    for index in range(int(terminals)):
        channel = grpc.insecure_channel(f'localhost:{50051 + int(servers) + int(index) + 1}')
        stubs.append(terminal_pb2_grpc.send_resultsStub(channel))

    while True:
        # Generate new data
        pollution_dict = generate_pollution_data()
        wellness_dict = generate_wellness_data()
        p1 = []
        w1 = []

        for id in pollution_dict.keys():
            for pollution_data in pollution_dict[id]:
                timer = create_timestamp(timestamp)
                pollution_data['timer_seconds'] = timer
                if p_last.get(pollution_data['id']) == None:
                    p1.append(terminal_pb2.pollutionData(id=pollution_data['id'], timestamp=pollution_data['timer_seconds'], coefficient=float(pollution_data['value'])))
                else:
                    if pollution_data['timer_seconds'].seconds == timestamp and (p_last.get(pollution_data['id'])['timer_seconds'].seconds != (pollution_data['timer_seconds'].seconds - timesleep) and p_last.get(pollution_data['id'])['value'] != pollution_data['value']):
                        p1.append(terminal_pb2.pollutionData(id=pollution_data['id'], timestamp=pollution_data['timer_seconds'], coefficient=float(pollution_data['value'])))
                p_last[pollution_data['id']] = pollution_data

        for id in wellness_dict.keys():
            for wellness_data in wellness_dict[id]:
                timer = create_timestamp(timestamp)
                wellness_data['timer_seconds'] = timer
                if w_last.get(wellness_data['id']) == None:
                    w1.append(terminal_pb2.wellnessData(id=wellness_data['id'], timestamp=wellness_data['timer_seconds'], coefficient=float(wellness_data['value'])))
                else:
                    if wellness_data['timer_seconds'].seconds == timestamp and (w_last.get(wellness_data['id'])['timer_seconds'].seconds != (wellness_data['timer_seconds'].seconds - timesleep) and w_last.get(wellness_data['id'])['value'] != wellness_data['value']):
                        w1.append(terminal_pb2.wellnessData(id=wellness_data['id'], timestamp=wellness_data['timer_seconds'], coefficient=float(wellness_data['value'])))
                w_last[wellness_data['id']] = wellness_data

        for x in stubs:
            data = terminal_pb2.airData(pollution=p1, wellness=w1)
            x.send_results(data)

        # time.sleep(timesleep)
        timestamp += 1

if __name__ == '__main__':
    run_client()
