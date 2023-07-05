import PyPDF2
from PyPDF2 import PdfWriter, PdfReader
import hashlib

def extraire_texte_pdf(chemin_fichier_pdf):
    texte = ""
    with open(chemin_fichier_pdf, "rb") as fichier_pdf:
        lecteur_pdf = PyPDF2.PdfReader(fichier_pdf)
        nombre_pages = len(lecteur_pdf.pages)

        for numero_page in range(nombre_pages):
            page = lecteur_pdf.pages[numero_page]
            texte += page.extract_text()

    return texte

# Exemple d'utilisation
chemin_fichier_pdf = "C:/Users/concepteur/Documents/pdftest.pdf"  # Spécifiez le chemin complet du fichier PDF
texte_extrait = extraire_texte_pdf(chemin_fichier_pdf)
# Convertir le texte en format binaire (UTF-8)
texte_binaire = texte_extrait.encode('utf-8')

# Calculer le hachage du texte
hachage = hashlib.sha256(texte_binaire).hexdigest()

print("Le hachage du texte est :", hachage)
print(hachage)
