import tkinter as tk
from tkinter import messagebox
from gestion import Gestion
from smartphone import Smartphone
from utilisateur import Utilisateur

USERS = [
    Utilisateur("admin", "admin123", "admin"),
    Utilisateur("visiteur", "visiteur123", "visiteur")
]

class Application:
    def __init__(self, root):
        self.root = root
        self.gestion = Gestion()
        self.utilisateur = None
        self.clear()
        self.login_screen()

    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    def login_screen(self):
        self.clear()
        tk.Label(self.root, text="Nom d'utilisateur").pack()
        self.nom_entry = tk.Entry(self.root)
        self.nom_entry.pack()
        tk.Label(self.root, text="Mot de passe").pack()
        self.mdp_entry = tk.Entry(self.root, show="*")
        self.mdp_entry.pack()
        tk.Button(self.root, text="Se connecter", command=self.login).pack()

    def login(self):
        nom = self.nom_entry.get()
        mdp = self.mdp_entry.get()
        for u in USERS:
            if u.nom == nom and u.mot_de_passe == mdp:
                self.utilisateur = u
                self.menu()
                return
        messagebox.showerror("Erreur", "Identifiants incorrects")

    def menu(self):
        self.clear()
        tk.Label(self.root, text=f"Bienvenue {self.utilisateur.nom} ({self.utilisateur.role})").pack(pady=10)

        if self.utilisateur.role == "admin":
            tk.Button(self.root, text="Ajouter Smartphone", command=self.ajouter).pack()
            tk.Button(self.root, text="Modifier Smartphone", command=self.modifier).pack()
            tk.Button(self.root, text="Supprimer Smartphone", command=self.supprimer).pack()
            tk.Button(self.root, text="Exporter en CSV", command=self.exporter_csv).pack(pady=5)

        tk.Button(self.root, text="Voir tous", command=self.afficher).pack()
        tk.Button(self.root, text="Recherche avancée", command=self.recherche_avancee_form).pack()  # <== bouton ajouté
        tk.Button(self.root, text="Détails", command=self.details_form).pack()
        tk.Button(self.root, text="Top 3 plus chers", command=self.top3).pack()
        tk.Button(self.root, text="Déconnexion", command=self.login_screen).pack(pady=10)

    def afficher(self):
        self.clear()
        for s in self.gestion.smartphones:
            tk.Label(self.root, text=f"{s.nom} - {s.marque} - {s.prix}").pack()
        tk.Button(self.root, text="Retour", command=self.menu).pack()

    def top3(self):
        self.clear()
        for s in self.gestion.top3():
            tk.Label(self.root, text=f"{s.nom} - {s.prix}").pack()
        tk.Button(self.root, text="Retour", command=self.menu).pack()

    def details_form(self):
        self.clear()
        tk.Label(self.root, text="Nom du smartphone à chercher :").pack()
        self.nom_recherche = tk.Entry(self.root)
        self.nom_recherche.pack()
        tk.Button(self.root, text="Chercher", command=self.details).pack()
        tk.Button(self.root, text="Retour", command=self.menu).pack()

    def details(self):
        s = self.gestion.trouver(self.nom_recherche.get())
        if s:
            details = (f"Nom: {s.nom}\nMarque: {s.marque}\nDescription: {s.description}\n"
                       f"Prix: {s.prix}\nRAM: {s.ram}\nROM: {s.rom}\nÉcran: {s.ecran}\n"
                       f"Couleurs: {', '.join(s.couleurs) if isinstance(s.couleurs, list) else s.couleurs}")
            messagebox.showinfo("Détails", details)
        else:
            messagebox.showerror("Erreur", "Smartphone non trouvé")

    def ajouter(self):
        self.clear()
        labels = ["Nom", "Marque", "Description", "Prix", "RAM", "ROM", "Écran", "Couleurs (séparées par ,)"]
        self.champs = {}
        for label in labels:
            tk.Label(self.root, text=label).pack()
            entry = tk.Entry(self.root)
            entry.pack()
            self.champs[label] = entry

        def valider():
            try:
                s = Smartphone(
                    self.champs["Nom"].get(),
                    self.champs["Marque"].get(),
                    self.champs["Description"].get(),
                    float(self.champs["Prix"].get()),
                    self.champs["RAM"].get(),
                    self.champs["ROM"].get(),
                    self.champs["Écran"].get(),
                    [c.strip() for c in self.champs["Couleurs (séparées par ,)"].get().split(",")]
                )
                self.gestion.ajouter(s)
                messagebox.showinfo("Succès", "Smartphone ajouté avec succès.")
                self.menu()
            except Exception as e:
                messagebox.showerror("Erreur", f"Vérifiez les champs.\n{e}")

        tk.Button(self.root, text="Valider", command=valider).pack()
        tk.Button(self.root, text="Retour", command=self.menu).pack()

    def supprimer(self):
        self.clear()
        tk.Label(self.root, text="Nom du smartphone à supprimer :").pack()
        self.nom_supprimer = tk.Entry(self.root)
        self.nom_supprimer.pack()
        def valider():
            if self.gestion.supprimer(self.nom_supprimer.get()):
                messagebox.showinfo("Succès", "Smartphone supprimé.")
            else:
                messagebox.showerror("Erreur", "Smartphone non trouvé.")
            self.menu()
        tk.Button(self.root, text="Supprimer", command=valider).pack()
        tk.Button(self.root, text="Retour", command=self.menu).pack()

    def modifier(self):
        self.clear()
        tk.Label(self.root, text="Nom du smartphone à modifier :").pack()
        self.nom_modif = tk.Entry(self.root)
        self.nom_modif.pack()

        labels = ["Marque", "Description", "Prix", "RAM", "ROM", "Écran", "Couleurs (séparées par ,)"]
        self.champs_modif = {}
        for label in labels:
            tk.Label(self.root, text=label).pack()
            entry = tk.Entry(self.root)
            entry.pack()
            self.champs_modif[label] = entry

        def valider():
            try:
                nouvelles_infos = {
                    "marque": self.champs_modif["Marque"].get(),
                    "description": self.champs_modif["Description"].get(),
                    "prix": float(self.champs_modif["Prix"].get()),
                    "ram": self.champs_modif["RAM"].get(),
                    "rom": self.champs_modif["ROM"].get(),
                    "ecran": self.champs_modif["Écran"].get(),
                    "couleurs": [c.strip() for c in self.champs_modif["Couleurs (séparées par ,)"].get().split(",")]
                }
                if self.gestion.modifier(self.nom_modif.get(), nouvelles_infos):
                    messagebox.showinfo("Succès", "Smartphone modifié.")
                else:
                    messagebox.showerror("Erreur", "Smartphone non trouvé.")
                self.menu()
            except Exception as e:
                messagebox.showerror("Erreur", f"Prix invalide ou champs incorrects.\n{e}")

        tk.Button(self.root, text="Modifier", command=valider).pack()
        tk.Button(self.root, text="Retour", command=self.menu).pack()

    def exporter_csv(self):
        self.gestion.exporter_csv()
        messagebox.showinfo("Exportation", "Exportation réussie dans 'export_smartphones.csv'")
        self.menu()

    # --------- NOUVELLES MÉTHODES POUR RECHERCHE AVANCÉE ---------

    def recherche_avancee_form(self):
        self.clear()
        tk.Label(self.root, text="Recherche avancée (nom ou marque):").pack()
        self.recherche_entry = tk.Entry(self.root)
        self.recherche_entry.pack()
        tk.Button(self.root, text="Chercher", command=self.recherche_avancee).pack()
        tk.Button(self.root, text="Retour", command=self.menu).pack()

    def recherche_avancee(self):
        critere = self.recherche_entry.get().lower()
        resultats = []
        for s in self.gestion.smartphones:
            if critere in s.nom.lower() or critere in s.marque.lower():
                resultats.append(s)
        self.clear()
        if resultats:
            for s in resultats:
                tk.Label(self.root, text=f"{s.nom} - {s.marque} - {s.prix}").pack()
        else:
            tk.Label(self.root, text="Aucun smartphone trouvé.").pack()
        tk.Button(self.root, text="Retour", command=self.menu).pack()
