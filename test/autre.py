import tkinter as tk
from tkinter import ttk

# Fonction pour créer la page de chargement
def create_loading_page():
    # Création de la fenêtre
    fenetre = tk.Toplevel()
    fenetre.title("Loading Page")
    fenetre.geometry("400x200")  # Ajustez la taille de la fenêtre selon vos besoins

    # Création d'un widget Label pour afficher le texte du chargement
    label_loading = tk.Label(fenetre, text="Chargement en cours...")
    label_loading.pack(pady=20)

    # Création d'un widget Progressbar pour l'indicateur de chargement animé
    progress_bar = ttk.Progressbar(fenetre, mode="indeterminate")
    progress_bar.pack(pady=10)

    # Lancement de l'animation de la Progressbar
    progress_bar.start()

    # Lancement de la boucle principale de la fenêtre
    fenetre.mainloop()

# Fonction pour gérer le clic sur le bouton
def start_loading():
    create_loading_page()

# Création de la fenêtre principale
fenetre_principale = tk.Tk()
fenetre_principale.title("Exemple de chargement")

# Création du bouton
bouton_loading = tk.Button(fenetre_principale, text="Démarrer le chargement", command=start_loading)
bouton_loading.pack(pady=20)

# Lancement de la boucle principale de la fenêtre principale
fenetre_principale.mainloop()
