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


def csv_to_pdf(input_path, output_path):
    try:
        _validate_extensions(input_path, output_path, '.csv', '.pdf')
        logger.info(f"Converting {input_path} to {output_path}")

        df = pd.read_csv(input_path)
        text = df.to_string(index=False)

        writer = PdfWriter()
        page = writer.add_blank_page(width=72 * 8.27, height=72 * 11.69)

        if text.strip():
            # Простий спосіб додати текст до PDF
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas
            import io

            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)
            can.drawString(50, 700, text)
            can.save()

            packet.seek(0)
            new_pdf = PdfReader(packet)
            page.merge_page(new_pdf.pages[0])

        with open(output_path, 'wb') as file:
            writer.write(file)
        logger.info("Conversion completed successfully")
    except Exception as e:
        logger.error(f"Error in csv_to_pdf: {str(e)}")
        raise


def pdf_to_csv(input_path, output_path):
    try:
        _validate_extensions(input_path, output_path, '.pdf', '.csv')
        logger.info(f"Converting {input_path} to {output_path}")

        with open(input_path, 'rb') as file:
            reader = PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"


        lines = text.strip().split('\n')
        if len(lines) > 0:
            data = [line.split() for line in lines if line.strip()]
            df = pd.DataFrame(data[1:], columns=data[0] if len(data) > 1 else None)
            df.to_csv(output_path, index=False)

        logger.info("Conversion completed successfully")
    except Exception as e:
        logger.error(f"Error in pdf_to_csv: {str(e)}")
        raise