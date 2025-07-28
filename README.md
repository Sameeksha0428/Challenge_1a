# Challenge_1a - PDF Outline Extractor

This repository contains the solution for Round 1A of the Adobe India Hackathon - "Connecting the Dots" Challenge.

# Objective

To extract a structured outline from a PDF document by identifying:
- Title (from the first page)
- Headings (H1, H2, H3) with their levels and corresponding page numbers

# Approach

This solution uses a heuristic-based approach and works fully offline. No machine learning models are used. Key features include:

- Font size is used as the primary basis for classifying heading levels (H1, H2, H3).
- Bold text is used to emphasize potential headings.
- The title is detected from the first page as the large, horizontally centered text.

# Folder Structure

├── main.py # Main script to extract title and outline
├── Dockerfile # Docker configuration
├── requirements.txt # Python dependencies
├── input/ # Input PDF files
├── output/ # Output JSON files


# Build Command

# Run the Docker image

Open a terminal in the project directory and run:



# Output Format

Each PDF will produce a corresponding `.json` file with the structure:
```json
{
  "title": "Document Title",
  "outline": [
    { "level": "H1", "text": "Section Heading", "page": 1 },
    { "level": "H2", "text": "Subsection Heading", "page": 2 },
    { "level": "H3", "text": "Sub-subsection Heading", "page": 3 }
  ]
}


