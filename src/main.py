import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="File Converter (TXT ↔ PDF ↔ CSV)")
    parser.add_argument("input_file", help="Input file path")
    parser.add_argument("output_file", help="Output file path")
    args = parser.parse_args()
    
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: File {input_path} not found!")
        return
        
    print(f"Converting {args.input_file} to {args.output_file}")

if __name__ == "__main__":
    main()