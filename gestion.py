import json
import os
from tkinter import messagebox
from smartphone import Smartphone
import csv

class Gestion:
    def __init__(self, fichier="data/smartphones.json"):
        self.fichier = fichier
        self.smartphones = self.charger()

    def charger(self):
        if os.path.exists(self.fichier):
            try:
                with open(self.fichier, "r") as f:
                    return [Smartphone.from_dict(d) for d in json.load(f)]
            except json.JSONDecodeError:
                return []
        return []

    def sauvegarder(self):
        with open(self.fichier, "w") as f:
            json.dump([s.to_dict() for s in self.smartphones], f, indent=4)

    def exporter_csv(self):
        try:
            with open("export_smartphones.csv", "w", newline='', encoding='utf-8') as csvfile:
                fieldnames = ["nom", "marque", "description", "prix", "ram", "rom", "ecran", "couleurs"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                for smartphone in self.smartphones:
                    writer.writerow({
                        "nom": smartphone.nom,
                        "marque": smartphone.marque,
                        "description": smartphone.description,
                        "prix": smartphone.prix,
                        "ram": smartphone.ram,
                        "rom": smartphone.rom,
                        "ecran": smartphone.ecran,
                        "couleurs": smartphone.couleurs
                    })

            messagebox.showinfo("Export CSV", "Exportation réussie dans 'export_smartphones.csv'.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'export : {e}")

    def ajouter(self, smartphone):
        self.smartphones.append(smartphone)
        self.sauvegarder()

    def supprimer(self, nom):
        self.smartphones = [s for s in self.smartphones if s.nom != nom]
        self.sauvegarder()

    def modifier(self, nom, nouvelles_infos):
        for s in self.smartphones:
            if s.nom == nom:
                s.marque = nouvelles_infos.get("marque", s.marque)
                s.description = nouvelles_infos.get("description", s.description)
                s.prix = nouvelles_infos.get("prix", s.prix)
                s.ram = nouvelles_infos.get("ram", s.ram)
                s.rom = nouvelles_infos.get("rom", s.rom)
                s.ecran = nouvelles_infos.get("ecran", s.ecran)
                s.couleurs = nouvelles_infos.get("couleurs", s.couleurs)
                self.sauvegarder()
                return True
        return False

    def top3(self):
        if not self.smartphones:
            return []
        return sorted(self.smartphones, key=lambda s: s.prix, reverse=True)[:3]

    def trouver(self, nom):
        for s in self.smartphones:
            if s.nom == nom:
                return s
        return None

    # --- Nouvelle méthode recherche avancée ---
    def recherche_avancee(self, critere):
        critere = critere.lower()
        return [s for s in self.smartphones if critere in s.nom.lower() or critere in s.marque.lower()]