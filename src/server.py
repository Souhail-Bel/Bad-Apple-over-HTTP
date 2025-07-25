import socket
# from typing import Union, Tuple

HTML_FRAME = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Test</title>
</head>
<body>
    <p>This is a real test.</p>
</body>
</html>
"""

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
    
    request = client_socket.recv(4096).decode('ISO 8859-1', errors='replace')
    
    request_lines = request.split('\r\n')
    request_head = request_lines[0].strip()
    print(f"Request: {request_head}")
    
    html_bytes = HTML_FRAME.encode('ISO 8859-1', errors='replace')
    response_header = b"".join([
        b"HTTP/1.1 200 OK\r\n",
        b"Content-Type: text/html\r\n",
        f"Content-Length: {len(html_bytes)}\r\n".encode('ISO 8859-1'),
        b"Connection: close\r\n",
        b"\r\n"
    ])
    
    client_socket.sendall(response_header+html_bytes)
    
    return