# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 00:21:39 2019

@author:Ariana Carnielli \\ Ivan Kachaikin
Méthodes pour le projet de MOGPL 2019-2020
"""
import numpy as np
from tqdm import tqdm

class Jeu:
    """
    Classe générale pour représenter le jeu Dice Battle.
    Contient des méthodes pour initialiser le jeu, définir les stratégies 
    utilisées pour chaque joueur, jouer une partie, donner le vainqueur, etc. 
    
    Attributs :
        D : Nombre maximum de dés qu'un joueur peut lancer dans 1 tour du jeu.
        N : Nombre de points à atteindre pour gagner une partie. 
        probas : Tableau qui stocke P(d, k), la probabilité qu'un joueur qui 
            lance d dés obtienne k points.
        joueur1 : score du premier joueur.
        joueur2 : score du deuxième joueur.
        strategie1 : stratégie utilisée pour lancer les dés du joueur 1.
        strategie2 : stratégie utilisée pour lancer les dés du joueur 2.
    """
    
    def __init__(self, D, N):
        """
        Crée un jeu avec les D et N passés en argument.
        Initialise le tableau probas qui stocke P(d, k), la probabilité qu'un
        joueur qui lance d dés obtienne k points.
        Initialise les scores des deux joueurs à zéro.
        
        Args :
            D : Nombre maximum de dés qu'un joueur peut lancer dans 1 tour du 
                jeu.
            N : Nombre de points à atteindre pour gagner une partie. 
        """
        self.D = D
        self.N = N
        self.probas = self._tableProba()
        
        self.joueur1 = 0
        self.joueur2 = 0
        
    def comparerStrategies(self, strategie1, strategie2, nbFois = 10000):
        """
        Joue nbFois parties avec les stratégies passées en argument et renvoie 
        des statistiques sur l'ensemble de parties.
        
        Args :
            strategie1 : Un objet du type Strategie.
            strategie2 : Un objet du type Strategie. Peut être le même que le 
                premier.
            nbFois : Quantité de parties à jouer.
        Returns :
            Un triplet formé par la quantité de victoires du joueur 1, la 
            quantité de victoires du joueur 2 et la quantité de parties nulles.
        """
        self.setStrategies(strategie1, strategie2)
        self._reset()  
        nbVic1 = 0
        nbVic2 = 0
        nbNul = 0
        for _ in tqdm(range(nbFois)):
            self.jouer(verbose = False)
            if self.vainqueur() == 1:
                nbVic1 += 1
            elif self.vainqueur() == 2:
                nbVic2 += 1
            else:
                nbNul += 1
            self._reset()
        return nbVic1, nbVic2, nbNul         
        
    def setStrategies(self, strategie1, strategie2):
        """
        Initialise les stratégies des deux joueurs. Cette méthode doit être 
        appelée avant de l'appel à la méthode jouer. 
        
        Args : 
            strategie1 : Un objet du type Strategie.
            strategie2 : Un objet du type Strategie. Peut être le même que le 
                premier.
        """
        self.strategie1 = strategie1
        self.strategie2 = strategie2
        
    def jouer(self, verbose = True):
        """
        Joue une partie du jeu, avec les D et N passés à la création de l'objet
        et les stratégies initialisées par la méthode setStrategie.
        
        Args : 
            verbose (facultatif) : si True, affiche des messages a chaque étape
                du jeu montrant le déroulement de la partie et quel joueur à
                gagné.            
        """
        if verbose :
            print ("La partie commence :")
            print("Joueur 1 | Joueur 2")
        while not self._estfini() :
            self._tour()
            if verbose :
                print("{:8d} | {:8d}".format(self.joueur1, self.joueur2))
        if verbose :
            if self.vainqueur() == 0:
                print("Match nul")    
            else:
                print("La partie est finie, le joueur", self.vainqueur(), \
                      "a gagné")
    
    def vainqueur(self):
        """
        Retourne le numéro du joueur gagnant et zéro si match nul.
        
        Returns : 
            1 si le joueur 1 a gagné, 2 si le joueur 2 a gagné et 0 si match 
            nul.
        """
        if self.joueur1 == self.joueur2 :
            return 0
        return 1 if self.joueur1 > self.joueur2 else 2
   
    def _reset(self):
        """
        Réinitialise les scores des joueurs pour qu'une nouvelle partie puisse
        être jouée.        
        """
        self.joueur1 = 0
        self.joueur2 = 0
    
    def _estfini(self):
        """
        Détermine si la partie est finie.
        
        Returns :
            True si la partie est finie (un des joueurs a plus de N points),
            False sinon.
        """
        return self.joueur1 >= self.N or self.joueur2 >= self.N
    
    def _tirageDes(self, d):
        """
        Simule le lancer de d dés de 6 faces non pipés, avec la règle du jeu 
        qui ramène le résultat à 1 si au moins un des dés est tombé à 1.
        
        Args : 
            d : La quantité de dés à jouer.
        Returns : 
            La somme de d lancés. Si au moins un des lancés donne 1, 
            retourne 1.         
        """
        res = np.random.randint(1, 7, d)
        if np.any(res == 1):
            return 1
        return res.sum()
        
    def _tour(self):
        """
        Spécifié dans les classes filles.
        """
        pass

    def _tableProba(self):
        """
        Calcule le tableau des probabilités P(d, k), la probabilité qu'un 
        joueur qui lance d dés obtienne k points.
        Le tableau a pour taille (D + 1) x (6D + 1) car pour avoir des indices 
        plus naturels on rajoute une colonne 0 et une ligne 0. 
        
        Returns : 
            Tableau des probabilités P(d, k).
        """
        #on va d'abord calculer le tableau des Q(d, k) 
        #on initialise le tableau à 0
        q = np.zeros((self.D + 1, 6 * self.D + 1))
        #on initialise la ligne correspondant à d = 1
        q[1, 2:7] = 1 / 5
            
        #on rempli le tableau q avec les Q(d, k)
        for di in range(2, self.D + 1):
            for k in range(2 * di, 6 * di + 1):
                q[di, k] = q[di - 1, max(k - 6, 0) : k - 1].sum() / 5
        
        #on crée le tableau de probabilités P(d, k)
        proba = np.zeros((self.D + 1, 6 * self.D + 1))
        #la probabilité d'avoir k = 0 avec 0 dés est égale à 1
        proba[0, 0] = 1
        #on initialise la colonne correspondant à k = 1
        proba[1:, 1] = 1 - (5 / 6) ** np.arange(1, self.D + 1)
        #on fait P(d, k) = Q(d, k) * (5/6)**d pour k >= 2
        proba[:, 2:] = q[:, 2:] * (5 / 6) ** \
            np.arange(self.D + 1).reshape((self.D + 1, 1))
        return proba
    
class JeuSequentiel(Jeu):
    """
    Classe pour représenter la version séquentielle du jeu Dice Battle.
    Contient des méthodes spécifiques pour jouer un tour du jeu, initialiser et
    réinitialiser l'attribut joueurCourant.
    
    Attributs :
        D : Nombre maximum de dés qu'un joueur peut lancer dans 1 tour du jeu.
        N : Nombre de points à atteindre pour gagner une partie. 
        probas : Tableau qui stocke P(d, k), la probabilité qu'un joueur qui 
            lance d dés obtienne k points.
        joueur1 : score du premier joueur.
        joueur2 : score du deuxième joueur.
        strategie1 : stratégie utilisée pour lancer les dés du joueur 1.
        strategie2 : stratégie utilisée pour lancer les dés du joueur 2.
        joueurCourant : détermine de quel joueur est le tour.
    """
    def __init__(self, D, N):
        """
        Crée un jeu avec les D et N passés en argument.
        Initialise le tableau probas qui stocke P(d, k), la probabilité qu'un
        joueur qui lance d dés obtienne k points.
        Initialise les scores des deux joueurs à zéro.
        Initialise le joueur courant à 1.
        
        Args :
            D : Nombre maximum de dés qu'un joueur peut lancer dans 1 tour du 
                jeu.
            N : Nombre de points à atteindre pour gagner une partie. 
        """
        super().__init__(D, N)
        self.joueurCourant = 1
        
    def _reset(self):
        """
        Réinitialise les scores des joueurs pour qu'une nouvelle partie puisse
        être jouée. Remet le joueur 1 comme joueur courant. 
        """
        super()._reset()
        self.joueurCourant = 1
        
    def _tour(self):
        """
        Joue un tour du jeu de façon séquentielle. Joue uniquement à un joueur 
        à la fois.
        """
        if self.joueurCourant == 1:
            des = self.strategie1.jouerTour(self.joueur1, self.joueur2)
            self.joueur1 += self._tirageDes(des)
        else:
            des = self.strategie2.jouerTour(self.joueur2, self.joueur1)
            self.joueur2 += self._tirageDes(des)
        self.joueurCourant = 3 - self.joueurCourant

class JeuSimultane(Jeu):
    """
    Classe pour représenter la version simultanée du jeu Dice Battle.
    Contient des méthodes spécifiques pour jouer un tour du jeu.
    
    Attributs :
        D : Nombre maximum de dés qu'un joueur peut lancer dans 1 tour du jeu.
        N : Nombre de points à atteindre pour gagner une partie. 
        probas : Tableau qui stocke P(d, k), la probabilité qu'un joueur qui 
            lance d dés obtienne k points.
        joueur1 : score du premier joueur.
        joueur2 : score du deuxième joueur.
        strategie1 : stratégie utilisée pour lancer les dés du joueur 1.
        strategie2 : stratégie utilisée pour lancer les dés du joueur 2.  
    """
    def __init__(self, D, N):
        """
        Crée un jeu avec les D et N passés en argument.
        Initialise le tableau probas qui stocke P(d, k), la probabilité qu'un
        joueur qui lance d dés obtienne k points.
        Initialise les scores des deux joueurs à zéro.
        
        Args :
            D : Nombre maximum de dés qu'un joueur peut lancer dans 1 tour du 
                jeu.
            N : Nombre de points à atteindre pour gagner une partie. 
        """
        super().__init__(D, N)

    def _tour(self):
        """
        Joue un tour du jeu de façon simultanée.
        """
        des1 = self.strategie1.jouerTour(self.joueur1, self.joueur2)
        des2 = self.strategie2.jouerTour(self.joueur2, self.joueur1)
        self.joueur1 += self._tirageDes(des1)
        self.joueur2 += self._tirageDes(des2)
