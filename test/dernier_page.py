import fitz



def convertir_page_en_image(chemin_pdf, numero_page, chemin_image):
    # Ouvrir le fichier PDF
    document = fitz.open(chemin_pdf)
    
    # Récupérer la page spécifiée par le numéro de page
    page = document.load_page(numero_page)
    
    # Récupérer les dimensions de la page
    matrice = fitz.Matrix(2, 2)  # Facteur d'échelle de 2 pour une meilleure résolution de l'image
    pix = page.get_pixmap(matrix=matrice)
    
    # Enregistrer l'image sous forme de fichier
    pix.save(chemin_image)

    # Fermer le document PDF
    document.close()

# Appeler la fonction convertir_page_en_image en fournissant le chemin du fichier PDF, le numéro de page et le chemin de l'image de sortie
chemin_pdf = 'chemin/vers/le/fichier.pdf'
numero_page = 1
chemin_image = 'chemin/vers/l/image.png'
convertir_page_en_image(chemin_pdf, numero_page, chemin_image)
