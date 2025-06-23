import pandas as pd
import hashlib
import sys
import re
import unicodedata

def normalize_text(text):
    """
    Normalize text for comparison by:
    - Converting to lowercase
    - Removing accents and special characters
    - Removing extra whitespace
    - Removing common punctuation
    """
    if pd.isna(text) or text is None:
        return ""

    # Convert to string and lowercase
    text = str(text).lower()

    # Remove accents and normalize unicode
    text = unicodedata.normalize('NFD', text)
    text = ''.join(char for char in text if unicodedata.category(char) != 'Mn')

    # Remove common punctuation and special characters
    text = re.sub(r'[^\w\s]', '', text)

    # Remove extra whitespace
    text = ' '.join(text.split())

    return text.strip()

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

def remove_duplicates_and_generate_ids(input_file, output_file=None, song_column='name', artist_column='artists'):
    """
    Remove duplicate songs based on normalized song name and artist, and generate unique song IDs.

    Args:
        input_file (str): Path to input CSV file
        output_file (str): Path to output CSV file (optional)
        song_column (str): Name of the column containing song names
        artist_column (str): Name of the column containing artist names
    """
    try:
        # Read the CSV file
        print(f"Reading CSV file: {input_file}")
        df = pd.read_csv(input_file)

        print(f"Original dataset shape: {df.shape}")
        original_count = len(df)

        # Check if required columns exist
        if song_column not in df.columns:
            print(f"Error: Column '{song_column}' not found in the dataset")
            print(f"Available columns: {list(df.columns)}")
            return None

        if artist_column not in df.columns:
            print(f"Error: Column '{artist_column}' not found in the dataset")
            print(f"Available columns: {list(df.columns)}")
            return None

        # Generate song IDs for all rows
        print("Generating song IDs...")
        df['song_id'] = df.apply(lambda row: generate_song_id(row[song_column], row[artist_column]), axis=1)

        # Show some examples of generated IDs
        print("\nSample song ID generations:")
        for i in range(min(5, len(df))):
            song = df.iloc[i][song_column]
            artist = df.iloc[i][artist_column]
            song_id = df.iloc[i]['song_id']
            print(f"  {i+1}. '{song}' by '{artist}' → {song_id}")

        # Create normalized columns for duplicate detection
        df['normalized_song'] = df[song_column].apply(normalize_text)
        df['normalized_artist'] = df[artist_column].apply(normalize_text)

        # Find duplicates based on normalized song and artist
        print("\nIdentifying duplicates...")
        duplicate_mask = df.duplicated(subset=['normalized_song', 'normalized_artist'], keep='first')
        duplicate_count = duplicate_mask.sum()

        if duplicate_count > 0:
            print(f"Found {duplicate_count} duplicate songs")

            # Show some examples of duplicates that will be removed
            duplicates_df = df[duplicate_mask].head(10)
            if len(duplicates_df) > 0:
                print("\nExamples of duplicates being removed:")
                for i, (_, row) in enumerate(duplicates_df.iterrows()):
                    print(f"  {i+1}. '{row[song_column]}' by '{row[artist_column]}'")
        else:
            print("No duplicates found")

        # Remove duplicates (keep first occurrence)
        df_deduplicated = df[~duplicate_mask].copy()

        # Remove the temporary normalization columns
        df_deduplicated = df_deduplicated.drop(columns=['normalized_song', 'normalized_artist'])

        # Reorder columns to put song_id first
        columns = ['song_id'] + [col for col in df_deduplicated.columns if col != 'song_id']
        df_deduplicated = df_deduplicated[columns]

        final_count = len(df_deduplicated)
        removed_count = original_count - final_count

        print(f"\nDeduplication summary:")
        print(f"- Original songs: {original_count}")
        print(f"- Duplicates removed: {removed_count}")
        print(f"- Final unique songs: {final_count}")
        print(f"- Reduction: {removed_count/original_count*100:.1f}%")

        # Save the processed data
        if output_file is None:
            if input_file.endswith('.csv'):
                output_file = input_file.replace('.csv', '_deduplicated.csv')
            else:
                output_file = input_file + '_deduplicated.csv'

        df_deduplicated.to_csv(output_file, index=False)
        print(f"\nDeduplicated data saved to: {output_file}")

        # Additional statistics
        print(f"\nFinal dataset info:")
        print(f"- Total columns: {len(df_deduplicated.columns)}")
        print(f"- Unique artists: {df_deduplicated[artist_column].nunique()}")
        print(f"- Unique song IDs: {df_deduplicated['song_id'].nunique()}")

        # Verify song_id uniqueness
        if df_deduplicated['song_id'].nunique() != len(df_deduplicated):
            print("Warning: Some song IDs are not unique! This shouldn't happen.")
        else:
            print("✓ All song IDs are unique")

        return df_deduplicated

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        return None
    except Exception as e:
        print(f"Error processing file: {e}")
        return None

def main():
    """Main function to run the script."""
    if len(sys.argv) < 2:
        print("Usage: python script.py <input_csv_file> [output_csv_file] [song_column] [artist_column]")
        print("Example: python script.py music_data.csv")
        print("Example: python script.py music_data.csv deduplicated_music.csv")
        print("Example: python script.py music_data.csv deduplicated_music.csv name artists")
        print("\nDefault column names: 'name' for songs, 'artists' for artists")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    song_column = sys.argv[3] if len(sys.argv) > 3 else 'name'
    artist_column = sys.argv[4] if len(sys.argv) > 4 else 'artists'

    print(f"Processing file: {input_file}")
    print(f"Song column: '{song_column}'")
    print(f"Artist column: '{artist_column}'")
    print()

    # Process the CSV file
    processed_df = remove_duplicates_and_generate_ids(input_file, output_file, song_column, artist_column)

    if processed_df is not None:
        print("\nDeduplication completed successfully!")
    else:
        print("\nDeduplication failed.")

if __name__ == "__main__":
    main()
