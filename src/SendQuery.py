import socket
from socket import timeout

import BuildQuery
import time

import RecordResponse


def sendQuery(args):
    # Creating a UDP socket
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    mySocket.settimeout(args.timeout)  # Setting the socket timeout
    query = BuildQuery.buildQuery(args.name, args.queryType)  # Building the query
    print(f"DnsClient sending request for {args.name}")
    print(f"Server: {args.serverAddress}")
    print(f"Request type: {str(args.queryType)}\n")

    # Looping for the specified number of retries
    for attempt in range(1, args.maxRetries + 1):
        try:
            startTime = time.time_ns()
            # Sending the query
            mySocket.sendto(query, (args.serverAddress, args.port))

            recvBuff, recvAddress = mySocket.recvfrom(1020)

            endTime = time.time_ns()

            mySocket.close()

            elapsed_time = (endTime - startTime) / 1e9

            print(
                f"Response received after {elapsed_time} seconds ({attempt - 1} retries)"
            )
            RecordResponse.recordResponse(recvBuff)
            break

        except socket.timeout:
            print("Request timed out")  # Printing a message if the request times out
            print(f"ERROR:\tSocket Timeout {socket.timeout}")
            if attempt < args.maxRetries:
                print("Reattempting request...")
        except (socket.gaierror, socket.herror) as e:
            print(f"ERROR:\tUnknown host: {e}")

        except socket.error as e:
            print(f"ERROR:\tCould not create socket: {e}")

        except Exception as e:
            print(f"ERROR:\t {e}")

        if attempt == args.maxRetries:
            print(
                f"ERROR:\tFailed to receive response after {args.maxRetries} retries "
            )
