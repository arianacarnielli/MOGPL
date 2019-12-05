# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 00:19:27 2019

@author:Ariana Carnielli \\ Ivan Kachaikin
Méthodes pour le projet de MOGPL 2019-2020
"""

import numpy as np
from scipy.optimize import linprog

class Strategie:
    """
    Classe générale pour les différentes stratégies du jeu Dice Battle. 
    Sert a initialiser l'attribut jeu qui est utilisé dans les stratégies 
    spécifiques.
    Toutes les stratégies implémentées peuvent être utilisées pour les deux
    variantes du jeu (séquentielle et simultanée).
    
    Attributs :
        jeu : Un objet du type Jeu.
    """
    def __init__(self, jeu):
        """
        Crée une stratégie avec le jeu passé en argument.
        
        Args : 
            jeu : Un objet du type Jeu.
        """
        self.jeu = jeu

    def jouerTour(self, moi, autre):
        """
        Spécifié dans les classes filles.
        """
        pass

class StrategieAleatoire(Strategie):
    """
    Stratégie aléatoire pour le jeu Dice Battle.
    
    Attributs :
        jeu : Un objet du type Jeu.
    """
    def jouerTour(self, moi, autre):
        """
        Rendre une quantité de dés entre 1 et D (la quantité maximale de dés) 
        selon une loi uniforme.
        
        Args : 
            moi : Score du joueur avec la stratégie courante.   
            autre : Score de l'autre joueur.
            (Ces arguments ne sont pas utilisés dans cette classe mais sont 
            nécessaires pour maintenir la signature de la méthode)
                
        Returns :
            La quantité de dés à jouer.
        """
        return np.random.randint(1, self.jeu.D + 1)
    
class StrategieAveugle(Strategie):
    """
    Stratégie dite aveugle pour le jeu Dice Battle.
    
    Attributs :
        jeu : Un objet du type Jeu.
    """
    
    def jouerTour(self, moi, autre):
        """
        Retourne le nombre de dés qui assure en moyenne un nombre de points
        maximum. Comme montré au rapport, cela revient a retourne le minimum 
        entre 6 et D (la quantité maximale de dés à jouer).
        Ancienne EsperanceDes(D).
        
        Args : 
            moi : Score du joueur avec la stratégie courante.   
            autre : Score de l'autre joueur.
            (Ces arguments ne sont pas utilisés dans cette classe mais sont 
            nécessaires pour maintenir la signature de la méthode)
                
        Returns :
            La quantité de dés à jouer.
        """
        return min(6, self.jeu.D)
    
class StrategieOptimaleSequentielle(Strategie):
    """
    Stratégie optimale pour la variante séquentielle du jeu Dice Battle.
    
    Attributs :
        jeu : Un objet du type Jeu.
        OPT : Tableau contenant les choix optimaux de dés pour toute 
            quantité de points possible.         
    """
    
    def __init__(self, jeu):
        """
        Crée une stratégie avec le jeu passé en argument.
        Initialise le tableau OPT qui garde la quantité optimale de dés à 
        jouer pour chaque quantité possible de points des joueurs 1 et 2, 
        en considérant que la stratégie est le joueur 1 et que le joueur 2 joue
        aussi de façon optimale. 
        
        Args : 
            jeu : Un objet du type Jeu.
        """
        super().__init__(jeu)
        _, self.OPT = self._esperanceGain()
        
    def _esperanceGain(self):
        """
        Calcule les tableaux contenant les espérances de gain EG(i,j) et les 
        choix optimaux OPT(i,j). Le tableau EG n'est pas retourné.
        
        Returns : 
            OPT : Le tableau des choix optimaux.
        """
        N = self.jeu.N
        D = self.jeu.D
        EG = np.full((N + 6 * D, N + 6 * D), np.nan)
        OPT = np.zeros((N, N), dtype = int)
        
        #remplissage des cas de base de l'esperance :
        EG[N: , :N] = 1
        EG[:N, N: ] = -1
        
        for x in range(N - 1, -1, -1):
            for y in range(x, -1, -1):
                for i, j in {(x, y), (y, x)}:
                    #tableau des esperances pour chaque quantité de dés 
                    #possible :
                    ed = - self.jeu.probas[ :, 1: ].dot(\
                                          EG[j, (i + 1):(i + 6 * D + 1)])
                    OPT[i, j] = ed[1: ].argmax() + 1
                    EG[i, j] =  ed[OPT[i, j]]
        return EG, OPT
    
    def jouerTour(self, moi, autre):
        """
        Retourne le nombre de dés à jouer optimaux considérant les scores des
        joueurs. La méthode ne fait que consulter le tableau OPT dans la case 
        correspondante aux nombres des points des deux joueurs et retourne le 
        nombre de dés correspondant.
        
        Args : 
            moi : Score du joueur avec la stratégie courante.   
            autre : Score de l'autre joueur.
       
        Returns :
            La quantité de dés à jouer.
        """
        return self.OPT[moi, autre]
    
class StrategieHumaine(Strategie):
    """
    Stratégie qui permet à un humain de jouer au jeu Dice Battle.
    
    Attributs :
        jeu : Un objet du type Jeu.
    """
    def jouerTour(self, moi, autre):
        """
        Retourne le nombre de dés choisi par le joueur.
        
         Args : 
            moi : Score du joueur avec la stratégie courante.   
            autre : Score de l'autre joueur.
            (Ces arguments ne sont pas utilisés dans cette classe mais sont 
            nécessaires pour maintenir la signature de la méthode)
       
        Returns :
            La quantité de dés à jouer.
        """
        des = input("Choisissez la quantité de dés : ")
        return int(des)


class StrategieOptimaleSimultaneeTour(Strategie):
    """
    Stratégie optimale pour la variante simultanée du jeu Dice Battle avec un
    seul tour.
    
    Attributs :
        jeu : Un objet du type Jeu.
        _EG1 : Tableau avec l'espérance de gain du joueur 1 lorsqu’il a 
            jeté d1 dés et le joueur 2 a jeté d2 dés.
        _strategie : Le vecteur de probabilités optimales pour toutes 
            possibilités de dés entre 1 et D (quantité maximale de dés).
    """

    def __init__(self, jeu):
        """
        Crée une stratégie avec le jeu passé en argument.
        Initialise le tableau _EG1 qui garde l'espérance de gain du joueur 1 
        lorsqu’il a jeté d1 dés et le joueur 2 a jeté d2 dés.
        Initialise le tableau _strategie qui garde le vecteur de probabilités
        optimales pour toutes possibilités de dés entre 1 et D (quantité 
        maximale de dés).
        
        Args : 
            jeu : Un objet du type Jeu.
        """ 
        super().__init__(jeu)
        self._EG1 = self._esperanceGainPremier()
        _, self._strategie = ResolutionPL.resoudrePL(self._EG1)

    def _esperanceGainPremier(self):
        """
        Calcule le tableau EG1 des espérances de gain du joueur 1 lorsqu’il a 
        jeté d1 dés et le joueur 2 a jeté d2 dés.
        
        Returns :
            EG1 : Tableau avec l'espérance de gain du joueur 1 lorsqu’il a jeté
            d1 dés et le joueur 2 a jeté d2 dés.
        """
        D = self.jeu.D
        probas = self.jeu.probas

        EG1 = np.zeros((D + 1, D + 1))
        EG1[1:, 0] = 1
        EG1[0, 1:] = -1
        for d1 in range(1, D + 1):
            for d2 in range(1, D + 1):
                for j in range(1, 6 * d2 + 1):
                    EG1[d1, d2] += probas[d2, j] * \
                    np.sum(probas[d1, j + 1:6 * d1 + 1])
                for i in range(1, 6 * d1 + 1):
                    EG1[d1, d2] -= probas[d1, i] * \
                    np.sum(probas[d2, i + 1:6 * d2 + 1])
        return EG1
    
    def jouerTour(self, moi, autre):
        """
        Retourne le nombre de dés à jouer selon le vecteur de probabilités 
        optimal calculé à partir des espérances en considérant que l'autre 
        joueur joue de façon optimale aussi. La méthode ne fait que tirer une 
        quantité de dés de façon aléatoire en utilisant le vecteur.
        
        Args : 
            moi : Score du joueur avec la stratégie courante.   
            autre : Score de l'autre joueur.
            (Ces arguments ne sont pas utilisés dans cette classe mais sont 
            nécessaires pour maintenir la signature de la méthode)
       
        Returns :
            La quantité de dés à jouer.
        """
        return np.random.choice(self.jeu.D + 1, p = self._strategie)

class StrategieOptimaleSimultanee(Strategie):
    """
    Stratégie optimale pour la variante simultanée du jeu Dice Battle.
    
    Attributs :
        jeu : Un objet du type Jeu.
        OPT : Un tableau numpy 3D qui stocke les vecteurs de probabilités 
        optimales pour toute quantité de points possible.
    """
    def __init__(self, jeu):
        """
        Crée une stratégie avec le jeu passé en argument.
        Initialise le tableau OPT qui garde les vecteurs de probabilités
        optimales pour toute quantité de points possible.
        
        Args : 
            jeu : Un objet du type Jeu.
        """
        super().__init__(jeu)
        _, self.OPT = self._esperanceGain()
        
    def _esperanceGain(self):
        """
        Calcule le tableau EG(i, j) des espérances de gain du joueur 1 
        lorsqu’il a i points et le joueur 2 à j points et le tableau opt qui
        garde les vecteurs de probabilités optimales pour chaque esperance.

        Returns :
            EG : Tableau avec l'espérance de gain du joueur 1.
            opt : Un tableau numpy 3D qui stocke les vecteurs de probabilités 
            optimales pour toute quantité de points possible.
        """
        N = self.jeu.N
        D = self.jeu.D
        EG = np.full((N + 6 * D, N + 6 * D), np.nan)
        #EG = np.zeros((n + 6 * d, n + 6 * d))
        opt = np.zeros((N, N, D + 1))
        
        #remplissage des cas de base de l'esperance
        EG[N: , :N] = 1
        EG[:N, N: ] = -1
        EG[N:, N:] = 0
        sliceEG = EG[N:, N:]
        sliceEG[np.tril_indices(6*D)] = 1
        sliceEG[np.triu_indices(6*D)] += -1
        
        for x in range(N - 1, -1, -1):
            for y in range(N - 1, -1, -1):
                E1 = self._calculE1(EG \
                                [x + 1 : x + 6 * D + 1, y + 1 : y + 6 * D + 1])
                EG[x, y], opt[x, y, :] = ResolutionPL.resoudrePL(E1)
                # À cause d'erreurs numériques, il se peut que la probabilité
                # retournée contienne des nombres négatifs petits ou des 
                # nombres légèrement plus grands que 1.
                opt[x, y, :] = np.minimum(np.maximum(opt[x, y, :], 0), 1)
                opt[x, y, :] /= opt[x, y, :].sum()
        return EG, opt
    
    def _calculE1(self, sliceEG):
        """
        Calcule le tableau des espérances de gain du joueur 1 E1(d1, d2) quand 
        il joue d1 dés et le joueur 2 joue d2 dés et le jeu est à un score fixé
        au préalable.
        
        Args :
            sliceEG : le tableau des espérances de gain du joueur 1 lorsque lui 
                et le joueur 2 ont une quantité fixe de points.
            
        Returns :
            E1 : tableau des espérances de gain du joueur 1 quand il joue d1 
            dés et le joueur 2 joue d2 dés et le jeu est à un score fixé au 
            préalable.
        """
        D = self.jeu.D
        E1 = np.zeros((D + 1, D + 1))
        #les valeurs de la 1ère ligne et 1ère colonne ne sont pas importantes.
        for d1 in range(1, D + 1):
            for d2 in range(1, D + 1):
                E1[d1, d2] = self.jeu.probas[d1, 1:].dot( \
                  sliceEG.dot(self.jeu.probas[d2, 1:]))
        return E1
    
    def jouerTour(self, moi, autre):
        """
        Retourne le nombre de dés à jouer selon le vecteur de probabilités 
        optimal calculé à partir des espérances en considérant que l'autre 
        joueur joue de façon optimale aussi et que leu jeu est a une quantité 
        (i, j) de points. La méthode ne fait que tirer une quantité de dés de 
        façon aléatoire en utilisant le vecteur.
        
        Args : 
            moi : Score du joueur avec la stratégie courante.   
            autre : Score de l'autre joueur.
        Returns :
            La quantité de dés à jouer.
        """
        return np.random.choice(self.jeu.D + 1, p = self.OPT[moi, autre, :])
        
class ResolutionPL:
    """
    Classe utilisée pour la résolution des programmes linéaires présents dans 
    les stratégies pour le jeu Dice Battle.
    """
    def _matriceContrainte(EG, D):
        """
        Produit la matrice de contraintes du programme linéaire d'après la 
        matrice EG et le nombre de contraintes D.
        
        Args : 
            EG : Matrice 2D avec les valeurs d'une partie de la matrice de 
                contraintes.
            D : Quantité de contraintes provenues de EG.
            
        Returns : 
            La matrice de contraintes mres.
        """
        mres = np.zeros((D + 2, D + 2))
        mres[:-2, 0] = 1
        mres[:-2, 1] = -1
        mres[-2, 2:] = 1
        mres[-1, 2:] = -1
        mres[:D, 2:] = -EG[1:, 1:].transpose()
        return mres
    
    @classmethod
    def resoudrePL(cls, EG):
        """
        Résoudre le programme linéaire crée d’après la matrice EG passée en 
        argument.
        
        Args :  
            EG : Matrice 2D avec les valeurs d'une partie de la matrice de 
                contraintes.
            
        Returns :
            la valeur optimale du programme linéaire crée et les valeurs 
            optimales pour les variables concernées.
        """
        D = EG.shape[0] - 1
        strategie_mixte = np.zeros(D + 1)

        A_ub = cls._matriceContrainte(EG, D)
        
        b_ub = np.zeros(D + 2)
        b_ub[-2] = 1.0
        b_ub[-1] = -1.0
        
        obj = np.zeros(D + 2)
        obj[0] = 1.0
        obj[1] = -1.0

        # linprog résoud un problème de minimisation, donc il faut changer
        # le signe de la fonction objectif.
        opt_res = linprog(-obj, method="revised simplex", \
                          A_ub = A_ub, b_ub = b_ub)
        # Attention, il faut une version récénte de scipy pour avoir la méthode
        # "revised simplex"
        strategie_mixte[1:] = opt_res.x[2:]

        # Comme on a changé le signe de la fonction objectif, il faut le
        # re-changer pour retourner la valeur optimale.
        return -opt_res.fun, strategie_mixte 
