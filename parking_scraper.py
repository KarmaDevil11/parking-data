import requests
from bs4 import BeautifulSoup
import json

# URL of the Ljubljana parking page
url = "https://www.lpt.si/parkirisca/informacije-za-parkiranje/prikaz-zasedenosti-parkirisc"

# Send a request to the website
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Extract all parking data
parking_data = []

# Find all table rows
rows = soup.find_all("tr")

for row in rows:
    # Extract parking name
    name_tag = row.find("a", class_="text-green underline hover:text-green-dark")
    if name_tag:
        parking_name = name_tag.text.strip()

        # Extract free and total parking slots
        slot_info = row.find_all("p", class_="w-1/3")  # Find all <p> with "w-1/3" class
        if len(slot_info) >= 2:  # Ensure there are at least two numbers
            free_spots = slot_info[0].text.strip()  # First <p> contains free spots
            total_spots = slot_info[1].text.strip()  # Second <p> contains total spots

            # Store data in JSON format
            parking_data.append({
                "name": parking_name,
                "free_slots": free_spots,
                "total_slots": total_spots
            })

# Save data as JSON
with open("parking_data.json", "w", encoding="utf-8") as f:
    json.dump(parking_data, f, indent=4, ensure_ascii=False)  # Ensure correct encoding

print("✅ Parking data scraped successfully!")
