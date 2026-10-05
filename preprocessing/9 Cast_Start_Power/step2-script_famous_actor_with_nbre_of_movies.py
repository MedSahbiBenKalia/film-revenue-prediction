import pandas as pd
from collections import Counter

#

# Charger le fichier de données
input_file = 'step1-movie-with-top3-actors.csv'
df = pd.read_csv(input_file)

# Initialiser une liste pour stocker tous les acteurs
all_actors = []

# Parcourir la colonne 'Top_3_Actors'
for actors_string in df['Top_3_Actors']:
    if pd.notna(actors_string):
        # Diviser la chaîne par la virgule et nettoyer les espaces
        actors = [actor.strip() for actor in actors_string.split(',')]
        all_actors.extend(actors)

# Compter le nombre d'occurrences de chaque acteur
actor_counts = Counter(all_actors)

# Créer un DataFrame à partir des comptes
actors_df = pd.DataFrame(actor_counts.items(), columns=['Actor_Name', 'Number_of_Movies'])

# Trier par nombre de films (décroissant)
actors_df = actors_df.sort_values(by='Number_of_Movies', ascending=False)

# Sauvegarder le résultat dans un fichier CSV
output_file = 'famous_actors_movie_count.csv'
actors_df.to_csv(output_file, index=False)

print(f"Le fichier '{output_file}' a été généré avec succès.")
print("\nAperçu des acteurs les plus fréquents :")
print(actors_df.head(10))
