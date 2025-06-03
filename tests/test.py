import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.converter import csv_to_txt, txt_to_csv
import pandas as pd
import tempfile

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

if __name__ == "__main__":
    import pytest
    pytest.main([__file__])