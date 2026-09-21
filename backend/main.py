from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import torch
import io

from plant_data import PLANT_CARE_DATA
from plant_api import search_plant


app = FastAPI()


# ========================================
# CORS
# ========================================

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
        "message": "FloraSense backend is running 🌿"
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
    # Get plant care information
    care = PLANT_CARE_DATA.get(plant_name)

# If local data is unavailable, try Perenual
    if care is None:

     print("Plant not found in local database.")
     print("Searching Perenual...")

    perenual_result = search_plant(plant_name)

    if perenual_result:

        common_name = perenual_result.get("common_name")
        scientific_name = perenual_result.get("scientific_name")
        family = perenual_result.get("family")
        genus = perenual_result.get("genus")

        if isinstance(scientific_name, list):
            scientific_name = ", ".join(scientific_name)

        care = {
            "water": "Information not available",
            "sunlight": "Information not available",
            "temperature": "Information not available",
            "humidity": "Information not available",
            "soil": "Information not available",
            "fertilizer": "Information not available",
            "lifespan": "Information not available",
            "difficulty": "Information not available",
            "tip": f"{common_name or plant_name} belongs to the {family or 'plant'} family."
        }

        print("Perenual plant:", common_name)
        print("Scientific name:", scientific_name)
        print("Family:", family)
        print("Genus:", genus)
    # Return result
    return {

        "success": True,

        "plant_name": plant_name,

        "confidence": round(
            confidence,
            2
        ),

        "care": care,

        "message": "Plant identified successfully 🌱"

    }