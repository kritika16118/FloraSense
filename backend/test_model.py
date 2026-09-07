from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import torch

print("Loading plant identification model...")

model_id = "domai-tb/OpenPlants-Identification-ViT-Base-Patch16-224"

processor = AutoImageProcessor.from_pretrained(model_id)

model = AutoModelForImageClassification.from_pretrained(model_id)

model.eval()

print("Plant identification model loaded successfully! 🌿")


# Open plant image
image = Image.open("photo.png").convert("RGB")

print("\nAnalyzing plant image... 🌱")

# Prepare image
inputs = processor(images=image, return_tensors="pt")


# Run AI model
with torch.no_grad():

    outputs = model(**inputs)

    probabilities = torch.softmax(outputs.logits, dim=-1)

    top_predictions = torch.topk(probabilities, 5)


print("\nTop predictions:")

for probability, index in zip(
    top_predictions.values[0],
    top_predictions.indices[0]
):

    plant_name = model.config.id2label[index.item()]

    confidence = probability.item() * 100

    print(
        f"{plant_name} -> {confidence:.2f}%"
    )