import pandas as pd
import numpy as np
import sys

def create_column_mapping():
    """
    Create mapping between popularity.csv columns and tracks.csv columns

    Returns:
        dict: Mapping dictionary
    """
    return {
        # Direct mappings
        'track_id': 'id',
        'track_name': 'name',
        'artist_name': 'artists',
        'acousticness': 'acousticness',
        'danceability': 'danceability',
        'duration_ms': 'duration_ms',
        'energy': 'energy',
        'instrumentalness': 'instrumentalness',
        'key': 'key',
        'liveness': 'liveness',
        'loudness': 'loudness',
        'mode': 'mode',
        'speechiness': 'speechiness',
        'tempo': 'tempo',
        'time_signature': 'time_signature',
        'valence': 'valence',
        'year': 'year'
    }

def merge_csv_files(tracks_file, popularity_file, output_file=None):
    """
    Merge popularity.csv data into tracks.csv by appending new rows

    Args:
        tracks_file (str): Path to tracks.csv
        popularity_file (str): Path to popularity.csv
        output_file (str): Path for output file (optional)

    Returns:
        bool: True if successful, False otherwise
    """

    try:
        # Read CSV files
        print("Reading CSV files...")
        tracks_df = pd.read_csv(tracks_file)
        popularity_df = pd.read_csv(popularity_file)

        print(f"Tracks CSV loaded: {len(tracks_df)} rows, {len(tracks_df.columns)} columns")
        print(f"Popularity CSV loaded: {len(popularity_df)} rows, {len(popularity_df.columns)} columns")

        # Display column structures
        print(f"\nTracks.csv columns: {list(tracks_df.columns)}")
        print(f"Popularity.csv columns: {list(popularity_df.columns)}")

        # Create column mapping
        column_mapping = create_column_mapping()

        print(f"\nColumn mapping:")
        for pop_col, track_col in column_mapping.items():
            print(f"  {pop_col} → {track_col}")

        # Verify that mapped columns exist
        missing_pop_cols = [col for col in column_mapping.keys() if col not in popularity_df.columns]
        missing_track_cols = [col for col in column_mapping.values() if col not in tracks_df.columns]

        if missing_pop_cols:
            print(f"\nWarning: Missing columns in popularity.csv: {missing_pop_cols}")
        if missing_track_cols:
            print(f"Warning: Missing columns in tracks.csv: {missing_track_cols}")

        # Get all columns from tracks.csv for the new rows structure
        tracks_columns = list(tracks_df.columns)

        # Create new rows from popularity.csv
        print(f"\nProcessing {len(popularity_df)} rows from popularity.csv...")
        new_rows = []

        for index, pop_row in popularity_df.iterrows():
            # Create a new row with NaN/None values for all tracks columns
            new_row = pd.Series([np.nan] * len(tracks_columns), index=tracks_columns)

            # Map values from popularity row to tracks row
            for pop_col, track_col in column_mapping.items():
                if pop_col in popularity_df.columns and track_col in tracks_df.columns:
                    new_row[track_col] = pop_row[pop_col]

            new_rows.append(new_row)

            # Progress indicator
            if (index + 1) % 1000 == 0:
                print(f"  Processed {index + 1} rows...")

        # Convert new rows to DataFrame
        new_rows_df = pd.DataFrame(new_rows)

        # Append new rows to tracks DataFrame
        print(f"Appending {len(new_rows_df)} new rows to tracks.csv...")
        merged_df = pd.concat([tracks_df, new_rows_df], ignore_index=True)

        # Determine output filename
        if output_file is None:
            output_file = tracks_file.replace('.csv', '_merged.csv')

        # Save the merged DataFrame
        merged_df.to_csv(output_file, index=False)

        # Summary statistics
        print(f"\n" + "="*60)
        print("MERGE SUMMARY")
        print("="*60)
        print(f"Original tracks.csv rows:     {len(tracks_df):,}")
        print(f"Popularity.csv rows added:    {len(new_rows_df):,}")
        print(f"Final merged CSV rows:        {len(merged_df):,}")
        print(f"Output file saved as:         {output_file}")

        # Show sample of added data
        print(f"\nSample of added rows (first 5):")
        sample_new_rows = new_rows_df.head(5)
        for i, (idx, row) in enumerate(sample_new_rows.iterrows(), 1):
            print(f"\nRow {i}:")
            for col in ['id', 'name', 'artists', 'danceability', 'energy', 'year']:
                if col in row.index:
                    value = row[col]
                    if pd.isna(value):
                        value = "NULL"
                    print(f"  {col}: {value}")

        # Check for data integrity
        print(f"\nData integrity check:")
        total_nulls = merged_df.isnull().sum().sum()
        total_cells = len(merged_df) * len(merged_df.columns)
        null_percentage = (total_nulls / total_cells) * 100
        print(f"  Total NULL values: {total_nulls:,} ({null_percentage:.2f}% of all cells)")

        # Show NULL counts for key columns
        key_columns = ['id', 'name', 'artists', 'danceability', 'energy']
        print(f"  NULL counts in key columns:")
        for col in key_columns:
            if col in merged_df.columns:
                null_count = merged_df[col].isnull().sum()
                print(f"    {col}: {null_count:,}")

        print("="*60)

        return True

    except FileNotFoundError as e:
        print(f"Error: Could not find file - {e}")
        return False
    except Exception as e:
        print(f"Error processing files: {e}")
        import traceback
        traceback.print_exc()
        return False

def validate_files(tracks_file, popularity_file):
    """
    Validate that the input files have the expected structure

    Args:
        tracks_file (str): Path to tracks.csv
        popularity_file (str): Path to popularity.csv

    Returns:
        bool: True if files are valid, False otherwise
    """

    try:
        # Expected columns
        expected_tracks_cols = [
            'id', 'name', 'album', 'album_id', 'artists', 'artist_ids',
            'track_number', 'disc_number', 'explicit', 'danceability',
            'energy', 'key', 'loudness', 'mode', 'speechiness',
            'acousticness', 'instrumentalness', 'liveness', 'valence',
            'tempo', 'duration_ms', 'time_signature', 'year', 'release_date'
        ]

        expected_pop_cols = [
            'artist_name', 'track_id', 'track_name', 'acousticness',
            'danceability', 'duration_ms', 'energy', 'instrumentalness',
            'key', 'liveness', 'loudness', 'mode', 'speechiness',
            'tempo', 'time_signature', 'valence', 'popularity', 'year'
        ]

        # Read just the headers
        tracks_cols = list(pd.read_csv(tracks_file, nrows=0).columns)
        pop_cols = list(pd.read_csv(popularity_file, nrows=0).columns)

        print("File validation:")
        print(f"  Tracks.csv columns match: {set(tracks_cols) == set(expected_tracks_cols)}")
        print(f"  Popularity.csv columns match: {set(pop_cols) == set(expected_pop_cols)}")

        if set(tracks_cols) != set(expected_tracks_cols):
            missing = set(expected_tracks_cols) - set(tracks_cols)
            extra = set(tracks_cols) - set(expected_tracks_cols)
            if missing:
                print(f"    Missing from tracks.csv: {missing}")
            if extra:
                print(f"    Extra in tracks.csv: {extra}")

        if set(pop_cols) != set(expected_pop_cols):
            missing = set(expected_pop_cols) - set(pop_cols)
            extra = set(pop_cols) - set(expected_pop_cols)
            if missing:
                print(f"    Missing from popularity.csv: {missing}")
            if extra:
                print(f"    Extra in popularity.csv: {extra}")

        return True

    except Exception as e:
        print(f"Error validating files: {e}")
        return False

def main():
    """Main function to run the script"""
    print("=== Merge Popularity Data into Tracks CSV ===\n")

    # Get file paths
    if len(sys.argv) >= 3:
        tracks_file = sys.argv[1]
        popularity_file = sys.argv[2]
        output_file = sys.argv[3] if len(sys.argv) > 3 else None
    else:
        tracks_file = input("Enter path to tracks.csv: ").strip()
        if not tracks_file:
            print("Error: No tracks.csv file specified.")
            return

        popularity_file = input("Enter path to popularity.csv: ").strip()
        if not popularity_file:
            print("Error: No popularity.csv file specified.")
            return

        output_file = input("Enter output filename (or press Enter for auto-generated): ").strip()
        if not output_file:
            output_file = None

    # Validate files
    print("Validating file structures...")
    if not validate_files(tracks_file, popularity_file):
        print("File validation failed. Proceeding anyway...")

    # Process the files
    success = merge_csv_files(tracks_file, popularity_file, output_file)

    if success:
        print("\nScript completed successfully!")
    else:
        print("\nScript failed. Please check your input files and try again.")

if __name__ == "__main__":
    main()
