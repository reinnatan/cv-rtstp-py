import argparse
import cv2
import numpy as np
import wave
import pyaudio
import time

# instantiate PyAudio
p = pyaudio.PyAudio()
wf = wave.open('bell_2.wav', 'rb')
# start the stream

# please change the threshold count people for the left camera
threshold_count_person = 0

# camera Name
left_camera_name = "Left Camera"
right_camera_name = "Right Camera"

# URL Camera, you can change to this url camera left and url camera right, from the ip camera
url_camera_left = "http://103.144.82.251:80/camera/SP_STRAAT_3.m3u8"
url_camera_right = "http://103.144.82.251:80/camera/KTL_DEPAN_DPRD.m3u8"

def callback(in_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)
    return (data, pyaudio.paContinue)

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
        channels=wf.getnchannels(),
        rate=wf.getframerate(),
        output=True,
        stream_callback=callback)

def callAlarm(isStart):
    if isStart:
        # time to play audio
        print("play wav")
        stream.start_stream()
    else:
        # time to play audio
        print("stop wav")
        stream.stop_stream()    
        # stop stream
        #stream.close()
        #wf.close()
        # close PyAudio
        #p.terminate()  

def yoloPersonDetection(frame_cam, window_title, net, output_layer_name):
    frame_cam =  cv2.resize(frame_cam, (710, 500))
    height, width, channels = frame_cam.shape
    blob = cv2.dnn.blobFromImage(frame_cam, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layer_name) 

    count = 0
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5 and class_id == 0:  # 0 is the class ID for 'person'
                count += 1
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                cv2.rectangle(frame_cam, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display count on frame & display frame
    cv2.putText(frame_cam, f"People Count: {count}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    #define threshold to activate the alarm if count person is to much in left camera
    if window_title == left_camera_name and count >threshold_count_person:
        cv2.putText(frame_cam, "Too many people in left camera, move to right camera", (5, 450), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 2)
        callAlarm(True)
    elif window_title == left_camera_name and count == 0:
        cv2.putText(frame_cam, "", (5, 450), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 2)           
        callAlarm(False)

    cv2.imshow(window_title, frame_cam)
        
def openStreamCamera(url_cam1, url_cam2):
    net = cv2.dnn.readNet("./yolov3.weights", "./yolov3.cfg")
    output_layer_name = net.getUnconnectedOutLayersNames()

    #simulate for camera 1
    vcap = cv2.VideoCapture(url_cam1)
    
    #simulate for camera 2
    vcap2 = cv2.VideoCapture(url_cam2)
    
    #new logic for detection
    while(1):
        #frame camera 
        ret, frame_cam1 = vcap.read()
        yoloPersonDetection(frame_cam=frame_cam1, window_title=left_camera_name, net=net, output_layer_name=output_layer_name)    

        ret, frame_cam2 = vcap2.read()
        yoloPersonDetection(frame_cam=frame_cam2, window_title=right_camera_name, net=net, output_layer_name=output_layer_name)    

        #wait user trigger the cammera
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

if __name__ == "__main__":
    openStreamCamera(url_cam1=url_camera_left, 
                     url_cam2=url_camera_right)
