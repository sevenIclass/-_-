import asyncio
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
import uvicorn
from pydantic import BaseModel
from fastapi_frame_stream import FrameStreamer
import cv2
import dxcam

camera = dxcam.create()
app = FastAPI()
fs = FrameStreamer()


async def screen():
    while True:
        screenshot = camera.grab()
        if screenshot is not None:
            ret, buffer = cv2.imencode('.jpg', screenshot)
            frame = buffer.tobytes()
            yield(b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        elif screenshot is None:
            pass
        await asyncio.sleep(1)


async def generator():
    for i in range(10):
        yield 'some streamed data'
        await asyncio.sleep(1)


@app.get('/')
async def main():
    return StreamingResponse(screen())


if __name__ == '__main__':
    uvicorn.run(app)