import os
import requests
from dotenv import load_dotenv


# Load .env file
load_dotenv()


API_KEY = os.getenv("PERENUAL_API_KEY")


def search_plant(plant_name):

    url = "https://perenual.com/api/v2/species-list"

    params = {
        "key": API_KEY,
        "q": plant_name
    }

    response = requests.get(
        url,
        params=params,
        timeout=30
    )

    if response.status_code != 200:
        print("Perenual API error:", response.status_code)
        return None

    data = response.json()

    if not data.get("data"):
        return None

    return data["data"][0]


if __name__ == "__main__":

    print("Testing Perenual API...")

    result = search_plant("Monstera deliciosa")

    if result:

        print("\nPlant found! 🌿")

        print("\nFull Perenual result:")
        print(result)

    else:

        print("\nPlant not found.")

        print("Name:", result.get("common_name"))
        print("Scientific name:", result.get("scientific_name"))
        print("Watering:", result.get("watering"))
        print("Sunlight:", result.get("sunlight"))

else:

        print("\nPlant not found.")