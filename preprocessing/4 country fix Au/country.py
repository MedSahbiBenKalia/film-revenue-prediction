import pandas as pd
import csv

def count_countries_and_save():
    """
    Read the movie dataset, count country occurrences, sort them, 
    and save to a new CSV file called 'country.csv'
    """
    # Read the movie dataset
    try:
        df = pd.read_csv('movie_cleaned.csv')
        print(f"Successfully loaded {len(df)} records from movie dataset")
        
        # Count occurrences of each country
        country_counts = df['country'].value_counts()
        
        # Create a new dataframe with country and count columns
        result_df = pd.DataFrame({
            'country': country_counts.index,
            'count': country_counts.values
        })
        
        # Sort by count in descending order (most frequent countries first)
        result_df = result_df.sort_values('count', ascending=False).reset_index(drop=True)
        
        # Save to CSV file
        result_df.to_csv('country.csv', index=False)
        
        print(f"\nCountry occurrence report:")
        print(f"Total unique countries: {len(result_df)}")
        print("\nTop 10 countries by movie count:")
        print(result_df.head(10).to_string(index=False))
        
        print(f"\nResults saved to 'country.csv'")
        
        return result_df
        
    except FileNotFoundError:
        print("Error: 'movie(slipt date).csv' file not found!")
        return None
    except Exception as e:
        print(f"Error processing data: {str(e)}")
        return None

if __name__ == "__main__":
    count_countries_and_save()