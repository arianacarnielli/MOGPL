import numpy as np
from projet import JeuSimultanee, StrategieAveugleAdapte, StrategieOptimaleSimultanee, StrategieOptimaleSimultaneeTour
import matplotlib.pyplot as plt


if __name__ == '__main__':
    S = int(1e+5)
    Dmin, Dmax, Dstep = 2, 8, 2
    Nmin, Nmax, Nstep = 10, 40, 10
    pourcent_vict_diff = []
    for N in range(Nmin, Nmax, Nstep):
        pourcent_vict_diff.append([])
        for D in range(Dmin, Dmax, Dstep):
            jeu = JeuSimultanee(D, N)
            stgAA = StrategieAveugleAdapte(jeu)
            stgOS = StrategieOptimaleSimultanee(jeu)
            jeu.setStrategies(stgOS, stgAA)
            pourcentage = jeu.comparerStrategiesPourcentage(S)
            pourcent_vict_diff[-1].append(pourcentage[1] - pourcentage[2])
    pourcent_vict_diff = np.array(pourcent_vict_diff)
    print('Difference entre les pourcentage du joueur 1 et 2')
    print(pourcent_vict_diff)

    plt.figure(1)
    plt.contourf(np.arange(Dmin, Dmax, Dstep), np.arange(Nmin, Nmax, Nstep), pourcent_vict_diff,
                 levels=np.sort(pourcent_vict_diff.ravel()))
    plt.xticks(np.arange(Dmin, Dmax, Dstep))
    plt.yticks(np.arange(Nmin, Nmax, Nstep))
    plt.colorbar()

    plt.show()
