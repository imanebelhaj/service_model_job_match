import pandas as pd
from langdetect import detect

# Load your dataset
file_path = "Job.csv"  # Replace with your actual file path
df = pd.read_csv(file_path)

# Function to detect language (fr or en)
def detect_language(text):
    try:
        lang = detect(text)
        # Only return 'fr' or 'en', ignore other languages
        if lang == 'fr':
            return 'fr'
        elif lang == 'en':
            return 'en'
        else:
            return 'other'  # For other languages, you can customize it as needed
    except:
        return 'unknown'  # In case of error or empty text

# Apply the language detection function to the 'Description' or relevant column
# Replace 'Description' with the actual column name where you want to detect the language
df['Language'] = df['Description'].apply(detect_language)  # Replace 'Description' with your column name

# Reorder columns to make 'Language' the second column
columns = ['Company', 'Language'] + [col for col in df.columns if col not in ['Company', 'Language']]
df = df[columns]

# Save the updated dataset to a new file
output_path = "Job_with_language.csv"
df.to_csv(output_path, index=False)

print("Language detection added and saved with Language as second column in 'Job_with_language_second_column.csv'")
