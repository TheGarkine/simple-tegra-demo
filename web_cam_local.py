from contextlib import contextmanager
import cv2
import time
import numpy as np

@contextmanager
def camera() -> cv2.VideoCapture:
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
    camera.set(cv2.CAP_PROP_FPS,30)
    try:
        yield camera
    finally:
        camera.release()

if __name__ == "__main__":
    with camera() as cap:
        try:
            t = time.time()
            # read the first frame
            ret, frame = cap.read()
            if ret:
                previous_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                hsv = np.zeros_like(frame, np.float32)
                hsv[..., 1] = 1.0
                while True:
                    freq = 1/(time.time() - t)
                    t = time.time()
                    
                    ret, frame = cap.read()

                    if not ret:
                        break

                    current_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    flow = cv2.calcOpticalFlowFarneback(
                        previous_frame, current_frame, None, 0.5, 5, 15, 3, 5, 1.2, 0,
                    )

                    magnitude, angle = cv2.cartToPolar(
                        flow[..., 0], flow[..., 1], angleInDegrees=True,
                    )

                    hsv[..., 0] = angle * ((1 / 360.0) * (180 / 255.0))
                    hsv[..., 2] = cv2.normalize(
                        magnitude, None, 0.0, 1.0, cv2.NORM_MINMAX, -1,
                    )

                    hsv_8u = np.uint8(hsv * 255.0)
                    bgr = cv2.cvtColor(hsv_8u, cv2.COLOR_HSV2BGR)

                    previous_frame = current_frame                    

                    cv2.imshow("img", bgr)
                    cv2.waitKey(1)
        except Exception as e:
            print(e)
            raise e
