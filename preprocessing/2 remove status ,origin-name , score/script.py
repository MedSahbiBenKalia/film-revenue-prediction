import pandas as pd
import os

def process_movies():
    input_file = 'released-movies.csv'
    output_file = 'movie(not score,orig-title,status).csv'
    
    # Columns to remove based on the requirements
    # "score, orig_title, status"
    columns_to_remove = ['score', 'orig_title', 'status']
    
    if not os.path.exists(input_file):
        print(f"Error: The file '{input_file}' was not found in the current directory.")
        return

    try:
        # Read the CSV file
        df = pd.read_csv(input_file)
        
        # Check which columns are actually present and drop them
        present_columns = [col for col in columns_to_remove if col in df.columns]
        missing_columns = [col for col in columns_to_remove if col not in df.columns]
        
        if missing_columns:
            print(f"Warning: The following columns were not found in the input file: {missing_columns}")
        
        df_dropped = df.drop(columns=present_columns)
        
        # Save the modified DataFrame to the new CSV file
        df_dropped.to_csv(output_file, index=False)
        
        print(f"Successfully removed columns: {present_columns}")
        print(f"Saved processed data to: {output_file}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    process_movies()
