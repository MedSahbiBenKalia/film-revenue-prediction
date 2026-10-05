"""
Movie Dataset Country Code Enrichment Script
Uses TMDB API to fix incorrectly labeled country codes
Targets rows where country == 'AU' (likely scraped with AU regional filter)
"""

import pandas as pd
import requests
import time
from typing import Optional, List, Tuple

# TMDB API Configuration
TMDB_API_KEY = "0ec8764a109b727d05b2b31d218d6099"
TMDB_BASE_URL = "https://api.themoviedb.org/3"
REQUEST_DELAY = 0.25  # 250ms delay between requests (4 requests/second to stay under free tier limits)

# File paths
INPUT_FILE = "movie(slipt date).csv"
OUTPUT_FILE = "movie_cleaned.csv"


def search_movie_on_tmdb(movie_name: str, release_year: int) -> Optional[dict]:
    """
    Search for a movie on TMDB using name and year.
    
    Args:
        movie_name: The name of the movie
        release_year: The release year of the movie
    
    Returns:
        Movie data dict if found, None otherwise
    """
    search_url = f"{TMDB_BASE_URL}/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "query": movie_name,
        "year": release_year,
        "language": "en-US"
    }
    
    try:
        response = requests.get(search_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Return the first result if available
        if data.get("results") and len(data["results"]) > 0:
            return data["results"][0]
        return None
    
    except requests.exceptions.RequestException as e:
        print(f"  ⚠️  API request error for '{movie_name}': {e}")
        return None


def get_movie_origin_country(movie_id: int) -> Optional[List[str]]:
    """
    Get the origin_country for a specific movie by its TMDB ID.
    
    Args:
        movie_id: The TMDB movie ID
    
    Returns:
        List of country codes or None if not found
    """
    details_url = f"{TMDB_BASE_URL}/movie/{movie_id}"
    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US"
    }
    
    try:
        response = requests.get(details_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Get origin_country (list of ISO country codes)
        origin_countries = data.get("origin_country", [])
        return origin_countries if origin_countries else None
    
    except requests.exceptions.RequestException as e:
        print(f"  ⚠️  Error fetching movie details (ID: {movie_id}): {e}")
        return None


def enrich_country_data(df: pd.DataFrame, dry_run: bool = False) -> Tuple[pd.DataFrame, List[str]]:
    """
    Enrich the dataset by fixing country codes for rows with 'AU'.
    
    Args:
        df: The input DataFrame
        dry_run: If True, only show what would change without modifying data
    
    Returns:
        Tuple of (updated DataFrame, list of movies that couldn't be found)
    """
    # Track movies that couldn't be matched
    not_found_movies = []
    
    # Filter rows where country == 'AU'
    au_mask = df['country'] == 'AU'
    au_rows = df[au_mask]
    
    print(f"\n🔍 Found {len(au_rows)} movies labeled as 'AU' to check\n")
    print("=" * 80)
    
    # Process each AU-labeled movie
    for idx, row in au_rows.iterrows():
        movie_name = row['names']
        release_year = int(row['release-year'])
        current_country = row['country']
        
        print(f"\n📽️  Processing: '{movie_name}' ({release_year})")
        print(f"   Current country: {current_country}")
        
        # Search for the movie on TMDB
        movie_data = search_movie_on_tmdb(movie_name, release_year)
        time.sleep(REQUEST_DELAY)  # Rate limiting
        
        if movie_data:
            movie_id = movie_data['id']
            tmdb_title = movie_data.get('title', 'N/A')
            
            print(f"   ✓ Found on TMDB: '{tmdb_title}' (ID: {movie_id})")
            
            # Get origin country
            origin_countries = get_movie_origin_country(movie_id)
            time.sleep(REQUEST_DELAY)  # Rate limiting
            
            if origin_countries and len(origin_countries) > 0:
                # Use the first origin country (primary production country)
                new_country = origin_countries[0]
                
                if new_country != current_country:
                    print(f"   🔄 Update: {current_country} -> {new_country}")
                    
                    if not dry_run:
                        df.at[idx, 'country'] = new_country
                else:
                    print(f"   ℹ️  Country already correct: {new_country}")
            else:
                print(f"   ⚠️  No origin_country found in TMDB data")
                not_found_movies.append(f"{movie_name} ({release_year}) - No origin_country in API")
        else:
            print(f"   ❌ Not found on TMDB")
            not_found_movies.append(f"{movie_name} ({release_year}) - Not found in search")
    
    print("\n" + "=" * 80)
    return df, not_found_movies


def main():
    """Main execution function."""
    print("\n" + "=" * 80)
    print("🎬 MOVIE DATASET COUNTRY CODE ENRICHMENT SCRIPT")
    print("=" * 80)
    
    # Load the dataset
    print(f"\n📂 Loading dataset: {INPUT_FILE}")
    try:
        df = pd.read_csv(INPUT_FILE)
        print(f"   ✓ Loaded {len(df)} movies")
        print(f"   Columns: {', '.join(df.columns.tolist())}")
    except FileNotFoundError:
        print(f"   ❌ Error: File '{INPUT_FILE}' not found!")
        return
    except Exception as e:
        print(f"   ❌ Error loading file: {e}")
        return
    
    # Show distribution of countries before cleaning
    print(f"\n📊 Current country distribution:")
    country_counts = df['country'].value_counts()
    for country, count in country_counts.items():
        print(f"   {country}: {count} movies")
    
    # Ask user if they want a dry run
    print(f"\n" + "=" * 80)
    user_choice = input("Run in DRY RUN mode? (y/n): ").strip().lower()
    dry_run = user_choice == 'y'
    
    if dry_run:
        print("\n🔍 DRY RUN MODE - No changes will be saved\n")
    else:
        print("\n✏️  LIVE MODE - Dataset will be updated\n")
    
    # Enrich the data
    df_updated, not_found = enrich_country_data(df, dry_run=dry_run)
    
    # Summary
    print("\n" + "=" * 80)
    print("📋 SUMMARY")
    print("=" * 80)
    
    if not dry_run:
        # Show distribution after cleaning
        print(f"\n📊 Updated country distribution:")
        country_counts_after = df_updated['country'].value_counts()
        for country, count in country_counts_after.items():
            print(f"   {country}: {count} movies")
    
    # Report movies that couldn't be matched
    if not_found:
        print(f"\n⚠️  {len(not_found)} movies could not be matched:")
        for movie in not_found:
            print(f"   - {movie}")
    else:
        print(f"\n✓ All movies were successfully matched!")
    
    # Save the updated dataset
    if not dry_run:
        print(f"\n💾 Saving cleaned dataset to: {OUTPUT_FILE}")
        try:
            df_updated.to_csv(OUTPUT_FILE, index=False)
            print(f"   ✓ Successfully saved!")
        except Exception as e:
            print(f"   ❌ Error saving file: {e}")
    else:
        print(f"\n💡 Dry run complete. No changes saved.")
        print(f"   Run again without dry run mode to save changes.")
    
    print("\n" + "=" * 80)
    print("✅ Script completed!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
