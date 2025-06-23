import pandas as pd
import ast
import sys

def process_music_csv(input_file, output_file=None):
    """
    Process music CSV file by removing specified columns and cleaning artists data.

    Args:
        input_file (str): Path to input CSV file
        output_file (str): Path to output CSV file (optional)
    """
    try:
        # Read the CSV file
        print(f"Reading CSV file: {input_file}")
        df = pd.read_csv(input_file)

        print(f"Original dataset shape: {df.shape}")
        print(f"Original columns: {list(df.columns)}")

        # Define columns to remove
        columns_to_remove = ['id', 'album_id', 'artist_ids', 'track_number', 'disc_number']

        # Remove specified columns (only if they exist)
        existing_columns_to_remove = [col for col in columns_to_remove if col in df.columns]
        if existing_columns_to_remove:
            df = df.drop(columns=existing_columns_to_remove)
            print(f"Removed columns: {existing_columns_to_remove}")
        else:
            print("No columns to remove found in the dataset")

        # Process the artists column
        if 'artists' in df.columns:
            print("Processing artists column...")

            def extract_main_artist(artists_str):
                """Extract the first (main) artist from the artists string."""
                try:
                    # Handle NaN values
                    if pd.isna(artists_str):
                        return None

                    # Convert string representation of list to actual list
                    if isinstance(artists_str, str):
                        # Handle cases where the string might already be clean
                        if not artists_str.startswith('['):
                            return artists_str.strip()

                        # Use ast.literal_eval to safely evaluate the string as a list
                        artists_list = ast.literal_eval(artists_str)

                        # Return the first artist if list is not empty
                        if artists_list and len(artists_list) > 0:
                            return artists_list[0].strip()
                        else:
                            return None
                    else:
                        return str(artists_str)

                except (ValueError, SyntaxError) as e:
                    print(f"Error processing artist string '{artists_str}': {e}")
                    # Fallback: try to extract manually
                    if isinstance(artists_str, str) and '[' in artists_str:
                        # Remove brackets and quotes, then split by comma
                        cleaned = artists_str.strip('[]').replace("'", "").replace('"', '')
                        first_artist = cleaned.split(',')[0].strip()
                        return first_artist if first_artist else None
                    return str(artists_str) if not pd.isna(artists_str) else None

            # Apply the extraction function
            df['artists'] = df['artists'].apply(extract_main_artist)

            # Show some examples of the transformation
            print("\nSample artist transformations:")
            non_null_artists = df['artists'].dropna().head(5)
            for i, artist in enumerate(non_null_artists):
                print(f"  {i+1}. {artist}")
        else:
            print("Warning: 'artists' column not found in the dataset")

        print(f"\nProcessed dataset shape: {df.shape}")
        print(f"Final columns: {list(df.columns)}")

        # Save the processed data
        if output_file is None:
            # Create output filename based on input filename
            if input_file.endswith('.csv'):
                output_file = input_file.replace('.csv', '_processed.csv')
            else:
                output_file = input_file + '_processed.csv'

        df.to_csv(output_file, index=False)
        print(f"\nProcessed data saved to: {output_file}")

        # Display basic statistics
        print(f"\nDataset summary:")
        print(f"- Total rows: {len(df)}")
        print(f"- Total columns: {len(df.columns)}")
        if 'artists' in df.columns:
            unique_artists = df['artists'].nunique()
            print(f"- Unique artists: {unique_artists}")

        return df

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        return None
    except Exception as e:
        print(f"Error processing file: {e}")
        return None

def main():
    """Main function to run the script."""
    if len(sys.argv) < 2:
        print("Usage: python script.py <input_csv_file> [output_csv_file]")
        print("Example: python script.py music_data.csv")
        print("Example: python script.py music_data.csv cleaned_music_data.csv")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    # Process the CSV file
    processed_df = process_music_csv(input_file, output_file)

    if processed_df is not None:
        print("\nProcessing completed successfully!")
    else:
        print("\nProcessing failed.")

if __name__ == "__main__":
    main()
