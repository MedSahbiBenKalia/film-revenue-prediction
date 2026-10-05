import pandas as pd

# Load the dataset
input_file = 'movie_cleaned.csv'
output_file = 'movie_one-hot-country.csv'

try:
    df = pd.read_csv(input_file)
    print(f"Successfully loaded {input_file}")
except FileNotFoundError:
    print(f"Error: {input_file} not found.")
    exit()

# Define the top 13 countries to keep
top_countries = ['US', 'JP', 'GB', 'KR', 'FR', 'CA', 'ES', 'HK', 'IT', 'CN', 'DE', 'AU', 'MX']

# Function to process the country column
def process_country(country):
    # Convert to string and strip whitespace just in case
    country_str = str(country).strip()
    if country_str in top_countries:
        return country_str
    else:
        return 'other'

# Apply the processing to the 'country' column
df['country'] = df['country'].apply(process_country)

# Perform one-hot encoding
# columns=['country'] will perform encoding on the 'country' column and remove the original column
# dtype=int ensures the output is 0 and 1 instead of True and False
df_encoded = pd.get_dummies(df, columns=['country'], prefix='country', dtype=int)

# Save the result
df_encoded.to_csv(output_file, index=False)
print(f"One-hot encoding completed. Saved to {output_file}")
