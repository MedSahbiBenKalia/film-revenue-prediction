import pandas as pd
import os

# Define file paths
input_file = 'imdb_movies.csv'
released_file = 'released-movies.csv'
not_released_file = 'not-released-movies.csv'

# Check if input file exists
if not os.path.exists(input_file):
    print(f"Error: The file '{input_file}' was not found in the current directory.")
else:
    try:
        # Read the CSV file
        df = pd.read_csv(input_file)

        # Strip whitespace from the 'status' column to ensure accurate filtering
        # The sample data showed " Released" with a leading space
        if 'status' in df.columns:
            df['status'] = df['status'].astype(str).str.strip()
            
            # Filter for Released movies
            released_df = df[df['status'] == 'Released']

            # Filter for Not Released movies (everything else)
            not_released_df = df[df['status'] != 'Released']

            # Save to CSV files
            released_df.to_csv(released_file, index=False)
            not_released_df.to_csv(not_released_file, index=False)

            print(f"Successfully split '{input_file}':")
            print(f" - {len(released_df)} released movies saved to '{released_file}'")
            print(f" - {len(not_released_df)} not released movies saved to '{not_released_file}'")
        else:
            print("Error: The 'status' column was not found in the CSV file.")

    except Exception as e:
        print(f"An error occurred: {e}")
