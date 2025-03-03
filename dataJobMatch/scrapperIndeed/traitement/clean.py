import pandas as pd

def clean_description_column(file_path):
    """
    Cleans the 'Description' column of a dataset by removing tabs, line breaks,
    and extra spaces, and converts it into a single line per entry.

    Args:
        file_path (str): Path to the dataset.
    """
    try:
        # Load the dataset
        data = pd.read_csv(file_path)

        # Check if the 'Description' column exists
        if 'Description' not in data.columns:
            print("The 'Description' column was not found in the dataset.")
            return

        # Clean the 'Description' column
        data['Description'] = data['Description'].astype(str)  # Ensure all entries are strings
        data['Description'] = data['Description'].apply(
            lambda x: ' '.join(x.split())  # Remove tabs, line breaks, and extra spaces
        )

        # Save the cleaned dataset
        data.to_csv(file_path, index=False)
        print(f"Cleaned dataset saved to: {file_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Replace with your dataset path
if __name__ == "__main__":
    dataset_path = "JOB/scrapperIndeed/indeed_jobs.csv"  # Replace with your file path
    clean_description_column(dataset_path)
