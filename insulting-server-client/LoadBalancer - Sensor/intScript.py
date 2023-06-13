import getopt
import sys
import grpc_terminal, grpc_proxy
import matplotlib
matplotlib.use('TkAgg')
import multiprocessing
import time

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

    processes = []


    for index in range(int(terminals)):
        process = multiprocessing.Process(target=grpc_terminal.send_resultsServicer.run_server, args=(terminals, servers_num, index + 1,))
        process.start()
        processes.append(process)

    process = multiprocessing.Process(target=grpc_proxy.run_client, args=(terminals, servers_num,))
    process.start()
    processes.append(process)

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        pass

    for process in processes:
        process.terminate()
        process.join()

if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()
