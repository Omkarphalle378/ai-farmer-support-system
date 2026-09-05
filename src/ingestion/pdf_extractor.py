import fitz
import os
import json

PDF_FOLDER = "data/raw/pdfs"
OUTPUT_FOLDER = "data/interim/extracted"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)
pdf_files = os.listdir(PDF_FOLDER)


for filename in pdf_files:
    if not filename.lower().endswith(".pdf"):
        continue

    pdf_path = os.path.join(PDF_FOLDER, filename)
    try:
        doc = fitz.open(pdf_path)
        pages = []

        for page_number, page in enumerate(doc, start=1):
            text = page.get_text("text")
            text = text.strip()

            if not text:
                continue

            pages.append({
                "page": page_number,
                "text": text
            })

        output = {
            "source": filename,
            "pages": pages
        }

        output_filename = os.path.splitext(filename)[0] + ".json"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(
                output,
                f,
                ensure_ascii=False,
                indent=2
            )

        doc.close()

        print(f"Saved:{output_filename}")

    except Exception as e:
        print(f"✗ Error processing {filename}: {e}")

print("\nAll PDFs extracted!")
