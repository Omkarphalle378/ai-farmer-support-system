import re
import os
import json

INPUT_FOLDER = "data/interim/extracted"
OUTPUT_FOLDER = "data/interim/cleaned"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
json_files = os.listdir(INPUT_FOLDER)


def clean_text(text):
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\s+([,.!?;:])', r'\1', text)
    text = re.sub(r'\s*/\s*', '/', text)
    text = re.sub(r'\n+', '\n', text)
    text = text.strip()
    return text


for filename in json_files:
    if not filename.endswith(".json"):
        continue

    input_path = os.path.join(INPUT_FOLDER, filename)
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    cleaned_pages = []
    for page in data["pages"]:
        text = clean_text(page["text"])
        if len(text) < 30:
            continue

        cleaned_pages.append({
            "page": page["page"],
            "text": text
        })

    output = {
        "source": data["source"],
        "pages": cleaned_pages
    }

    output_path = os.path.join(OUTPUT_FOLDER, filename)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"✓ Saved: {filename}")

print("\nCleaning completed!")
