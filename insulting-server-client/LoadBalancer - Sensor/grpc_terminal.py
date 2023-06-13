import grpc, time
from concurrent import futures
from terminal_service import terminal_service

# import the generated classes
import terminal_pb2
import terminal_pb2_grpc

class send_resultsServicer(terminal_pb2_grpc.send_resultsServicer):

    def __init__(self, servers, id_terminal):
        self.id_terminal = id_terminal
        self.servers = servers
        self.stubs = []
        for index in range(int(servers)):
            channel = grpc.insecure_channel(f"localhost:{int(50051 + int(servers) + int(id_terminal) + 1)}")
            self.stubs.append(terminal_pb2_grpc.send_resultsStub(channel))

    def send_results(self, airData, context):
        terminal_service.send_results(airData.pollution,airData.wellness,self.id_terminal)
        response = terminal_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response

    def run_server(terminals, servers, id_terminal):
        # Configurar el servidor
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        # use the generated function `add_InsultingServiceServicer_to_server`
        # to add the defined class to the server
        terminal_pb2_grpc.add_send_resultsServicer_to_server(
            send_resultsServicer(servers, id_terminal), server)

        # listen on port 50051
        print(f'Starting server. Listening on port {int(50051 + int(servers) + int(id_terminal) + 1)}')
        server.add_insecure_port(f'0.0.0.0:{50051 + int(servers) + int(id_terminal) + 1}')
        server.start()

        # since server.start() will not block,
        # a sleep-loop is added to keep alive
        try:
            while True:
                time.sleep(86400)
        except KeyboardInterrupt:
            server.stop(0)
