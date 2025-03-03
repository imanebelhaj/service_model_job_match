import os
import PyPDF2
from langdetect import detect
import spacy

# Load SpaCy models for English and French
nlp_en = spacy.load("en_core_web_sm")
nlp_fr = spacy.load("fr_core_news_sm")

def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None
    


def detect_language(text):
    try:
        language = detect(text)
        return language
    except Exception as e:
        print(f"Error detecting language: {e}")
        return None



def process_text_with_spacy(text, language):
    if language == "en":
        doc = nlp_en(text)
    elif language == "fr":
        doc = nlp_fr(text)
    else:
        print(f"Unsupported language: {language}")
        return None

    # Extract named entities as an example
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

def process_folder(folder_path):
    for filename in os.listdir(folder_path):
        # Only process PDF files
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            print(f"Processing {filename}...")
            
            # Step 1: Extract text from the PDF
            text = extract_text_from_pdf(pdf_path)
            if not text:
                continue

            # Step 2: Detect the language of the text
            language = detect_language(text)
            if not language:
                continue
            print(f"Detected Language: {language}")

            # Step 3: Process text with the appropriate SpaCy model
            entities = process_text_with_spacy(text, language)
            if entities is not None:
                print(f"Extracted Entities for {filename}:\n{entities}")
            print("\n" + "-"*50 + "\n")

# Define the folder containing the resumes
folder_path = "CV"

# Process all PDFs in the folder
process_folder(folder_path)
