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
from strategie import StrategieAveugle, StrategieOptimaleSequentielle,\
 StrategieAleatoire, StrategieHumaine, StrategieOptimaleSimultaneeTour,\
 StrategieOptimaleSimultanee

def EvaluationGainSequentiel(listeStrat, D, N, nbFois):
    """
    Calcule les gains moyens en nbFois jeux séquentiels entre les stratégies 
    listées dans listeStrat.
    
    Args :
        listeStrat : tableau avec les stratégies (pas encore initialisées) 
            qu'on veut tester.
        D : Nombre maximum de dés qu'un joueur peut lancer dans 1 tour du 
            jeu.
        N : Nombre de points à atteindre pour gagner une partie. 
        nbFois : Quantité de jeux joués pour remplir chaque case.

    Returns :
        Un tableau de taille listeStrat**2 où chaque case (i, j) représente le
        gain moyen en nbFois jeux de la stratégie listeStrat[i] contre la 
        stratégie listeStrat[j].
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
    Calcule les gains moyens en nbFois jeux simultanés entre les stratégies 
    listées dans listeStrat.
    
    Args :
        listeStrat : tableau avec les stratégies (pas encore initialisées) 
            qu'on veut tester.
        D : Nombre maximum de dés qu'un joueur peut lancer dans 1 tour du 
            jeu.
        N : Nombre de points à atteindre pour gagner une partie. 
        nbFois : Quantité de jeux joués pour remplir chaque case.

    Returns :
        Un tableau de taille listeStrat**2 où chaque case (i, j) représente le
        gain moyen en nbFois jeux de la stratégie listeStrat[i] contre la 
        stratégie listeStrat[j].
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
    Calcule deux tableaux avec le nombre de victoires du joueur 1 et du 
    joueur 2 avec des stratégies fixes et en variant D, le nombre maximum de 
    dés. On joue nbFois pour chaque case.
    
     Args :
        TypeJeu : le type de Jeu qu'on veut jouer (Simultané ou Séquentiel).
            Pas initialisé.
        S1 : Une stratégie. Pas initialisé.
        S2 : Une stratégie. Pas initialisé.
        Dvect : Tableau avec les nombres maximums de dés qu'un joueur peut 
            lancer dans 1 tour du jeu. Pour chaque case de Dvect, la fonction 
            joue nbFois fois.
        N : Nombre de points à atteindre pour gagner une partie. 
        nbFois : Quantité de jeux joués pour remplir chaque case.

    Returns :
        Un couple de tableaux de même taille que Dvect où chaque case i 
        représente la quantité de victoires en nbFois jeux de la stratégie S1 
        contre la stratégie S2. 
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
    Calcule deux tableaux avec le nombre de victoires du joueur 1 et du 
    joueur 2 avec des stratégies fixes et en variant N, le nombre de points à 
    atteindre pour gagner une partie. On joue nbFois pour chaque case.
    
     Args :
        TypeJeu : le type de Jeu qu'on veut jouer (Simultané ou Séquentiel).
            Pas initialisé.
        S1 : Une stratégie. Pas initialisé.
        S2 : Une stratégie. Pas initialisé.
        D : Nombre maximum de dés qu'un joueur peut lancer dans 1 tour du 
            jeu.
        Nvect : Tableau avec les nombres de points à atteindre pour gagner une 
            partie. Pour chaque case de Nvect, la fonction joue nbFois fois. 
        nbFois : Quantité de jeux joués pour remplir chaque case.

    Returns :
        Un couple de tableaux de même taille que Nvect où chaque case i 
        représente la quantité de victoires en nbFois jeux de la stratégie S1 
        contre la stratégie S2. 
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

if __name__=="__main__":
    D = 10
    N = 100
    jeu = JeuSimultane(D, N)
    strategieAv = StrategieAveugle(jeu)
    strategieO = StrategieOptimaleSequentielle(jeu)
    strategieAlea = StrategieAleatoire(jeu)
    strategieH = StrategieHumaine(jeu)
    strategieOST = StrategieOptimaleSimultaneeTour(jeu)
    strategieOS = StrategieOptimaleSimultanee(jeu)
    jeu.setStrategies(strategieOS, strategieH)
    jeu.jouer()