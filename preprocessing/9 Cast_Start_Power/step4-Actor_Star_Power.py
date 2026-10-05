import pandas as pd
import numpy as np

# Configuration
input_file = 'step1-movie-with-top3-actors.csv'
output_file = 'actor_star_power_final.csv'
m = 5  # Seuil minimum de films

# Charger les données
df = pd.read_csv(input_file)

# 1. Calculer C (Moyenne globale des revenus)
C = df['revenue'].mean()
print(f"Moyenne globale des revenus (C) : {C:,.2f}")

# 2. Collecter les revenus pour chaque acteur
actor_revenues = {}

for index, row in df.iterrows():
    actors_string = row['Top_3_Actors']
    revenue = row['revenue']
    
    # On ignore les lignes sans acteurs ou sans revenu valide
    if pd.notna(actors_string) and pd.notna(revenue):
        actors = [actor.strip() for actor in actors_string.split(',')]
        for actor in actors:
            if actor not in actor_revenues:
                actor_revenues[actor] = []
            actor_revenues[actor].append(revenue)

# 3. Calculer v, R et le Score pour chaque acteur
results = []

for actor, revenues in actor_revenues.items():
    v = len(revenues)            # Volume (nombre de films)
    R = np.mean(revenues)        # Revenu moyen de l'acteur
    
    # Calcul du score Star Power selon la formule
    # Score = (v / (v + m)) * R + (m / (v + m)) * C
    score = (v / (v + m)) * R + (m / (v + m)) * C
    
    results.append({
        'Actor_Name': actor,
        'Number_of_Movies': v,
        'Average_Revenue': R,
        'Star_Power_Score': score
    })

# Créer le DataFrame final
results_df = pd.DataFrame(results)

# Trier par Star Power Score décroissant
results_df = results_df.sort_values(by='Star_Power_Score', ascending=False)

# Sauvegarder
results_df.to_csv(output_file, index=False)

print(f"Fichier '{output_file}' généré avec succès !")
print("\nTop 10 Acteurs par Star Power Score :")
pd.options.display.float_format = '{:,.0f}'.format
print(results_df[['Actor_Name', 'Number_of_Movies', 'Star_Power_Score']].head(10))
