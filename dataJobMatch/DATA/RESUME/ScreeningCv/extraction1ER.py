import pdfplumber
import os
import re
import csv
from langdetect import detect
import geonamescache
import spacy

# Folder containing PDF CVs
folder_path = "RESUME/CV"
output_csv = "extracted_cv_data.csv"


nlp_en = spacy.load("en_core_web_sm")
nlp_fr = spacy.load("fr_core_news_sm")

# ignore_keywords = [
#     "References", "Charity", "Volunteer", "Volunteering", "Declaration", 
#     "Marital Status", "Driving License", "Salary", "Expectations",
#     "Availability", "Personal Statement", "Profile Summary",
#     "Miscellaneous", "Awards", "Social Media", "Cover Letter"
# ]


# Define functions to extract each field
def extract_name(text):
    lines = text.splitlines()

    for line in lines[:3]:  # Limit to the first 3 lines
        line = line.strip()  # Remove leading and trailing whitespace

        if line.isupper() and 1 <= len(line.split()) <= 3:
            return line

        if line.istitle() and 1 <= len(line.split()) <= 3:
            return line
    return "null"




def extract_email(text):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, text)
    return emails[0] if emails else "null"

def extract_phone(text):
    phone_pattern = r'\+?\d[\d -]{8,}\d'
    phones = re.findall(phone_pattern, text)
    return phones[0] if phones else "null"

def extract_website(text):
    website_pattern = r'(https?://[^\s]+|www\.[^\s]+)'
    websites = re.findall(website_pattern, text)
    return websites[0] if websites else "null"

def extract_hobbies(text):
    text = re.sub(r'[^\w]', ' ', text)
    hobbies_pattern = r"(Hobbies|Interests|Passions|Loisirs)"
    match = re.search(hobbies_pattern, text, re.IGNORECASE)
    if match:
        start_index = match.start()
        return text[start_index:start_index + 200]
    return "null"

def extract_experience(text, language):
    text = re.sub(r'[^\w]', ' ', text)  # Remove punctuation
    if language == "fr":
        experience_pattern = r"(Expériences? Professionnelles?|Travail|Emplois?)"
    else:
        experience_pattern = r"(Experience|Work History|Employment|Professional Experience|Working Experiences)"
    match = re.search(experience_pattern, text, re.IGNORECASE)
    if match:
        start_index = match.start()
        return text[start_index:start_index + 300]
    return "null"

def extract_project(text, language):
    text = re.sub(r'[^\w]', ' ', text)
    if language == "fr":
        projects_pattern = r"(Projets|Réalisations)"
    else:
        projects_pattern = r"(Projects|Achievements)"
    match = re.search(projects_pattern, text, re.IGNORECASE)
    if match:
        start_index = match.start()
        return text[start_index:start_index + 300]
    return "null"

def extract_education(text, language):
    text = re.sub(r'[^\w]', ' ', text)
    if language == "fr":
        education_pattern = r"(Éducation|Formation|Diplômes?|Université)"
    else:
        education_pattern = r"(Education|Qualifications|Bachelor|Master|PhD|University|Academic Qualifications)"
    match = re.search(education_pattern, text, re.IGNORECASE)
    if match:
        start_index = match.start()
        return text[start_index:start_index + 300]
    return "null"

def extract_certificate(text, language):
    text = re.sub(r'[^\w]', ' ', text)
    if language == "fr":
        certificate_pattern = r"(Certificats?|Certifications?)"
    else:
        certificate_pattern = r"(Certificates?|Certifications?)"
    match = re.search(certificate_pattern, text, re.IGNORECASE)
    if match:
        start_index = match.start()
        return text[start_index:start_index + 300]
    return "null"

def extract_languages(text, language):
    text = re.sub(r'[^\w]', ' ', text)
    if language == "fr":
        language_pattern = r"(Langues|Compétences Linguistiques)"
    else:
        language_pattern = r"(Languages|Fluency)"
    match = re.search(language_pattern, text, re.IGNORECASE)
    if match:
        start_index = match.start()
        return text[start_index:start_index + 200]
    return "null"


def extract_location(text):
    # Initialize geonamescache
    gc = geonamescache.GeonamesCache()

    # Get list of all cities and countries
    countries = gc.get_countries()
    cities = gc.get_cities()

    # Extract potential locations from text
    text = re.sub(r'[^\w\s]', ' ', text)  # Remove special characters
    words = text.split()
    found_locations = []

    # Check for matches in countries
    for country_code, country_info in countries.items():
        if country_info['name'] in text:
            found_locations.append(country_info['name'])

    # Check for matches in cities
    for city_id, city_info in cities.items():
        if city_info['name'] in text:
            found_locations.append(city_info['name'])

    # Return the first match if any, otherwise return "null"
    return found_locations[0] if found_locations else "null"


def detect_language(text):
    try:
        return detect(text)
    except Exception as e:
        print(f"Error detecting language: {e}")
        return None

# Process each PDF in the folder
extracted_data = []

for filename in os.listdir(folder_path):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(folder_path, filename)
        cv_data = {"filename": filename}
        
        # Extract text from PDF
        try:
            with pdfplumber.open(pdf_path) as pdf:
                full_text = ""
                for page in pdf.pages:
                    full_text += page.extract_text()
        except Exception as e:
            print(f"Error reading PDF {filename}: {e}")
            continue
        
        # Detect language
        language = detect_language(full_text)
        cv_data["language"] = language
        if language not in ["en", "fr"]:
            print(f"Unsupported language in {filename}. Skipping...")
            continue
        
        # Extract fields
        cv_data["name"] = extract_name(full_text)
        cv_data["email"] = extract_email(full_text)
        cv_data["phone"] = extract_phone(full_text)
        cv_data["experience"] = extract_experience(full_text, language)
        cv_data["project"] = extract_project(full_text, language)
        cv_data["education"] = extract_education(full_text, language)
        cv_data["certificate"] = extract_certificate(full_text, language)
        cv_data["languages"] = extract_languages(full_text, language)
        cv_data["website"] = extract_website(full_text)
        cv_data["hobbies"] = extract_hobbies(full_text)
        cv_data["location"] = extract_location(full_text)
        
        extracted_data.append(cv_data)

# Save extracted data to CSV
fieldnames = ["filename", "language", "name", "email", "phone", "experience",
              "project", "education", "certificate", "languages", "website",
              "hobbies", "location"]

with open(output_csv, mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(extracted_data)

print(f"Data saved to {output_csv}")
