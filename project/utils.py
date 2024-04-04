import os
import requests

def download_pdf_file():
    # Get PDF document path
    pdf_path = "../data/raw/human-nutrition-text.pdf"

    # Download
    if not os.path.exists(pdf_path):
        print(f"[INFO] File doesn't exist, downloading...")

        # Enter the URL of the PDF
        url="https://pressbooks.oer.hawaii.edu/humannutrition2/open/download?type=pdf"

        # The local filename to save the downloaded file
        filename = pdf_path

        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Open the file and save it
            with open(filename,"wb") as file:
                file.write(response.content)
                print(f"[INFO] The file has been downloaded and saved as {filename}")
        else:
            print(f"[INFO] Failed to download the file. Status code: {response.status_code}")
    else:
        print(f"File {pdf_path} exists.")

import fitz  # !pip install PyMuPDF
from tqdm.auto import tqdm  # !pip install tqdm

def text_formatter(text: str) -> str:
    """Performs minor formatting on text."""
    cleaned_text = text.replace("\n", " ").strip()
    # Potentially more text formatting functions can go here
    return cleaned_text

def open_and_read_pdf(pdf_path: str) -> list[dict]:
    doc = fitz.open(pdf_path)
    pages_and_texts = []
    for page_number, page in tqdm(enumerate(doc)):
        text = page.get_text()
        text = text_formatter(text=text)
        pages_and_texts.append({
            "page_number": page_number - 41,
            "page_char_count": len(text),
            "page_word_count": len(text.split(" ")),
            "page_sentence_count_raw": len(text.split(". ")),
            "page_token_count": len(text) / 4,  # 1 token =~ 4 characters
            "text": text
        })
    return pages_and_texts

def select_example_pages(pages_and_texts,selected_page_numbers):
    selected_pages = []

    for page_info in pages_and_texts:
        page_number = page_info.get('page_number')
        
        if page_number in selected_page_numbers:
            selected_pages.append(page_info)
    
    return selected_pages