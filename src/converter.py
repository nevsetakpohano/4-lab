import pandas as pd
from PyPDF2 import PdfReader, PdfWriter

def csv_to_txt(input_path, output_path):
    df = pd.read_csv(input_path)
    df.to_csv(output_path, sep="\t", index=False)


def txt_to_csv(input_path, output_path):
    df = pd.read_csv(input_path, sep="\t")
    df.to_csv(output_path, index=False)

def pdf_to_txt(input_path, output_path):
    with open(input_path, 'rb') as file:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
    
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(text)

def txt_to_pdf(input_path, output_path):
    writer = PdfWriter()
    
    with open(input_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    writer.add_blank_page(width=72 * 8.27, height=72 * 11.69)
    
    with open(output_path, 'wb') as file:
        writer.write(file)