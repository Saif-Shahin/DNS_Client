# DnsClient

A fully-functional DNS Client program that:
• Is invoked from the command line (STDIN);
• Sends a query to the server for the given domain name using a UDP socket;
• Waits for the response to be returned from the server;
• Interprets the response and outputs the result to terminal display (STDOUT).

The client is capable of the following:
• Sends queries for A (IP addresses), MX (mail server), and NS (name server) records;
• Interprets responses that contain A records (iPad dresses) and CNAME records (Unaliases);
• Retransmits queries that are lost.

# Versions

python 3.10.9


# Usage

```console
$ cd src
$ python DnsClient.py [-h] [-t TIMEOUT] [-r MAXRETRIES] [-p PORT] [-mx | -ns] server name
```

For example:
```console
$ python DnsClient.py -mx -t 10 -r 7 @8.8.8.8 mcgill.ca
```

For more help about options and arguments:
```console
$ python DnsClient.py -h
```
