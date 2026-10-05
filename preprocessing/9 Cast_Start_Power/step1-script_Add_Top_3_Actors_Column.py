import pandas as pd

# Load the dataset
df = pd.read_csv('movie-one-hot-language.csv')

def extract_top_3_actors(crew_string):
    """
    Extract the top 3 actor names from the crew string.
    Only include names with more than one word.
    
    The crew format is: Actor Name, Character Name, Actor Name, Character Name, ...
    So actor names are at even indices (0, 2, 4, ...) when split by comma.
    """
    if pd.isna(crew_string):
        return ""
    
    # Split by comma and strip whitespace
    crew_parts = [part.strip() for part in crew_string.split(',')]
    
    # Extract actor names (every other item, starting from index 0)
    actor_names = []
    for i in range(0, len(crew_parts), 2):
        actor_name = crew_parts[i]
        # Only include names with more than one word
        if len(actor_name.split()) > 1:
            actor_names.append(actor_name)
    
    # Get top 3 actors
    top_3 = actor_names[:3]
    
    # Join with comma separator
    return ', '.join(top_3)

# Apply the function to create the new feature
df['Top_3_Actors'] = df['crew'].apply(extract_top_3_actors)

# Save the updated dataset
df.to_csv('step1-movie-with-top3-actors.csv', index=False)

print("New feature 'Top_3_Actors' added successfully!")
print("\nSample of the new feature:")
print(df[['names', 'Top_3_Actors']].head(10))
