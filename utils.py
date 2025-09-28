import re
import os

def clean_text_folder(raw_dir, clean_dir, expressions):
    """
    Cleans all text files in a folder using regex expressions and normalizes verses.

    Parameters:
    - raw_dir: folder containing raw text files
    - clean_dir: folder where cleaned files will be saved
    - expressions: list of (pattern, replacement) tuples
    """

    os.makedirs(clean_dir, exist_ok=True)

    for file in os.listdir(raw_dir):
        if file.endswith(".txt"):
            raw_path = os.path.join(raw_dir, file)
            clean_path = os.path.join(clean_dir, file)

            with open(raw_path, "r", encoding="utf-8") as f:
                text = f.read()

            # Apply regex cleaning (remove headers, notes, etc.)
            for pattern, repl in expressions:
                text = re.sub(pattern, repl, text)

            # Normalize
            text = re.sub(r"\s+", " ", text).strip()
            if not text.endswith(" "):
                text += " "

            # Flatten Verses
            verse_pattern = r"(\d+)\s+(.*?)(?=\s+\d+\s+|$)"
            matches = re.findall(verse_pattern, text)

            if matches:
                # Rebuild as "VerseNumber Text" per line
                text = "\n".join(f"{num} {verse.strip()}" for num, verse in matches if verse.strip())

            # Save cleaned file
            with open(clean_path, "w", encoding="utf-8") as f:
                f.write(text)

            print(f"Cleaned: {file}")