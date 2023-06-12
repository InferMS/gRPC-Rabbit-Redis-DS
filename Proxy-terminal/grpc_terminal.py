import grpc, time
from concurrent import futures
from terminal_service import terminal_service

# import the generated classes
import terminal_pb2
import terminal_pb2_grpc

class send_resultsServicer(terminal_pb2_grpc.send_resultsServicer):

    def send_results(self, airData, context):
        terminal_service.send_results(airData.pollution,airData.wellness)
        response = terminal_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response

def run_server(port):
    # Configurar el servidor
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    terminal_pb2_grpc.add_send_resultsServicer_to_server(
        send_resultsServicer(), server)
    server.add_insecure_port(f'localhost:{port}')

    # Iniciar el servidor
    server.start()
    print(f'Starting server. Listening on port {port}.')

    # Mantener el servidor en ejecución
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    base_port = 50051  # Puerto base
    num_servers = 1  # Número total de servidores que deseas ejecutar

    for i in range(num_servers):
        port = base_port + i
        run_server(port)
"""
# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

# use the generated function `add_InsultingServiceServicer_to_server`
# to add the defined class to the server
terminal_pb2_grpc.add_send_resultsServicer_to_server(
    send_resultsServicer(), server)

# listen on port 50051
print('Starting server. Listening on port 50051.')
server.add_insecure_port('0.0.0.0:50051')
server.start()

# since server.start() will not block,
# a sleep-loop is added to keep alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
"""