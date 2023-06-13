import random

import grpc, redis, time, pickle
from google.protobuf.timestamp_pb2 import Timestamp

r = redis.Redis(host='localhost', port=6379)

while True:

    p111 = []
    p222 = []
    w111 = []
    data1 = []
    timer = Timestamp()
    timer.GetCurrentTime()

    pollution = dict()
    pickled_object = pickle.dumps(timer)
    data1 = {"id": 111, "timer_seconds": pickled_object, "value": random.uniform(0.0,2.0)}
    p111.append(data1)
    pollution[111] = p111
    data1 = {"id": 222, "timer_seconds": pickled_object, "value": random.uniform(0.0,2.0)}
    p222.append(data1)
    pollution[111] = p111
    pollution[222] = p222

    wellness = dict()
    pickled_object = pickle.dumps(timer)
    data2 = {"id": 111, "timer_seconds": pickled_object, "value": random.uniform(0.0,2.0)}
    w111.append(data2)
    wellness[111] = w111

    # pollution = {str(key): value for key, value in pollution.items()}
    # wellness = {str(key): value for key, value in wellness.items()}

    # Guardar los bytes en Redis
    pollution_bytes = pickle.dumps(pollution)
    wellness_bytes = pickle.dumps(wellness)

    r.execute_command('SET', 'pollution', pollution_bytes)
    r.execute_command('SET', 'wellness', wellness_bytes)
    # r.set('pollution',pollution)

    # data3 = {"id": 111, "timer_seconds": pickled_object, "value": 23.5}
    # data3_bytes = pickle.dumps(data3)
    # r.append("pollution",data3_bytes)
    time.sleep(2)


