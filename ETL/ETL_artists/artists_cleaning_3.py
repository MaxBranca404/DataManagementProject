#!/usr/bin/env python3
"""
drop_artist_img.py

Read merge_artist.csv, drop the artist_img column,
and save the cleaned file to merge_artist_no_img.csv.

Usage:
    python drop_artist_img.py           # uses the default filenames
    python drop_artist_img.py input.csv output.csv
"""

import sys
import pandas as pd

def main(infile: str = "artists_final.csv",
         outfile: str = "artists_final_no_img.csv") -> None:
    df = pd.read_csv(infile)

    # Silently ignore if the column is already missing
    if "artist_img" in df.columns:
        df = df.drop(columns=["artist_img"])

    df.to_csv(outfile, index=False)
    print(f"✓ Wrote cleaned file to {outfile}")

if __name__ == "__main__":
    # Allow custom filenames from the command line
    if len(sys.argv) >= 2:
        infile = sys.argv[1]
        outfile = sys.argv[2] if len(sys.argv) >= 3 else "artists_final_no_img.csv"
        main(infile, outfile)
    else:
        main()
