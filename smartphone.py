class Smartphone:
    def __init__(self, nom, marque, description, prix, ram, rom, ecran, couleurs):
        self.nom = nom
        self.marque = marque
        self.description = description
        self.prix = prix
        self.ram = ram
        self.rom = rom
        self.ecran = ecran
        self.couleurs = couleurs

    def to_dict(self):
        return {
            "nom": self.nom,
            "marque": self.marque,
            "description": self.description,
            "prix": self.prix,
            "ram": self.ram,
            "rom": self.rom,
            "ecran": self.ecran,
            "couleurs": self.couleurs
        }

    @staticmethod
    def from_dict(data):
        return Smartphone(
            data["nom"], data["marque"], data["description"],
            data["prix"], data["ram"], data["rom"],
            data["ecran"], data["couleurs"]
        )