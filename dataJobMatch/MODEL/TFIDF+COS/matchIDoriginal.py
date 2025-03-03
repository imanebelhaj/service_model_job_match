import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import seaborn as sns

# Load the datasets (replace paths with your actual file paths)
resumes = pd.read_csv("resumes.csv")  # Columns: ["Category", "Resume"]
jobs = pd.read_csv("jobs.csv")  # Columns: ["Job Title", "Company", "Description", "Language"]

# Preprocessing: Clean text
def preprocess_text(text):
    # Convert to lowercase, remove special characters, extra spaces
    text = str(text).lower()
    text = ''.join(e for e in text if e.isalnum() or e.isspace())
    return text

# Clean the text for resumes and jobs
resumes["Resume"] = resumes["Resume"].apply(preprocess_text)
jobs["Description"] = jobs["Description"].apply(preprocess_text)

# Combine text from resumes and job descriptions for TF-IDF vectorization
all_text = pd.concat([resumes["Resume"], jobs["Description"]])

# TF-IDF Vectorization
tfidf_vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(all_text)

# Split TF-IDF Matrix back into resumes and jobs
resume_vectors = tfidf_matrix[:len(resumes)]
job_vectors = tfidf_matrix[len(resumes):]

# Calculate Cosine Similarity
cosine_similarities = cosine_similarity(resume_vectors, job_vectors)

# Match resumes with jobs
matches = []
category_job_matches = []
job_ids_per_resume = {}  # Dictionary to store job IDs for each resume

for i, resume in resumes.iterrows():
    similar_jobs_indices = cosine_similarities[i].argsort()[-3:][::-1]  # Top 3 matches
    similar_jobs = jobs.iloc[similar_jobs_indices]
    
    # Store matched job IDs for each resume
    matched_job_ids = similar_jobs.index.tolist()
    job_ids_per_resume[resume.name] = matched_job_ids  # resume.name is the ID of the resume
    
    matches.append({
        "Resume_ID": resume.name,  # Include Resume ID
        "Resume_Category": resume["Category"],
        "Top_Matched_Jobs": similar_jobs["Job Title"].tolist(),
        "Job_IDs": matched_job_ids,  # Include Job IDs
        "Similarities": cosine_similarities[i, similar_jobs_indices].tolist()
    })
    # Save Resume Category and Top Matched Job Title
    category_job_matches.append({
        "Resume_Category": resume["Category"],
        "Top_Matched_Job": similar_jobs["Job Title"].iloc[0]  # Best match
    })

# Convert matches to DataFrames
matches_df = pd.DataFrame(matches)
category_job_matches_df = pd.DataFrame(category_job_matches)

# Save results to CSV files
matches_df.to_csv("resume_job_matches_with_ids.csv", index=False)
category_job_matches_df.to_csv("resume_category_job_matches_with_ids.csv", index=False)

# Display results: Show Resume ID and the Jobs it Matched to
print("Resume ID and Matched Jobs (Job IDs):")
for resume_id, matched_jobs in job_ids_per_resume.items():
    print(f"Resume ID: {resume_id}, Matched Jobs: {matched_jobs}")


print("Visualization and CSV generation completed!")
