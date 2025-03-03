import os
import re
import pandas as pd
import pdfplumber
from langdetect import detect
from transformers import pipeline

# Path to the folder containing PDFs
folder_path = "RESUME/CV"  # Replace with your folder path

# Initialize Hugging Face zero-shot classification pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Expanded list of fields (categories) for classification
categories = [
    "IT", "Marketing", "Finance", "Engineering", "Healthcare", "Education", "Human Resources", 
    "Law", "Sales", "Operations", "Logistics", "Project Management", "Customer Service", 
    "Real Estate", "Hospitality", "Construction", "Manufacturing", "Design", "Creative Arts", 
    "Media", "Telecommunications", "Retail", "Research", "Science", "Pharmaceuticals", 
    "Agriculture", "Energy", "Public Relations", "Data Science", "AI/ML", "Cybersecurity", 
    "Game Development", "Animation", "Legal Services", "Social Services", "Government", 
    "Transportation", "Aviation", "Space Exploration", "Biotechnology", "Environmental Sciences"
]

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return None

# Function to clean and preprocess the text
def clean_text(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r"[^\w\s]", " ", text)  # Remove punctuation
    text = re.sub(r"\s+", " ", text)  # Remove extra whitespace
    return text.strip()

# Function to detect language and ensure supported models
def detect_language(text):
    try:
        return detect(text)
    except Exception as e:
        print(f"Language detection error: {e}")
        return "unknown"

# Process each PDF
data = []
for filename in os.listdir(folder_path):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(folder_path, filename)
        print(f"Processing {filename}...")
        
        # Extract text from PDF
        raw_text = extract_text_from_pdf(pdf_path)
        if not raw_text:
            continue

        # Clean the text
        cleaned_text = clean_text(raw_text)

        # Detect language
        language = detect_language(cleaned_text)
        if language not in ["en", "fr"]:
            print(f"Skipping unsupported language in {filename}.")
            continue

        # Use zero-shot classification to determine the field of expertise
        result = classifier(cleaned_text[:1024], categories)  # Use only the first 1024 characters for efficiency
        category = result["labels"][0]  # The highest-ranked category

        # Append to the dataset
        data.append({
            "filename": filename,
            "language": language,
            "category": category,
            "resume": cleaned_text
        })

# Convert the data into a DataFrame
df = pd.DataFrame(data)

# Save the dataset to a CSV file
output_csv = "processed_resumes_with_categories.csv"
df.to_csv(output_csv, index=False)
print(f"Dataset saved to {output_csv}")
