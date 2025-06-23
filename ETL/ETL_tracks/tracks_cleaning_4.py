import pandas as pd
import sys
import os

def remove_release_date_column(input_file, output_file=None):
    """
    Remove the 'release_date' column from a CSV file

    Args:
        input_file (str): Path to input CSV file
        output_file (str): Path for output CSV file (optional)

    Returns:
        bool: True if successful, False otherwise
    """

    try:
        # Read the CSV file
        print(f"Reading CSV file: {input_file}...")
        df = pd.read_csv(input_file)

        print(f"Original CSV loaded: {len(df)} rows, {len(df.columns)} columns")

        # Check if 'release_date' column exists
        if 'release_date' not in df.columns:
            print("Warning: 'release_date' column not found in the CSV file.")
            print("Available columns:", list(df.columns))
            return False

        # Remove the 'release_date' column
        df_cleaned = df.drop('release_date', axis=1)

        print(f"Removed 'release_date' column. New CSV: {len(df_cleaned)} rows, {len(df_cleaned.columns)} columns")

        # Determine output filename
        if output_file is None:
            # Create output filename by adding '_no_release_date' before the extension
            base_name, ext = os.path.splitext(input_file)
            output_file = f"{base_name}_no_release_date{ext}"

        # Save the cleaned CSV
        df_cleaned.to_csv(output_file, index=False)

        print(f"Cleaned CSV saved as: {output_file}")

        # Show column structure
        print("\nFinal column structure:")
        for i, col in enumerate(df_cleaned.columns, 1):
            print(f"{i:2d}. {col}")

        return True

    except FileNotFoundError:
        print(f"Error: Could not find file '{input_file}'")
        return False
    except Exception as e:
        print(f"Error processing file: {e}")
        return False

def main():
    """Main function to run the script"""
    print("=== Remove Release Date Column from CSV ===\n")

    # Get file paths from command line arguments or user input
    if len(sys.argv) >= 2:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
    else:
        input_file = input("Enter path to input CSV file: ").strip()
        if not input_file:
            print("Error: No input file specified.")
            return

        output_file = input("Enter output filename (or press Enter for auto-generated name): ").strip()
        if not output_file:
            output_file = None

    # Process the file
    success = remove_release_date_column(input_file, output_file)

    if success:
        print("\nScript completed successfully!")
    else:
        print("\nScript failed. Please check your input file and try again.")

if __name__ == "__main__":
    main()
