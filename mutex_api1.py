import win32event
import time

TIMEOUT = 100 # timeout - waiting for mutex
SLEEP_TIME = 30 # mutex holding period

def main():
     """
     a script generating mutex and holding it for 30 seconds
     """
     m = win32event.CreateMutex(None, False, 'MyMutex')
     r = win32event.WaitForSingleObject(m, TIMEOUT)
     time.sleep(SLEEP_TIME)
     win32event.ReleaseMutex(m)