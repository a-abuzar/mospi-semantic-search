import pandas as pd
import pdfplumber
import re
from pathlib import Path

def clean_description(text):
    """
    The definitive cleaning function. It removes all known noise patterns
    aggressively to produce the cleanest possible description.
    """
    # 1. Remove major recurring blocks of noise first.
    text = re.sub(r'ISCO 08 Unit Group Details:.*?(?=Family|\d{4}\.\d{4}|$)', '', text, flags=re.DOTALL)
    text = re.sub(r'Qualification Pack Details:.*?(?=ISCO 08|Family|\d{4}\.\d{4}|$)', '', text, flags=re.DOTALL)
    
    # 2. Remove all known headers and footers.
    text = re.sub(r'VOLUME II [A|B]\s+\d+', '', text, flags=re.DOTALL)
    text = re.sub(r'National Classification of Occupations – 2015\s+Divi?si?on\s+\d', '', text, flags=re.DOTALL) # Handles "Division" and "Divison"
    text = re.sub(r'VOLUM Division \d', '', text, flags=re.DOTALL)
    
    # 3. Remove any remaining isolated titles from other sections.
    text = re.sub(r'Title\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*', '', text)

    # 4. Final whitespace cleanup.
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def parse_nco_pdfs_definitive():
    """
    Implements the "Single Document" method for maximum accuracy.
    """
    data_path = Path('data')
    pdf_files = [
        data_path / 'National_Classification_of_Occupations_Vol_II-A-2015.pdf',
        data_path / 'National_Classification_of_Occupations_Vol_II-B-2015.pdf'
    ]

    print("Starting GOLD STANDARD PDF parsing...")
    full_text_in_order = []
    
    for pdf_file in pdf_files:
        if not pdf_file.exists():
            print(f"FATAL ERROR: File not found at {pdf_file}.")
            return
        
        print(f"Reading and ordering file: {pdf_file.name}...")
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages[13:]:
                width = page.width
                height = page.height
                left_bbox = (0, 0, 0.5 * width, height)
                right_bbox = (0.5 * width, 0, width, height)
                left_text = page.crop(left_bbox).extract_text(x_tolerance=2, y_tolerance=2) or ""
                right_text = page.crop(right_bbox).extract_text(x_tolerance=2, y_tolerance=2) or ""
                full_text_in_order.append(left_text)
                full_text_in_order.append(right_text)

    full_text = "\n".join(full_text_in_order)
    print("Full document text constructed. Applying final regex...")

    pattern = re.compile(r'(\d{4}\.\d{4})\s+(.*?)(?=\d{4}\.\d{4}\s+|INDEX|$)', re.DOTALL)
    matches = pattern.findall(full_text)

    if not matches:
        print("FATAL ERROR: No matches found.")
        return

    print(f"Found {len(matches)} raw entries. Applying gold standard cleaning...")

    occupations = []
    for code, raw_description in matches:
        description = clean_description(raw_description)
        nco_code = code.replace('.', '')

        if description and len(description) > 20:
            occupations.append({
                'nco_code': nco_code,
                'description': description
            })

    df = pd.DataFrame(occupations)
    output_path = data_path / 'nco_data.csv'
    df.to_csv(output_path, index=False, encoding='utf-8')

    print(f"\n--- PARSING COMPLETE ---")
    print(f"Successfully processed and saved {len(df)} occupations.")
    print(f"Definitive clean data is now available at: {output_path}")

if __name__ == '__main__':
    parse_nco_pdfs_definitive()