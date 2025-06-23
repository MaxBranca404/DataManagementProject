import pandas as pd
import sys
from collections import Counter

def analyze_song_ids(csv_file):
    """
    Analyze song_id column for unique values and provide detailed statistics

    Args:
        csv_file (str): Path to the CSV file

    Returns:
        dict: Dictionary containing analysis results
    """

    try:
        # Read the CSV file
        print(f"Reading CSV file: {csv_file}...")
        df = pd.read_csv(csv_file)

        print(f"CSV loaded successfully: {len(df)} rows, {len(df.columns)} columns")

        # Check if 'song_id' column exists
        if 'song_id' not in df.columns:
            print("\nError: 'song_id' column not found in the CSV file.")
            print("Available columns:", list(df.columns))
            return None

        print(f"\nAnalyzing 'song_id' column...")

        # Get song_id column
        song_ids = df['song_id']

        # Handle missing values
        non_null_song_ids = song_ids.dropna()
        null_count = len(song_ids) - len(non_null_song_ids)

        # Convert to string to handle mixed types
        song_ids_str = non_null_song_ids.astype(str)

        # Basic statistics
        total_song_ids = len(song_ids)
        total_non_null = len(non_null_song_ids)
        unique_song_ids = song_ids_str.nunique()
        duplicate_count = total_non_null - unique_song_ids

        # Calculate percentages
        unique_percentage = (unique_song_ids / total_non_null * 100) if total_non_null > 0 else 0
        duplicate_percentage = (duplicate_count / total_non_null * 100) if total_non_null > 0 else 0
        null_percentage = (null_count / total_song_ids * 100) if total_song_ids > 0 else 0

        # Print detailed analysis
        print("\n" + "="*60)
        print("           SONG ID ANALYSIS RESULTS")
        print("="*60)

        print(f"\n📊 BASIC STATISTICS:")
        print(f"   Total rows in CSV:           {total_song_ids:,}")
        print(f"   Non-null song IDs:           {total_non_null:,}")
        print(f"   Null/empty song IDs:         {null_count:,}")
        print(f"   Unique song IDs:             {unique_song_ids:,}")
        print(f"   Duplicate song IDs:          {duplicate_count:,}")

        print(f"\n📈 PERCENTAGES:")
        print(f"   Unique IDs percentage:       {unique_percentage:.2f}%")
        print(f"   Duplicate IDs percentage:    {duplicate_percentage:.2f}%")
        if null_count > 0:
            print(f"   Null/empty IDs percentage:   {null_percentage:.2f}%")

        # Analyze duplicates if they exist
        if duplicate_count > 0:
            print(f"\n🔍 DUPLICATE ANALYSIS:")

            # Count occurrences of each song_id
            id_counts = Counter(song_ids_str)
            duplicated_ids = {k: v for k, v in id_counts.items() if v > 1}

            print(f"   Number of IDs that appear multiple times: {len(duplicated_ids)}")

            # Show top duplicates
            most_common_duplicates = Counter(duplicated_ids).most_common(10)
            print(f"\n   Top duplicated song IDs:")
            for i, (song_id, count) in enumerate(most_common_duplicates, 1):
                print(f"   {i:2d}. ID '{song_id}' appears {count} times")

            # Distribution of duplicate counts
            duplicate_counts = list(duplicated_ids.values())
            duplicate_distribution = Counter(duplicate_counts)
            print(f"\n   Duplicate distribution:")
            for dup_count in sorted(duplicate_distribution.keys()):
                freq = duplicate_distribution[dup_count]
                print(f"      {freq} IDs appear {dup_count} times each")

        # Sample of unique IDs
        print(f"\n📋 SAMPLE UNIQUE SONG IDs:")
        unique_ids_sample = song_ids_str.unique()[:10]
        for i, sample_id in enumerate(unique_ids_sample, 1):
            print(f"   {i:2d}. {sample_id}")
        if len(unique_ids_sample) == 10 and unique_song_ids > 10:
            print(f"   ... and {unique_song_ids - 10:,} more unique IDs")

        # Data quality assessment
        print(f"\n🎯 DATA QUALITY ASSESSMENT:")
        if unique_percentage >= 95:
            quality = "EXCELLENT"
            emoji = "🟢"
        elif unique_percentage >= 85:
            quality = "GOOD"
            emoji = "🟡"
        elif unique_percentage >= 70:
            quality = "FAIR"
            emoji = "🟠"
        else:
            quality = "POOR"
            emoji = "🔴"

        print(f"   Data uniqueness quality: {emoji} {quality}")
        print(f"   Recommendation: ", end="")

        if unique_percentage >= 95:
            print("Data quality is excellent for unique identification.")
        elif unique_percentage >= 85:
            print("Data quality is good, minor duplicates present.")
        elif unique_percentage >= 70:
            print("Consider investigating duplicate entries.")
        else:
            print("Significant duplicates detected - data cleaning recommended.")

        print("="*60)

        # Return results for potential further processing
        results = {
            'total_rows': total_song_ids,
            'non_null_count': total_non_null,
            'null_count': null_count,
            'unique_count': unique_song_ids,
            'duplicate_count': duplicate_count,
            'unique_percentage': unique_percentage,
            'duplicate_percentage': duplicate_percentage,
            'null_percentage': null_percentage,
            'duplicated_ids': duplicated_ids if duplicate_count > 0 else {}
        }

        return results

    except FileNotFoundError:
        print(f"Error: Could not find file '{csv_file}'")
        return None
    except Exception as e:
        print(f"Error processing file: {e}")
        return None

def save_analysis_report(results, csv_file):
    """Save analysis results to a text file"""
    if results is None:
        return

    output_file = csv_file.replace('.csv', '_song_id_analysis.txt')

    try:
        with open(output_file, 'w') as f:
            f.write("SONG ID ANALYSIS REPORT\n")
            f.write("="*50 + "\n\n")
            f.write(f"Source file: {csv_file}\n")
            f.write(f"Analysis date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            f.write("SUMMARY STATISTICS:\n")
            f.write(f"Total rows: {results['total_rows']:,}\n")
            f.write(f"Non-null song IDs: {results['non_null_count']:,}\n")
            f.write(f"Unique song IDs: {results['unique_count']:,}\n")
            f.write(f"Duplicate song IDs: {results['duplicate_count']:,}\n")
            f.write(f"Unique percentage: {results['unique_percentage']:.2f}%\n")
            f.write(f"Duplicate percentage: {results['duplicate_percentage']:.2f}%\n")

            if results['duplicated_ids']:
                f.write(f"\nDUPLICATE DETAILS:\n")
                for song_id, count in sorted(results['duplicated_ids'].items(),
                                           key=lambda x: x[1], reverse=True)[:20]:
                    f.write(f"ID '{song_id}': {count} occurrences\n")

        print(f"\n📄 Analysis report saved to: {output_file}")

    except Exception as e:
        print(f"Warning: Could not save report file: {e}")

def main():
    """Main function to run the script"""
    print("=== Song ID Unique Values Analyzer ===\n")

    # Get file path from command line argument or user input
    if len(sys.argv) >= 2:
        csv_file = sys.argv[1]
    else:
        csv_file = input("Enter path to CSV file: ").strip()
        if not csv_file:
            print("Error: No input file specified.")
            return

    # Analyze the file
    results = analyze_song_ids(csv_file)

    if results:
        # Ask if user wants to save report
        save_report = input("\nSave detailed report to file? (y/n): ").strip().lower()
        if save_report in ['y', 'yes']:
            save_analysis_report(results, csv_file)

        print("\nAnalysis completed successfully!")
    else:
        print("\nAnalysis failed. Please check your input file and try again.")

if __name__ == "__main__":
    main()
