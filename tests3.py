import numpy as np
from projet import Jeu, JeuSequentiel, StrategieAveugle, StrategieOptimaleSequentielle,\
    StrategieAleatoire, StrategieHumaine, JeuSimultanee, StrategieAveugleAdapte, StrategieOptimaleSimultaneeTour,\
    StrategieOptimaleSimultanee


if __name__ == "__main__":
    D = 2
    N = 10
    jeu = JeuSimultanee(D, N)
    stgAA = StrategieAveugleAdapte(jeu)
    stgOS = StrategieOptimaleSimultanee(jeu)
    jeu.setStrategies(stgOS, stgAA)
