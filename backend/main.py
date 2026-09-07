from fastapi import FastAPI, UploadFile, File

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "FloraSense backend is running 🌿"
    }


@app.post("/api/identify")
async def identify_plant(image: UploadFile = File(...)):
    return {
        "message": "Image received successfully 🌱",
        "filename": image.filename
    }