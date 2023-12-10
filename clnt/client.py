import socket
import sys
import winreg
import methods
import protocol
from constants import IP, PORT, EOF, requestType

# constants
REQUEST_FIRST_WORD = 0
REQUEST_SECOND_WORD = 1
CORRECT_LEN = 2
SECOND_POSITION = 1
VALUES_COUNT = 2


class Client(object):

    def __init__(self):
        self.my_socket = None
        self.initiate_client_socket(IP, PORT)

    def read_reg(self):
        ip = IP
        port = PORT
        # open registry keyValues_COUNT = 2
        winreg.RawKey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                         R"SOFTWARE\\Technition Server")
        for i in range(VALUES_COUNT):
            try:
                name, value, winreg.type = winreg.EnumValue(winreg.RawKey, i)
                if name == "IP":
                    ip = value
                if name == "port":
                    port = value
                print(i, name, value, type)
            except EnvironmentError:
                print("You have ", i, " values")
                break
            winreg.CloseKey(winreg.RawKey)
            return ip, port

    def initiate_client_socket(self, ip, port):
        """
        initiates the clients socket
        """
        try:
            self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.my_socket.connect((ip, port))
        except socket.error as msg:
            print("socket error:", msg)
            sys.exit(1)
        except Exception as msg:
            print("general error:", msg)
            sys.exit(1)

    @staticmethod
    def valid_request(request):
        """
        checks if the received request is valid (is one of the functions and
        gave the correct parameters)
        """
        request = request.upper()
        request_list = request.split()
        if request_list[REQUEST_FIRST_WORD] in requestType.keys():
            if len(request_list[REQUEST_SECOND_WORD:]) == requestType[request_list[REQUEST_FIRST_WORD]]:
                return True
            else:
                return False
        elif request_list[REQUEST_FIRST_WORD] == 'SEND_FILE' and len(request_list) == CORRECT_LEN:
            return True
        else:
            return False

    def send_request_to_server(self, request):
        """
        sends a request to the server
        """
        protocol.Protocol.send(self.my_socket, request)
        if request.upper() == "RELOAD":
            methods.Methods.send_file("methods.py", self.my_socket)

    def handle_server_response(self, request):
        """
        receives the server answer and prints it
        """
        if request.split()[REQUEST_FIRST_WORD] == 'SEND_FILE':
            methods.Methods.receive_file_request(request.split()[SECOND_POSITION], self.my_socket)
        server_answer = protocol.Protocol.recv(self.my_socket)
        if server_answer == EOF.decode():
            server_answer = "illegal command"
        return server_answer

    def send_command(self, request):
        rsp = ""
        if self.valid_request(request):
            self.send_request_to_server(request)
            rsp = self.handle_server_response(request)
        else:
            return "request NOT valid"
        return rsp

    def handle_user_input(self):
        """
        receives a string for the user (the request) and sends to the server
        and prints the answer from server in bytes and strings
        """
        try:
            request = ""
            while request.upper() != "QUIT" and request.upper() != "EXIT":
                request = input("please enter a request ")
                request = request.upper()
                if self.valid_request(request):
                    self.send_request_to_server(request)
                    self.handle_server_response(request)
                else:
                    print("illegal request")
            self.my_socket.close()
        except socket.error as msg:
            print("socket error", msg)
        except Exception as msg:
            print("general error", msg)


def main():
    """
    sends to the handle user input function the IP and PORT
    """
    client = Client()
    client.handle_user_input()


if __name__ == '__main__':
    main()
