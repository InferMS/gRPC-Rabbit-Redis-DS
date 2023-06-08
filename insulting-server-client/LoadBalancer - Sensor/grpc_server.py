import loadBalancerServer_pb2_grpc
import loadBalancerServer_pb2


class ServerServicer(loadBalancerServer_pb2_grpc.ServerServicer):
    def processMeteoData(self, SensorMeteoData, context):
        # Contactar con server real
        print(
            f"Meteo Data received from Sensor {SensorMeteoData.id} -> Temperature: {SensorMeteoData.RawMeteoData.temperature} Humidity: {SensorMeteoData.RawMeteoData.humidity}")
        response = loadBalancerServer_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response

    def processPollutionData(self, SensorPollutionData, context):
        # Contactar con server real
        print(
            f"Pollution Data received from Sensor {SensorPollutionData.id} -> Co2: {SensorPollutionData.RawPollutionData.co2}")
        response = loadBalancerServer_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response
