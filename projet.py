# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 00:19:27 2019

@author: arian
"""
import numpy as np


def tableProba(d):
    """
    d + 1 car pour avoir des indices de façon plus naturel on rajoute une 
    colonne 0 et une ligne 0. 
    """
    #on va d'abord calculer le tableau des Q(d, k) 
    #on initialise le tableau à 0
    q = np.zeros((d + 1, 6 * d + 1))
    #on initialise la ligne correspondant à d = 1
    q[1, 2:7] = 1 / 5
        
    #on rempli le tableau q avec les Q(d, k)
    for di in range(2, d + 1):
        for k in range(2 * di, 6 * di + 1):
            q[di, k] = q[di - 1, max(k - 6, 0) : k - 1].sum() / 5
    
    #on crée le tableau de probabilités P(d, k)
    proba = np.zeros((d + 1, 6 * d + 1))
    #la probabilité d'avoir k = 0 avec 0 dés est égale à 1
    proba[0, 0] = 1
    #on initialise la colonne correspondant à k = 1
    proba[1:, 1] = 1 - (5 / 6) ** np.arange(1, d + 1)
    #on fait P(d, k) = Q(d, k) * (5/6)**d pour k >= 2
    proba[:, 2:] = q[:, 2:] * (5 / 6) ** np.arange(d + 1).reshape((d + 1, 1))
    return proba

def esperanceDes(D):
    """
    """
    d = np.arange(D + 1)
    esperance = 4 * d * (5 / 6) ** d + 1 - (5 / 6) ** d 
    return esperance.argmax()

    
    
    
    
    
    