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


class StrategieOptimaleSimultaneeTour(Strategie):

    def __init__(self, jeu):
        super().__init__(jeu)
        self._EG1 = self._esperanceGainPremier()
        self._strategie = ResolutionPL.resoudrePL(self._EG1)

    def _esperanceGainPremier(self):
        D = self.jeu.D
        probas = self.jeu.probas

        EG1 = np.zeros((D + 1, D + 1))
        EG1[1:, 0] = 1
        EG1[0, 1:] = -1
        for d1 in range(1, D + 1):
            for d2 in range(1, D + 1):
                for j in range(1, 6 * d2 + 1):
                    EG1[d1, d2] += probas[d2, j] * np.sum(probas[d1, j + 1:6 * d1 + 1])
                for i in range(1, 6 * d1 + 1):
                    EG1[d1, d2] -= probas[d1, i] * np.sum(probas[d2, i + 1:6 * d2 + 1])

        return EG1
    
    def jouerTour(self, moi, autre):
        return np.random.choice(self.jeu.D + 1, p = self._strategie)

class StrategieOptimaleSimultanee(Strategie):

    def __init__(self, jeu):
        super().__init__(jeu)
        _, self.opt = self._esperanceGain()
        
    def _esperanceGain(self):
        """
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
                E1 = self._calculE1(EG[x + 1 : x + 6 * D + 1, y + 1 : y + 6 * D + 1])
                EG[x, y], opt[x, y, :] = ResolutionPL.resoudrePL(E1)
                # À cause d'erreurs numériques, il se peut que la probabilité
                # retournée contienne des nombres négatifs petits ou des nombres
                # légèrement plus grands que 1.
                opt[x, y, :] = np.minimum(np.maximum(opt[x, y, :], 0), 1)
                opt[x, y, :] /= opt[x, y, :].sum()
        return EG, opt
    
    def _calculE1(self, sliceEG):
        """
        """
        D = self.jeu.D
        E1 = np.zeros((D + 1, D + 1))
        #les valeurs de la première ligne et la première colonne ne sont pas importantes
        for d1 in range(1, D + 1):
            for d2 in range(1, D + 1):
                E1[d1, d2] = self.jeu.probas[d1, 1:].dot(sliceEG.dot(self.jeu.probas[d2, 1:]))
        return E1
    
    def jouerTour(self, moi, autre):
        """
        """
        return np.random.choice(self.jeu.D + 1, p = self.opt[moi, autre, :])
        
class ResolutionPL:
    """
    """
    def _matriceContrainte(EG, D):
        """
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
        opt_res = linprog(-obj, method="revised simplex", A_ub = A_ub, b_ub = b_ub)
        # Attention, il faut une version récénte de scipy pour avoir la méthode
        # "revised simplex"
        strategie_mixte[1:] = opt_res.x[2:]

        # Comme on a changé le signe de la fonction objectif, il faut le
        # re-changer pour retourner la valeur optimale.
        return -opt_res.fun, strategie_mixte
