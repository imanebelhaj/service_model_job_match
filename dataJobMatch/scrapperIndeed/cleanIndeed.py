import pandas as pd

def clean_and_remove_duplicates(input_file, output_file):
    """
    Removes the 'Link' column and any duplicate rows from the dataset,
    then saves the cleaned data to a new CSV file.
    
    Args:
        input_file (str): Path to the original dataset.
        output_file (str): Path to save the cleaned dataset.
    """
    try:
        # Load the dataset
        data = pd.read_csv(input_file)

        # Check if the 'Link' column exists
        if 'Link' in data.columns:
            data.drop(columns=['Link'], inplace=True)  # Remove the 'Link' column

        # Remove duplicates based on all columns
        data_cleaned = data.drop_duplicates()

        # Save the cleaned dataset to a new CSV file
        data_cleaned.to_csv(output_file, index=False)
        print(f"Cleaned dataset saved to: {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Replace with your dataset paths
if __name__ == "__main__":
    input_file = "collected.csv"  # Replace with the path to your original dataset
    output_file = "cleaned.csv"  # Path for the cleaned dataset
    clean_and_remove_duplicates(input_file, output_file)
