import queue
from threading import Thread
import socket
from cheese_network.my_helpers import MyHelpers
from cheese_network.cheese_protocol import CheeseProtocol
import random

# magic word
magic_word = "magic"

"""Refactor to load from disk to avoid data loss on restart"""
connected_peers = []


def main():  # called at the end of the file

    # for storing clients requests
    q = queue.Queue()
    #c = consumer(d, q)

    #c.daemon = True  # the program terminates when all non daemon threads are done
    #c.start()


    # start a new thread to accept new connections
    handle_accept_all(q).start()


def handle_accept_all(my_queue):
    def handle():
        # create a socket that listens (on a port of your choice)
        server_socket = socket.socket()
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((CheeseProtocol.TRACKER_HOST, CheeseProtocol.TRACKER_PORT))
        server_socket.listen()
        print(server_socket)
        print('waiting for connection from peers')

        # accept new clients connections,
        while True:
            s, addr = server_socket.accept()  # blocking
            print('received connection', s)

            # notify peer of successful connection
            connection_message = "Connection Successful"
            s.send(connection_message.encode())

            # and start a handle_peer thread every time
            handle_peer(s, my_queue).start()

    t = Thread(target=handle)
    return t


# handle_peer returns a Thread that can be started, i.e., use: handle_peer(.......).start()
# producer
def handle_peer(socket, my_queue):
    def handle(): #add elements to queue
        # initialise a random integer position, e.g. between 0 and 100


        # loop over the received data, ignoring (or just printing) this data for now (e.g., use netutils to read lines)
        # be sure to end the loop when the connection is closed (readLine returns None or throws an exception)
        while True:
            line = MyHelpers.read_line(socket)
            if line is None:
                # remove client from connected peers
                break
            else:
                print("received", line)

                """process request"""
                request_type = CheeseProtocol.process_peer_request(line)

                if request_type == CheeseProtocol.PCONNECT:
                    # get peer host and port
                    request_body = line.split(':')
                    peer_host = request_body[1]
                    peer_port = request_body[2]
                    peer_id = MyHelpers.generate_peer_id()
                    peer_info = {
                        'peer_id': peer_id,
                        'host': peer_host,
                        'port': peer_port,
                        'socket': socket
                    }
                    connected_peers.append(peer_info)
                    print('Tracker\'s connected peers')
                    print(connected_peers)
                    # send peer_id to client, id will be required for other requests
                    response = CheeseProtocol.TCONNECTACK+':'+peer_id
                    socket.send(response.encode())

                if request_type == CheeseProtocol.GETPEERS:
                    peer_data = CheeseProtocol.validate_request(line, connected_peers)
                    if peer_data is not False:
                        connected_peers_sublist = MyHelpers.get_part_of_peers(connected_peers, True)
                        connected_peers_sublist = CheeseProtocol.GETPEERSACK + connected_peers_sublist
                        socket.send(connected_peers_sublist.encode())
                    else:
                        response_message = CheeseProtocol.INVALIDPEERID + '\r\n'
                        socket.send(response_message.encode())


    t = Thread(target=handle)
    return t


def consumer(d, q):
    def consume():
        while True:
            e = q.get()
            if e == "RENDER":
                d.render()
            else:
                i, v, direction = e
                if direction is None:
                    d.add_value(i, v)
                else:
                    d.move_value_right(i, direction, v)

    t = Thread(target=consume)
    return t


def is_magic_word(word):
    if word == magic_word:
        return True
    return False


if __name__ == "__main__":
    main()
