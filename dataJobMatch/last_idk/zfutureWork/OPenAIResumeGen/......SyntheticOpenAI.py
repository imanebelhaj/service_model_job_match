import OPenAIResumeGen.scriptResumeOpen as scriptResumeOpen
import random
import pandas as pd

# OpenAI API Key
scriptResumeOpen.api_key = "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"

# Function to generate a resume using GPT-3
def generate_resume(job_title):
    prompt = f"Create a detailed resume for a {job_title} with 0-12 years of experience( any type inrnship / full time / part time / etc) by speccifying the job title and descriptions and skills in that job,  also the resume includes their skills, education, experience"
    response = scriptResumeOpen.ChatCompletion.create(
        model="gpt-4",  # You can use 'gpt-3.5-turbo' if you want a cheaper version
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500 
    )
    return response['choices'][0]['message']['content'].strip()

# Define the job titles for which to generate resumes
job_titles = ['Advertising','Software Engineer', 'Product Manager','Web Developer','Event manager','Finance','Health','Fitness','Social Media','Marketing','Architect','News & Media','Lawyer','Teacher','Sales','Retail','Tech','Testing','HR','Security','Scrum','Erp','Businees','Chef','Driver','Assistant','Ecommerce']

# Generate synthetic resume data using GPT-3
data = []
for _ in range(2000):  # Number of resumes to generate
    Category = random.choice(job_titles)
    resume_content = generate_resume(Category)
    
    data.append({
        'Category': Category,
        'resume': resume_content,
    })

# Convert to DataFrame and save as CSV
df = pd.DataFrame(data)
df.to_csv('gpt_generated_resumes.csv', index=False)
print("Synthetic resumes generated using  GPT-3.5/GPT-4 and saved.")
