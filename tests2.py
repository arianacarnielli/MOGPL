# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 22:49:37 2019

@author: ivan
"""
import numpy as np
from projet import Jeu, JeuSequentiel, StrategieAveugle, StrategieOptimaleSequentielle,\
    StrategieAleatoire, StrategieHumaine, JeuSimultanee, StrategieAveugleAdapte, StrategieOptimaleSimultaneeTour


if __name__ == "__main__":
    D = 10
    N = 100
    jeu = JeuSimultanee(D, N)
    stgAA = StrategieAveugleAdapte(jeu)
    stgOST = StrategieOptimaleSimultaneeTour(jeu)
    jeu.setStrategies(stgOST, stgAA)
    print(stgOST.jouerTour(0, 0))
    jeu.jouer()
    print(jeu.comparerStrategiesPourcentage(100000) * 100)
    # jeu = Jeu(D, N)
    # probas = jeu.probas.copy()
    #
    # _EG1 = np.zeros((D+1, D+1))
    # _EG1[1:, 0] = 1
    # _EG1[0, 1:] = -1
    # for d1 in range(1, D+1):
    #     for d2 in range(1, D+1):
    #         for j in range(1, 6 * d2 + 1):
    #             _EG1[d1, d2] += probas[d2, j] * np.sum(probas[d1, j+1:6*d1+1])
    #         for i in range(1, 6 * d1 + 1):
    #             _EG1[d1, d2] -= probas[d1, i] * np.sum(probas[d2, i+1:6*d2+1])
    #
    # np.set_printoptions(precision=4)
    # print(_EG1)

