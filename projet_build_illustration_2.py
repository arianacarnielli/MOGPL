# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 22:49:37 2019

@author: ivan
"""
import numpy as np
from projet import Jeu, JeuSequentiel, StrategieAveugle, StrategieOptimaleSequentielle,\
    StrategieAleatoire, StrategieHumaine, JeuSimultanee, StrategieAveugleAdapte, StrategieOptimaleSimultaneeTour
from matplotlib import pyplot as plt


if __name__ == "__main__":
    Dmin, Dmax, Dstep = 2, 22, 2
    N = 1
    S = 100000
    pourcent_match_nul, pourcent_gagner, pourcent_perdre = [], [], []
    for D in range(Dmin, Dmax, Dstep):
        jeu = JeuSimultanee(D, N)
        stgAA = StrategieAveugleAdapte(jeu)
        stgOST = StrategieOptimaleSimultaneeTour(jeu)
        jeu.setStrategies(stgOST, stgAA)
        pourcentage = jeu.comparerStrategiesPourcentage(S) * 100
        pourcent_match_nul.append(pourcentage[0])
        pourcent_gagner.append(pourcentage[1])
        pourcent_perdre.append(pourcentage[2])
    plt.plot(range(Dmin, Dmax, Dstep), pourcent_match_nul, 'k-', label='Match nul')
    plt.plot(range(Dmin, Dmax, Dstep), pourcent_gagner, 'r-', label='Joueur 1')
    plt.plot(range(Dmin, Dmax, Dstep), pourcent_perdre, 'b-', label='Joueur 2')
    plt.legend()
    plt.grid(True)
    plt.xlabel('D : nombre maximal de dés permis à lancer')
    plt.ylabel('Pourcentage de gagne')
    plt.xticks(range(Dmin, Dmax, Dstep))
    plt.show()
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

