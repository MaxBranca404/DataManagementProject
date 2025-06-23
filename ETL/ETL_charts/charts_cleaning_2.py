import pandas as pd
import hashlib
import re

def normalize_text(text):
    """
    Normalize text by:
    - Converting to lowercase
    - Removing extra whitespace
    - Removing special characters except letters, numbers, and spaces
    """
    if pd.isna(text):
        return ""

    # Convert to string and lowercase
    text = str(text).lower()

    # Remove special characters, keep only alphanumeric and spaces
    text = re.sub(r'[^a-z0-9\s]', '', text)

    # Remove extra whitespace and strip
    text = ' '.join(text.split())

    return text

def generate_song_id(song, artist):
    """
    Generate MD5 hash from normalized song+artist combination
    """
    # Normalize both song and artist
    normalized_song = normalize_text(song)
    normalized_artist = normalize_text(artist)

    # Combine song and artist with a separator
    combined = f"{normalized_song}|{normalized_artist}"

    # Generate MD5 hash
    md5_hash = hashlib.md5(combined.encode('utf-8')).hexdigest()

    return md5_hash

def extract_main_artist(artist):
    """
    Extract main artist by removing featuring artists (text after '-')
    """
    if pd.isna(artist):
        return ""

    # Convert to string and split on '-'
    artist_str = str(artist)
    main_artist = artist_str.split('-')[0].strip()

    return main_artist

def process_charts_csv(input_file='source_dataset/charts.csv', output_file='charts_processed4.csv'):
    """
    Process the charts CSV file:
    1. Remove existing song_id column
    2. Extract main artist (remove featuring artists after '-')
    3. Generate new song_id column with MD5 hash
    """
    try:
        # Read the CSV file
        print(f"Reading {input_file}...")
        df = pd.read_csv(input_file)

        # Display original shape and columns
        print(f"Original data shape: {df.shape}")
        print(f"Original columns: {list(df.columns)}")

        # Remove existing song_id column if it exists
        if 'song_id' in df.columns:
            df = df.drop('song_id', axis=1)
            print("Removed existing song_id column")

        # Check if required columns exist
        required_columns = ['song', 'artist']
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

        # Extract main artist (remove featuring artists)
        print("Extracting main artists (removing featuring artists after '-')...")
        df['artist'] = df['artist'].apply(extract_main_artist)

        # Show some examples of artist extraction
        print("\nSample of artist extraction:")
        sample_artists = df['artist'].head(10).unique()[:5]
        for artist in sample_artists:
            print(f"Main artist: '{artist}'")

        # Generate new song_id column
        print("\nGenerating new song_id column with MD5 hashes...")
        df['song_id'] = df.apply(lambda row: generate_song_id(row['song'], row['artist']), axis=1)

        # Reorder columns to put song_id first
        columns = ['song_id'] + [col for col in df.columns if col != 'song_id']
        df = df[columns]

        # Display some examples
        print("\nSample of generated song IDs:")
        sample_df = df[['song_id', 'song', 'artist']].head()
        for _, row in sample_df.iterrows():
            print(f"Song: '{row['song']}' | Artist: '{row['artist']}' | ID: {row['song_id']}")

        # Check for duplicate song IDs
        duplicate_count = df['song_id'].duplicated().sum()
        unique_songs = df['song_id'].nunique()
        total_rows = len(df)

        print(f"\nStatistics:")
        print(f"Total rows: {total_rows}")
        print(f"Unique song IDs: {unique_songs}")
        print(f"Duplicate song IDs: {duplicate_count}")

        # Save the processed data
        df.to_csv(output_file, index=False)
        print(f"\nProcessed data saved to {output_file}")
        print(f"Final data shape: {df.shape}")
        print(f"Final columns: {list(df.columns)}")

        return df

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return None

if __name__ == "__main__":
    # Process the charts.csv file
    processed_df = process_charts_csv()

    if processed_df is not None:
        print("\nProcessing completed successfully!")
    else:
        print("\nProcessing failed!")
