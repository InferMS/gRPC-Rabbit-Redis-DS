import time

import grpc
from concurrent import futures

import loadBalancerServer_pb2_grpc
import loadBalancerServer_pb2
import meteo_utils
import redis, pickle


class ServerServicer(loadBalancerServer_pb2_grpc.ServerServicer):

    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, decode_responses=False)

    def processMeteoData(self, ForwardSensorMeteoData, context):
        # if self.r.exists('wellness')
        wellness_bytes = self.r.get('wellness'.encode())
        wellness_dict = pickle.loads(wellness_bytes)
        processor = meteo_utils.MeteoDataProcessor()
        wellness = processor.process_meteo_data(ForwardSensorMeteoData.RawMeteoData)
        meteoData = {
            "id": ForwardSensorMeteoData.id,
            "timer_seconds": pickle.dumps(ForwardSensorMeteoData.RawMeteoData.timestamp),
            "value": wellness
        }

        if ForwardSensorMeteoData.id not in wellness_dict:
            wellness_dict[ForwardSensorMeteoData.id] = []

        wellness_dict[ForwardSensorMeteoData.id].append(meteoData)

        # print(wellness_dict[ForwardSensorMeteoData.id])
        wellness_bytes = pickle.dumps(wellness_dict)
        self.r.set('wellness', wellness_bytes)
        response = loadBalancerServer_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response

    def processPollutionData(self, ForwardSensorPollutionData, context):
        # pollution_dict = pickle.loads(self.r.get('pollution'))
        pollution_bytes = self.r.get('pollution'.encode())
        pollution_dict = pickle.loads(pollution_bytes)
        processor = meteo_utils.MeteoDataProcessor()
        quality = processor.process_pollution_data(ForwardSensorPollutionData.RawPollutionData)
        pollutionData = {
            "id": ForwardSensorPollutionData.id,
            "timer_seconds": pickle.dumps(ForwardSensorPollutionData.RawPollutionData.timestamp),
            "value": quality
        }
        if ForwardSensorPollutionData.id not in pollution_dict:
            pollution_dict[ForwardSensorPollutionData.id] = []

        pollution_dict[ForwardSensorPollutionData.id].append(pollutionData)

        pollution_bytes = pickle.dumps(pollution_dict)
        self.r.set('pollution', pollution_bytes)
        response = loadBalancerServer_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response

    def start(index):
        server = (grpc.server(futures.ThreadPoolExecutor(max_workers=10)))
        loadBalancerServer_pb2_grpc.add_ServerServicer_to_server(
            ServerServicer(),
            server
        )
        server.add_insecure_port(f"0.0.0.0:{50051 + index + 1}")
        server.start()

        try:
            while True:
                time.sleep(86400)
        except KeyboardInterrupt:
            pass
        server.stop(0)
