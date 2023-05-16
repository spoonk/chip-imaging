from mock_camera import MockCamera

cam = MockCamera()

cam.connect()
print(cam.take_image())
cam.set_gain(10)
cam.set_exposure(20)
cam.close()
