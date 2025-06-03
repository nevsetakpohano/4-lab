import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.converter import csv_to_txt, txt_to_csv, pdf_to_txt, txt_to_pdf
import pandas as pd
import tempfile
from PyPDF2 import PdfWriter

def test_csv_to_txt():

    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as csv_file:
        csv_path = csv_file.name
        pd.DataFrame({"Name": ["Test"], "Value": [123]}).to_csv(csv_path, index=False)
    
    txt_path = csv_path.replace('.csv', '.txt')
    
    csv_to_txt(csv_path, txt_path)

    assert os.path.exists(txt_path)
    with open(txt_path, 'r') as f:
        content = f.read()
        print("Converted content:", content)
        assert "Test\t123" in content
    
    os.unlink(csv_path)
    os.unlink(txt_path)

def test_txt_to_csv():
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as txt_file:
        txt_path = txt_file.name
        with open(txt_path, 'w') as f:
            f.write("Name\tValue\nTest\t123")
    
    csv_path = txt_path.replace('.txt', '.csv')
    
    txt_to_csv(txt_path, csv_path)
    
    assert os.path.exists(csv_path)
    df = pd.read_csv(csv_path)
    print("Converted DataFrame:", df)
    assert "Test" in df["Name"].values
    assert 123 in df["Value"].values
    
    os.unlink(txt_path)
    os.unlink(csv_path)


def test_pdf_to_txt():
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as pdf_file:
        writer = PdfWriter()
        writer.add_blank_page(width=72, height=72)
        with open(pdf_file.name, 'wb') as f:
            writer.write(f)
    
    txt_path = pdf_file.name.replace('.pdf', '.txt')
    pdf_to_txt(pdf_file.name, txt_path)
    
    assert os.path.exists(txt_path)
    os.unlink(pdf_file.name)
    os.unlink(txt_path)

def test_txt_to_pdf():
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as txt_file:
        with open(txt_file.name, 'w') as f:
            f.write("Test content")
    
    pdf_path = txt_file.name.replace('.txt', '.pdf')
    txt_to_pdf(txt_file.name, pdf_path)
    
    assert os.path.exists(pdf_path)
    assert os.path.getsize(pdf_path) > 100
    os.unlink(txt_file.name)
    os.unlink(pdf_path)


def test_csv_to_pdf():
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as csv_file:
        csv_path = csv_file.name
        pd.DataFrame({"Name": ["Test"], "Value": [123]}).to_csv(csv_path, index=False)

    pdf_path = csv_path.replace('.csv', '.pdf')
    csv_to_pdf(csv_path, pdf_path)

    assert os.path.exists(pdf_path)
    assert os.path.getsize(pdf_path) > 100

    reader = PdfReader(pdf_path)
    assert len(reader.pages) > 0
    content = reader.pages[0].extract_text()
    assert "Name" in content
    assert "Test" in content
    assert "123" in content

    os.unlink(csv_path)
    os.unlink(pdf_path)


def test_pdf_to_csv():
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as pdf_file:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Table

        doc = SimpleDocTemplate(pdf_file.name, pagesize=letter)
        data = [["Name", "Value"], ["Test", "123"]]
        table = Table(data)
        doc.build([table])

    csv_path = pdf_file.name.replace('.pdf', '.csv')
    pdf_to_csv(pdf_file.name, csv_path)

    assert os.path.exists(csv_path)
    df = pd.read_csv(csv_path)
    assert "Name" in df.columns
    assert "Test" in df["Name"].values
    assert 123 in df["Value"].values

    os.unlink(pdf_file.name)
    os.unlink(csv_path)

if __name__ == "__main__":
    import pytest
    pytest.main([__file__])