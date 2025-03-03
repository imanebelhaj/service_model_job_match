import pandas as pd
import random
import names
import geonamescache

# Initialize geonamescache
gc = geonamescache.GeonamesCache()

# Load O*NET Occupation Data
occupation_data_path = "Occupation Data.txt"  # Replace with your actual path
occupation_columns = ["O*NET-SOC Code", "Title", "Description"]
occupation_df = pd.read_csv(occupation_data_path, sep="\t", usecols=occupation_columns)

# Load Skills Data from O*NET
skills_data_path = "Skills.txt"  # Replace with your actual path
skills_columns = ["O*NET-SOC Code", "Element Name"]
skills_df = pd.read_csv(skills_data_path, sep="\t", usecols=skills_columns)

# Load Education Data (Fixed columns based on your dataset structure)
education_data_path = "Education, Training, and Experience.txt"  # Replace with your actual path
education_columns = ["O*NET-SOC Code", "Category", "Data Value"]  # Adjusted columns
education_df = pd.read_csv(education_data_path, sep="\t", usecols=education_columns)

# Load Online Course Data (certifications)
online_courses_path = "Online_Courses.csv"  # Replace with your actual path
courses_df = pd.read_csv(online_courses_path)

# Static data
domains = ["gmail.com", "yahoo.com", "outlook.com", "example.com"]
languages = ["en", "fr"]
phone_prefixes = ["+1", "+33", "+44", "+91", "+971", "+27", "+212", "+34"]

# Helper function to generate names based on location
def generate_name(location):
    if location in ["India", "Pakistan", "Sri Lanka"]:
        return f"{names.get_first_name()} Kumar"
    elif location in ["USA", "Canada", "UK"]:
        return names.get_full_name()
    elif location in ["France", "Germany", "Italy"]:
        return f"{names.get_first_name()} Müller"
    elif location in ["Morocco", "Egypt", "UAE"]:
        return f"{names.get_first_name()} Al-Rashid"
    elif location in ["South Africa", "Nigeria"]:
        return f"{names.get_first_name()} Mensah"
    elif location in ["Japan", "China", "Korea"]:
        return f"{names.get_first_name()} Tanaka"
    else:
        return names.get_full_name()

# Function to generate a synthetic resume with matching education, experience, skills, and certifications
def generate_resume(occupation_df, skills_df, education_df, courses_df):
    # Randomly select a job from O*NET
    job = occupation_df.sample(1).iloc[0]
    job_title = job["Title"]
    job_description = job["Description"]
    soc_code = job["O*NET-SOC Code"]

    # Get skills associated with the job (from O*NET)
    job_skills = skills_df[skills_df["O*NET-SOC Code"] == soc_code]["Element Name"].tolist()
    selected_skills = random.sample(job_skills, min(len(job_skills), 5)) if job_skills else ["Skill not available"]

    # Match course skills to job title dynamically
    matched_courses = courses_df[courses_df['Category'].str.contains(job_title, case=False, na=False)]
    course_skills = matched_courses['Skill'].tolist() if not matched_courses.empty else []
    selected_course_skills = random.sample(course_skills, min(len(course_skills), 5)) if course_skills else ["Skill not available"]

    # Generate experience (ensure it's relevant to the job)
    experience_years = random.randint(1, 10)
    experience = f"{experience_years} years of experience as {job_title}."

    # Generate education (Ensure it matches the job title)
    job_education = education_df[education_df["O*NET-SOC Code"] == soc_code]
    if not job_education.empty:
        education_level = job_education["Data Value"].tolist()[0]
    else:
        education_level = "BSc in relevant field"

    # Generate certification (use the certification generation function)
    certification = generate_certification(job_title, courses_df)

    # Compile resume
    resume = {
        "job_title": job_title,
        "description": job_description,
        "skills": ", ".join(selected_skills),
        "skills2": ", ".join(selected_course_skills),  # Adding course-based skills
        "education": education_level,
        "experience": experience,
        "certificate": certification
    }
    return resume

# Function to get relevant certification based on job title (from course dataset)
def generate_certification(job_title, courses_df):
    matched_courses = courses_df[courses_df['Category'].str.contains(job_title, case=False, na=False)]
    if not matched_courses.empty:
        return random.choice(matched_courses['Course Name'].tolist())
    else:
        return "No certification available"

# Example of how to generate 2000 synthetic resumes
data = []
for i in range(2000):
    # Randomly select a city and get the corresponding country
    city, city_info = random.choice(list(gc.get_cities().items()))
    location = city_info['name']
    country = city_info.get('countryName', 'Unknown')

    # Generate name based on location
    name = generate_name(country)

    # Generate random resume data using O*NET and Online Courses
    resume_data = generate_resume(occupation_df, skills_df, education_df, courses_df)

    # Generate the synthetic resume
    data.append({
        "filename": f"resume_{i+1}.pdf",
        "language": random.choice(languages),
        "name": name,
        "email": f"{name.lower().replace(' ', '.')}@{random.choice(domains)}",
        "phone": f"{random.choice(phone_prefixes)}-{random.randint(100,999)}-{random.randint(1000,9999)}",
        "experience": resume_data["experience"],
        "project": random.choice(["Developed an AI chatbot", "Built a scalable cloud application", "Redesigned a company website"]),
        "education": resume_data["education"],
        "certificate": resume_data["certificate"],
        "languages": random.choice(["English, French", "English, Spanish", "French, Arabic"]),
        "website": random.choice(["www.example.com", "www.portfolio.org", "www.myresume.net"]),
        "hobbies": random.choice(["Reading, Traveling", "Photography, Hiking", "Gaming, Painting"]),
        "location": f"{location}, {country}",
        "skills": resume_data["skills"],
        "skills2": resume_data["skills2"],  # Adding skills2 column from course dataset
    })

# Convert to DataFrame and display a sample
df = pd.DataFrame(data)

# Save to CSV
df.to_csv("synthetic_resumes_with_onet_and_certifications_and_skills.csv", index=False)
print("Synthetic resumes saved as synthetic_resumes_with_onet_and_certifications_and_skills.csv")

# Display the first few rows
print(df.head())
