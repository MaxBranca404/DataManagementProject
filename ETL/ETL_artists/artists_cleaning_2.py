#!/usr/bin/env python3
"""merge_artists.py

Merge two artist CSV files.

Usage:
    python merge_artists.py artist.csv artist_todo.csv [merged_output.csv] [overlap_output.csv]

Outputs:
    - merged_output.csv (default: artist_final.csv)
    - overlap_output.csv (default: artist_overlap.csv)

The script:
    1. Keeps the artist_id from artist.csv.
    2. Matches rows on artist_name (case‑insensitive, trimmed).
    3. Adds artist_genre, artist_img and country from artist_todo.csv where available.
    4. Leaves missing columns blank if no match is found.
    5. Writes a second CSV listing artist_name values that appeared in both input files.
"""

import sys
import pandas as pd
from pathlib import Path

def merge_artists(base_csv: str,
                  todo_csv: str,
                  merged_out: str = "artist_final.csv",
                  overlap_out: str = "artist_overlap.csv") -> None:
    """Carry out the merge and write the outputs."""
    df_base = pd.read_csv(base_csv)
    df_todo = pd.read_csv(todo_csv)

    # Build a normalised key for matching
    df_base["__key__"] = df_base["artist_name"].str.strip().str.lower()
    df_todo["__key__"] = df_todo["artist_name"].str.strip().str.lower()

    # Columns to copy across (ignore the artist_id from artist_todo)
    cols_to_add = ["artist_genre", "artist_img", "country"]
    df_todo_subset = df_todo.set_index("__key__")[cols_to_add]

    merged = (
        df_base
        .set_index("__key__")
        .join(df_todo_subset, how="left")
        .reset_index(drop=True)
    )

    # Re‑order columns for clarity
    ordered_cols = ["artist_id", "artist_name"] + cols_to_add
    merged = merged[ordered_cols]

    merged.to_csv(merged_out, index=False)

    # Artists present in both input files
    overlap = (
        df_base[df_base["__key__"].isin(df_todo["__key__"])]
        ["artist_name"]
        .drop_duplicates()
    )
    overlap.to_csv(overlap_out, index=False, header=["artist_name"])

    print(f"✓ Merged file written to {merged_out}")
    print(f"✓ Overlap file written to {overlap_out}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python merge_artists.py artist.csv artist_todo.csv [merged_output.csv] [overlap_output.csv]")
        sys.exit(1)

    merge_artists(*sys.argv[1:])
