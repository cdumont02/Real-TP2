__authors__ = 'Carl Dumont et Simon Provencher'
__date__ = "31 mars 2015"

"""Ce fichier permet d'exécuter une partie du jeu tic-tac-toe."""

from plateau import Plateau
from joueur import Joueur

class Partie:
    """
    Classe modélisant une partie du jeu Tic-Tac-Toe utilisant
    un plateau et deux joueurs (deux personnes ou une personne et un ordinateur).

    Attributes:
        plateau             (obj Plateau)       : Représente le plateau sur lequel la partie se déroule.
        joueurs             (liste obj Joueur)  : Représente les joueurs qui vont joueur la partie. Ils sont soit des personnes ou un ordinateur.
        joueur_courant      (obj Joueur)        : Contient le joueur qui est en train d'exécuter son tour
        nb_partie_nulles    (int)               : Nombre de parties qu'aucun de joueur n'a gagné.
        est_terminée        (bool)              : Est vrai si les condition de fin de partie sont rencontrées.  False autrement.
        joueur_gagnant      (str)               : Contient le nom du joueur gagnant.
        pion_non_choisi     (str)               : Contient la valeur du pion qui n'a pas été choisi par l'utilisateur.

    """

    def __init__(self):
        """
        Méthode spéciale initialisant une nouvelle partie du jeu Tic-Tac-Toe.
        """
        self.plateau = Plateau()    # Le plateau du jeu contenant les 9 cases.
        self.joueurs = []           # La liste des deux joueurs (initialement une liste vide).
                                    # Au début du jeu, il faut ajouter les deux joueurs à cette liste.
        self.joueur_courant = None  # Le joueur courant (initialisé à une valeur nulle: None)
                                    # Pendant le jeu et à chaque tour d'un joueur,
                                    # il faut affecter à cet attribut ce joueur courant.
        self.nb_parties_nulles = 0  # Le nombre de parties nulles (aucun joueur n'a gagné).
        self.est_terminee = False
        self.joueur_gagnant = ""
        self.pion_non_choisi = ""

    def jouer(self):
        """
        Permet de démarrer la partie en commençant par l'affichage de ce texte:

        Bienvenue au jeu Tic Tac Toe.
        ---------------Menu---------------
        1- Jouer avec l'ordinateur.
        2- Jouter avec une autre personne.
        0- Quitter.
        -----------------------------------
        Entrez s.v.p. un nombre entre 0 et 2:?

        Cette méthode doit donc utiliser la méthode saisir_nombre().
        Elle doit par la suite demander à l'utilisateur les noms des joueurs.
        Veuillez utiliser 'Colosse' comme nom pour l'ordinateur.
        Il faut créer des instances de la classe Joueur et les ajouter à la liste joueurs.
        Il faut utiliser entre autres ces méthodes:
            *- demander_forme_pion(): pour demander au premier joueur la forme de son pion (X ou O).
              (Pas besoin de demander à l'autre joueur ou à l'ordinateur cela, car on peut le déduire).
            *- plateau.non_plein(): afin d'arrêter le jeu si le plateau est plein (partie nulle).
            *- tour(): afin d'exécuter le tour du joueur courant.
            *- plateau.est_gagnant(): afin de savoir si un joueur a gagné et donc arrêter le jeu.
        Il faut alterner entre le premier joueur et le deuxième joueur à chaque appel de tour()
        en utilisant l'attribut joueur_courant.
        Après la fin de chaque partie, il faut afficher les statistiques sur le jeu.
        Voici un exemple:

        Partie terminée! Le joueur gagnant est: Colosse
        Parties gagnées par Mondher : 2
        Parties gagnées par Colosse : 1
        Parties nulles: 1
        Voulez-vous recommencer (O,N)?

        Il ne faut pas oublier d'initialiser le plateau avant de recommencer le jeu.
        Si l'utilisateur ne veut plus recommencer, il faut afficher ce message:
        ***Merci et au revoir !***
        """

        #On prend le choix de l'utilisateur dans le menu principal
        choix = self.menu_principal()

        #On initialise la partie selon le choix de l'utilisateur dans le menu principal
        self.initialiser_partie(choix)

        #Prermière loop pour savoir si la partie est terminée.
        #Si l'utilisateur a entré 0 comme choix, est-terminee == True donc la partie est automatiquement terminée.
        while self.est_terminee == False:

            #On execute les tours jusqu'à ce que le match soit complet.
            self.tour(choix)

            #On affichie les statisqiques de la partie
            self.afficher_statistiques()

            #On détermine si la partie est terminée en inversant le choix de recommencer nouveau match.
            #Si on recommence un nouveau match, la partie n'est donc pas terminée.
            self.est_terminee = not(self.recommencer_nouveau_match())

        #On Termine la partie
        self.terminer_partie()


    def saisir_nombre(self, nb_min, nb_max):
        """
        Permet de demander à l'utilisateur un nombre et doit le valider.
        Ce nombre doit être une valeur entre nb_min et nb_max.
        Vous devez utiliser la méthode isnumeric() afin de vous assurer que l'utilisateur entre
        une valeur numérique et non pas une chaîne de caractères.
        Veuillez consulter l'exemple d'exécution du jeu mentionné dans l'énoncé du TP
        afin de savoir quoi afficher à l'utilisateur.

        Args:
            nb_min (int): Un entier représentant le minimum du nombre à entrer.
            nb_max (int): Un entier représentant le maximum du nombre à entrer.

        Returns:
            int: Le nombre saisi par l'utilisateur après validation.
        """
        assert isinstance(nb_min, int), "Partie: nb_min doit être un entier."
        assert isinstance(nb_max, int), "Partie: nb_max doit être un entier."

        est_valeur_valide = False
        while est_valeur_valide == False:
            valeur_entree = input("Veuillez entrer un nombre entre {} et {}".format(nb_min, nb_max))
            if valeur_entree.isnumeric():
                valeur_entree = int(valeur_entree)
                if valeur_entree >= nb_min and valeur_entree <= nb_max:
                    est_valeur_valide = True
                    continue
                else:
                    print("Le nombre entré est invalide")
            else:
                print("La valeur entrée n'est pas un nombre.  Veuillez entrer un nombre")
        return valeur_entree


    def demander_forme_pion(self):
        """
        Permet de demander à l'utilisateur un caractère et doit le valider.
        Ce caractère doit être soit 'O' soit 'X'.
        Veuillez consulter l'exemple d'exécution du jeu mentionné dans l'énoncé du TP
        afin de savoir quoi afficher à l'utilisateur.

        Returns:
            string: Le catactère saisi par l'utilisateur après validation.
        """
        est_choix_valide = False
        while est_choix_valide == False:
            choix = input("Veuillez choisir le pion pour le premier joueur entre X ou O")
            choix = choix.upper()
            if (choix == "X" or choix =="O"):
                est_choix_valide = True
            else:
                print("Choix invalide.  Veuillez choisir entre X ou O")
                continue
        if choix == "X":
            self.pion_non_choisi = "O"
        else:
            self.pion_non_choisi ="X"
        return choix


    def tour(self, choix):
        """
        Permet d'exécuter le tour d'un joueur (une personne ou un ordinateur).
        Cette méthode doit afficher le plateau (voir la méthode __str__() de la classe Plateau).
        Si le joueur courant est un ordinateur, il faut calculer la position de la prochaine
        case à jouer par cet ordinateur en utilisant la méthode choisir_prochaine_case().
        Si le joueur courant est une personne, il faut lui demander la position de la prochaine
        case qu'il veut jouer en utilisant la méthode demander_postion().
        Finalement, il faut utiliser la méthode selectionner_case() pour modifier le contenu
        de la case choisie soit par l'ordinateur soit par la personne.

        Args:
            choix (int): Un entier représentant le choix de l'utilisateur dans le menu du jeu (1 ou 2).
        """

        assert isinstance(choix, int), "Partie: choix doit être un entier."
        assert choix in [1, 2], "Partie: choix doit être 1 ou 2."

        def determiner_joueur_actif(tour, liste_joueurs):
            """
            Fonction déterminant qui est le joueur actif dans une liste en fonction du tour.  Un tour pair équivaut nécessairement au
            tour du joueur numéro 2

            Args:
                tour (int) : Un entier représentant le tour actif
                joueurs (liste d'objets Joueurs) : Liste contenant les joueurs de la partie.

             Returns:
                Rien
            """
            if tour%2==0:
                self.joueur_courant=liste_joueurs[1]
            else:
                self.joueur_courant=liste_joueurs[0]

        def executer_action_joueur():
            """
            Cette Fonction permet d'executer le tour d'un joueur de type Personne soit demander la position souhaitée, la valider et la sélectionner.

            Args:
                Rien
            Returns:
                Rien
            """
            coord = self.demander_postion()
            while(self.plateau.position_valide(coord[0], coord[1])==False):
                print("La case est déjà occupée.  Veuillez choisir une autre case.")
                coord = self.demander_postion()
            self.plateau.selectionner_case(coord[0], coord[1], self.joueur_courant.pion)

        def executer_action_ordinateur(pion):
            """
            Cette Fonctione permet d'exécuter la tour d'un joureur de type Ordinateur.
            Args:
                Rien
            Returns:
                Rien
            """
            a,b = self.plateau.choisir_prochaine_case(pion)
            self.plateau.selectionner_case(a,b,pion)
            #la fonction choisir_prochaine _case doit retourner une paire d'entiers
            #on doit donc avoir une nouvelle ligne de code ici pour assigner une case


        #SI le joueur a choisi 1 au menu principal les tours se déroulent de cette façon.
        if choix  == 1:
            tour = 0
            self.plateau.initialiser()
            while self.plateau.non_plein():
                tour += 1
                determiner_joueur_actif(tour, self.joueurs)
                print(self.plateau)
                print("C'est maintenant le tour de : ", self.joueur_courant.nom)
                if(self.joueur_courant.type == "PERSONNE"):
                    executer_action_joueur()
                else:
                    executer_action_ordinateur(self.joueur_courant.pion)
                if(self.plateau.est_gagnant(self.joueur_courant.pion)):
                    self.est_terminee = True
                    self.joueur_gagnant = self.joueur_courant.nom
                    self.joueur_courant.nb_parties_gagnees += 1
                    print(self.plateau)
                    break
            if(self.plateau.non_plein() == False):
                est_terminee = True
                self.nb_parties_nulles += 1
                print(self.plateau)
                self.joueur_gagnant = "Partie Nulle"
                print("***Partie Nulle***")

        #Sinon si le joueur a choisi 2 dans le menu principal, le tours s'exécutent de cette façon.
        elif choix == 2:
            tour = 0
            self.plateau.initialiser()
            while self.plateau.non_plein():
                tour += 1
                determiner_joueur_actif(tour, self.joueurs)
                print(self.plateau)
                print("C'est maintenant le tour de : ", self.joueur_courant.nom)
                executer_action_joueur()
                if(self.plateau.est_gagnant(self.joueur_courant.pion)):
                    self.est_terminee = True
                    self.joueur_gagnant = self.joueur_courant.nom
                    self.joueur_courant.nb_parties_gagnees += 1
                    print(self.plateau)
                    break
            if(self.plateau.non_plein() == False):
                est_terminee = True
                self.nb_parties_nulles += 1
                print(self.plateau)
                self.joueur_gagnant = "Partie Nulle"
                print("***Partie Nulle***")
        else:
            assert "Choix Invalide est passé en paramètre du tour"

    def demander_postion(self):
        """
        Permet de demander à l'utilisateur les coordonnées de la case qu'il veut jouer.
        Cette méthode doit valider ces coordonnées (ligne,colonne).
        Voici un exemple de ce qu'il faut afficher afin de demander cette position:

        Mondher : Entrez s.v.p. les coordonnées de la case à utiliser:
        Numéro de la ligne:Entrez s.v.p. un nombre entre 0 et 2:? 0
        Numéro de la colonne:Entrez s.v.p. un nombre entre 0 et 2:? 0

        Il faut utiliser la méthode saisir_nombre() et position_valide().

        Returns:
            (int,int):  Une paire d'entiers représentant les
                        coordonnées (ligne, colonne) de la case choisie.
        """
        est_choix_valide = False
        while est_choix_valide == False:
            print("Veuillez entrer le numéro de la ligne")
            premiere_coordonne = self.saisir_nombre(0,2)
            print("Veuillez entrer le numéro de la colonne.")
            deuxieme_coordone = self.saisir_nombre(0,2)
            if (self.plateau.position_valide(premiere_coordonne, deuxieme_coordone)):
                coord = (premiere_coordonne, deuxieme_coordone)
                est_choix_valide = True
            else:
                print("La case est occupée, veuillez entre une nouvelle coordonée")
                continue
        return coord

    def menu_principal(self):
        """
        Cette méthode affiche le menu principal du jeu.  Elle retourne le choix de l'utilisateur.

        :return:
            int choix qui varie entre 0 et 2
        """

        print("Bienvenue au jeu Tic Tac Toe.")
        print("---------------Menu---------------")
        print("1- Jouer avec l'ordinateur.\n2- Jouter avec une autre personne.\n0- Quitter.")
        print("----------------------------------")
        choix = self.saisir_nombre(0,2)
        return choix

    def recommencer_nouveau_match(self):
        """
        Cette méthode demande à l'utilisateur s'il veur faire un nouveau match.

        :return:
            rien
        """
        est_choix_valide = False
        print("Voulez vous recommencer? (O, N)")
        while est_choix_valide==False:
            choix = str(input().upper())
            if choix == "O":
                return True
                est_choix_valide == True
            elif choix == "N":
                return False
                est_choix_valide == True
            else:
                print("Veuillez entrer un choix valide")

    def initialiser_partie(self, choix):
        """
        Cette Méthode permet d'unitialise la partie.  Elle ajoute les joueurs dans la liste et assigne les pions selon le choix de l'utilisateur.
        :param choix (int): choix du menu principal.  Dépend si le joueur a chasi de jouer cntre un ordinateur ou contre une autre personne.
        :return:
            Rien
        """
        def append_joueurs(joueur1, joueur2):
            self.joueurs.append(joueur1)
            self.joueurs.append(joueur2)

        if choix == 1:
            joueur1 = Joueur("PERSONNE", self.demander_forme_pion())
            joueur2 = Joueur("ORDINATEUR", self.pion_non_choisi)
            append_joueurs(joueur1, joueur2)

        elif choix == 2:
            joueur1 = Joueur("PERSONNE", self.demander_forme_pion(),"1")
            joueur2 = Joueur("PERSONNE", self.pion_non_choisi, "2")
            append_joueurs(joueur1, joueur2)

        elif choix == 0:
            self.est_terminee = True




    def afficher_statistiques(self):
        """
        Cette méthode afficher les statistiques de la partie en cours

        :return:
            rien
        """
        print("Le match est terminé. Le joueur gagnant est: ", self.joueur_gagnant)
        for joueur in self.joueurs:
            print("Nombre de parties gagnées par ", joueur.nom, " : ",joueur.nb_parties_gagnees )
        print("Nombres de parties nulles : ", self.nb_parties_nulles)

    def terminer_partie(self):
        """
        Cette méthode exécute le code lorsque la partie est considérée comme terminée.

        :return:
            Rien
        """
        print("***Merci et au revoir !***  ")


if __name__ == "__main__":
    # Point d'entrée du programme.
    # On initialise une nouvelle partie, et on appelle la méthode jouer().
    partie = Partie()
    partie.jouer()