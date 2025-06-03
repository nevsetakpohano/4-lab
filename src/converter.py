import pandas as pd

def csv_to_txt(input_path, output_path):
    df = pd.read_csv(input_path)
    df.to_csv(output_path, sep="\t", index=False)


def txt_to_csv(input_path, output_path):
    df = pd.read_csv(input_path, sep="\t")
    df.to_csv(output_path, index=False)
