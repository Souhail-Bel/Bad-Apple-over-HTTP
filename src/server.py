import sys
import socket
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


def createSocket(HOST: str, PORT: int) -> socket.socket:
    """
    Create socket and bind to HOST:PORT
    
    Args:
        HOST: string, representing the IPv4 address of the host
        PORT: integer, representing the port
    
    Returns:
        Socket
    """
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Allow reuse to avoid conflict next time
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    return s

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