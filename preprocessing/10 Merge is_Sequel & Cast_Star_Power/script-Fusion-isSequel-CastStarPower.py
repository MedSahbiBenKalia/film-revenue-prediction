import pandas as pd

# Load the datasets
# Assuming the file names are derived from the context
file1_path = 'step5-movie-with-cast-star-power.csv'
file2_path = 'movies_is_sequel.csv'

df1 = pd.read_csv(file1_path)
df2 = pd.read_csv(file2_path)

# Print columns to verify
print("Columns in df1:", df1.columns.tolist())
print("Columns in df2:", df2.columns.tolist())

# It seems the datasets have the same rows (movies).
# Merging on 'names', 'score', 'overview', 'release-year' is a safer bet than just 'names' if there are remakes,
# but 'names' + 'release-year' is usually unique enough.
# Let's check for duplicates in 'names' first.
duplicates1 = df1[df1.duplicated(subset=['names', 'release-year'], keep=False)]
duplicates2 = df2[df2.duplicated(subset=['names', 'release-year'], keep=False)]

if not duplicates1.empty:
    print(f"Warning: Duplicates found in {file1_path} based on names and release-year.")
if not duplicates2.empty:
    print(f"Warning: Duplicates found in {file2_path} based on names and release-year.")

# Check if the datasets are row-aligned
# We need to handle potential NaNs in names for comparison
names_match = (df1['names'].fillna('') == df2['names'].fillna('')).all()

if df1.shape[0] == df2.shape[0] and names_match:
    print("Datasets are aligned by row count and names order. Using direct concatenation for unique columns.")
    # Identify unique columns in df2 not in df1
    cols_diff = df2.columns.difference(df1.columns)
    print(f"Adding columns from df2: {cols_diff.tolist()}")
    
    # Concatenate
    combined_df = pd.concat([df1, df2[cols_diff]], axis=1)
else:
    print("Datasets are NOT perfectly aligned. Performing merge.")
    # Merge on names and release-year
    # Check for duplicates in keys used for merging
    if df1.duplicated(subset=['names', 'release-year']).any():
        print("Warning: Duplicates in merge keys for df1")
    if df2.duplicated(subset=['names', 'release-year']).any():
        print("Warning: Duplicates in merge keys for df2")
        
    combined_df = pd.merge(df1, df2[['names', 'release-year', 'franchise_name', 'is_sequel']], 
                           on=['names', 'release-year'], 
                           how='left')
    
    # If duplicates expanded rows, try to deduce uniqueness or warn
    if combined_df.shape[0] > df1.shape[0]:
        print(f"Warning: Row count increased to {combined_df.shape[0]}. Duplicates produced.")
        # Attempt minimal deduplication on df2
        df2_unique = df2.drop_duplicates(subset=['names', 'release-year'])
        combined_df = pd.merge(df1, df2_unique[['names', 'release-year', 'franchise_name', 'is_sequel']], 
                               on=['names', 'release-year'], 
                               how='left')

print(f"Final shape: {combined_df.shape}")

# Save to new csv
output_file = 'merged_movies_data.csv'
combined_df.to_csv(output_file, index=False)
print(f"File saved to {output_file}")
