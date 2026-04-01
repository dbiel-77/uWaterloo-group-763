import os
import pandas as pd

# =========================
# CONFIG
# =========================

INPUT_FOLDER = "data/input"
OUTPUT_FILE = "data/output/combined.csv"

# List CSVs explicitly if needed, otherwise auto-detect
# Explicitly listed due to no standard convention, or folder standardization
CSV_FILES = [
    'employment_2021.csv',
    'Knowledge of Official Languages - Florence Daran.csv',
    'Land Area Data - Denish Manogarakumar.csv',
    'Population Data Transposed - Alireza Nouri.csv',
    'TransposedPopDwelCountMNK.csv',
    'Data Set(Visual Minorities) - Andrew.csv',
    'Immigration - Akshini Nithi.csv',
]

# =========================
# LOADING ----- COMPLETE
# =========================

def load_csv(file_path):
    """
    Load a CSV file into a DataFrame.

    #TODO:
    - Handle encoding issues if they arise -- this has not been added for the time being
    """
    
    try:
        df = pd.read_csv(file_path, dtype={"DGUID": str})
        return df

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None

    except pd.errors.EmptyDataError:
        print(f"File is empty: {file_path}")
        return None

    except pd.errors.ParserError as e:
        print(f"Parser error in {file_path}: {e}")
        return None

    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None


def load_all_csvs(folder):
    """
    Load all CSV files from a folder.

    Returns:
        dict of {filename: DataFrame}
    """
    dataframes = {}

    files = CSV_FILES if CSV_FILES else [
        f for f in os.listdir(folder) if f.endswith(".csv")
    ]

    for file in files:
        path = os.path.join(folder, file)
        df = load_csv(path)

        if df is not None:
            dataframes[file] = df

    return dataframes

# =========================
# CLEANING PER FILE
# =========================

def clean_dataframe(name, df):
    """
    Apply file-specific cleaning logic.

    #TODO: Add cleaning rules for each file, such as:
    - Add conditional logic per file
    - Standardize column names
    - Ensure DGUID exists and is formatted consistently
    """

    # Example placeholder logic
    df.columns = df.columns.str.strip()

    if "DGUID" not in df.columns:
        print(f"Warning: {name} missing DGUID")

    # TODO: Add file-specific rules
    # if name == "file1.csv":
    #     df = ...

    return df


def clean_all(dataframes):
    """
    Apply cleaning to all DataFrames.
    """
    cleaned = {}

    for name, df in dataframes.items():
        cleaned[name] = clean_dataframe(name, df)

    return cleaned


# =========================
# MERGING
# =========================

def merge_dataframes(dataframes):
    """
    Merge all DataFrames on DGUID.

    #TODO: Add logic to handle merging:
    - Decide join type (inner, left, outer)
    - Handle duplicate columns
    """

    dfs = list(dataframes.values())

    if not dfs:
        return pd.DataFrame()

    merged = dfs[0]

    for df in dfs[1:]:
        merged = pd.merge(
            merged,
            df,
            on="DGUID",
            how="outer",  # you can tweak this one
            suffixes=("", "_dup")
        )

    return merged


# =========================
# POST-MERGE CLEANING
# =========================

def post_merge_cleanup(df):
    """
    Final cleanup after merging.

    #TODO: Add logic to handle issues that arise from merging, such as:
    - Remove duplicate columns
    - Handle missing values
    - Reorder columns
    """

    # Example: drop duplicate columns created by merge
    dup_cols = [col for col in df.columns if col.endswith("_dup")]
    df = df.drop(columns=dup_cols)

    return df


# =========================
# EXPORT
# =========================

def save_output(df, output_path):
    """
    Save final DataFrame to CSV.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    df.to_csv(output_path, index=False)
    print(f"Saved to {output_path}")


# =========================
# MAIN PIPELINE
# =========================

def main():
    """
    Full pipeline:
    1. Load
    2. Clean individually
    3. Merge
    4. Post-clean
    5. Export
    """

    data = load_all_csvs(INPUT_FOLDER)

    cleaned = clean_all(data)

    merged = merge_dataframes(cleaned)

    final_df = post_merge_cleanup(merged)

    save_output(final_df, OUTPUT_FILE)


if __name__ == "__main__":
    main()
