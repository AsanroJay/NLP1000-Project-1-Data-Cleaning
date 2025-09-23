#!/usr/bin/env python3
import os
import time
import requests
from bs4 import BeautifulSoup

base_url = "https://www.biblegateway.com/passage/"
book = input("Enter the book of the Bible (e.g., John): ").strip()
translation = input("Enter the translation: ").strip().upper()
chapters = int(input("How many chapters does this book have? "))


path = os.path.join("Bible", translation, book)
os.makedirs(path, exist_ok=True)

headers = {"User-Agent": "Mozilla/5.0"}  # avoids being blocked

for chapter in range(1, chapters+1):
    full_url = f"{base_url}?search={book}+{chapter}&version={translation}"
    print("Fetching:", full_url)

    page = requests.get(full_url, headers=headers)
    soup = BeautifulSoup(page.text, "html.parser")

    # Get all verse text spans
    verses = soup.find_all("span", class_="text")

    chapter_text = []
    for v in verses:
        text = v.get_text(" ", strip=True)
        chapter_text.append(text)

    # Save to file
    filename = os.path.join(path, f"{book}_{chapter}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(chapter_text))

    time.sleep(2)  # pause between requests
