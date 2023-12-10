from PIL import ImageGrab
import glob
import os
import shutil
import subprocess
from srvr.constants import EOF, CHUNK_SIZE
from srvr import protocol
import importlib
import sys
import threading

# constants
RECEIVED_FILE_LOCATION = "c:\\test_folder\\client"
FIRST_PARAM = 0
SECOND_PARAM = 1
LAST_PART_OF_FILE_PATH = -1


class Methods:

    hist = {}
    lock = threading.Lock()

    def HISTORY(params, sock, address):
        Methods.lock.acquire()
        rsp = str(Methods.hist[address])
        Methods.lock.release()
        return rsp

    def add_to_hist(address, request):
        Methods.lock.acquire()
        Methods.hist[address].append(request)
        Methods.lock.release()

    def new_hist(address):
        Methods.lock.acquire()
        Methods.hist[address] = []
        Methods.lock.release()

    @staticmethod
    def new_hist(address):
        """
        insert new entry to dict
        """
        Methods.hist[address] = []

    @staticmethod
    def add_to_hist(address, request):
        """
        add a request to dict
        """
        Methods.hist[address].append(request)

    @staticmethod
    def HISTORY(params, sock, address):
        """
        returns history for the given address
        """
        return str(Methods.hist[address])

    @staticmethod
    def QUIT(params, my_socket, address):
        """
        stops only the client
        """
        return "QUIT"

    @staticmethod
    def TAKE_SCREENSHOT(params, my_socket, address):
        """
        takes a screenshot and sends it to
        c:\test_folder\server
        """
        im = ImageGrab.grab()
        im.save('C:\\test_folder\\server\\screen.jpg')
        return "screenshot takenn"

    @staticmethod
    def DIR(params, my_socket, address):
        """
        receives a file location and returns the names of the files,
        and their type that are in that location
        """
        file_list = glob.glob(params[FIRST_PARAM] + r'\*.*')
        return str(file_list)

    @staticmethod
    def DELETE(params, my_socket, address):
        """
        receives a file path and deletes said file
        """
        os.remove(params[FIRST_PARAM])
        return "file deleted"

    @staticmethod
    def COPY(params, my_socket, address):
        """
        receives a file path and copies said file to another file
        """
        shutil.copy(params[FIRST_PARAM], params[SECOND_PARAM])
        return "file copied"

    @staticmethod
    def EXECUTE(params, my_socket, address):
        """
        receives a program path and opens said program
        """
        subprocess.call(params[FIRST_PARAM])
        return "program executed"

    @staticmethod
    def receive_file_request(request, my_socket, address):
        """
        receives a file name and creates a new and corrected name for it
        """
        f = request.split("\\")
        answer_file = RECEIVED_FILE_LOCATION + "\\" + f[LAST_PART_OF_FILE_PATH].lower()
        Methods.receive_file(answer_file, my_socket)

    @staticmethod
    def receive_file(file_name, sock, address):
        """
        gets a file
        """
        done = False
        with open(file_name, 'wb') as f:
            while not done:
                data = protocol.Protocol.recv_bin(sock)
                if data == EOF:
                    done = True
                else:
                    f.write(data)

    @staticmethod
    def SEND_FILE(file_path, socket, address):
        """
        sends a file from the server to the client
        """
        Methods.send_file(file_path[FIRST_PARAM], socket, address)
        return "file sent"

    @staticmethod
    def send_file(file_name, sock, address):
        """
        sends a file from the server to the client
        """
        with open(file_name, 'rb') as f_read:
            bbb = f_read.read(CHUNK_SIZE)
            while True:
                if not bbb:
                    break
                protocol.Protocol.send_bin(sock, bbb)
                bbb = f_read.read(CHUNK_SIZE)
            protocol.Protocol.send_bin(sock, EOF)

    @staticmethod
    def RELOAD(prm, sock, address):
        """
        reloads srvr\methods to be the same as clnt\methods
        """
        Methods.receive_file("methods.py", sock)
        importlib.reload(sys.modules[__name__])
        return "module reloaded"
