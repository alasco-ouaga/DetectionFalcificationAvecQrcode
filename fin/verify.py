import tkinter as tk
import qrcode
import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from pdf2image import convert_from_path
from fpdf import FPDF
import json
import glob
import cv2
import pytesseract
from PIL import Image
import hashlib
import PyPDF2
from datetime import datetime
from tkinter import messagebox


class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Detection falsification")
        self.state("zoomed")

        # Créer la barre de navigation
        self.navigation_bar = ttk.Treeview(self)
        self.navigation_bar.pack(side="left", fill="y")

        # Ajouter les pages à la barre de navigation
        self.navigation_bar.tag_configure("big_font", font=("Arial", 12))
        self.navigation_bar.insert("", "end", text="verification", values=("accueil_page",), tags=("big_font",))

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
        
        self.label = tk.Label(self, text="LIEN :" , font=("arial" , 15 , "bold"))
        self.label.grid(row=0, column=0, sticky=tk.E , pady=50,padx=20)

        self.entry = tk.Entry(self , font=("arial" , 15 , "bold"),border=3)
        self.entry.grid(row=0, column=1, sticky=tk.W+tk.E , padx=5)
        self.entry.bind("<Configure>", self.agrandir_entry)

        self.button = tk.Button(self, text="selectionner",padx=10, font=("arial" , 11 , "bold"),bg="green",command=self.select_pdf)
        self.button.grid(row=0, column=2, sticky=tk.W,padx=20)
        
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)
        
    def agrandir_entry(self, event):
            self.entry.config(width=(self.entry.winfo_width() + 1))
    
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
    
    def transform_premiere_page_en_image(self,path_fichier_pdf):
        images = convert_from_path(path_fichier_pdf)
        for index,image in enumerate(images):
            # Obtenir le nom de fichier avec l'extension
            image_name = f"image_{index}.jpg"
            
            # Chemin complet du fichier de destination
            folder_name = "premiere_image"
            folder_path = self.create_folder(folder_name)

            # Lien de la premiere image
            first_image_path = os.path.join(folder_path,image_name)
            first_image_path_formated = first_image_path.replace("\\", "/")
            
            # Enregistrer l'image avec le QR code dans le dossier de destination
            image.save(first_image_path)
            break
        
        return first_image_path_formated
    
    def extraire_hash_dans_qrcode(self,first_image_path):

        # Charger l'image
        img = cv2.imread(first_image_path)

        # Convertir l'image en échelle de gris
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Définir le détecteur de codes QR
        qr_detector = cv2.QRCodeDetector()

        try:
            # Détecter les codes QR dans l'image
            get_qrcode = qr_detector.detectAndDecodeMulti(gray)
            
            # Recuperer l'information enrgistrée dans la deuxieme ligne des informations contenues dans le qr code
            # cette information est enregistre sous forme de tuple.
            tuple = get_qrcode[1]
            
            # Extraire le dictionnaire dans le tuple
            dictionnaire = tuple[0]
            
            # Reformatter le dictionnaire pour avoir la varribale de type json
            decoded_mon_dictionnaire = json.loads(dictionnaire)
            hash = decoded_mon_dictionnaire.get("hash")
            return hash
        except Exception as e:
            messagebox.showinfo("Erreur rencontrée", "Echec : le document ne comporte pas de qrcode")

    
    def compare_deux_hash(self,hash1,hash2):
        
        if hash1 == hash2 :
            return True
        else :
            return False
        

    def select_pdf(self):
        path_entre_pdf = filedialog.askopenfilename(filetypes=[("Fichiers PDF", "*.pdf")])
        text=self.extraire_texte_pdf(path_entre_pdf)
        text_hash=self.hasher_texte(text)
        #print(hash)
        #print(path_entre_pdf)

        first_image_path = self.transform_premiere_page_en_image(path_entre_pdf)
        print(first_image_path)

        qrcode_hash = self.extraire_hash_dans_qrcode(first_image_path)
        print(text_hash)
        print(qrcode_hash)

        response = self.compare_deux_hash(text_hash,qrcode_hash)
        self.entry.delete(0, tk.END)  # Effacer le contenu précédent
        self.entry.insert(tk.END, path_entre_pdf)

        if response == True :
            messagebox.showinfo("Authentique", "Le document est authentique")
        else :
            messagebox.showinfo("Falsifié", "Le document n'est pas authentique (Falsifié)")
        
if __name__ == "__main__":
    app = Application()
    app.mainloop()
