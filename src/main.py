from server import *

# -- CONFIGURATIONS --
SERVER_IP       = "192.168.1.144"
SERVER_PORT     = 28333
SERVER_SOCKET   = None

VIDEO_SOURCE    = "BadApple.mp4"


if __name__ == "__main__":
    
    # Capture video on a separate thread
    
    try:
        # Start socket HTTP server
        SERVER_SOCKET = createSocket(SERVER_IP, SERVER_PORT)
        # Queue up to 5 connections
        SERVER_SOCKET.listen(5)
        print(f"Started MJPEG server on http://{SERVER_IP}:{SERVER_PORT}")
        
        # Handle clients
        # Multithreading is used for the purpose of handling each client connection properly
        # This would've been a problem since our aim is keeping the connection (video stream)
        while True:
            client_socket, client_addr = SERVER_SOCKET.accept()
            print(f"Connection from client {client_addr}")
            handleClient(client_socket, client_addr)
            
    except KeyboardInterrupt:
        print("Exiting gracefully...")
        
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        if SERVER_SOCKET:
            SERVER_SOCKET.close()
            print("Server socket closed.")
        print("Server has been shut.")
    
    pass