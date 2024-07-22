import random

class Plateau:
    def __init__(self, taille):
        self.taille = taille
        self.positions = [1, taille]

    def afficher(self):
        plateau = ['_'] * self.taille
        plateau[self.positions[0] - 1] = 'A'  # Premier ordinateur
        plateau[self.positions[1] - 1] = 'B'  # Deuxième ordinateur
        print(" ".join(plateau))

class Ordinateur:
    def __init__(self, nom):
        self.nom = nom
        self.main = []
        self.a_battu_en_retraite_pour_esquiver = False

    def piocher_cartes(self, pioche, nombre):
        for _ in range(nombre):
            if pioche:
                self.main.append(pioche.pop())
        print(f"{self.nom} pioche.")

    def deplacer(self, plateau, pas, simulation=False):
        pos = plateau.positions[0] if self.nom == 'A' else plateau.positions[1]
        if pas < 0:
            pas = -pas
            nouvelle_position = pos - pas if self.nom == 'A' else pos + pas
            if nouvelle_position <= 0 or nouvelle_position > plateau.taille or (self.nom == 'A' and nouvelle_position >= plateau.positions[1]) or (self.nom == 'B' and nouvelle_position <= plateau.positions[0]):
                return False
        else:
            nouvelle_position = pos + pas if self.nom == 'A' else pos - pas
            if nouvelle_position >= plateau.positions[1] or (self.nom == 'B' and nouvelle_position <= plateau.positions[0]):
                return False

        if not simulation:
            if self.nom == 'A':
                plateau.positions[0] = nouvelle_position
            else:
                plateau.positions[1] = nouvelle_position
        return True

    def recup_coups_legaux_action(self, jeu, evenement):
        coups_legaux = {}
        if evenement == "deplacement":
            coups_legaux["D"] = []
            for carte in self.main:
                if self.deplacer(jeu.plateau, carte, simulation=True):
                  coups_legaux["D"].append(carte)
                if self.deplacer(jeu.plateau, -carte, simulation=True):
                  coups_legaux["D"].append(-carte) # A basculer en positif pour remove plus tard
            coups_legaux["D"] = list(set(coups_legaux["D"]))
            dep_pos = [dep for dep in coups_legaux["D"] if dep > 0]
            for dep in dep_pos:
                ind_dep = coups_legaux["D"].index(dep)
                self.deplacer(jeu.plateau, dep, simulation=False)
                self.main.remove(dep) # Afin d'éviter d'utiliser la carte dep dans l'attaque indirecte
                attaques_dep = self.recup_coups_legaux_action(jeu, "attaque")["AD"] # Liste de listes
                self.deplacer(jeu.plateau, -dep, simulation=False)
                self.main.append(dep)
                if attaques_dep:
                  coups_legaux["D"][ind_dep] = [dep, attaques_dep] # Changement de type
            return coups_legaux
        if evenement == "attaque":
            coups_legaux["AD"] = []
            distance = abs(jeu.plateau.positions[0] - jeu.plateau.positions[1])
            maxi_combi = self.main.count(distance)
            if maxi_combi > 0:
              for i in range(1, maxi_combi+1):
                combi = [distance] * i
                coups_legaux["AD"].append(combi)
            else:
              pass
            return coups_legaux
        else:
            return coups_legaux

    def recup_coups_legaux_reaction(self, jeu, evenement, cartes_attaque):
        coups_legaux = {}
        if evenement == "def directe":
            coups_legaux["DD"] = []
            cartes_defense = [carte for carte in self.main if carte == cartes_attaque[0]]
            if len(cartes_defense) >= len(cartes_attaque):
              coups_legaux["DD"] = cartes_attaque # Pas besoin de append
            return coups_legaux
        if evenement == "def indirecte":
            coups_legaux["DI"] = []
            for carte in self.main:
              if self.deplacer(jeu.plateau, -carte, simulation=True):
                  coups_legaux["DI"].append(-carte) # A basculer en positif pour remove plus tard
            coups_legaux["DI"] = list(set(coups_legaux["DI"]))
            dd = self.recup_coups_legaux_reaction(jeu, "def directe", cartes_attaque)["DD"]
            coups_legaux["DI"].append(dd)
            return coups_legaux
        else:
            return coups_legaux

class JeuEnGarde:
    def __init__(self):
        self.taille_plateau = 23
        self.cartes = [1, 2, 3, 4, 5] * 5
        self.plateau = Plateau(self.taille_plateau)
        self.ordinateur1 = Ordinateur('A')
        self.ordinateur2 = Ordinateur('B')
        self.pioche = []
        self.joueur_actuel = self.ordinateur1
        self.fini = False
        self.gagnant = None

    def melanger_pioche(self):
        self.pioche = self.cartes[:]
        random.shuffle(self.pioche)

    def initialiser(self):
        self.melanger_pioche()
        self.plateau = Plateau(self.taille_plateau)
        self.ordinateur1.main = []
        self.ordinateur2.main = []
        self.ordinateur1.piocher_cartes(self.pioche, 5)
        self.ordinateur2.piocher_cartes(self.pioche, 5)
        self.joueur_actuel = self.ordinateur1

    def changer_joueur(self):
        self.joueur_actuel = self.ordinateur2 if self.joueur_actuel == self.ordinateur1 else self.ordinateur1

    def jouer_tour(self):
        self.tour_ordi()
        self.joueur_actuel.piocher_cartes(self.pioche, 5 - len(self.joueur_actuel.main))

    def tour_ordi(self):
        print(f"C'est le tour de l'ordinateur {self.joueur_actuel.nom}.")
        self.plateau.afficher()

        defense_adversaire = False
        att_indirecte = False

        actions_possibles = {**self.joueur_actuel.recup_coups_legaux_action(self, "deplacement"), **self.joueur_actuel.recup_coups_legaux_action(self, "attaque")}
        actions_possibles = {k: v for k, v in actions_possibles.items() if v}
        action = random.choice(list(actions_possibles.keys()))
        coup = random.choice(actions_possibles[action])

        if action == "D":
          if type(coup) == int:
            print(f"L'ordinateur {self.joueur_actuel.nom} se déplace de {coup} cases.")
            self.joueur_actuel.deplacer(self.plateau, coup, simulation=False)
            if coup < 0 : coup = -coup # Pour revenir dans le positif
            self.joueur_actuel.main.remove(coup)
          elif type(coup) == list:
            print(f"L'ordinateur {self.joueur_actuel.nom} se déplace de {coup[0]} cases.")
            self.joueur_actuel.deplacer(self.plateau, coup[0], simulation=False)
            if coup[0] < 0 : coup[0] = -coup[0] # Pour revenir dans le positif
            self.joueur_actuel.main.remove(coup[0])
            on_y_va_pour_une_att_indirecte = random.choice([True, False])
            if on_y_va_pour_une_att_indirecte:
                  defense_adversaire = True
                  att_indirecte = True
                  puissance_att = random.choice(coup[1]) # Plusieurs puissances peuvent être disponibles (liste de listes)
                  for carte in puissance_att:
                    self.joueur_actuel.main.remove(carte)
                  print(f"L'ordinateur {self.joueur_actuel.nom} attaque indirectement avec {puissance_att}.")

        if action == "AD":
          defense_adversaire = True
          for carte in coup:
            self.joueur_actuel.main.remove(carte)
          print(f"L'ordinateur {self.joueur_actuel.nom} attaque avec {coup}.")

        if defense_adversaire:
            adversaire = self.ordinateur2 if self.joueur_actuel == self.ordinateur1 else self.ordinateur1
            if not att_indirecte:
                resultat_defense = self.defendre(adversaire, coup, est_indirect=False)
                if resultat_defense == "parer":
                    print(f"L'ordinateur {adversaire.nom} a paré l'attaque!")
                elif resultat_defense == "échouer":
                    print(f"L'ordinateur {adversaire.nom} n'a pas pu parer l'attaque. L'ordinateur {self.joueur_actuel.nom} gagne!")
                    self.fini = True
                    self.gagnant = self.joueur_actuel
            else:
                resultat_defense = self.defendre(adversaire, puissance_att, est_indirect=True)
                if resultat_defense == "parer":
                  print(f"L'ordinateur {adversaire.nom} a paré l'attaque!")
                elif resultat_defense == "retraite":
                  print(f"L'ordinateur {adversaire.nom} a battu en retraite!")
                else:
                  print(f"L'ordinateur {adversaire.nom} n'a pas pu parer l'attaque. L'ordinateur {self.joueur_actuel.nom} gagne!")
                  self.fini = True
                  self.gagnant = self.joueur_actuel

    def defendre(self, joueur, cartes_attaque, est_indirect):
      if not est_indirect:
          reaction_possible = joueur.recup_coups_legaux_reaction(self, "def directe", cartes_attaque)["DD"]
          if reaction_possible:
            for carte in reaction_possible:
              joueur.main.remove(carte)
            return "parer"
          else:
            return "échouer"

      else:
          reactions_possibles = joueur.recup_coups_legaux_reaction(self, "def indirecte", cartes_attaque)
          coup = random.choice(reactions_possibles["DI"])
          if type(coup) == list:
            for carte in coup:
              joueur.main.remove(carte)
            return "parer"
          else:
            joueur.deplacer(self.plateau, coup, simulation=False)
            print(f"L'ordinateur {joueur.nom} se déplace de {coup} cases en arrière pour parer l'attaque indirecte.")
            coup = -coup # Passer dans le positif pour remove
            joueur.main.remove(coup)
            joueur.piocher_cartes(self.pioche, 5 - len(joueur.main))
            joueur.a_battu_en_retraite_pour_esquiver = True
            return "retraite"


    def verifier_conditions_fin(self):
        if not self.pioche:
            print("La pioche est épuisée.")
            # Condition 3a: Le joueur avec le plus de cartes valides pour une attaque directe gagne
            distance = abs(self.plateau.positions[0] - self.plateau.positions[1])
            cartes_valides_ordi1 = self.ordinateur1.main.count(distance)
            cartes_valides_ordi2 = self.ordinateur2.main.count(distance)
            if cartes_valides_ordi1 > cartes_valides_ordi2:
                print("L'ordinateur A gagne par nombre de cartes d'attaque valide.")
                self.gagnant = self.ordinateur1
                return True
            elif cartes_valides_ordi2 > cartes_valides_ordi1:
                print("L'ordinateur B gagne par nombre de cartes d'attaque valide.")
                self.gagnant = self.ordinateur2
                return True
            # Condition 3b: Si égalité, celui qui est le plus avancé vers le camp adverse gagne
            if self.plateau.positions[0] > (self.plateau.taille - self.plateau.positions[1] + 1):
                print("L'ordinateur A gagne par avancée sur la piste.")
                self.gagnant = self.ordinateur1
                return True
            elif self.plateau.positions[1] <= (self.plateau.taille - self.plateau.positions[0]):
                print("L'ordinateur B gagne par avancée sur la piste.")
                self.gagnant = self.ordinateur2
                return True
            else:
                print("La manche est déclarée nulle.")
                return True

        # Condition 2: Un joueur ne peut plus effectuer de mouvement autorisé
        for ordi in [self.ordinateur1, self.ordinateur2]:
            peut_bouger = False
            for carte in ordi.main:
                if ordi.deplacer(self.plateau, carte, simulation=True):
                    peut_bouger = True
                    break
                elif ordi.deplacer(self.plateau, -carte, simulation=True):
                    peut_bouger = True
                    break
            if not peut_bouger:
                print(f"L'ordinateur {ordi.nom} ne peut plus effectuer de mouvement autorisé et perd la manche.")
                if ordi.nom == "A": self.gagnant = self.ordinateur2
                else: self.gagnant = self.ordinateur1
                return True

        return False

    def jouer_jeu(self):
        self.initialiser()
        autre_ordi = None
        while not self.fini and not self.verifier_conditions_fin():
            self.ordinateur1.a_battu_en_retraite_pour_esquiver = False
            self.ordinateur2.a_battu_en_retraite_pour_esquiver = False
            self.jouer_tour()
            if self.joueur_actuel.nom == "A": autre_ordi = self.ordinateur2
            else: autre_ordi = self.ordinateur1
            if not autre_ordi.a_battu_en_retraite_pour_esquiver:
                self.changer_joueur()
        if self.gagnant:
          return self.gagnant.nom
        else:
          return None

# Démarrer le jeu
jeu = JeuEnGarde()
jeu.jouer_jeu()
