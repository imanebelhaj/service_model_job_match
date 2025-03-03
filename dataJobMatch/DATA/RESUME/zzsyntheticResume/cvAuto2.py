import pandas as pd
import random
import names
import geonamescache
from mimesis import Generic

# Initialize geonamescache and mimesis
gc = geonamescache.GeonamesCache()
generic = Generic()

# Fetch lists of countries and cities
countries = gc.get_countries()
cities = gc.get_cities()

# Define static data
domains = ["gmail.com", "yahoo.com", "outlook.com", "example.com"]
languages = ["en", "fr"]
phone_prefixes = ["+1", "+33", "+44", "+91", "+971", "+27","+212","+34"]

# Predefined lists for job experiences, job types, companies, and descriptions
job_titles = ["Software Engineer", "Data Scientist", "Marketing Manager", "Product Manager", "UI/UX Designer", "Full Stack Developer", "DevOps Engineer"]
companies = ["Google", "Microsoft", "Amazon", "Apple", "Facebook", "Tesla", "IBM", "Oracle", "Accenture", "Deloitte"]
durations = ["1 year", "2 years", "3 years", "6 months", "4 years"]
job_types = ["Full-time", "Internship", "Part-time", "Freelance"]
experience_descriptions = [
    "Developed and maintained software applications.",
    "Analyzed data and created machine learning models.",
    "Managed digital marketing campaigns.",
    "Collaborated with the design team to improve user interface.",
    "Led product development initiatives.",
    "Designed and implemented cloud infrastructure.",
    "Worked on frontend and backend development using modern frameworks."
]

fields = {
    "IT": {
        "experiences": job_titles,
        "projects": ["Developed a Cloud-Based E-commerce Platform", "Implemented a Scalable Machine Learning Pipeline", "Redesigned a Company Intranet Portal"],
        "education": ["BSc in Computer Science", "MSc in Data Science", "PhD in Artificial Intelligence"],
        "certificates": ["AWS Solutions Architect", "Certified Python Developer", "Azure DevOps Expert"]
    },
    "Marketing": {
        "experiences": job_titles,
        "projects": ["Led a Successful Marketing Campaign for a New Product", "Created a Viral Video Marketing Campaign", "Increased Engagement by 30% on Social Media"],
        "education": ["BBA in Marketing", "MBA in Digital Marketing"],
        "certificates": ["Certified Digital Marketer", "Google Ads Specialist"]
    },
    "Finance": {
        "experiences": job_titles,
        "projects": ["Developed a Financial Risk Assessment Model", "Implemented an Automated Tax Filing System", "Optimized Investment Portfolios for High-Net-Worth Clients"],
        "education": ["BSc in Finance", "MBA in Financial Management"],
        "certificates": ["CFA Level 2", "Certified Financial Planner"]
    }
}

# Helper function to generate realistic names based on location (country)
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

# Generate 2000 rows of data, making sure the name matches the location
data = []
for i in range(2000):
    # Randomly select a city and get the corresponding country
    city, city_info = random.choice(list(cities.items()))
    location = city_info['name']
    country = city_info.get('countryName', 'Unknown')  # Corrected key for country

    # Generate name based on location
    name = generate_name(country)

    # Randomly pick a field (IT, Marketing, Finance)
    field = random.choice(list(fields.keys()))
    field_data = fields[field]

    # Generate random job experiences (1 to 3 experiences per person)
    num_experiences = random.randint(1, 3)
    experiences = []
    for _ in range(num_experiences):
        company = random.choice(companies)
        job_title = random.choice(job_titles)
        duration = random.choice(durations)
        job_type = random.choice(job_types)
        description = random.choice(experience_descriptions)
        
        experience = f"{job_title} at {company} ({duration}) - {job_type} role: {description}"
        experiences.append(experience)

    experience_column = " | ".join(experiences)  # Join experiences in a single column

    # Append the generated row to the data
    data.append({
        "filename": f"resume_{i+1}.pdf",
        "language": random.choice(languages),
        "name": name,
        "email": f"{name.lower().replace(' ', '.')}@{random.choice(domains)}",
        "phone": f"{random.choice(phone_prefixes)}-{random.randint(100,999)}-{random.randint(1000,9999)}",
        "experience": experience_column,  # Add the generated experience
        "project": random.choice(field_data["projects"]),
        "education": random.choice(field_data["education"]),
        "certificate": random.choice(field_data["certificates"]),
        "languages": random.choice(["English, French", "English, Spanish", "French, Arabic"]),
        "website": random.choice(["www.example.com", "www.portfolio.org", "www.myresume.net"]),
        "hobbies": random.choice(["Reading, Traveling", "Hiking, Painting", "Photography, Gaming", "Cycling, Cooking"]),
        "location": f"{location}, {country}",
    })

# Convert to DataFrame and show a sample
df = pd.DataFrame(data)

# Save the generated data to a CSV file
df.to_csv("realistic_resumes_with_experience.csv", index=False)
print("Dataset saved as realistic_resumes_with_experience.csv")

# Display the first few rows of the generated dataset
print(df.head())
