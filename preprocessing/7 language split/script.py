import pandas as pd

# Read the CSV file
df = pd.read_csv('movie-multi-hot-genre.csv')

# Calculate the distribution of orig_lang
# value_counts() counts unique values
distribution = df['orig_lang'].value_counts().reset_index()

# Rename columns for clarity (optional but good practice)
distribution.columns = ['orig_lang', 'count']

# Save the result to a new CSV file
distribution.to_csv('orig_lang-distrubution.csv', index=False)

print("Distribution calculated and saved to 'orig_lang-distrubution.csv'")
