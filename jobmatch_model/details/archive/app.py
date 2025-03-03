from flask import Flask, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

app = Flask(__name__)

# Load your pre-trained TF-IDF model and dataset
resumes = pd.read_csv("resumes.csv")
jobs = pd.read_csv("jobs.csv")
tfidf_vectorizer = pickle.load(open("tfidf_vectorizer.pkl", "rb"))
cosine_similarities = pickle.load(open("cosine_similarities.pkl", "rb"))

@app.route('/match-jobs', methods=['POST'])
def match_jobs():
    # Get the resume content from the request
    data = request.get_json()
    resume_text = data.get("resume_text")

    if not resume_text:
        return jsonify({"error": "Resume text is required"}), 400

    # Preprocess the input resume (same as your preprocessing function)
    resume_vector = tfidf_vectorizer.transform([resume_text])

    # Calculate cosine similarity between the resume and job descriptions
    job_similarities = cosine_similarity(resume_vector, tfidf_vectorizer.transform(jobs['Description'])).flatten()

    # Define a threshold (or top N) for job selection
    SIMILARITY_THRESHOLD = 0.01
    similar_jobs_indices = [idx for idx, sim in enumerate(job_similarities) if sim >= SIMILARITY_THRESHOLD]

    # Sort by similarity score
    similar_jobs_indices = sorted(similar_jobs_indices, key=lambda idx: job_similarities[idx], reverse=True)
    top_job_titles = jobs.iloc[similar_jobs_indices]["Job Title"].tolist()

    return jsonify({"matched_jobs": top_job_titles})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
