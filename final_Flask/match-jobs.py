from flask import Flask, request, jsonify
import mysql.connector
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load your pre-trained TF-IDF model
tfidf_vectorizer = pickle.load(open("tfidf_vectorizer.pkl", "rb"))

# MySQL Database Configuration
db_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'imane',
    'database': 'jobmatchdb'
}

@app.route('/match-jobs', methods=['POST'])
def match_jobs():
    # Get the resume content from the request
    data = request.get_json()
    resume_text = data.get("resume_text")

    if not resume_text:
        return jsonify({"error": "Resume text is required"}), 400

    # Test database connection
    try:
        print("Attempting to connect to the database...")
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            print("Database connected successfully!")
        else:
            print("Failed to connect to the database.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conn.cursor(dictionary=True)

    # Fetch job data from the database
    cursor.execute("SELECT id, job_form FROM jobs")
    jobs = cursor.fetchall()
    conn.close()

    # Extract job descriptions
    job_ids = [job["id"] for job in jobs]
    job_forms = [job["job_form"] for job in jobs]

    # Preprocess the input resume
    resume_vector = tfidf_vectorizer.transform([resume_text])

    # Calculate cosine similarity between the resume and job descriptions
    job_vectors = tfidf_vectorizer.transform(job_forms)
    job_similarities = cosine_similarity(resume_vector, job_vectors).flatten()

    # Define a threshold for job selection
    SIMILARITY_THRESHOLD = 0.1
    similar_jobs_indices = [idx for idx, sim in enumerate(job_similarities) if sim >= SIMILARITY_THRESHOLD]

    # Sort by similarity score
    similar_jobs_indices = sorted(similar_jobs_indices, key=lambda idx: job_similarities[idx], reverse=True)

    # Retrieve job IDs of the matched jobs
    matched_job_ids = [job_ids[idx] for idx in similar_jobs_indices]

    return jsonify({"matched_jobs": matched_job_ids})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
