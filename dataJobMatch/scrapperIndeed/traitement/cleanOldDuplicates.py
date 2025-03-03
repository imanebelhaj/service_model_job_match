import pandas as pd

def remove_duplicates(input_file, output_file):
    """
    Reads a CSV file, detects duplicate rows, and writes a cleaned CSV file with duplicates removed.
    
    Args:
        input_file (str): Path to the input CSV file.
        output_file (str): Path to save the cleaned CSV file.
    """
    try:
        # Load the dataset
        df = pd.read_csv(input_file)
        print(f"Original dataset has {df.shape[0]} rows and {df.shape[1]} columns.")
        
        # Detect duplicated rows
        duplicate_count = df.duplicated().sum()
        print(f"Number of duplicated rows detected: {duplicate_count}")
        
        # Remove duplicates and keep the first instance
        df_cleaned = df.drop_duplicates()
        print(f"Dataset after removing duplicates: {df_cleaned.shape[0]} rows remaining.")
        
        # Save the cleaned dataset
        df_cleaned.to_csv(output_file, index=False)
        print(f"Cleaned dataset saved to: {output_file}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

# Replace 'input.csv' and 'output.csv' with your file paths
if __name__ == "__main__":
    input_file = "JOB/scrapperIndeed/indeed_jobs.csv"  # Input file containing the dataset
    output_file = "cleaned_indeed_jobs.csv"  # Output file for cleaned dataset
    remove_duplicates(input_file, output_file)
