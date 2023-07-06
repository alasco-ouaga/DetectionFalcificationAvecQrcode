import tkinter as tk
from turtle import RawTurtle, TurtleScreen, ScrolledCanvas

# Fonction pour afficher le rond tournant
def afficher_rond_tournant():
    # Création de la fenêtre
    fenetre = tk.Tk()
    fenetre.title("Patientez...")

    # Création du canevas pour le dessin du rond tournant
    canevas = ScrolledCanvas(fenetre)
    canevas.pack()

    # Création de l'écran de la tortue
    ecran = TurtleScreen(canevas)

    # Création de la tortue pour dessiner le rond tournant
    tortue = RawTurtle(ecran)

    # Configuration de la tortue
    tortue.shape("circle")
    tortue.color("black")
    tortue.width(3)
    tortue.speed(0)

    # Dessin du rond tournant
    for _ in range(36):  # 36 étapes pour faire un tour complet
        tortue.forward(10)
        tortue.right(10)

    # Fermeture de la fenêtre lorsque le rond tournant est terminé
    fenetre.destroy()

# Exemple d'utilisation de la fonction
afficher_rond_tournant()
