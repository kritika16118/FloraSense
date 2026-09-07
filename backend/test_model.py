from transformers import pipeline

print("Loading plant AI model...")

classifier = pipeline(
    "image-classification",
    model="microsoft/resnet-50"
)

print("Plant AI model loaded successfully! 🌿")