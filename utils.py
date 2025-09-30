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

            
            # Rebuild as "VerseNumber Text" per line
            if matches:
                fixed = []
                for i, (num, verse) in enumerate(matches):
                    if i == 0:  
                        fixed.append(f"1 {verse.strip()}")
                    else:
                        fixed.append(f"{num} {verse.strip()}")
                text = "\n".join(fixed)

            # Save cleaned file
            with open(clean_path, "w", encoding="utf-8") as f:
                f.write(text)

            print(f"Cleaned: {file}")
            
            
            
def clean_text_folder_no_flatten(raw_dir, clean_dir, expressions):
    """
    Cleans all text files in a folder using regex expressions without flattening verses.

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
                lines = f.readlines()  # Keep verses as separate lines

            cleaned_lines = []
            for line in lines:
                for pattern, repl in expressions:
                    line = re.sub(pattern, repl, line)
                # Normalize spaces but keep line breaks
                line = re.sub(r"\s+", " ", line).strip()
                if line:
                    cleaned_lines.append(line)

            # Save cleaned file
            with open(clean_path, "w", encoding="utf-8") as f:
                f.write("\n".join(cleaned_lines))

            print(f"Cleaned: {file}")
            

def clean_verses_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)

            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

            cleaned = clean_verses(text)

            with open(file_path, "w", encoding="utf-8") as f:
                for num, verse in cleaned:
                    f.write(f"{num} {verse}\n")

            print(f"Cleaned Verses {filename}")

def clean_verses(text):
    lines = text.splitlines()
    verses = []
    expected = 1

    for line in lines:
        parts = line.strip().split(maxsplit=1)

        if not parts:
            continue

        num = parts[0]
        verse_text = parts[1] if len(parts) > 1 else ""

        # Handle ranges like 2-3
        if "-" in num and all(x.isdigit() for x in num.split("-")):
            start, end = map(int, num.split("-"))
            # Save the whole range as one verse entry
            verses.append((f"{start}-{end}", verse_text.strip()))
            expected = end + 1
            continue

        elif num.isdigit():
            num = int(num)

            if num == expected:
                verses.append((num, verse_text.strip()))
                expected += 1
            else:
                # Mis-detected number → merge with previous
                if verses:
                    prev_num, prev_text = verses[-1]
                    verses[-1] = (prev_num, prev_text + " " + line.strip())
                else:
                    verses.append((num, verse_text.strip()))
        else:
            # Continuation line
            if verses:
                prev_num, prev_text = verses[-1]
                verses[-1] = (prev_num, prev_text + " " + line.strip())

    return verses


def align_verses(book, chapters, folder):
    """
    For each chapter file in a book, ensure every verse number or verse range
    starts on a new line.

    Args:
        book (str): Book name (e.g., 'Leviticus')
        chapters (list[int]): Specific chapters to process (e.g., [1,2,5])
        folder (str): Path to folder containing the chapter text files
    """
    verse_pattern = r'(\d+(?:-\d+)?)\s+'  # matches "1 " or "18-19 "

    for chapter in chapters:
        filename = f"{book}_{chapter}.txt"
        file_path = os.path.join(folder, filename)

        if not os.path.exists(file_path):
            print(f"Skipping missing file: {file_path}")
            continue

        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        # Insert newline before each verse number/range
        aligned = re.sub(verse_pattern, r'\n\1 ', text)
        aligned = aligned.strip()

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(aligned)

        print(f"Aligned {filename}")