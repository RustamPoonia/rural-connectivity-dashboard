import pandas as pd


def load_data(file_path):
    """Load the GP Wise Data CSV."""
    return pd.read_csv(
        file_path,
        dtype={"GP Code": "string"}
    )


def clean_data(df):
    """Perform basic data cleaning."""
    df = df.copy()

    # Standardize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("/", "_", regex=False)
    )

    # Remove extra spaces from text columns
    text_columns = df.select_dtypes(
        include=["object", "string"]
    ).columns

    for column in text_columns:
        df[column] = df[column].str.strip()

    return df