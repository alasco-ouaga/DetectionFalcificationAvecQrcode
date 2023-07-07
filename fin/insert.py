import tkinter as tk
import qrcode
import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from pdf2image import convert_from_path
import shutil
#from fpdf import FPDF
import json
#import glob
#from PIL import Image
import hashlib
#from PyPDF2 import PdfWriter, PdfReader
import qrcode
#from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import PyPDF2
from datetime import datetime
#from PIL import Image, ImageTk
from tkinter import messagebox
import send2trash


class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Detection de falsification")
        #self.state("zoomed")
        self.geometry("900x600")  

        # Créer la barre de navigation
        self.navigation_bar = ttk.Treeview(self)
        self.navigation_bar.pack(side="left", fill="y")

        # Ajouter les pages à la barre de navigation
        self.navigation_bar.tag_configure("big_font", font=("Arial", 12))
        self.navigation_bar.insert("", "end", text="inserer Qrcode", values=("accueil_page",), tags=("big_font",))

        # Associer les pages aux boutons de la barre de navigation
        self.navigation_bar.bind("<<TreeviewSelect>>", self.show_selected_page)

        # Créer les pages
        self.accueil_page = AccueilPage(self)

        # Afficher la page d'accueil par défaut
        self.show_page(self.accueil_page)

    def show_selected_page(self, event):
        selected_item = self.navigation_bar.selection()
        page_id = self.navigation_bar.item(selected_item)["values"][0]
        if page_id == "accueil_page":
            self.show_page(self.accueil_page)
        elif page_id == "enregistrer_page":
            self.show_page(self.enregistrer_page)

    def show_page(self, page):
        if hasattr(self, "current_page"):
            self.current_page.pack_forget()
        
        page.pack(fill="both", expand=True)
        self.current_page = page

class AccueilPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master,bg="#c3c3c3", highlightbackground="black", highlightthickness=1)  # Ajout du fond rouge au cadre principal
        self.pack(fill="both", expand=True)
        
        self.label = tk.Label(self, text="LIEN :" , font=("Times New Roman" , 18 , "bold"))
        self.label.grid(row=0, column=0, sticky=tk.E , pady=50, padx=20)

        self.link = tk.Entry(self , font=("Times New Roman" , 22),border=3)
        self.link.grid(row=0, column=1, sticky=tk.W+tk.E , padx=5)
        self.link.bind("<Configure>", self.agrandir_entry)

        self.button = tk.Button(self, text="selectionner",padx=10, font=("arial" , 15 , "bold"),bg="green",command=self.select_pdf)
        self.button.grid(row=0, column=2, sticky=tk.W ,  padx=20)
        
        self.message = tk.Text(self , height=10, font=("Times New Roman" , 25 ),border=3)
        self.message.grid(row=1, column=1, sticky=tk.W+tk.E , padx=6, pady = 50 )
        self.message.bind("<Configure>", self.agrandir_entry)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)

    def agrandir_entry(self, event):
            self.link.config(width=(self.link.winfo_width() + 1))

    def hasher_texte(self,texte):
        # Convertir le texte en format binaire (UTF-8)
        texte_binaire = texte.encode('utf-8')

        # Calculer le hachage du texte
        hachage = hashlib.sha256(texte_binaire).hexdigest()
        return hachage
    
    def extraire_texte_pdf(self,chemin_fichier_pdf):
        texte = ""
        with open(chemin_fichier_pdf, "rb") as fichier_pdf:
            lecteur_pdf = PyPDF2.PdfReader(fichier_pdf)
            nombre_pages = len(lecteur_pdf.pages)

            for numero_page in range(nombre_pages):
                page = lecteur_pdf.pages[numero_page]
                texte += page.extract_text()

        return texte
    
    def fusionner_pdf(self,chemin_pdf1, chemin_pdf2, chemin_sortie):
        # Charger les fichiers PDF
        pdf1 = PyPDF2.PdfReader(open(chemin_pdf1, 'rb'))
        pdf2 = PyPDF2.PdfReader(open(chemin_pdf2, 'rb'))

        try:
            # Créer un nouveau fichier PDF
            pdf_fusionne = PyPDF2.PdfMerger()
            pdf_fusionne.append(pdf1)
            pdf_fusionne.append(pdf2)
            # Enregistrer le fichier PDF fusionné
            pdf_fusionne.write(chemin_sortie)
            response = True

        except Exception as e:
            response = False

        return response

    def creer_qrcode_et_pdf(self,data, path_qrcode_pdf):
        # Créer le QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")

        # creer un dossier temporaire pour stocker le qrcode image
        name = "Dossier_temporaire_qrcode_image"
        path_qrcode_image = self.create_folder(name)
        delete_path = path_qrcode_image

        # Enregistrer le QR code en tant qu'image temporaire
        qr_img_path = path_qrcode_image+"/"+"qr_code.png"
        qrcode_image_path = self.format_the_path(qr_img_path)
        qr_img.save(qrcode_image_path)

        # Dimensions de la page PDF
        page_width = 595  # Largeur en points (1 point = 1/72 pouces)
        page_height = 842  # Hauteur en points (1 point = 1/72 pouces)

        # Créer un fichier PDF
        c = canvas.Canvas(path_qrcode_pdf, pagesize=(page_width, page_height))

        # Calculer les coordonnées pour centrer l'image du QR code sur la page
        qr_img_width, qr_img_height = qr_img.size
        x = (page_width - qr_img_width)
        y = (page_height - qr_img_height)

        # Ajouter l'image du QR code à la page PDF
        c.drawImage(qr_img_path, 100, 100)

        # Enregistrer le fichier PDF
        c.save()
        shutil.rmtree(delete_path)

    #Fonction de creation d'un dossier
    def create_folder(self,name):
        # creation d'un dossier dans le repertoire Documents  pour stocker les images 
        documents_path = os.path.expanduser("~\Documents")
        tableau = []

        # Boucle for pour insérer des entier de 1 a 20 dans un tableau pour preparer la creation du dossier
        #le tableau sert a : creer un autre dossier si le dossier en creation existe
        for indice in range(20):
            tableau.append(indice)

        #etape pour la creation du dossier
        for i in tableau:
            folder_name =""
            folder_name = name +"_" +str(i)
            
            # Chemin complet du dossier à créer
            path_dossier_image_sans_Qrcode = os.path.join(documents_path, folder_name)

            # Si le dossier n'existe pas , passer à sa creation
            if not os.path.exists(path_dossier_image_sans_Qrcode):
                # Créer le dossier
                os.makedirs(path_dossier_image_sans_Qrcode)
                
                #formatter le path pour avoir le bon
                path_dossier_image_sans_Qrcode_formatted = path_dossier_image_sans_Qrcode.replace("\\", "/")
                
                print("le dossier créé avec succès dans le repertoir Document :", path_dossier_image_sans_Qrcode_formatted)
                break
        return path_dossier_image_sans_Qrcode_formatted
    
    def get_document_link(self) :
        documents_path = os.path.expanduser("~\Documents")
        return documents_path

    def format_the_path(self,path) :
            path_formated = path.replace("\\", "/")
            return path_formated
    
    def obtenir_date(self) :
        heure = datetime.now()
        # date_actuelle = datetime.date.today()   path_dossier_image_sans_Qrcode_formatted = path_dossier_image_sans_Qrcode.replace("\\", "/")
        # heure_actuelle = heure.hour
        # indice = date_actuelle+"_"+heure_actuelle
        date_string = heure.strftime("%Y-%m-%d %H:%M:%S")

        # Remplacement des caractères non autorisés
        date_string = date_string.replace(':', '_')
        return date_string
    
    def action_message(self,response,lien_sortie_document_securisé):
        if response == True : 
            messagebox.showinfo("Succès", "L'opération a réussie avec succès : le document est securisé")
            messagebox.showinfo("Lien de sortie", "Le lien:"+lien_sortie_document_securisé)
            return True
        else :
            messagebox.showinfo("Succès", "L'opération a echouée ! : Essayer une nouvelle fois")
            return False

    def select_pdf(self):
        path_entre_pdf = filedialog.askopenfilename(filetypes=[("Fichiers PDF", "*.pdf")])
        text=self.extraire_texte_pdf(path_entre_pdf)
        hash=self.hasher_texte(text)

        # les differentes donnée du qrcode
        data = {'hash': hash}

        #Formatter le dictionnaire en une varriable Json
        data = json.dumps(data)

        print(hash)

        # creer un dossier temporaire pour stocker le qrcode
        name = "Dossier_temporaire_qrcode_pdf"
        path_qrcode_pdf = self.create_folder(name)
        delete_path = path_qrcode_pdf
        path_du_qrcode_pdf = path_qrcode_pdf+"/"+"qrcode.pdf"
        path_qrcode_pdf = self.format_the_path(path_du_qrcode_pdf)
        print("Le path temporaire du Qr code est : ", self.format_the_path(path_du_qrcode_pdf))

        # Preparer le path de sortie du pdf finale
        file_name = "PdfSecurisé"+"_"+self.obtenir_date()+".pdf"
        document_link = self.get_document_link()
        lien = document_link+"/"+file_name
        lien_sortie_fusion= self.format_the_path(lien)
        print("Le path du pdf finale est avec qrcode est : ",lien_sortie_fusion)

        self.creer_qrcode_et_pdf(data, path_qrcode_pdf)
        response = self.fusionner_pdf(path_qrcode_pdf,path_entre_pdf,lien_sortie_fusion)

        self.link.delete(0, tk.END)
        self.link.insert(tk.END, path_entre_pdf)

        responses = self.action_message(response,lien_sortie_fusion)

        if responses == True :
            message ="L'opération a réussie avec succès : le document est securisé avec succès"
            self.message.delete(tk.END)
            self.message.insert(tk.END, message)
        else :
            message ="L'opération a echouée : le document n'a pas été securisé"
            self.message.delete(tk.END)
            self.message.insert(tk.END, message)
        
        #shutil.rmtree(delete_path)
        #send2trash.send2trash(delete_path)


if __name__ == "__main__":
    app = Application()
    app.mainloop()
