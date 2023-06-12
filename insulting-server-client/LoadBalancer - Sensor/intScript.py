import getopt
import sys
import threading
import time
import grpc_terminal, grpc_proxy
def main():
    servers_num = 2
    terminals = 2

    argv = sys.argv[1:]

    opts, args = getopt.getopt(argv, "s:t:",
                               ["servers=",
                                "terminals="])

    for opt, arg in opts:
        if opt in ['-s', '--servers']:
            servers_num = arg
        elif opt in ['-t', '--terminals']:
            terminals = arg

    threads = []

    for index in range(int(terminals)):
        thread = threading.Thread(target=grpc_terminal.send_resultsServicer.run_server, args=(terminals, servers_num, int(index + 1),))
        thread.start()
        threads.append(thread)

    thread = threading.Thread(target=grpc_proxy.run_client, args=(terminals, servers_num,))
    thread.start()
    threads.append(thread)

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        pass

    for thread in threads:
        thread.join()

main()