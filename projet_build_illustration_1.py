import numpy as np
import matplotlib.pyplot as plt


if __name__ == '__main__':
    Dmin, Dmax, Dstep = 2, 22, 4
    D = np.arange(Dmin, Dmax, Dstep)
    pourcent_match_nul = np.array([15.717, 36.323, 36.062, 36.492, 36.297])
    pourcent_gagner = np.array([42.182, 32.559, 32.431, 32.597, 32.51])
    pourcent_perdre = np.array([42.101, 31.118, 31.507, 30.911, 31.193])

    plt.plot(D, pourcent_match_nul, 'k-', label='Match nul')
    plt.plot(D, pourcent_gagner, 'r-', label='Joueur 1')
    plt.plot(D, pourcent_perdre, 'b-', label='Joueur 2')
    plt.legend()
    plt.grid(True)
    plt.xlabel('D : nombre maximal de dés permis à lancer')
    plt.ylabel('Pourcentage de gagne')
    plt.xticks(D)
    plt.show()
