from PyPDF2 import PdfReader

def extract_text_from_pdf(file_path):
    pdf = PdfReader(open(file_path, 'rb'))
    num_pages = len(pdf.pages)
    page_texts = []
    for page_num in range(num_pages):
        page = pdf.pages[page_num]
        text = page.extract_text()
        page_texts.append(text)
    return page_texts

# Exemple d'utilisation
file_path = 'C:/Users/concepteur/Documents/tesPdf/devoir_enonce.pdf'
page_texts = extract_text_from_pdf(file_path)
for i, text in enumerate(page_texts):
    print(f"Page {i+1}:")
    print(text)
    print("--------------------")
