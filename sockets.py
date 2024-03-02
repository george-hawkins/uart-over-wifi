import socket


def connect(host, port):
    socket_address = socket.getaddrinfo(host, port, 0, socket.SOCK_STREAM)[0][-1]

    sock = socket.socket()
    # I've seen connect fail with `OSError: [Errno 104] ECONNRESET` so, make sure to call in try: reset setup.
    sock.connect(socket_address)
    sock.setblocking(False)  # The default is blocking.

    print(f"connected to server {host}:{port}")

    return sock


def accept(port):
    bind_address = socket.getaddrinfo('0.0.0.0', port, 0, socket.SOCK_STREAM)[0][-1]

    server = socket.socket()
    server.bind(bind_address)
    server.listen(1)

    client, client_address = server.accept()
    client.setblocking(False)  # The default is blocking.

    server.close()
    print(f"client socket connected from {client_address[0]}")

    return client
