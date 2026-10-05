import pandas as pd

# Load the data from step 2
input_file = 'step2-famous_actors_movie_count.csv'
df = pd.read_csv(input_file)

# Count how many actors have participated in X number of movies
# Value_counts on the 'Number_of_Movies' column gives us exactly that
distribution = df['Number_of_Movies'].value_counts().reset_index()

# Rename columns for clarity
distribution.columns = ['Number_of_Movies', 'Count_of_Actors']

# Sort by Number_of_Movies in ascending order (or descending if preferred)
distribution = distribution.sort_values(by='Number_of_Movies', ascending=True)

# Save the result to a new CSV
output_file = 'step3-movies_distribution.csv'
distribution.to_csv(output_file, index=False)

print(f"Distribution file '{output_file}' created successfully!")
print("\nSample of the distribution (How many actors played in X movies):")
print(distribution.head(10))
