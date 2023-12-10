# python-server-client
server that can access the clients files and do many actions with them
list of available actions:
1. TAKE_SCREENSHOT: takes a screenshot of the clients screen and sends it to c:\test_folder\server
2. DIR: receives a file location and returns the names of the files, and their type that are in that location
3. DELETE: receives a file path and deletes said file
4. COPY: receives a file path and copies said file to another file
5. EXECUTE: receives a program path and opens said program
6. SENDֹFILE: sends a file from the server to the client
7. RELOAD: reloads srvr\methods to be the same as clnt\methods
8. HISTORY: returns history for the given address
