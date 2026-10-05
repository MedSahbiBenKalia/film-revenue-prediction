import pandas as pd
import os

# Define file paths
input_file = 'merged_movies_data.csv'
output_file = 'cleaned_movies_data.csv'

# Check if the input file exists
if not os.path.exists(input_file):
    print(f"Error: The file '{input_file}' was not found.")
else:
    # Load the dataset
    df = pd.read_csv(input_file)

    # List of columns to remove
    # Note: Using 'Top_3_Actors' matches the exact case in your CSV file
    columns_to_remove = ['score', 'overview', 'crew', 'Top_3_Actors', 'franchise_name']

    # Remove the columns
    # We use errors='ignore' so the script doesn't crash if a column is missing, 
    # but prints which ones were actually dropped.
    existing_cols_to_drop = [col for col in columns_to_remove if col in df.columns]
    missing_cols = [col for col in columns_to_remove if col not in df.columns]
    
    if missing_cols:
        print(f"Warning: The following columns were not found in the dataset: {missing_cols}")

    df_cleaned = df.drop(columns=existing_cols_to_drop)

    # Save the cleaned data to a new CSV file
    df_cleaned.to_csv(output_file, index=False)

    print(f"Successfully removed {len(existing_cols_to_drop)} columns.")
    print(f"Cleaned data saved to '{output_file}'.")
