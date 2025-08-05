import time # For framerate
import cv2

LATEST_FRAME = None
IS_CAPTURE_ACTIVE = False

class VideoCaptureHandler:
    """
    Handles video capture from video
    """
    
    def __init__(self, video_source, framerate):
        self.video_source = video_source
        self.frame_delay = 1.0/framerate
        self.cap = None
        self.is_running = False
    
    def init_capture(self) -> bool:
        """
        Initialize OpenCV video capture
        Returns success state
        """
        
        # Use 0 for default camera
        self.cap = cv2.VideoCapture(self.video_source)
        if not self.cap.isOpened():
            print(f"Error: Unable to load file '{self.video_source}'")
            return False
        return True
    
    def run(self):
        """
        Frame capture loop on a thread
        """
        
        global LATEST_FRAME, IS_CAPTURE_ACTIVE
        
        IS_CAPTURE_ACTIVE = self.init_capture()
        if not IS_CAPTURE_ACTIVE:
            return
        
        self.is_running = True
        print("🎥 Video capture started.")
        
        while self.is_running:
            t = time.time()
            ret, frame = self.cap.read()
            
            if not ret:
                # Loop once done
                if self.cap.isOpened():
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    print("Looping...")
                    continue 
                else:
                    break
            else:
                LATEST_FRAME = frame
        
            dt = time.time() - t
            if dt < self.frame_delay:
                time.sleep(self.frame_delay-dt)
        
        self.release()
        print("🎥 Video capture stopped.")
    
    def release(self):
        """
        Release video capture object
        """
        
        global IS_CAPTURE_ACTIVE
        
        self.is_running = False
        IS_CAPTURE_ACTIVE = False
        self.cap.release()
        print("VideoCapture object released.")