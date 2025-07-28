import fitz
import os
import json
import glob
from statistics import mean

def is_centered(span, page_width, tolerance=50):
    """Check if the span is horizontally centered"""
    x0, x1 = span["bbox"][0], span["bbox"][2]
    center_of_text = (x0 + x1) / 2
    return abs(center_of_text - (page_width / 2)) <= tolerance

def extract_title(page):
    """Extract large, centered text from first page as title"""
    blocks = page.get_text("dict")["blocks"]
    candidates = []
    for b in blocks:
        if "lines" not in b:
            continue
        for l in b["lines"]:
            for span in l["spans"]:
                if is_centered(span, page.rect.width) and span["size"] > 16:
                    candidates.append((span["size"], span["text"].strip()))
    if candidates:
        # Choose the largest font text that's centered
        candidates.sort(reverse=True)
        return candidates[0][1]
    return "Untitled Document"

def clean_text(text):
    """Remove extra spaces and newline characters"""
    return " ".join(text.split())

def classify_level(size):
    """Classify heading level based on font size"""
    if size > 16:
        return "H1"
    elif size > 13:
        return "H2"
    elif size > 11:
        return "H3"
    return None

def extract_outline(pdf_path):
    doc = fitz.open(pdf_path)
    outline = []
    seen_texts = set()

    title = extract_title(doc[0]).strip()
    title_lower = title.lower()

    font_sizes = []

    # First pass: collect font sizes
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if "lines" not in b:
                continue
            for l in b["lines"]:
                for span in l["spans"]:
                    font_sizes.append(span["size"])
    avg_size = mean(font_sizes)

    # Second pass: extract headings using heuristics
    for i, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if "lines" not in b:
                continue
            for l in b["lines"]:
                spans = l["spans"]
                if not spans:
                    continue

                # Join all spans in this line
                line_text = " ".join([clean_text(span["text"]) for span in spans])
                line_text_cleaned = line_text.strip()

                if not line_text_cleaned:
                    continue

                # Skip if line matches title exactly
                if line_text_cleaned.lower() == title_lower:
                    continue

                max_size = max([span["size"] for span in spans])
                is_bold = any((span["flags"] & 2) != 0 for span in spans)

                # Heuristic check for heading
                if is_bold or max_size > 12:
                    level = classify_level(max_size)
                    if level and line_text_cleaned.lower() not in seen_texts:
                        outline.append({
                            "level": level,
                            "text": line_text_cleaned,
                            "page": i
                        })
                        seen_texts.add(line_text_cleaned.lower())

    return {
        "title": title,
        "outline": outline
    }

def main():
    for file in glob.glob("input/*.pdf"):
        data = extract_outline(file)
        name = os.path.basename(file).replace(".pdf", ".json")
        with open(f"output/{name}", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

if __name__ == "__main__":
    main()
