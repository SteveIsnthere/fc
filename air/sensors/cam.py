import picamera

camera = picamera.PiCamera()
camera.resolution = (1600, 1000)
camera.start_recording('my_video.h264')
camera.wait_recording(20)
camera.stop_recording()