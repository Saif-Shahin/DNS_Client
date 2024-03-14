import argparse
import socket
from datetime import datetime
from socket import timeout


def get_args():
    parser = argparse.ArgumentParser(description="DNS Client")
    # Adding optional arguments with default values
    parser.add_argument(
        "-t", dest="timeout", default=5, type=int, help="timeout (default: 5)"
    )
    parser.add_argument(
        "-r", dest="maxRetries", default=3, type=int, help="max retries (default: 3)"
    )
    parser.add_argument(
        "-p", dest="port", default=53, type=int, help="port (default: 53)"
    )
    # Adding flags for MX and NS queries
    parser.add_argument(
        "-mx", dest="isMailServer", action="store_true", help="mail server query"
    )
    parser.add_argument(
        "-ns", dest="isNameServer", action="store_true", help="name server query"
    )
    # Adding required arguments for server address and domain name
    parser.add_argument("server", help="server address")
    parser.add_argument("name", help="domain name")
    args = parser.parse_args()

    # Formatting the server address
    args.serverAddress = args.server.replace("@", "")

    # Determining the query type based on the flags provided
    if args.isMailServer and args.isNameServer:
        print("Argument Error: Options -mx and -ns are both true, thus conflicting.")
        exit()
    elif args.isMailServer:
        args.queryType = "MX"
    elif args.isNameServer:
        args.queryType = "NS"
    else:
        args.queryType = "A"  # Defaulting to A record query if no flags are provided

    return args
