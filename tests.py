# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 22:49:37 2019

@author:Ariana Carnielli \\ Ivan Kachaikin
Tests pour le projet de MOGPL 2019-2020
"""
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({"pgf.texsystem": "pdflatex"})

from tqdm import tqdm

from jeu import JeuSequentiel, JeuSimultane
from strategie import StrategieAveugle, StrategieOptimaleSequentielle,\
 StrategieAleatoire, StrategieHumaine, StrategieOptimaleSimultaneeTour,\
 StrategieOptimaleSimultanee

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

# if __name__ == "__main__":
    # Calcul du gain dans le jeu séquentiel pour différentes stratégies
#    D = 10
#    N = 100
#    nbFois = 1000000
#    EG1 = EvaluationGainSequentiel([StrategieAveugle, StrategieOptimaleSequentielle, StrategieAleatoire], D, N, nbFois)
    
    # Visualisation des matrices d'espérance de gain et de la stratégie
    # optimale pour le jeu séquentiel
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
    
    # Simulation de deux stratégies en fonction de D à N fixé
#==============================================================================
#     nbVic1, nbVic2 = EvaluationVictoiresFonctionD(JeuSequentiel, \
#         StrategieOptimaleSequentielle, StrategieAveugle, np.arange(2, 15), 100, 100000)
#==============================================================================
#    data = np.load("VictoiresSequentielFonctionD.npz")
#    D = data["D"]
#    N = data["N"]
#    nbVic1 = data["nbVic1"]
#    nbVic2 = data["nbVic2"]
#    fig, ax = plt.subplots(figsize=(5, 5))
#    ax.grid(True)
#    ax.set_axisbelow(True)
#    ax.plot(D, (nbVic1 - nbVic2)/(nbVic1 + nbVic2))
#    ax.set_xlabel("D")
#    ax.set_ylabel("Gain du joueur 1")
#    ax.set_title("Gain à $N$ fixé en fonction de $D$")
#    ax.set_ylim([0, 0.25])
#    ax.set_yticks(np.linspace(0, 0.25, 6))
#    fig.show()
    
    # Simulation de deux stratégies en fonction de N à D fixé
#==============================================================================
#     nbVic1, nbVic2 = EvaluationVictoiresFonctionN(JeuSequentiel, \
#         StrategieOptimaleSequentielle, StrategieAveugle, 10, np.array([20, 50, 100, 200, 500, 1000, 2000]), 100000)
#==============================================================================
#    data = np.load("VictoiresSequentielFonctionN.npz")
#    D = data["D"]
#    N = data["N"]
#    nbVic1 = data["nbVic1"]
#    nbVic2 = data["nbVic2"]
#    fig, ax = plt.subplots(figsize=(5, 5))
#    ax.grid(True)
#    ax.set_axisbelow(True)
#    ax.plot(N, (nbVic1 - nbVic2)/(nbVic1 + nbVic2))
#    ax.set_xlabel("N")
#    ax.set_ylabel("Gain du joueur 1")
#    ax.set_title("Gain à $D$ fixé en fonction de $N$")
#    ax.set_ylim([0, 0.25])
#    ax.set_yticks(np.linspace(0, 0.25, 6))
#    ax.set_xscale("log")
#    ax.set_xticks(N)
#    fig.show()

    # Jeu simultané en un coup
    # Calcul des stratégies optimales pour différentes valeurs de D.

    # Calcul du gain dans le jeu simultané à un tour pour différentes stratégies
#==============================================================================
#     D = 10
#     N = 1
#     nbFois = 1000000
#     EG1 = EvaluationGainSimultane([StrategieAveugleAdapte, StrategieOptimaleSimultaneeTour, StrategieAleatoireAdapte], D, N, nbFois)
#==============================================================================

     # Simulation de deux stratégies en fonction de D à N fixé pour le jeu simultané
#    D = np.arange(2, 11)
#    N = 1
#    nbFois = 1000000
#    nbVic1, nbVic2 = EvaluationVictoiresFonctionD(JeuSimultanee, \
#        StrategieOptimaleSimultaneeTour, StrategieAveugleAdapte, D, N, nbFois)
#    np.savez("VictoiresSimultaneUnTourFonctionD", D = D, N = N, nbFois = nbFois, nbVic1 = nbVic1, nbVic2 = nbVic2)
#    data = np.load("VictoiresSimultaneUnTourFonctionD.npz")
#    D = data["D"]
#    N = data["N"]
#    nbFois = data["nbFois"]
#    nbVic1 = data["nbVic1"]
#    nbVic2 = data["nbVic2"]
#    
#    fig, ax = plt.subplots(figsize=(5, 5))
#    ax.grid(True)
#    ax.set_axisbelow(True)
#    ax.plot(D, (nbVic1 - nbVic2)/nbFois)
#    ax.set_xlabel("D")
#    ax.set_ylabel("Gain du joueur 1")
#    ax.set_title("Gain en fonction de $D$")
#    #ax.set_ylim([0, 0.25])
#    #ax.set_yticks(np.linspace(0, 0.25, 6))
#    fig.show()
#
#    fig, ax = plt.subplots(figsize = (5, 5))
#    ax.grid(True)
#    ax.set_axisbelow(True)
#    ax.plot(D, nbVic1/nbFois*100, label="Joueur 1")
#    ax.plot(D, nbVic2/nbFois*100, label="Joueur 2")
#    ax.plot(D, (nbFois - nbVic1 - nbVic2)/nbFois*100, label="Match nul")
#    ax.set_xlabel("D")
#    ax.set_ylabel("Pourcentage de victoire")
#    ax.set_title("Pourcentage de victoire en fonction de $D$")
#    ax.set_ylim([10, 50])
#    #ax.set_yticks(np.linspace(0, 0.25, 6))
#    ax.legend()
#    fig.show()
    
#    jeu = JeuSequentiel(10, 100)
#    s = StrategieOptimaleSimultanee(jeu)
#    eg, opt = s._esperanceGain()
#    
#    fig, ax = plt.subplots()
#    egColors = ax.imshow(eg)
#    fig.colorbar(egColors)

#==============================================================================
#     D = 10
#     N = 1
#     nbFois = 1000000
#     EG1 = EvaluationGainSimultane([StrategieAveugle, StrategieAleatoire, StrategieOptimaleSequentielle, StrategieOptimaleSimultanee], D, N, nbFois)
#     
# 
#==============================================================================
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
