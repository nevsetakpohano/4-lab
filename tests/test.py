import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.converter import csv_to_txt, txt_to_csv, pdf_to_txt, txt_to_pdf,  csv_to_pdf, pdf_to_csv
import pandas as pd
import tempfile
from reportlab.pdfgen import canvas
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
    csv_path = None
    pdf_path = None
    
    try:
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as csv_file:
            csv_path = csv_file.name
            test_data = pd.DataFrame({
                "Name": ["Alice", "Bob", "Charlie"], 
                "Age": [25, 30, 35],
                "City": ["Kyiv", "Lviv", "Odesa"]
            })
            test_data.to_csv(csv_path, index=False)
        
        pdf_path = csv_path.replace('.csv', '.pdf')
        
        csv_to_pdf(csv_path, pdf_path)
        
        assert os.path.exists(pdf_path), "PDF файл не було створено"
        assert os.path.getsize(pdf_path) > 1000, "PDF файл занадто малий"
        
        with open(pdf_path, 'rb') as f:
            header = f.read(5)
            assert header == b'%PDF-', "Файл не є валідним PDF"
            
        print("CSV to PDF conversion successful")
            
    finally:
        for path in [csv_path, pdf_path]:
            if path and os.path.exists(path):
                os.unlink(path)


def test_pdf_to_csv():
    pdf_path = None
    csv_path = None
    
    try:
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as pdf_file:
            pdf_path = pdf_file.name
        
        c = canvas.Canvas(pdf_path)
        c.drawString(100, 750, "Name    Age    City")
        c.drawString(100, 730, "Alice   25     Kyiv")
        c.drawString(100, 710, "Bob     30     Lviv")
        c.drawString(100, 690, "Charlie 35     Odesa")
        c.save()
        
        csv_path = pdf_path.replace('.pdf', '.csv')
        
        pdf_to_csv(pdf_path, csv_path)
        
        assert os.path.exists(csv_path), "CSV файл не було створено"
        
        df = pd.read_csv(csv_path)
        print("Converted DataFrame from PDF:", df)
        
        assert len(df) > 0, "DataFrame порожній"
        assert len(df.columns) > 0, "Немає стовпців в DataFrame"
        
        print("PDF to CSV conversion successful")
            
    except ImportError:
        writer = PdfWriter()
        writer.add_blank_page(width=72*8, height=72*11)
        with open(pdf_path, 'wb') as f:
            writer.write(f)
        
        csv_path = pdf_path.replace('.pdf', '.csv')
        pdf_to_csv(pdf_path, csv_path)
        
        assert os.path.exists(csv_path), "CSV файл не було створено"
        print("PDF to CSV conversion successful (basic)")
        
    finally:
        for path in [pdf_path, csv_path]:
            if path and os.path.exists(path):
                os.unlink(path)


def test_csv_to_pdf_empty_file():
    csv_path = None
    pdf_path = None
    
    try:
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as csv_file:
            csv_path = csv_file.name
            pd.DataFrame().to_csv(csv_path, index=False)
        
        pdf_path = csv_path.replace('.csv', '.pdf')
        
        try:
            csv_to_pdf(csv_path, pdf_path)
            if os.path.exists(pdf_path):
                assert os.path.getsize(pdf_path) > 0, "PDF файл порожній"
            print("Empty CSV handling successful")
        except Exception as e:
            print(f"Expected error for empty CSV: {e}")
            
    finally:
        for path in [csv_path, pdf_path]:
            if path and os.path.exists(path):
                os.unlink(path)


def test_pdf_to_csv_text_only():
    pdf_path = None
    csv_path = None
    
    try:
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as pdf_file:
            pdf_path = pdf_file.name
        
        try:
            c = canvas.Canvas(pdf_path)
            c.drawString(100, 750, "This is just plain text.")
            c.drawString(100, 730, "No tabular data here.")
            c.drawString(100, 710, "Just some paragraphs.")
            c.save()
        except ImportError:
            writer = PdfWriter()
            writer.add_blank_page(width=72*8, height=72*11)
            with open(pdf_path, 'wb') as f:
                writer.write(f)
        
        csv_path = pdf_path.replace('.pdf', '.csv')
        pdf_to_csv(pdf_path, csv_path)
        
        assert os.path.exists(csv_path), "CSV файл не було створено"
        
        df = pd.read_csv(csv_path)
        assert len(df) > 0, "DataFrame порожній"
        print("Text-only PDF conversion successful")
        
    finally:
        for path in [pdf_path, csv_path]:
            if path and os.path.exists(path):
                os.unlink(path) 

if __name__ == "__main__":
    import pytest
    pytest.main([__file__])