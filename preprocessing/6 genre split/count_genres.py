import pandas as pd
import os

# Define file paths
input_file = 'movie_one-hot-country.csv'
output_file = 'genre-distrubution.csv'

def main():
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    try:
        # Read the CSV file
        df = pd.read_csv(input_file)
        
        # Check if 'genre' column exists
        if 'genre' not in df.columns:
            print("Error: 'genre' column not found in input file.")
            return

        # Split the genre string by comma, explode the list to rows, and strip whitespace
        # The regex includes the non-breaking space character (char 160) just in case
        genre_series = df['genre'].dropna().astype(str).str.split(',')
        
        # Explode the list of genres into separate rows
        genres_exploded = genre_series.explode()
        
        # Strip whitespace (including non-breaking spaces if any)
        genres_cleaned = genres_exploded.str.strip()
        
        # Count occurrences
        genre_counts = genres_cleaned.value_counts().reset_index()
        genre_counts.columns = ['genre', 'count']
        
        # Write to CSV
        genre_counts.to_csv(output_file, index=False)
        print(f"Successfully wrote genre distribution to {output_file}")
        print(genre_counts)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
