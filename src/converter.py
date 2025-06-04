import pandas as pd
from PyPDF2 import PdfReader, PdfWriter

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import re


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


def csv_to_pdf(input_path, output_path):
    df = pd.read_csv(input_path)

    doc = SimpleDocTemplate(output_path, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()
    title_style = styles['Title']

    title = Paragraph("CSV Data Report", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.2 * inch))

    table_data = [list(df.columns)]

    for _, row in df.iterrows():
        table_data.append([str(cell) for cell in row])

    table = Table(table_data)

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
    ]))

    elements.append(table)

    doc.build(elements)


def pdf_to_csv(input_path, output_path):
    with open(input_path, 'rb') as file:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"

    lines = text.strip().split('\n')
    lines = [line.strip() for line in lines if line.strip()]

    potential_table_lines = []

    for line in lines:
        if len(line) < 5:
            continue

        parts = re.split(r'\s{2,}|\t+', line)
        if len(parts) > 1:
            potential_table_lines.append(parts)

    if not potential_table_lines:
        df = pd.DataFrame({'Text': lines})
    else:
        max_cols = max(len(parts) for parts in potential_table_lines)

        normalized_data = []
        for parts in potential_table_lines:
            while len(parts) < max_cols:
                parts.append('')
            normalized_data.append(parts[:max_cols])

        if normalized_data:
            first_row = normalized_data[0]
            if all(not any(char.isdigit() for char in str(cell)) for cell in first_row if cell):
                columns = [f'Column_{i + 1}' if not cell else cell for i, cell in enumerate(first_row)]
                data = normalized_data[1:] if len(normalized_data) > 1 else []
            else:
                columns = [f'Column_{i + 1}' for i in range(max_cols)]
                data = normalized_data

            df = pd.DataFrame(data, columns=columns)
        else:
            df = pd.DataFrame({'Text': ['No tabular data found']})

    df.to_csv(output_path, index=False)

