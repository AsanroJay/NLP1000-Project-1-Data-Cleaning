#!/usr/bin/env python3
import os
import time
import requests
from bs4 import BeautifulSoup

def book_equivalence(book):
    if book == "GEN":
        return "Genesis"
    elif book == "EXO":
        return "Exodus"
    elif book == "LEV":
        return "Leviticus"
    
base_url = "https://www.bible.com/bible"
version = input("Enter the version seen on bible.com (e.g., 1588 for KJV): ").strip()
book = input("Enter the book of the Bible (e.g., GEN for Genesis, JHN for John): ").strip().upper()
translation = input("Enter the translation code (e.g., KJV, NIV, TGL): ").strip().upper()
chapters = int(input("How many chapters does this book have? "))
language = input("Enter the language name: ").strip()

pathname = translation +' - '+ language

# Save path
newbook = book_equivalence(book)
path = os.path.join("Bible", pathname, newbook)
os.makedirs(path, exist_ok=True)

headers = {"User-Agent": "Mozilla/5.0"}

for chapter in range(1, chapters+1):
    full_url = f"{base_url}/{version}/{book}.{chapter}.{translation}"
    print("Fetching:", full_url)

    page = requests.get(full_url, headers=headers)
    soup = BeautifulSoup(page.text, "html.parser")

    # On Bible.com, verses are in spans with data-usfm attributes
    verses = soup.find_all("span", attrs={"data-usfm": True})

    chapter_text = []
    for v in verses:
        text = v.get_text(" ", strip=True)
        if text:
            chapter_text.append(text)

    # Save each chapter
    filename = os.path.join(path, f"{newbook}_{chapter}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(chapter_text))

    time.sleep(2)  # pause between requests

