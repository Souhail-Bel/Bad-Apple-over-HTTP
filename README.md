# Bad Apple over HTTP
This is an **MJPEG** server used, in this case, to stream *Bad Apple!! PV*. Nonetheless, it use can be extended to any video or even feed from the video camera. 
## Preview
<img width="644" height="498" alt="Bad Apple streamed on 192.168.1.144:28333" src="https://github.com/user-attachments/assets/d4a6cdb7-9dda-46f6-9158-acd0db55473e" />


## Building this project
The project relies on OpenCV to turn the video into .jpg frames. Either install it or run:
```
make install
```
In order to execute the project, simply type:
```
make
```

## Project layout
The project is distributed into two folders:
### src folder
* ```main.py``` where the video capture object is initialized and the server start is called.
* ```server.py``` housing two functions:
  - ```startServer```: Binds the MJPEG server to HOST:PORT and  takes the capture object created in main in order to release it upon server shut down and create client handler thread
  - ```handleClient```: Sends the HTML page containing the feed then send the individual frames
* ```capture.py``` Contains VideoCaptureHandler object which relies on *OpenCV* to run video capture
### res folder
* ```index.html``` The page that the user is presented with and which relies on /live_feed source provided by the video capture
* ```BadApple.mp4``` The source video itself, though *.gitignore*'d
