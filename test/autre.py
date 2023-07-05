import qrcode
from reportlab.pdfgen import canvas

def creer_qrcode_et_pdf(data, nom_fichier_pdf):
    # Créer le QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Enregistrer le QR code en tant qu'image temporaire
    qr_img_path = "qr_code.png"
    qr_img.save(qr_img_path)

    # Dimensions de la page PDF
    page_width = 595  # Largeur en points (1 point = 1/72 pouces)
    page_height = 842  # Hauteur en points (1 point = 1/72 pouces)

    # Créer un fichier PDF
    c = canvas.Canvas(nom_fichier_pdf, pagesize=(page_width, page_height))

    # Calculer les coordonnées pour centrer l'image du QR code sur la page
    qr_img_width, qr_img_height = qr_img.size
    x = (page_width - qr_img_width)
    y = (page_height - qr_img_height)

    # Ajouter l'image du QR code à la page PDF
    c.drawImage(qr_img_path, 200, 200)

    # Enregistrer le fichier PDF
    c.save()

    print("Le QR code a été créé et enregistré en tant que fichier PDF avec succès.")

# Exemple d'utilisation
data = "Hello, QR Code!"
nom_fichier_pdf = 'C:/Users/concepteur/Documents/devoir_enonce.pdf'

creer_qrcode_et_pdf(data, nom_fichier_pdf)
