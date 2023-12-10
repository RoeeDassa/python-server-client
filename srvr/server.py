import socket
import protocol
import methods
from constants import IP, PORT, EOF
import threading

# constants
MINIMUM_LENGTH = 1
FIRST_POSITION = 0
SECOND_POSITION = 1
ONE_CLIENT = 1


class Server(object):

    def __init__(self, ip, port):
        self.server_socket = None
        self.initiate_server_socket(IP, PORT)

    @staticmethod
    def receive_client_request(client_socket, address):
        """
        divides a given request to a command and a list of parameters, returns them both
        """
        # read from socket
        request = protocol.Protocol.recv(client_socket)
        methods.Methods.add_to_hist(address, request)
        if request == '':
            return None, None
        # split to request and parameters
        req_and_prms = request.split()
        if len(req_and_prms) > MINIMUM_LENGTH:
            return req_and_prms[FIRST_POSITION].upper(), req_and_prms[SECOND_POSITION:]
        else:
            return req_and_prms[FIRST_POSITION].upper(), None  # no parameters

    @staticmethod
    def handle_client_request(request, params, client_socket, address):
        """
        receives parameters and sends them to functions in methods
        """
        try:
            cls = getattr(methods, "Methods")
            return getattr(cls, request)(params, client_socket, address)
        except Exception as e:
            print("handle_client_request", e)
            if request == 'SEND_FILE':
                self.send_response_to_client(EOF.decode(), client_socket)
            return "illegal command"

    def send_response_to_client(self, response, client_socket):
        """
        sends a response to the client
        """
        protocol.Protocol.send(client_socket, response)

    def initiate_server_socket(self, ip, port):
        """
        initiates the servers sockets
        """
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((ip, port))
            self.server_socket.listen(ONE_CLIENT)
            return self.server_socket
        except socket.error as msg:
            print("Socket error", msg)
        except Exception as msg:
            print("General error", msg)

    def handle_clients(self):
        done = False
        while not done:
            try:
                client_socket, address = self.server_socket.accept()
                methods.Methods.new_hist(address)
                clnt_thread = threading.Thread(target=self.handle_single_client, args=(client_socket, address))
                clnt_thread.start()
            except socket.error as msg:
                print("socket error:", msg)
            except Exception as msg:
                print("general error:", msg)

    def handle_single_client(self, client_socket, address):
        done = False
        while not done:
            try:
                request, params = Server.receive_client_request(client_socket, address)
                response = Server.handle_client_request(request, params, client_socket, address)
                self.send_response_to_client(response, client_socket)
                done = request == 'QUIT'
            except socket.error as e:
                print("booz!! ", e)
                done = True
            except Exception as e:
                print("booozzz!!!", e)
                done = True
        return False


def main():
    """
    sends to the handle clients function the SERVER IP and PORT
    """
    try:
        server = Server(IP, PORT)
        server.handle_clients()
    except socket.error as msg:
        print("Socket error", msg)
    except Exception as msg:
        print("General error", msg)


if __name__ == '__main__':
    main()
