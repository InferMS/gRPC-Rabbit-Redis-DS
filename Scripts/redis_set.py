import grpc, redis, time, pickle
from google.protobuf.timestamp_pb2 import Timestamp

r = redis.Redis(host='localhost', port=6379)

p111 = []
w111 = []

timer = Timestamp()
timer.GetCurrentTime()

pollution = dict()
pickled_object = pickle.dumps(timer)
data1 = {"id": 111, "timer_seconds": pickled_object, "value": 0.5}
p111.append(data1)
pollution[111] = p111

wellness = dict()
pickled_object = pickle.dumps(timer)
data2 = {"id": 111, "timer_seconds": pickled_object, "value": 1.5}
w111.append(data2)
wellness[111] = w111


pollution_bytes = pickle.dumps(pollution)
wellness_bytes = pickle.dumps(wellness)

r.execute_command('SET', 'pollution', pollution_bytes)
r.execute_command('SET', 'wellness', wellness_bytes)

data3 = {"id": 111, "timer_seconds": pickled_object, "value": 23.5}
data3_bytes = pickle.dumps(data3)
r.append("pollution",data3_bytes)



