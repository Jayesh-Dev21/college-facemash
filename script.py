import os
import requests
from dotenv import load_dotenv


load_dotenv() #load phpsessid from .evn

PHPSESSID = os.getenv("PHPSESSID")
if not PHPSESSID: #error handling
    raise ValueError("PHPSESSID not found in .env file!")

BASE_URL = os.getenv("BASE_URL")
ROUTE = os.getenv("ROUTE")


HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:142.0) Gecko/20100101 Firefox/142.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Connection": "keep-alive",
    "Cookie": f"PHPSESSID={PHPSESSID}",
}

def fetch_photo(roll):
    """Fetch and save photo for a given roll number"""
    url = f"{BASE_URL}{ROUTE}?roll={roll}"
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "")
        if "image" not in content_type:
            print(f"[!] Roll {roll}: No image returned (content-type: {content_type})")
            return

        location = "saves"
        ext = "jpg" if "jpeg" in content_type else "png"
        filename = f"{location}/{roll}.{ext}"

        with open(filename, "wb") as f:
            f.write(response.content)

        print(f"[+] Saved photo for roll {roll} → {filename}")

    except Exception as e:
        print(f"[!] Failed to fetch {roll}: {e}")

if __name__ == "__main__":
    roll_numbers = [
        ""
    ] #enter your roll numbers here

    for roll in roll_numbers:
        fetch_photo(roll)