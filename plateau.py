__authors__ = 'Carl Dumont et Simon Provencher!'
__date__ = "31 avril 2015"

"""Ce fichier permet d'afficher un plateau de tic-tac-toe, d'initialiser les positions des pièces et de modifier le plateau
selon les commandes envoyées par les joueurs dans la partie! Il gère aussi l'intelligence artificielle de l'ordinateur"""

from case import Case
from random import randrange

class Plateau:
    """
    Classe modélisant le plateau du jeu Tic-Tac-Toe.

    Attributes:
        cases           (dict)      : Dictionnaire des cases et de leur contenu
        chaîne_plateau  (str)       : Contient la chaîne affichant le plateau de jeu
        victoire        (bool)      : Retourne si le jouer a gagné la partie, Vrai si oui, Faux si non
        non_plein       (bool)      : Retourne si le plateau est plein
        choisir_prochaine_case (int): Retourne deux coordonnées numériques correspondant au prochain mouvement de
                                        l'ordinateur



    """

    def __init__(self):
        """
        Méthode spéciale initialisant un nouveau plateau contenant les 9 cases du jeu.
        """

        # Dictionnaire de cases.
        # La clé est une position (ligne, colonne), et la valeur est une instance de la classe Case.
        self.cases = {}

        # Appel d'une méthode qui initialise un plateau contenant des cases vides.
        self.initialiser()

    def initialiser(self):
        """
        Initialise le plateau avec des cases vides (contenant des espaces).
        """

        # Vider le dictionnaire (pratique si on veut recommencer le jeu).
        self.cases.clear()
        # Parcourir le dictionnaire et mettre des objets de la classe Case.
        # dont l'attribut "contenu" serait un espace (" ").

        for i in range(0, 3):
            for j in range(0, 3):
                self.cases[i,j] = Case(" ")

    def __str__(self):
        """Méthode spéciale indiquant à Python comment représenter une instance de Plateau
        sous la forme d'une chaîne de caractères. Permet donc d'afficher le plateau du jeu
        à l'écran en faisant par exemple:
        p1 = Plateau()
        print(p1)

        Voici un exemple d'affichage:
         +-0-+-1-+-2-+
        0|   | X | X |
         +---+---+---+
        1| O | O | X |
         +---+---+---+
        2|   |   | O |
         +---+---+---+

        Returns:
            string: Retourne la chaîne de caractères à afficher.
        """

        chaîne_plateau= " +-0-+-1-+-2-+ \n"
        for i in range(0,3):
            chaîne_plateau += str(i) + "| "
            for j in range(0,3):
                chaîne_plateau += self.cases[i,j].contenu +" | "
            chaîne_plateau += " \n"
            chaîne_plateau += " +---+---+---+ \n"
        return chaîne_plateau




    def non_plein(self):
        """
        Retourne si le plateau n'est pas encore plein.
        Il y a donc encore des cases vides (contenant des espaces et non des "X" ou des "O").

        Returns:
            bool: True si le plateau n'est pas plein, False autrement.
        """
        for i in range(0,3):
            for j in range(0,3):
                if self.cases[i,j].est_vide():
                    return True
        return False

    def position_valide(self, ligne, colonne):
        """
        Vérifie si une position est valide pour jouer.
        La position ne doit pas être occupée.
        Il faut utiliser la méthode est_vide() de la classe Case.

        Args:
            ligne (int): Le numéro de la ligne dans le plateau du jeu.
            colonne (int): Le numéro de la colonne dans le plateau du jeu.

        Returns:
            bool: True si la position est valide, False autrement.
        """
        assert isinstance(ligne, int), "Plateau: ligne doit être un entier."
        assert isinstance(colonne, int), "Plateau: colonne doit être un entier."

        return self.cases[ligne, colonne].est_vide()


    def selectionner_case(self, ligne, colonne, pion):
        """
        Permet de modifier le contenu de la case
        qui a les coordonnées (ligne,colonne) dans le plateau du jeu
        en utilisant la valeur de la variable pion.

        Args:
            ligne (int): Le numéro de la ligne dans le plateau du jeu.
            colonne (int): Le numéro de la colonne dans le plateau du jeu.
            pion (string): Une chaîne de caractères ("X" ou "O").
        """
        assert isinstance(ligne, int), "Plateau: ligne doit être un entier."
        assert isinstance(colonne, int), "Plateau: colonne doit être un entier."
        assert isinstance(pion, str), "Plateau: pion doit être une chaîne de caractères."
        assert pion in ["O", "X"], "Plateau: pion doit être 'O' ou 'X'."
        assert ligne in [0, 1, 2], "Plateau: ligne doit être 0, 1 ou 2."
        assert colonne in [0, 1, 2], "Plateau: colonne doit être 0, 1 ou 2."

        self.cases[ligne, colonne].contenu = pion


    def est_gagnant(self, pion):
        """
        Permet de vérifier si un joueur a gagné le jeu.
        Il faut vérifier toutes les lignes, colonnes et diagonales du plateau.

        Args:
            pion (string): La forme du pion utilisé par le joueur en question ("X" ou "O").

        Returns:
            bool: True si le joueur a gagné, False autrement.
        """

        assert isinstance(pion, str), "Plateau: pion doit être une chaîne de caractères."
        assert pion in ["O", "X"], "Plateau: pion doit être 'O' ou 'X'."
        for i in range (0,3):
            victoire = (self.cases[i,0].contenu == pion and self.cases[i,1].contenu == pion and self.cases[i,2].contenu == pion) or \
                       (self.cases[0,i].contenu == pion and self.cases[1,i].contenu == pion and self.cases[2,i].contenu == pion)
            if victoire == True:
                return victoire #comparaison pour les lignes ou les colonnes gagnantes

        victoire = True
        i=0
        while i<=2:
            if self.cases[i,i].contenu != pion:
                victoire = False
            i +=1
        if victoire == True:
            return victoire
        i = 0
        j = 2
        victoire = True
        while i <=2:
            if self.cases[i,j].contenu != pion:
                victoire = False
            i += 1
            j -= 1
        if victoire == True:
            return victoire
        #comparaison pour les deux diagonales possibles
        return False





    def choisir_prochaine_case(self, pion):
        """
        Permet de retourner les coordonnées (ligne, colonne) de la case que l'ordinateur
        peut choisir afin de jouer contre un autre joueur qui est normalement une personne.
        Ce choix doit se faire en fonction de la configuration actuelle du plateau.
        L'algorithme que vous allez concevoir permettant de faire jouer l'ordinateur
        n'a pas besoin d'être optimal. Cela permettra à l'adversaire de gagner de temps en temps.
        Il faut par contre essayer de mettre le pion de l'ordinateur dans une ligne, une colonne
        ou une diagonale contenant deux pions de l'adversaire pour que ce dernier ne gagne pas facilement.
        Il faut aussi essayer de mettre le pion de l'ordinateur dans une ligne, une colonne
        ou une diagonale contenant deux pions de l'ordinateur pour que ce dernier puisse gagner.
        Vous pouvez utiliser ici la fonction randrange() du module random.
        Par exemple: randrange(1,10) vous retourne une valeur entre 1 et 9 au hasard.

        Args:
            pion (string): La forme du pion de l'adversaire de l'ordinateur ("X" ou "O").

        Returns:
            (int,int): Une paire d'entiers représentant les coordonnées de la case choisie.
        """
        assert isinstance(pion, str), "Plateau: pion doit être une chaîne de caractères."
        assert pion in ["O", "X"], "Plateau: pion doit être 'O' ou 'X'."

        if pion == "X":
            pion_ordi= "O"
        else:
            pion_ordi = "X"
        for i in range(0,3):
            for j in range(0,3):
                if self.position_valide(i, j):
                    self.cases[i,j] = Case(pion_ordi)
                    if self.est_gagnant(pion_ordi):
                        return (i,j)
                    else: self.cases[i,j]=Case(" ")
                    #teste si l'ordinateur peut gagner au prochain tour
                    #si oui, il place un pion pour gagner
        for i in range(0,3):
            for j in range(0,3):
                if self.position_valide(i,j):
                    self.cases[i,j] = Case(pion)
                    if self.est_gagnant(pion):
                        return (i,j)
                    else: self.cases[i,j]=Case(" ")
                    #teste si l'humain peut gagner au prochain tour
                    #si oui, il place un pion pour le bloquer
        x = 0
        while x != 10:
            a = randrange(0,3)
            b = randrange(0,3)
            if self.position_valide(a,b):
                return (a,b)
        #si il n'y a pas de mouvement victorieux, on place un pion au hasard




