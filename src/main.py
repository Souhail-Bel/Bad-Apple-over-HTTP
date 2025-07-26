from server import startServer, handleClient

# -- CONFIGURATIONS --
SERVER_IP       = "192.168.1.144"
SERVER_PORT     = 28333

VIDEO_SOURCE    = "BadApple.mp4"

def main():
    """
    Main program function
    """
    
    # Capture video on a separate thread
    
    # Start server
    startServer(
        SERVER_IP,
        SERVER_PORT
    )
    
    

if __name__ == "__main__":
    main()
    