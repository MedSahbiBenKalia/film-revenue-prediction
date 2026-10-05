import pandas as pd

# Read the CSV file
df = pd.read_csv('movie-multi-hot-genre.csv')

# Strip whitespace from the 'orig_lang' column to ensure accurate matching
df['orig_lang'] = df['orig_lang'].str.strip()

# Define the list of languages to encode
target_languages = [
    'English',
    'Japanese',
    'Spanish, Castilian',
    'Korean',
    'French',
    'Chinese',
    'Cantonese',
    'Italian',
    'German',
    'Russian'
]

# Create one-hot encoded columns for each target language
for lang in target_languages:
    # create a column name, e.g., 'orig_lang_English'
    # The value is 1 if the row's orig_lang matches the target language, else 0
    df[f'orig_lang_{lang}'] = (df['orig_lang'] == lang).astype(int)

# Create the 'Other' column
# It is 1 if the language is NOT in the target list, else 0
df['orig_lang_Other'] = (~df['orig_lang'].isin(target_languages)).astype(int)

# Remove the original 'orig_lang' column
df.drop(columns=['orig_lang'], inplace=True)

# Save the result to a new CSV file
df.to_csv('movie-one-hot-language.csv', index=False)

print("One-hot encoding completed (with Other). Saved to 'movie-one-hot-language.csv'")
