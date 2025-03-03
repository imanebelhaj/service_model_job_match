import pandas as pd

def merge_datasets(data1_file, data2_file):
    """
    Merges data1 into data2 and saves the result back to data2.

    Args:
        data1_file (str): Path to the first dataset (to append).
        data2_file (str): Path to the second dataset (target).
    """
    try:
        # Load the datasets
        data1 = pd.read_csv(data1_file)
        data2 = pd.read_csv(data2_file)

        print(f"Data1 (to append): {data1.shape[0]} rows, {data1.shape[1]} columns.")
        print(f"Data2 (target): {data2.shape[0]} rows, {data2.shape[1]} columns.")

        # Append data1 to data2
        merged_data = pd.concat([data2, data1], ignore_index=True)
        print(f"Merged dataset: {merged_data.shape[0]} rows, {merged_data.shape[1]} columns.")

        # Save the result back to data2 file
        merged_data.to_csv(data2_file, index=False)
        print(f"Merged dataset saved to: {data2_file}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Replace with your file paths
if __name__ == "__main__":
    data1_file = "JOB/scrapperIndeed/traitement/old_cleaned_indeed_jobs.csv"  # File to append
    data2_file = "JOB/scrapperIndeed/indeed_jobs.csv"         # Target file to merge into
    merge_datasets(data1_file, data2_file)
