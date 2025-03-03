import OPenAIResumeGen.scriptResumeOpen as scriptResumeOpen
import random
import pandas as pd
from openai import OpenAI
from openai.types.chat import ChatCompletion
# import openai
import os
# Set your OpenAI API key
# api_key='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'

client = OpenAI(
    api_key ="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"
    #api_key=os.environ.get("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"),

    )

# client = OpenAI()
# OpenAI.api_key ="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"

# openai.api_key = "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"

# Function to generate a resume using the latest OpenAI API
def generate_resume(job_title):
    response = client.chat.completions.create( 
        model="gpt-3.5-turbo",  # Replace with "gpt-3.5-turbo" if preferred
        messages=[
        {"role": "system", "content": "You are a professional resume generator."},
        {"role": "user", "content": f"Create a detailed resume for a {job_title} with 0-12 years of experience. Specify the job title, descriptions, skills, education, and experiences."}
        ],
        max_tokens=200,
        temperature=0.7
    )
    return response['choices'][0]['message']['content']

# Define job titles for generating resumes
job_titles = [
    'Advertising', 'Software Engineer', 'Product Manager', 'Web Developer', 
    'Event Manager', 'Finance', 'Health', 'Fitness', 'Social Media', 
    'Marketing', 'Architect', 'News & Media', 'Lawyer', 'Teacher', 'Sales', 
    'Retail', 'Tech', 'Testing', 'HR', 'Security', 'Scrum', 'ERP', 'Business', 
    'Chef', 'Driver', 'Assistant', 'Ecommerce'
]

# Generate synthetic resume data
data = []
for _ in range(50):  # Adjust the number of resumes as needed
    category = random.choice(job_titles)
    resume_content = generate_resume(category)
    data.append({
        'Category': category,
        'Resume': resume_content,
    })

# Convert to DataFrame and save as CSV
df = pd.DataFrame(data)
df.to_csv('gpt_generated_resumes.csv', index=False)
print("Synthetic resumes generated and saved to gpt_generated_resumes.csv")
