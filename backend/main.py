from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import base64

app = FastAPI(title="Image Caption Generator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ALLOWED_TYPES = {"image/png", "image/jpeg", "image/jpg", "image/webp"}

@app.get("/")
def root():
    return {"message": "Image Caption Generator API is running!"}

@app.post("/caption/")
async def caption_image(file: UploadFile = File(...)):
    # Validate file type
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file.content_type}. Use PNG, JPG, or WEBP."
        )

    try:
        image_bytes = await file.read()

        if len(image_bytes) == 0:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")

        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llava",
                "prompt": (
                    "Describe this image in one clear and detailed sentence. "
                    "Focus on the main subject, setting, and any notable details."
                ),
                "images": [image_base64],
                "stream": False
            },
            timeout=120
        )

        result = response.json()
        caption = result.get("response", "").strip()

        if not caption:
            return {"caption": "No caption could be generated.", "raw": ""}

        return {"caption": caption}

    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Could not connect to Ollama. Make sure it is running on port 11434."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
