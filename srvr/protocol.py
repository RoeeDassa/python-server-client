SIZE_TO_FILL = 4
MINIMUM_SIZE = 0


class Protocol:

    @staticmethod
    def send(socket, data):
        """
        sends the file in chunks
        """
        encoded_msg = data.encode()
        l = len(encoded_msg)
        ll = str(l)
        lll = ll.zfill(SIZE_TO_FILL)
        llll = lll.encode()
        socket.send(llll + encoded_msg)

    @staticmethod
    def recv(sock):
        """
        receives the data
        """
        TOTAL_SIZE = b""
        SIZE = 4
        TOTAL_DATA = b""
        while SIZE > MINIMUM_SIZE:
            data = sock.recv(SIZE)
            SIZE -= len(data)
            TOTAL_SIZE = TOTAL_SIZE + data
        SIZE = int(TOTAL_SIZE.decode())
        while SIZE > MINIMUM_SIZE:
            data = sock.recv(SIZE)
            SIZE -= len(data)
            TOTAL_DATA += data
        return TOTAL_DATA.decode()

    @staticmethod
    def send_bin(sock, data):
        """
        sends the info to the file
        """
        lenn = len(data)
        ll = str(lenn)
        lll = ll.zfill(SIZE_TO_FILL)
        sock.send(lll.encode() + data)

    @staticmethod
    def recv_bin(sock):
        """
        receives the data
        """
        raw_size = 4
        data_size = ''
        while raw_size > MINIMUM_SIZE:
            data_size = sock.recv(raw_size)
            raw_size -= len(data_size)
        tot_data = b''
        if data_size.isdigit():
            size = int(data_size)
            while size > MINIMUM_SIZE:
                data = sock.recv(size)
                size -= len(data)
                tot_data += data
        return tot_data
