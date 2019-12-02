# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 22:49:37 2019

@author: arian
"""
import numpy as np
import matplotlib.pyplot as plt

from tqdm import tqdm

from projet import JeuSequentiel, StrategieAveugle, StrategieOptimaleSequentielle,\
 StrategieAleatoire, StrategieHumaine

def EvaluationGainSequentiel(listeStrat, D, N, nbFois):
    """
    """
    jeu = JeuSequentiel(D, N)
    res = np.zeros((len(listeStrat), len(listeStrat)))
    strats = [S(jeu) for S in listeStrat]
    for i, s1 in enumerate(strats):
        for j, s2 in enumerate(strats):
            nbVic1, nbVic2, nbNul = jeu.comparerStrategies(s1, s2, nbFois)
            res[i, j] = (nbVic1 - nbVic2) / nbFois
    return res

def EvaluationVictoiresSequentielFonctionD(S1, S2, Dvect, N, nbFois):
    """
    """
    nbVic1 = np.zeros(Dvect.shape)
    nbVic2 = np.zeros(Dvect.shape)
    
    for i, D in enumerate(Dvect):
        jeu = JeuSequentiel(D, N)
        s1 = S1(jeu)
        s2 = S2(jeu)
        jeu.setStrategies(s1, s2)
        for _ in tqdm(range(nbFois)):
            jeu.jouer(verbose = False)
            if jeu.vainqueur() == 1:
                nbVic1[i] += 1
            else:
                nbVic2[i] += 1
            jeu._reset()
    return nbVic1, nbVic2

if __name__ == "__main__":
    D = 10
    N = 100
    nbFois = 1000000
    
    # EG1 = EvaluationGainSequentiel([StrategieAveugle, StrategieOptimaleSequentielle, StrategieAleatoire], D, N, nbFois)
    
#==============================================================================
#     jeu = JeuSequentiel(10, 100)
#     s = StrategieOptimaleSequentielle(jeu)
#     eg, opt = s._esperanceGain()
#     
#     fig, ax = plt.subplots()
#     egColors = ax.imshow(eg)
#     fig.colorbar(egColors)
#     
#     fig, ax = plt.subplots()
#     optColors = ax.imshow(opt)
#     fig.colorbar(optColors)
#==============================================================================
    
    nbVic1, nbVic2 = EvaluationVictoiresSequentielFonctionD(\
        StrategieOptimaleSequentielle, StrategieAveugle, np.arange(2, 15), 100, 100000)

#==============================================================================
#     
#     jeu = JeuSequentiel(D, N)
#     strategieAv = StrategieAveugle(jeu)
#     strategieO = StrategieOptimaleSequentielle(jeu)
#     strategieAlea = StrategieAleatoire(jeu)
#     strategieH = StrategieHumaine(jeu)
#     jeu.setStrategies(strategieH, strategieAlea)
#     jeu.jouer()
#==============================================================================
