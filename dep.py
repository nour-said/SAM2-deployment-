import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import base64
from PIL import Image, ImageDraw
import io
import numpy as np
from fastapi import FastAPI, File, UploadFile, Form 

app = FastAPI()

class ImageRequest(BaseModel):
    # image_base64: str
    image_base64 : UploadFile = File
    x: int
    y: int

@app.get("/")
def home():
    return {"message": "API is working"}

@app.post("/process-image")
async def process_image(data: ImageRequest):

    image_bytes = base64.b64decode(data.image_base64)
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    # draw = ImageDraw.Draw(image)
    # radius = 20
    # draw.ellipse(
    #     (data.x - radius, data.y - radius, data.x + radius, data.y + radius),
    #     outline="red",
    #     width=5
    # )

    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    return {
        "processed_image_base64": img_str
    }