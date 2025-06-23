import pandas as pd
import re
import hashlib

def clean_artist_name(artist):
    """
    Clean and standardize artist names by:
    1. Removing quotes
    2. Standardizing separators to ' - '
    """
    if pd.isna(artist):
        return artist

    # Remove quotes
    artist = str(artist).replace('"', '').replace("'", '')

    # Define patterns for different separators and their replacements
    patterns = [
        r'\s+x\s+',           # " x "
        r'\s+feat\.?\s+',     # " feat " or " feat. "
        r'\s+featuring\s+',   # " featuring "
        r'\s+&\s+',           # " & "
        r'\s*,\s*'            # ", " (comma with optional spaces)
    ]

    # Replace all patterns with " - "
    for pattern in patterns:
        artist = re.sub(pattern, ' - ', artist, flags=re.IGNORECASE)

    # Clean up any multiple spaces and strip
    artist = re.sub(r'\s+', ' ', artist).strip()

    return artist

def generate_song_id(song, artist):
    """
    Generate a consistent song ID based on song name and artist.
    Uses MD5 hash of normalized song+artist combination.
    """
    if pd.isna(song) or pd.isna(artist):
        return None

    # Normalize the combination for consistent hashing
    normalized = f"{str(song).lower().strip()}_{str(artist).lower().strip()}"

    # Generate MD5 hash (first 10 characters for readability)
    song_id = hashlib.md5(normalized.encode()).hexdigest()[:10]

    return song_id

def process_charts_csv(input_file='source_dataset/charts.csv', output_file='charts_processed.csv'):
    """
    Process the charts CSV file according to specifications:
    1. Remove last-week column
    2. Format artist column
    3. Add song_id column
    """
    try:
        # Read the CSV file
        print(f"Reading {input_file}...")
        df = pd.read_csv(input_file)

        print(f"Original shape: {df.shape}")
        print(f"Original columns: {list(df.columns)}")

        # 1. Remove last-week column
        if 'last-week' in df.columns:
            df = df.drop('last-week', axis=1)
            print("Removed 'last-week' column")
        else:
            print("Warning: 'last-week' column not found")

        # 2. Format artist column
        if 'artist' in df.columns:
            print("Cleaning artist names...")
            df['artist'] = df['artist'].apply(clean_artist_name)
            print("Artist column formatted")
        else:
            print("Warning: 'artist' column not found")

        # 3. Add song_id column
        if 'song' in df.columns and 'artist' in df.columns:
            print("Generating song IDs...")
            df['song_id'] = df.apply(lambda row: generate_song_id(row['song'], row['artist']), axis=1)
            print("Song ID column added")
        else:
            print("Warning: Cannot generate song_id - missing 'song' or 'artist' columns")

        # Reorder columns to put song_id at the beginning
        cols = df.columns.tolist()
        if 'song_id' in cols:
            cols.remove('song_id')
            cols.insert(0, 'song_id')
            df = df[cols]

        # Save the processed file
        df.to_csv(output_file, index=False)
        print(f"\nProcessed file saved as: {output_file}")
        print(f"Final shape: {df.shape}")
        print(f"Final columns: {list(df.columns)}")

        # Show sample of processed data
        print("\nSample of processed data:")
        print(df.head())

        # Show some statistics about song_id consistency
        if 'song_id' in df.columns:
            unique_songs = df[['song', 'artist', 'song_id']].drop_duplicates()
            print(f"\nUnique song/artist combinations: {len(unique_songs)}")
            print(f"Total rows: {len(df)}")

            # Check for songs that appear multiple times
            song_counts = df['song_id'].value_counts()
            recurring_songs = song_counts[song_counts > 1]
            if len(recurring_songs) > 0:
                print(f"Songs appearing multiple times: {len(recurring_songs)}")
                print("Top 5 most frequent songs:")
                for song_id, count in recurring_songs.head().items():
                    sample_row = df[df['song_id'] == song_id].iloc[0]
                    print(f"  {sample_row['song']} by {sample_row['artist']}: {count} times")

        return df

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        return None
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return None

# Example usage and testing function
def test_artist_cleaning():
    """Test the artist cleaning function with various examples"""
    test_cases = [
        "Taylor Swift",
        "Post Malone feat. 21 Savage",
        "Dua Lipa & Elton John",
        "The Weeknd x Ariana Grande",
        "Drake featuring Rihanna",
        "Ed Sheeran, Justin Bieber",
        '"Billie Eilish"',
        "Bad Bunny feat. Rosalía",
        "Marshmello & Bastille"
    ]

    print("Testing artist name cleaning:")
    for artist in test_cases:
        cleaned = clean_artist_name(artist)
        print(f"  '{artist}' -> '{cleaned}'")

if __name__ == "__main__":
    # Test the cleaning function
    test_artist_cleaning()

    print("\n" + "="*50 + "\n")

    # Process the actual file
    processed_df = process_charts_csv()

    if processed_df is not None:
        print("\nProcessing completed successfully!")
    else:
        print("\nProcessing failed. Please check the error messages above.")
