# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 22:49:37 2019

@author: arian
"""
from projet import JeuSequentiel, StrategieAveugle, StrategieOptimaleSequentielle, StrategieAleatoire, StrategieHumaine


if __name__ == "__main__":
    D = 10
    N = 100
    jeu = JeuSequentiel(D, N)
    strategieAv = StrategieAveugle(jeu)
    strategieO = StrategieOptimaleSequentielle(jeu)
    strategieAlea = StrategieAleatoire(jeu)
    strategieH = StrategieHumaine(jeu)
    jeu.setStrategies(strategieH, strategieAlea)
    jeu.jouer()