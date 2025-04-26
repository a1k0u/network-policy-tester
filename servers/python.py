import socket
import argparse
import select

from typing import Union
from argparse import ArgumentTypeError
from enum import Enum

class Protocol(Enum):
    TCP = "tcp"
    UDP = "udp"

class Server:
    def __init__(self, port: int, protocol: Protocol):
        self.port = port
        self.protocol = protocol
        self.socket = None

    @staticmethod
    def parse(v: str) -> Union["Server", ArgumentTypeError]:
        splitted = v.split(':')
        if len(splitted) != 2:
            raise ArgumentTypeError(f"Invalid server format: {v}. Expected <port>:<protocol>")
        
        port, protocol = splitted
        if not port.isdigit():
            raise ArgumentTypeError(f"Invalid port: {port}. Expected a number")
        
        port = int(port)
        if port < 0 or port > 65535:
            raise ArgumentTypeError(f"Invalid port: {port}. Expected a number between 0 and 65535")

        protocol = protocol.upper()
        if protocol not in Protocol.__members__:
            raise ArgumentTypeError(f"Invalid protocol: {protocol}. Expected one of {list(Protocol.__members__.keys())}")
        
        return Server(port, Protocol[protocol])
    
    def create(self) -> socket.socket:
        k: socket.SocketKind = socket.SOCK_STREAM
        if self.protocol == Protocol.UDP:
            k = socket.SOCK_DGRAM

        self.socket = socket.socket(socket.AF_INET, k)
        self.socket.bind(('', self.port))

        print(f"Listening on port {self.port} with protocol {self.protocol.name}")

        if self.protocol == Protocol.TCP:
            self.socket.listen(1)

        return self.socket

parser = argparse.ArgumentParser(
                    prog='Socket Server',
                    description='Accept client connection and returns id, protocol and port number',
                    epilog='Made for kubernetes network testing')

parser.add_argument('-S', '--servers', nargs='+', required=True, type=Server.parse, help='List of servers to listen on in format <port>:<protocol>')

args = parser.parse_args()

if __name__ == "__main__":
    sockets = [s.create() for s in args.servers]

    while True:
        readable, _, _ = select.select(sockets, [], [])
        for s in readable:
            protocol = next(server.protocol for server in args.servers if server.socket == s)
            if protocol == Protocol.TCP:
                conn, addr = s.accept()
                print(f"[TCP] Connection from {addr} on port {conn.getsockname()[1]}")
                conn.sendall(b"hello tcp\n")
                conn.close()
            else:
                data, addr = s.recvfrom(1024)
                print(f"[UDP] Packet from {addr} on port {s.getsockname()[1]}")
                s.sendto(b"hello udp\n", addr)
