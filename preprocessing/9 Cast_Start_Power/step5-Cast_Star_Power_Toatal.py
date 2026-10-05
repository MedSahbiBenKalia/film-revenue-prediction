import pandas as pd

# Files
movies_file = 'step1-movie-with-top3-actors.csv'
actors_score_file = 'step4-actor_star_power_final.csv'
output_file = 'movie-with-cast-star-power.csv'

# Weights configuration (Tes calculs sont bons !)
weights_3 = [0.5, 0.3, 0.2]
weights_2 = [0.625, 0.375] # (0.5/0.8 et 0.3/0.8 = c'est un poil plus précis que 0.62/0.38)
weights_1 = [1.0]

# Load data
df_movies = pd.read_csv(movies_file)
df_scores = pd.read_csv(actors_score_file)

# --- CORRECTION CRITIQUE 1 : Calculer la "Valeur par Défaut" ---
# Si on ne connait pas l'acteur, on lui donne la moyenne de tous les acteurs
global_mean_score = df_scores['Star_Power_Score'].mean()
print(f"Score par défaut (Moyenne globale) utilisé pour les inconnus : {global_mean_score:,.0f}")

# Create dictionary
actor_score_map = dict(zip(df_scores['Actor_Name'], df_scores['Star_Power_Score']))

def calculate_cast_power(actors_string):
    # --- CORRECTION 2 : Gestion des films sans acteurs ---
    # Si pas d'acteur, le film reçoit le score moyen (et pas 0)
    if pd.isna(actors_string) or str(actors_string).strip() == "":
        return global_mean_score
    
    # Split actors string into a list
    actors = [a.strip() for a in str(actors_string).split(',')]
    
    # --- CORRECTION 3 : Utilisation du Global Mean au lieu de 0.0 ---
    scores = [actor_score_map.get(actor, global_mean_score) for actor in actors]
    
    num_actors = len(scores)
    
    if num_actors >= 3:
        # On prend les 3 premiers au cas où il y en aurait plus
        total_power = (scores[0] * weights_3[0] + 
                       scores[1] * weights_3[1] + 
                       scores[2] * weights_3[2])
    elif num_actors == 2:
        total_power = (scores[0] * weights_2[0] + 
                       scores[1] * weights_2[1])
    elif num_actors == 1:
        total_power = scores[0] * weights_1[0]
    else:
        # Cas théoriquement impossible ici, mais par sécurité
        total_power = global_mean_score
            
    return total_power

# Apply calculation
print("Calculating Cast Star Power Total...")
df_movies['Cast_Star_Power_Total'] = df_movies['Top_3_Actors'].apply(calculate_cast_power)

# Save
df_movies.to_csv(output_file, index=False)

print(f"File '{output_file}' created successfully!")
# Petit formatage pour l'affichage
pd.options.display.float_format = '{:,.0f}'.format
print("\nSample of the new feature:")
print(df_movies[['names', 'Top_3_Actors', 'Cast_Star_Power_Total']].head(10))