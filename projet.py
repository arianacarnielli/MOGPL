# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 00:19:27 2019

@author: arian
"""
import numpy as np

class Jeu:
    """
    """
    
    def __init__(self, D, N):
        """
        """
        self.D = D
        self.N = N
        self.probas = self._tableProba()
        
        self.joueur1 = 0
        self.joueur2 = 0
        
    def setStrategies(self, strategie1, strategie2):
        """
        """
        self.strategie1 = strategie1
        self.strategie2 = strategie2
        
    def jouer(self, verbose = True):
        """
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
                print("La partie est finie, le joueur", self.vainqueur(), "a gagné")
    
    def vainqueur(self):
        """
        """
        if self.joueur1 == self.joueur2 :
            return 0
        return 1 if self.joueur1 > self.joueur2 else 2
    
    def _estfini(self):
        """
        """
        return self.joueur1 >= self.N or self.joueur2 >= self.N
    
    def _tirageDes(self, d):
        """
        """
        res = np.random.randint(1, 7, d)
        if np.any(res == 1):
            return 1
        return res.sum()
        
    def _tour(self):
        pass

    def _tableProba(self):
        """
        D + 1 car pour avoir des indices de façon plus naturel on rajoute une 
        colonne 0 et une ligne 0. 
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
        proba[:, 2:] = q[:, 2:] * (5 / 6) ** np.arange(self.D + 1).reshape((self.D + 1, 1))
        return proba
    
class JeuSequentiel(Jeu):
    """
    """
    def __init__(self, D, N):
        super().__init__(D, N)
        self.joueurCourant = 1
        
    def _tour(self):
        """
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
    """

        
class Strategie:
    """
    """
    def __init__(self, jeu):
        self.jeu = jeu

    def jouerTour(self, moi, autre):
        """
        """
        pass

class StrategieAleatoire(Strategie):
    """
    """
    def jouerTour(self, moi, autre):
        """
        """
        return np.random.randint(1, self.jeu.D + 1)
    
class StrategieAveugle(Strategie):
    """
    """
    
    def jouerTour(self, moi, autre):
        """
        ancienne EsperanceDes(D).
        """
        return min(6, self.jeu.D)
    
class StrategieOptimaleSequentielle(Strategie):
    """
    """
    
    def __init__(self, jeu):
        super().__init__(jeu)
        _, self.opt = self._esperanceGain()
        
    def _esperanceGain(self):
        """
        """
        n = self.jeu.N
        d = self.jeu.D
        eg = np.full((n + 6 * d, n + 6 * d), np.nan)
        #eg = np.zeros((n + 6 * d, n + 6 * d))
        opt = np.zeros((n, n), dtype = int)
        
        #remplissage des cas de base de l'esperance
        eg[n: , :n] = 1
        eg[:n, n: ] = -1
        
        for x in range(n - 1, -1, -1):
            for y in range(x, -1, -1):
                for i, j in {(x, y), (y, x)}:
                    #tableau des esperances pour chaque quantité de dés possible :
                    ed = - self.jeu.probas[ :, 1: ].dot(eg[j, (i + 1):(i + 6 * d + 1)])
                    opt[i, j] = ed[1: ].argmax() + 1
                    eg[i, j] =  ed[opt[i, j]]
        return eg, opt
    
    def jouerTour(self, moi, autre):
        """
        """
        return self.opt[moi, autre]
    
class StrategieHumaine(Strategie):
    """
    """
    def jouerTour(self, moi, autre):
        """
        """
        des = input("Choisissez la quantité de dés : ")
        return int(des)
        
        
def EGunCoup(D):
    jeu = Jeu(D, 1)
    p = jeu.probas
    
    res = np.zeros((D, D))
    
    for d1 in range(D):
        for d2 in range(D):
            for j in range(1, (d2 + 1) * 6 + 1):
                res[d1, d2] += p[d2 + 1, j] * p[d1 + 1, j + 1 : (d1 + 1) * 6 + 1].sum()
            for i in range(1, (d1 + 1) * 6 + 1):
                res[d1, d2] -= p[d1 + 1, i] * p[d2 + 1, i + 1 : (d2 + 1) * 6 + 1].sum()
    return res
    
    
    