import threading, time

from server import startServer, handleClient
import capture

# -- CONFIGURATIONS --
SERVER_IP       = "192.168.1.144"
SERVER_PORT     = 28333

VIDEO_SOURCE    = "res/BadApple.mp4"
FRAMERATE       = 30

def main():
    """
    Main program function
    """
    
    # Capture video on a separate thread
    cap = capture.VideoCaptureHandler(VIDEO_SOURCE, FRAMERATE)
    cap_THREAD = threading.Thread(target=cap.run, daemon=True)
    cap_THREAD.start()
    
    time.sleep(2)
    if not capture.IS_CAPTURE_ACTIVE:
        print("Failed to initialize capture.")
        return
    
    # Start server
    startServer(
        SERVER_IP,
        SERVER_PORT,
        cap
    )
    
    

if __name__ == "__main__":
    main()
    