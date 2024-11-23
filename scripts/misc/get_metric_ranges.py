import pandas as pd
import sys

def min_max_csv(file_path):
    # Read the CSV file
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"The file '{file_path}' was not found.")
        return
    except pd.errors.EmptyDataError:
        print("The file is empty.")
        return
    except pd.errors.ParserError:
        print("Error while parsing the file.")
        return

    # Output the minimum and maximum value for each column
    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            min_value = df[column].min()
            max_value = df[column].max()
            print(f"Column '{column}': Min = {min_value}, Max = {max_value}")
        else:
            print(f"Column '{column}' is not numeric and will be skipped.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python min_max_csv.py <path_to_csv_file>")
    else:
        csv_file_path = sys.argv[1]
        min_max_csv(csv_file_path)
