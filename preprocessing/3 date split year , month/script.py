import pandas as pd
from datetime import datetime

def split_date_features():
    """
    Split the date_x feature into release-month and release-year
    """
    # Load the original CSV file
    input_file = "movie(no ,orig-title,status).csv"
    output_file = "movie(slipt date).csv"
    
    try:
        # Read the CSV file
        df = pd.read_csv(input_file)
        
        print(f"Loaded {len(df)} rows from {input_file}")
        print(f"Columns: {list(df.columns)}")
        
        # Check if date_x column exists
        if 'date_x' not in df.columns:
            print("Error: 'date_x' column not found in the dataset")
            return
        
        # Function to parse date and extract month and year
        def extract_date_components(date_str):
            try:
                # Handle the date format MM/DD/YYYY with potential extra spaces
                date_str = str(date_str).strip()
                
                # Parse the date
                date_obj = datetime.strptime(date_str, '%m/%d/%Y')
                
                return date_obj.month, date_obj.year
            except:
                # Return None for invalid dates
                return None, None
        
        # Apply the function to extract month and year
        print("Extracting release-month and release-year from date_x...")
        
        # Create new columns for month and year
        date_components = df['date_x'].apply(extract_date_components)
        df['release-month'] = [comp[0] for comp in date_components]
        df['release-year'] = [comp[1] for comp in date_components]
        
        # Count valid and invalid dates
        valid_dates = df['release-month'].notna().sum()
        invalid_dates = len(df) - valid_dates
        
        print(f"Successfully processed {valid_dates} dates")
        if invalid_dates > 0:
            print(f"Warning: {invalid_dates} invalid dates found (set to NaN)")
        
        # Remove the original date_x column
        df = df.drop('date_x', axis=1)
        print("Removed original 'date_x' feature")
        
        # Save to new CSV file
        df.to_csv(output_file, index=False)
        print(f"Data saved to {output_file}")
        
        # Display sample of the new columns
        print("\nSample of new features:")
        sample_cols = ['names', 'release-month', 'release-year']
        print(df[sample_cols].head(10))
        
        # Show summary statistics
        print(f"\nRelease Year Range: {df['release-year'].min()} - {df['release-year'].max()}")
        print(f"Release Month Range: {df['release-month'].min()} - {df['release-month'].max()}")
        
        return df
        
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Run the function
    result_df = split_date_features()