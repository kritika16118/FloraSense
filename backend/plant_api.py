import os
import requests
from dotenv import load_dotenv

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


def get_plant_details(plant_id):

    url = f"https://perenual.com/api/v2/species/details/{plant_id}"

    params = {
        "key": API_KEY
    }

    response = requests.get(
        url,
        params=params,
        timeout=30
    )

    if response.status_code != 200:
        print(
            "Perenual details API error:",
            response.status_code
        )
        return None

    return response.json()


if __name__ == "__main__":

    print("Testing Perenual API...")

    result = search_plant("Monstera deliciosa")

    if result:

        print("\nPlant found! 🌿")

        print("Name:", result.get("common_name"))
        print("Scientific name:", result.get("scientific_name"))
        print("Plant ID:", result.get("id"))

        plant_id = result.get("id")

        details = get_plant_details(plant_id)

        if details:

            print("\nPlant details found! 🌱")

            print("Watering:", details.get("watering"))
            print("Sunlight:", details.get("sunlight"))
            print("Cycle:", details.get("cycle"))
            print("Care level:", details.get("care_level"))
            print(
                "Watering benchmark:",
                details.get("watering_general_benchmark")
            )

        else:

            print("\nCould not get plant details.")

    else:

        print("\nPlant not found.")