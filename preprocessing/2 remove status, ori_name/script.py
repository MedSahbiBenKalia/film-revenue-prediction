import pandas as pd

# Load the dataset
input_file = 'released-movies.csv'
output_file = 'movie(no ,orig-title,status).csv'

try:
    df = pd.read_csv(input_file)
    
    # Columns to remove
    columns_to_remove = ['orig_title', 'status']
    
    # Drop the columns if they exist
    df.drop(columns=columns_to_remove, inplace=True, errors='ignore')
    
    # Save the modified dataset
    df.to_csv(output_file, index=False)
    
    print(f"Successfully processed '{input_file}' and saved to '{output_file}'")

except FileNotFoundError:
    print(f"Error: The file '{input_file}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")
