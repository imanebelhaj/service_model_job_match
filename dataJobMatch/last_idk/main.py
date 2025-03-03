import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk


nltk.download("stopwords")
nltk.download("punkt_tab")

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# from nltk.stem import WordNetLemmatizer


#load stopwords
stop_words = set(stopwords.words("english"))
#lemmatizer = WordNetLemmatizer()


# Function to clean and preprocess the text
def preprocess_text(text):
    # Remove non-alphabetic characters and lower case the text
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Tokenize the text
    tokens = word_tokenize(text)
    # Remove stopwords
    tokens = [word for word in tokens if word not in stop_words]
    #tokens = [lemmatizer.lemmatize(word) for word in tokens]  # Lemmatization
    return ' '.join(tokens)

# Load the datasets (replace paths with your actual file paths)
resumes = pd.read_csv("resumes.csv")  # Columns: ["Category", "Resume"]
jobs = pd.read_csv("jobs.csv")  # Columns: ["Job Title", "Company", "Description", "Language"]

# Apply preprocessing to job descriptions and resumes
jobs['processed_description'] = jobs['Description'].apply(preprocess_text)
jobs = jobs[jobs["Language"] == "en"]
resumes['processed_text'] = resumes['Resume'].apply(preprocess_text)