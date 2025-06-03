import pandas as pd

def csv_to_txt(input_path, output_path):
    df = pd.read_csv(input_path)
    df.to_csv(output_path, sep="\t", index=False)