import loadBalancerServer_pb2_grpc
import loadBalancerServer_pb2
import meteo_utils


class ServerServicer(loadBalancerServer_pb2_grpc.ServerServicer):
    def processMeteoData(self, ForwardSensorMeteoData, context):
        # Contactar con server real
        print(
            f"Meteo Data received from LB {ForwardSensorMeteoData.id} -> Temperature: {ForwardSensorMeteoData.RawMeteoData.temperature} Humidity: {ForwardSensorMeteoData.RawMeteoData.humidity}")
        response = loadBalancerServer_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response

    def processPollutionData(self, ForwardSensorPollutionData, context):
        # Contactar con server real
        print(
            f"Pollution Data received from LB {ForwardSensorPollutionData.id} -> Co2: {ForwardSensorPollutionData.RawPollutionData.co2}")
        response = loadBalancerServer_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response
