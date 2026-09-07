from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import torch
import io
from plant_data import PLANT_CARE_DATA

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========================================
# LOAD PLANT AI MODEL
# ========================================

print("Loading FloraSense plant AI model...")

MODEL_ID = "domai-tb/OpenPlants-Identification-ViT-Base-Patch16-224"

processor = AutoImageProcessor.from_pretrained(MODEL_ID)

model = AutoModelForImageClassification.from_pretrained(MODEL_ID)

model.eval()

print("FloraSense plant AI model loaded! 🌿")


# ========================================
# HOME
# ========================================

@app.get("/")
def home():

    return {
    "success": True,
    "plant_name": plant_name,
    "confidence": round(confidence, 2),
    "message": "Plant identified successfully 🌱"
    }


# ========================================
# PLANT IDENTIFICATION
# ========================================

@app.post("/api/identify")
async def identify_plant(image: UploadFile = File(...)):

    # Read uploaded image
    image_data = await image.read()

    # Open image
    plant_image = Image.open(
        io.BytesIO(image_data)
    ).convert("RGB")


    # Prepare image for AI
    inputs = processor(
        images=plant_image,
        return_tensors="pt"
    )


    # Run AI model
    with torch.no_grad():

        outputs = model(**inputs)

        probabilities = torch.softmax(
            outputs.logits,
            dim=-1
        )

        top_result = torch.argmax(
            probabilities,
            dim=-1
        ).item()


    # Get plant name
    plant_name = model.config.id2label[top_result]


    # Get confidence
    confidence = (
        probabilities[0][top_result].item() * 100
    )


    return {

        "success": True,

        "plant_name": plant_name,

        "confidence": round(
            confidence,
            2
        ),

        "message": "Plant identified successfully 🌱"

    }