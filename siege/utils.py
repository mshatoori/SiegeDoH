import socket
import time
import typing

import dns.message
import dns.query


def send_dns_query(domain: str, sock: socket.socket, server_ip: str) -> typing.Tuple[int, float]:
    if sock is None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    query = dns.message.make_query(qname=domain, rdtype='A')
    timeout = time.time() + 3  # 3 seconds timeout
    return dns.query.send_udp(sock, query, (server_ip, 53), timeout)
