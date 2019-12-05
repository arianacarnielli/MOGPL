# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 19:40:25 2019

@author:Ariana Carnielli \\ Ivan Kachaikin
Fonctions de test pour le projet de MOGPL 2019-2020
"""

import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({"pgf.texsystem": "pdflatex"})

from tqdm import tqdm
from jeu import JeuSequentiel, JeuSimultane

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

def EvaluationGainSimultane(listeStrat, D, N, nbFois):
    """
    """
    jeu = JeuSimultane(D, N)
    res = np.zeros((len(listeStrat), len(listeStrat)))
    strats = [S(jeu) for S in listeStrat]
    for i in range(len(strats)):
        for j in range(i+1):
            s1 = strats[i]
            s2 = strats[j]
            nbVic1, nbVic2, nbNul = jeu.comparerStrategies(s1, s2, nbFois)
            res[i, j] = (nbVic1 - nbVic2) / nbFois
    return res

def EvaluationVictoiresFonctionD(TypeJeu, S1, S2, Dvect, N, nbFois):
    """
    """
    nbVic1 = np.zeros(Dvect.shape)
    nbVic2 = np.zeros(Dvect.shape)
    
    for i, D in enumerate(Dvect):
        jeu = TypeJeu(D, N)
        s1 = S1(jeu)
        s2 = S2(jeu)
        jeu.setStrategies(s1, s2)
        for _ in tqdm(range(nbFois)):
            jeu.jouer(verbose = False)
            if jeu.vainqueur() == 1:
                nbVic1[i] += 1
            elif jeu.vainqueur() == 2:
                nbVic2[i] += 1
            jeu._reset()
    return nbVic1, nbVic2

def EvaluationVictoiresFonctionN(TypeJeu, S1, S2, D, Nvect, nbFois):
    """
    """
    nbVic1 = np.zeros(Nvect.shape)
    nbVic2 = np.zeros(Nvect.shape)
    
    for i, N in enumerate(Nvect):
        jeu = TypeJeu(D, N)
        s1 = S1(jeu)
        s2 = S2(jeu)
        jeu.setStrategies(s1, s2)
        for _ in tqdm(range(nbFois)):
            jeu.jouer(verbose = False)
            if jeu.vainqueur() == 1:
                nbVic1[i] += 1
            elif jeu.vainqueur() == 2:
                nbVic2[i] += 1
            jeu._reset()
    return nbVic1, nbVic2
