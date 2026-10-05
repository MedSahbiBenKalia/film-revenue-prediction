import pandas as pd
import os

input_file = 'movie_one-hot-country.csv'
output_file = 'movie-multi-hot-genre.csv'

# Genres provided by the user (from genre-distrubution.csv)
target_genres = [
    'Drama', 'Comedy', 'Action', 'Thriller', 'Adventure', 'Romance', 
    'Horror', 'Animation', 'Family', 'Fantasy', 'Crime', 'Science Fiction', 
    'Mystery', 'History', 'War', 'Music', 'Documentary', 'TV Movie', 'Western'
]

def main():
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    print("Reading input file...")
    df = pd.read_csv(input_file)

    print("Processing genres...")
    # Fill NaN genres with empty string to avoid errors
    df['genre'] = df['genre'].fillna('')

    # Clean the genre strings: convert to list of stripped strings
    # This handles "Drama, Action" -> ["Drama", "Action"]
    # And "Action" -> ["Action"]
    # And "  Action  " -> ["Action"]
    df['temp_genre_list'] = df['genre'].astype(str).str.split(',').apply(
        lambda x: [i.strip() for i in x]
    )

    # Create a new column for each target genre
    new_cols = {}
    for genre in target_genres:
        col_name = f"genre_{genre}"
        # Create a boolean mask and convert to int (1/0)
        new_cols[col_name] = df['temp_genre_list'].apply(lambda x: 1 if genre in x else 0)
    
    # Concatenate new columns to the original dataframe
    # Using concat is generally more efficient than adding columns one by one in a loop
    df = pd.concat([df, pd.DataFrame(new_cols)], axis=1)

    # Drop the temporary processing column and original genre feature
    df.drop(columns=['temp_genre_list', 'genre'], inplace=True)

    print(f"Saving result to {output_file}...")
    df.to_csv(output_file, index=False)
    print("Done.")

    # Verification: Print the first few rows of the new columns
    print("\nVerification (first 3 rows):")
    genre_cols = [f"genre_{g}" for g in target_genres]
    print(df[genre_cols[:3]].head(3)) # Show first 3 new columns

if __name__ == "__main__":
    main()
