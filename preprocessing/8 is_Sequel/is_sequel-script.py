import pandas as pd
import tmdbsimple as tmdb
import re
import time
from tqdm import tqdm

# ================= CONFIGURATION =================
tmdb.API_KEY = '0ec8764a109b727d05b2b31d218d6099' 

INPUT_FILE = 'movie-one-hot-language.csv'   
OUTPUT_FILE = 'movies_is_sequel.csv' 
# =================================================

def check_heuristic(row):
    """Analyse textuelle simple (Titre + Résumé)."""
    title = str(row['names']).lower().strip()
    overview = str(row['overview']).lower().strip()
    score = 0
    
    if ':' in title: score += 1
    if re.search(r'\b(2|3|4|5|6|7|ii|iii|iv|v|vi|vii|vol\.|part)\b$', title): score += 1
    if any(x in title for x in ['sequel', 'chapter', 'returns', 'forever', 'reloaded', 'begins']): score += 1
    
    keywords_ov = ['sequel', 'trilogy', 'saga', 'franchise', 'previous film', 'first film', 'next chapter']
    if any(x in overview for x in keywords_ov): score += 1
        
    return 1 if score > 0 else 0

def check_api(movie_name, release_year=None):
    """Vérification via l'API TMDB avec filtrage par année."""
    search = tmdb.Search()
    try:
        response = search.movie(query=movie_name)
        if search.results:
            best_match = None
            if release_year:
                for result in search.results:
                    release_date = result.get('release_date', '')
                    if release_date and len(release_date) >= 4:
                        try:
                            if int(release_date[:4]) == release_year:
                                best_match = result
                                break
                        except ValueError: continue
            
            if not best_match: best_match = search.results[0]
            
            details = tmdb.Movies(best_match['id']).info()
            collection = details.get('belongs_to_collection')
            
            if collection:
                return True, collection['name']
        return False, None
    except Exception:
        return None, None

def process_data(file_path):
    print(f"Chargement des données depuis {file_path}...")
    df = pd.read_csv(file_path)
    
    # 1. Calcul de l'heuristique (temporaire)
    print("Analyse heuristique en cours...")
    df['_tmp_heu'] = df.apply(check_heuristic, axis=1)
    
    # 2. Appel API
    print("Consultation de l'API TMDB (Vérification des franchises)...")
    api_flags = []
    franchise_names = []
    
    for idx, row in tqdm(df.iterrows(), total=len(df)):
        title = row['names']
        year = int(row['release-year']) if pd.notna(row['release-year']) else None
        
        is_seq, coll_name = check_api(title, year)
        api_flags.append(is_seq)
        franchise_names.append(coll_name)
        time.sleep(0.25) 

    df['_tmp_api'] = api_flags
    df['franchise_name'] = franchise_names # On garde celle-ci
    
    # 3. Fusion de la logique pour créer la colonne finale 'is_sequel'
    def combine(row):
        api_res = row['_tmp_api']
        heu_res = row['_tmp_heu']
        
        if api_res is True: return 1
        if api_res is False: return 0
        return heu_res # Fallback si l'API échoue

    df['is_sequel'] = df.apply(combine, axis=1)
    
    # 4. NETTOYAGE : On supprime les colonnes de calcul intermédiaires
    df.drop(columns=['_tmp_heu', '_tmp_api'], inplace=True)
    
    return df

if __name__ == "__main__":
    try:
        final_df = process_data(INPUT_FILE)
        
        print(f"Sauvegarde dans {OUTPUT_FILE}...")
        final_df.to_csv(OUTPUT_FILE, index=False)
        
        print("\n--- Succès ! Aperçu des nouvelles colonnes : ---")
        print(final_df[['names', 'is_sequel', 'franchise_name']].head(10))
        
    except FileNotFoundError:
        print("Erreur : Fichier introuvable.")