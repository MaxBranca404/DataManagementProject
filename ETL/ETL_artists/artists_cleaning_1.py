import pandas as pd
import numpy as np
import hashlib

def process_csv_files():
    """
    Process tracks_final.csv and charts_final.csv to add artist_id columns
    and generate artists.csv with unique artist identifiers.
    """

    # Read the CSV files
    print("Reading CSV files...")
    tracks_df = pd.read_csv('tracks_final.csv')
    charts_df = pd.read_csv('charts_final.csv')

    print(f"Loaded {len(tracks_df)} tracks and {len(charts_df)} chart entries")

    # Extract all unique artists from both datasets
    print("Extracting unique artists...")

    # Get artists from tracks (may contain multiple artists separated by commas)
    tracks_artists = set()
    for artists_str in tracks_df['artists'].dropna():
        # Split by comma and clean up whitespace
        artists = [artist.strip() for artist in str(artists_str).split(',')]
        tracks_artists.update(artists)

    # Get artists from charts
    charts_artists = set()
    for artist_str in charts_df['artist'].dropna():
        # Split by comma and clean up whitespace (in case of collaborations)
        artists = [artist.strip() for artist in str(artist_str).split(',')]
        charts_artists.update(artists)

    # Combine all unique artists
    all_artists = tracks_artists.union(charts_artists)
    all_artists = sorted(list(all_artists))  # Sort for consistency

    print(f"Found {len(all_artists)} unique artists")

    # Function to generate MD5 hash from artist name
    def generate_artist_id(artist_name):
        # Normalize the artist name (lowercase, strip whitespace)
        normalized_name = artist_name.strip().lower()
        # Generate MD5 hash
        return hashlib.md5(normalized_name.encode('utf-8')).hexdigest()

    # Create artist_id mapping using MD5 hashes
    artist_to_id = {artist: generate_artist_id(artist) for artist in all_artists}

    # Create artists.csv
    artists_df = pd.DataFrame({
        'artist_id': [artist_to_id[artist] for artist in all_artists],
        'artist_name': all_artists
    })

    # Function to get artist_id for a string that may contain multiple artists
    def get_artist_ids(artists_str):
        if pd.isna(artists_str):
            return None
        artists = [artist.strip() for artist in str(artists_str).split(',')]
        # Return comma-separated list of artist_ids
        ids = [artist_to_id[artist] for artist in artists if artist in artist_to_id]
        return ','.join(ids) if ids else None

    # Add artist_id column to tracks_df
    print("Adding artist_id to tracks dataset...")
    tracks_df['artist_id'] = tracks_df['artists'].apply(get_artist_ids)

    # Add artist_id column to charts_df
    print("Adding artist_id to charts dataset...")
    charts_df['artist_id'] = charts_df['artist'].apply(get_artist_ids)

    # Save the updated CSV files
    print("Saving updated CSV files...")
    tracks_df.to_csv('tracks_final_with_artist_id.csv', index=False)
    charts_df.to_csv('charts_final_with_artist_id.csv', index=False)
    artists_df.to_csv('artists_id.csv', index=False)

    # Print summary statistics
    print("\n=== SUMMARY ===")
    print(f"Total unique artists: {len(all_artists)}")
    print(f"Tracks with artist_id: {tracks_df['artist_id'].notna().sum()}/{len(tracks_df)}")
    print(f"Charts with artist_id: {charts_df['artist_id'].notna().sum()}/{len(charts_df)}")

    print("\nFiles created:")
    print("- tracks_final_with_artist_id.csv")
    print("- charts_final_with_artist_id.csv")
    print("- artists.csv")

    # Show sample of artists.csv
    print("\nSample of artists.csv:")
    print(artists_df.head(10))

    # Show sample of how artist_id looks in tracks
    print("\nSample of tracks with artist_id:")
    sample_tracks = tracks_df[['name', 'artists', 'artist_id']].head(5)
    print(sample_tracks)

    return tracks_df, charts_df, artists_df

if __name__ == "__main__":
    try:
        tracks_df, charts_df, artists_df = process_csv_files()
        print("\nProcessing completed successfully!")
    except FileNotFoundError as e:
        print(f"Error: Could not find CSV file - {e}")
        print("Make sure 'tracks_final.csv' and 'charts_final.csv' are in the same directory as this script.")
    except Exception as e:
        print(f"Error processing files: {e}")
