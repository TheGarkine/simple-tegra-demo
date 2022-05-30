from contextlib import contextmanager
import cv2
from fastapi import FastAPI, WebSocket
import base64
import time
import numpy as np

app = FastAPI()

def gstreamer_pipeline():
    return  "v4l2src device=/dev/video0 ! image/jpeg,framerate=30/1,width=1280,height=720 ! jpegparse ! jpegdec ! video/x-raw ! videoconvert ! video/x-raw,width=1280,height=720,format=BGRx,framerate=30/1 ! videoconvert  ! videorate ! appsink drop=1"

@contextmanager
def camera() -> cv2.VideoCapture:
    camera = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
    # camera.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
    # camera.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
    # camera.set(cv2.CAP_PROP_FPS,30)
    try:
        yield camera
    finally:
        camera.release()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print("started")
    await websocket.accept()
    with camera() as cap:
        try:
            t = time.time()
            ret, frame = cap.read()

            if ret:
                gpu_frame = cv2.cuda_GpuMat()
                gpu_frame.upload(frame)

                previous_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                gpu_previous = cv2.cuda_GpuMat()
                gpu_previous.upload(previous_frame)

                gpu_hsv = cv2.cuda_GpuMat(gpu_frame.size(), cv2.CV_32FC3)
                gpu_hsv_8u = cv2.cuda_GpuMat(gpu_frame.size(), cv2.CV_8UC3)

                gpu_h = cv2.cuda_GpuMat(gpu_frame.size(), cv2.CV_32FC1)
                gpu_s = cv2.cuda_GpuMat(gpu_frame.size(), cv2.CV_32FC1)
                gpu_v = cv2.cuda_GpuMat(gpu_frame.size(), cv2.CV_32FC1)

                gpu_s.upload(np.ones_like(previous_frame, np.float32))

                while True:
                    freq = 1/(time.time() - t)
                    t = time.time()

                    ret, frame = cap.read()

                    gpu_frame.upload(frame)

                    if not ret:
                        break

                    gpu_current = cv2.cuda.cvtColor(gpu_frame, cv2.COLOR_BGR2GRAY)

                    gpu_flow = cv2.cuda_FarnebackOpticalFlow.create(
                        5, 0.5, False, 15, 3, 5, 1.2, 0,
                    )

                    gpu_flow = cv2.cuda_FarnebackOpticalFlow.calc(
                        gpu_flow, gpu_previous, gpu_current, None,
                    )


                    gpu_flow_x = cv2.cuda_GpuMat(gpu_flow.size(), cv2.CV_32FC1)
                    gpu_flow_y = cv2.cuda_GpuMat(gpu_flow.size(), cv2.CV_32FC1)
                    cv2.cuda.split(gpu_flow, [gpu_flow_x, gpu_flow_y])

                    gpu_magnitude, gpu_angle = cv2.cuda.cartToPolar(
                        gpu_flow_x, gpu_flow_y, angleInDegrees=True,
                    )

                    gpu_v = cv2.cuda.normalize(gpu_magnitude, 0.0, 1.0, cv2.NORM_MINMAX, -1)

                    angle = gpu_angle.download()
                    angle *= (1 / 360.0) * (180 / 255.0)

                    gpu_h.upload(angle)

                    cv2.cuda.merge([gpu_h, gpu_s, gpu_v], gpu_hsv)
                    gpu_hsv.convertTo(cv2.CV_8U, 255.0, gpu_hsv_8u, 0.0)
                    gpu_bgr = cv2.cuda.cvtColor(gpu_hsv_8u, cv2.COLOR_HSV2BGR)
                    frame = gpu_frame.download()

                    bgr = gpu_bgr.download()

                    gpu_previous = gpu_current

                    cv2.putText(img=bgr, text=str(freq), org=(10, 30), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 255, 0),thickness=2)
                    

                    _, buffer = cv2.imencode('.jpg', bgr)
                    jpg_as_text = base64.b64encode(buffer).decode("utf-8")
                    await websocket.send_text(jpg_as_text)
        except Exception as e:
            print(e)
            raise e
        finally:
            await websocket.close()
