# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 00:19:27 2019

@author: arian
"""
import numpy as np


class Jeu:
    """
    """
    
    def __init__(self, D, N, jeuType = "sequentielle"):
        """
        """
        self.D = D
        self.N = N
        self.jeuType = jeuType
        self.probas = self._tableProba()

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
    
class Strategie:
    """
    """
    def __init__(self, jeu):
        self.jeu = jeu

    def jouerTour(self):
        pass
    
class StrategieAveugle(Strategie):
    """
    """
    
    def jouerTour(self):
        """
        ancienne EsperanceDes(D).
        """
        d = np.arange(self.jeu.D + 1)
        esperance = 4 * d * (5 / 6) ** d + 1 - (5 / 6) ** d 
        return esperance.argmax()
    
class StrategieOptimaleSequentielle(Strategie):
    """
    """
    
    def esperanceGain(self):
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
        
    
    
    
    
    