import cv2
import PyPDF2
import os


def convertir_premiere_page_en_image(chemin_pdf, chemin_image):
    lecteur_pdf = PyPDF2.PdfReader(open(chemin_pdf, 'rb'))
    page = lecteur_pdf.pages[0]
    image = page.convertToImage()
    image.save(chemin_image, 'PNG')

chemin_pdf = 'C:/Users/concepteur/Documents/fusion.pdf'
chemin_image = 'C:/Users/concepteur/Documents/image.jpg'
convertir_premiere_page_en_image(chemin_pdf, chemin_image)