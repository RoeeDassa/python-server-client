SERVER_IP = "127.0.0.1"  # the servers IP
PORT = 1729  # the port
MSG_LEN = 1024  # correct length of message
IP = "127.0.0.1"  # the IP
EOF = b'-999'  # sign to convey that the message has ended
CHUNK_SIZE = 1024  # chunk size
requestType = {
    # all correct names for the functions
    # and how many values they receive
    "DIR": 1,
    "EXIT": 0,
    "QUIT": 0,
    "TAKE_SCREENSHOT": 0,
    "DELETE": 1,
    "COPY": 2,
    "EXECUTE": 1,
    "SEND_FILE": 1,
    "RELOAD": 0,
    "HISTORY": 0
}
