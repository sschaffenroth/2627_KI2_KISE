import threading
import pyrealsense2 as rs
import numpy as np
import cv2

latest = {"img": None}
WINDOW = "RealSense Farbbild"

def capture():
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)

    profil = pipeline.start(config)
    kamera = profil.get_device().first_color_sensor()
    kamera.set_option(rs.option.enable_auto_exposure, 0)
    kamera.set_option(rs.option.exposure, 150)
    kamera.set_option(rs.option.enable_auto_white_balance, 0)
    kamera.set_option(rs.option.white_balance, 4600)

    try:
        while cv2.getWindowProperty(WINDOW, cv2.WND_PROP_VISIBLE) > 0:
            frames = pipeline.wait_for_frames()
            f = frames.get_color_frame()
            if f:
                latest["img"] = np.asanyarray(f.get_data()).copy()
    finally:
        pipeline.stop()

t = threading.Thread(target=capture, daemon=True)
t.start()

cv2.namedWindow(WINDOW)
while cv2.getWindowProperty(WINDOW, cv2.WND_PROP_VISIBLE) > 0:
    if latest["img"] is not None:
        cv2.imshow("RealSense Farbbild", latest["img"])
    if cv2.waitKey(10) & 0xFF in (ord("q"), 27):
        break

running = False
t.join()
cv2.destroyAllWindows()