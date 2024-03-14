# learning python programming using live stream and opencv with YOLO
# cara install
- jalankan perintah ```python3 -m venv venv```
- jalankan perintah ```source venv/bin/activate```
- jalankan perintah ``` pip3 install -r requirement.txt```
# running program
- untuk dapat menjalan program dengan mengetikan perintah ```python3 rtsp_camera.py```
# model weigths
- untuk model weights dapat di download di link ini ```https://pjreddie.com/darknet/yolo/```
  atau dapat juga mendownload dari drive yang suda saya download sebelumnya, karena file weightsnya yang terlalu besar
  ```https://drive.google.com/file/d/1ZfPHbFomThrXPbw9JMS-48UqWhzx3Hnk/view?usp=sharing```

# konstanta program
- untuk konstanta seperti url kamera 1, url kamera 2, dan threshold jumlah maksimal orang yang ingin 
  di trigger alarmnya dan nama kamera dapat mengganti di variable berikut ini
  ```
  please change the threshold count people for the left camera
  threshold_count_person = 0

  camera Name
  left_camera_name = "Left Camera"
  right_camera_name = "Right Camera"

  URL Camera, you can change to this url camera left and url camera right, from the ip camera
  url_camera_left = "http://103.144.82.251:80/camera/SP_STRAAT_3.m3u8"
  url_camera_right = "http://103.144.82.251:80/camera/KTL_DEPAN_DPRD.m3u8"
  ```
