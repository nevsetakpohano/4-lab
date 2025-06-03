import argparse
from pathlib import Path
from converter import csv_to_txt, txt_to_csv, pdf_to_txt, txt_to_pdf

def main():
    parser = argparse.ArgumentParser(description="File Converter (TXT ↔ PDF ↔ CSV)")
    parser.add_argument("input_file", help="Input file path")
    parser.add_argument("output_file", help="Output file path")
    args = parser.parse_args()
    
    input_path = Path(args.input_file)
    output_path = Path(args.output_file)
    
    if not input_path.exists():
        print(f"Error: File {input_path} not found!")
        return
    
    input_ext = input_path.suffix.lower()
    output_ext = output_path.suffix.lower()
    
    try:
        if input_ext == ".txt" and output_ext == ".csv":
            txt_to_csv(input_path, output_path)
        elif input_ext == ".csv" and output_ext == ".txt":
            csv_to_txt(input_path, output_path)
        elif input_ext == ".pdf" and output_ext == ".txt":
            pdf_to_txt(input_path, output_path)
        elif input_ext == ".txt" and output_ext == ".pdf":
            txt_to_pdf(input_path, output_path)
        else:
            print("Error: Unsupported conversion format")
    except Exception as e:
        print(f"Conversion error: {str(e)}")

if __name__ == "__main__":
    main()