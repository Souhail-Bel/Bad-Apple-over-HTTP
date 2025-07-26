import sys
import socket
import threading
# from typing import Union, Tuple

# Preload HTML page
try:
    with open('res/index.html', 'r') as f:
        HTML_FRAME = f.read()
    HTML_BYTES = HTML_FRAME.encode('utf-8', errors='replace')
    HTML_RESPONSE = b"".join([
        b"HTTP/1.1 200 OK\r\n",
        b"Content-Type: text/html\r\n",
        f"Content-Length: {len(HTML_BYTES)}\r\n".encode('utf-8'),
        b"Connection: close\r\n",
        b"\r\n",
        HTML_BYTES
    ])
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)


def startServer(HOST: str, PORT: int):
    """
    Start a server bound to HOST:PORT and listen for client requests
    
    Args:
        HOST: string, representing the IPv4 address of the host
        PORT: integer, representing the port
    
    Returns:
        void
    """
    
    try:
        # Start socket HTTP server
        SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Allow reuse to avoid conflict next time
        SERVER_SOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        SERVER_SOCKET.bind((HOST, PORT))
        # Queue up to 5 connections
        SERVER_SOCKET.listen(5)
        print(f"🌐 Started MJPEG server on http://{HOST}:{PORT}")
        
        # Handle clients
        # Multithreading is used for the purpose of handling each client connection properly
        # This would've been a problem since our aim is keeping the connection (video stream)
        while True:
            client_socket, client_addr = SERVER_SOCKET.accept()
            print(f"🔗 Connection from client {client_addr}")
            # handleClient(client_socket, client_addr)
            
            # Start a new thread to handle each client connection
            client_thread = threading.Thread(target=handleClient, args=(client_socket, client_addr), daemon=True)
            client_thread.start()
            
    except KeyboardInterrupt:
        print("Exiting gracefully...")
        
    except Exception as e:
        print(f"❌ Server error: {e}")
        
    finally:
        if SERVER_SOCKET:
            SERVER_SOCKET.close()
            print("Server socket closed.")
        print("🛑 Server has been shut.")

def handleClient(client_socket: socket.socket, client_addr: str):
    """
    Handle one client request and send an appropriate response
    
    Args:
        client_socket: socket.socket, the client connection socket
        client_addr: Tuple[str, int] or str (for simplicity), the client address
    
    Returns:
        void
    """
    
    try:
        request = client_socket.recv(4096).decode('UTF-8', errors='replace')
        
        request_lines = request.split('\r\n')
        request_head = request_lines[0].strip()
        print(f"Request: {request_head}")
        path = request_head.split(' ')[1]
        
        if path == '/badapple.jpg':
            try:
                with open('res/badapple.jpg', 'rb') as f:
                    IMAGE_BYTES = f.read()
                
                IMAGE_RESPONSE = b"".join([
                    b"HTTP/1.1 200 OK\r\n",
                    b"Content-Type: image/jpeg\r\n",
                    f"Content-Length: {len(IMAGE_BYTES)}\r\n".encode('utf-8'),
                    b"Connection: close\r\n",
                    b"\r\n",
                    IMAGE_BYTES
                ])
                
                client_socket.sendall(IMAGE_RESPONSE)
            except FileNotFoundError:
                print("Error: Unable to find badapple.jpg")
                client_socket.sendall(b"HTTP/1.1 404 Not Found\r\n\r\nNot Found")
        else:
            client_socket.sendall(HTML_RESPONSE)
    except Exception as e:
        print(f"❌ Error in client handling: {e}")
    finally:
        client_socket.close()
    
    return