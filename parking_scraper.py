import requests
from bs4 import BeautifulSoup
import json

# URL of the website to scrape
URL = "https://www.lpt.si/parkirisca/informacije-za-parkiranje/prikaz-zasedenosti-parkirisc"

# Dictionary to store parking locations and their coordinates
PARKING_COORDINATES = {
    "Bežigrad": (46.0704, 14.5106),
    "Dolenjska cesta (Strelišče)": (46.0415, 14.5183),
    "Gosarjeva ulica": (46.0651, 14.5268),
    "Gospodarsko razstavišče": (46.0639, 14.5103),
    "PH Kongresni trg": (46.0516, 14.5057),
    "Kozolec": (46.0589, 14.5091),
    "Kranjčeva ulica": (46.0675, 14.5194),
    "Linhartova": (46.0678, 14.5146),
    "Metelkova ulica": (46.0584, 14.5118),
    "Mirje": (46.0486, 14.5033),
    "NUK II.": (46.0481, 14.5030),
    "PH Kolezija": (46.0443, 14.4975),
    "Povšetova ulica": (46.0621, 14.5192),
    "Sanatorij Emona": (46.0568, 14.5095),
    "Tivoli I.": (46.0595, 14.4999),
    "Tivoli II.": (46.0599, 14.5021),
    "Trg mladinskih delovnih brigad": (46.0519, 14.4923),
    "Trg prekomorskih brigad": (46.0593, 14.4879),
    "Žale I.": (46.0738, 14.5263),
    "Žale II.": (46.0741, 14.5270),
    "Žale III.": (46.0744, 14.5278),
    "Žale IV.": (46.0747, 14.5285),
    "Žale V.": (46.0750, 14.5292),
    "PH Rog": (46.0563, 14.5162),
}

def scrape_parking_data():
    """Scrapes parking availability data from the LPT website."""
    response = requests.get(URL)
    if response.status_code != 200:
        print("Failed to fetch data from the website.")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    parking_data = []

    # Find all rows containing parking data
    rows = soup.find_all("tr")

    for row in rows:
        # Extract parking name
        parking_name_element = row.find("a", class_="text-green underline hover:text-green-dark")
        if not parking_name_element:
            continue  # Skip rows without a valid parking name

        parking_name = parking_name_element.text.strip()

        # Extract availability numbers
        slot_data = row.find_all("p", class_="w-1/3")
        if len(slot_data) < 2:
            continue  # Skip rows with missing data

        free_slots = slot_data[0].text.strip()
        total_slots = slot_data[1].text.strip()

        # Convert free slots to an integer if possible
        try:
            free_slots = int(free_slots)
        except ValueError:
            free_slots = "Unknown"

        # Convert total slots to an integer if possible
        try:
            total_slots = int(total_slots)
        except ValueError:
            total_slots = "Unknown"

        # Get coordinates if available
        coordinates = PARKING_COORDINATES.get(parking_name, (None, None))

        # Store extracted data
        parking_data.append({
            "name": parking_name,
            "free_slots": free_slots,
            "total_slots": total_slots,
            "latitude": coordinates[0],
            "longitude": coordinates[1]
        })

    return parking_data

def save_to_json(data, filename="parking_data.json"):
    """Saves parking data to a JSON file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Parking data saved to {filename}")

if __name__ == "__main__":
    parking_data = scrape_parking_data()
    if parking_data:
        save_to_json(parking_data)
