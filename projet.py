# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 00:19:27 2019

@author:Ariana Carnielli \\ Ivan Kachaikin
Méthodes pour le projet de MOGPL 2019-2020
"""
import numpy as np
from scipy.optimize import linprog
from tqdm import tqdm

eps = 1e-3

class Jeu:
    """
    Classe générale pour représenter le jeu Dice Battle.
    Contient des méthodes pour initialiser le jeu, définir les stratégies 
    utilisées pour chaque joueur, jouer une partie, donner le vainqueur, etc. 
    
    Attributs :
        D : Nombre maximum de dés qu'un joueur peut lancer dans 1 tour du jeu.
        N : Nombre de points à atteindre pour gagner une partie. 
        probas : Tableau qui stocke P(d, k), la probabilité qu'un joueur qui 
            lance d dés obtienne k points.
        joueur1 : score du premier joueur.
        joueur2 : score du deuxième joueur.
        strategie1 : stratégie utilisée pour lancer les dés du joueur 1.
        strategie2 : stratégie utilisée pour lancer les dés du joueur 2.
    """
    
    def __init__(self, D, N):
        """
        Crée un jeu avec les D et N passés en argument.
        Initialise le tableau probas qui stocke P(d, k), la probabilité qu'un
        joueur qui lance d dés obtienne k points.
        Initialise les scores des deux joueurs à zéro.
        
        Args :
            D : Nombre maximum de dés qu'un joueur peut lancer dans 1 tour du 
                jeu.
            N : Nombre de points à atteindre pour gagner une partie. 
        """
        self.D = D
        self.N = N
        self.probas = self._tableProba()
        
        self.joueur1 = 0
        self.joueur2 = 0

    def comparerStrategies(self, strategie1, strategie2, nbFois = 10000):
        """
        Joue nbFois parties avec les stratégies passées en argument et renvoie 
        des statistiques sur l'ensemble de parties.
        
        Args :
            strategie1 : Un objet du type Strategie.
            strategie2 : Un objet du type Strategie. Peut être le même que le 
                premier.
            nbFois : Quantité de parties à jouer.
        Returns :
            Un triplet formé par la quantité de victoires du joueur 1, la 
            quantité de victoires du joueur 2 et la quantité de parties nulles.
        """
        self.setStrategies(strategie1, strategie2)
        self._reset()
        nbVic1 = 0
        nbVic2 = 0
        nbNul = 0
        for _ in tqdm(range(nbFois)):
            self.jouer(verbose = False)
            if self.vainqueur() == 1:
                nbVic1 += 1
            elif self.vainqueur() == 2:
                nbVic2 += 1
            else:
                nbNul += 1
            self._reset()
        return nbVic1, nbVic2, nbNul
        
    def setStrategies(self, strategie1, strategie2):
        """
        Initialise les stratégies des deux joueurs. Ce méthode doit être 
        appelé avant de l'appel au méthode jouer. 
        
        Args : 
            strategie1 : Un objet du type Strategie.
            strategie2 : Un objet du type Strategie. Peut être le même que le 
                premier.
        """
        self.strategie1 = strategie1
        self.strategie2 = strategie2
        
    def jouer(self, verbose = True):
        """
        Joue une partie du jeu, avec les D et N passés à la création de l'objet
        et les stratégies initialisées par le méthode setStrategie.
        
        Args : 
            verbose (facultatif) : si True, affiche des messages a chaque étape
                du jeu montrant le déroulement de la partie et quel joueur à
                gagné.            
        """
        if verbose :
            print ("La partie commence :")
            print("Joueur 1 | Joueur 2")
        while not self._estfini() :
            self._tour()
            if verbose :
                print("{:8d} | {:8d}".format(self.joueur1, self.joueur2))
        if verbose :
            if self.vainqueur() == 0:
                print("Match nul")    
            else:
                print("La partie est finie, le joueur", self.vainqueur(), \
                      "a gagné")
    
    def vainqueur(self):
        """
        Retourne le numéro du joueur gagnant et zéro si match nul.
        
        Returns : 
            1 si le joueur 1 a gagné, 2 si le joueur 2 a gagné et 0 si match 
            nul.
        """
        if self.joueur1 == self.joueur2 :
            return 0
        return 1 if self.joueur1 > self.joueur2 else 2

    def _reset(self):
        """
        Réinitialise les scores des joueurs pour qu'une nouvelle partie puisse
        être jouée.        
        """
        self.joueur1 = 0
        self.joueur2 = 0
    
    def _estfini(self):
        """
        Détermine si la partie est finie.
        
        Returns :
            True si la partie est finie (un des joueurs a plus de N points),
            False sinon.
        """
        return self.joueur1 >= self.N or self.joueur2 >= self.N
    
    def _tirageDes(self, d):
        """
        Simule le lancer de d dés de 6 faces non pipés, avec la règle du jeu 
        qui ramène le résultat à 1 si au moins un des dés est tombé à 1.
        
        Args : 
            d : La quantité de dés à jouer.
        Returns : 
            La somme de d lancés. Si au moins un des lancés donne 1, 
            retourne 1.         
        """
        res = np.random.randint(1, 7, d)
        if np.any(res == 1):
            return 1
        return res.sum()
        
    def _tour(self):
        """
        Spécifié dans les classes filles.
        """
        pass

    def _tableProba(self):
        """
        Calcule le tableau des probabilités P(d, k), la probabilité qu'un 
        joueur qui lance d dés obtienne k points.
        Le tableau a pour taille (D + 1) x (6D + 1) car pour avoir des indices 
        plus naturels on rajoute une colonne 0 et une ligne 0. 
        
        Returns : 
            Tableau des probabilités P(d, k).
        """
        #on va d'abord calculer le tableau des Q(d, k) 
        #on initialise le tableau à 0
        q = np.zeros((self.D + 1, 6 * self.D + 1))
        #on initialise la ligne correspondant à d = 1
        q[1, 2:7] = 1 / 5
            
        #on rempli le tableau q avec les Q(d, k)
        for di in range(2, self.D + 1):
            for k in range(2 * di, 6 * di + 1):
                q[di, k] = q[di - 1, max(k - 6, 0) : k - 1].sum() / 5
        
        #on crée le tableau de probabilités P(d, k)
        proba = np.zeros((self.D + 1, 6 * self.D + 1))
        #la probabilité d'avoir k = 0 avec 0 dés est égale à 1
        proba[0, 0] = 1
        #on initialise la colonne correspondant à k = 1
        proba[1:, 1] = 1 - (5 / 6) ** np.arange(1, self.D + 1)
        #on fait P(d, k) = Q(d, k) * (5/6)**d pour k >= 2
        proba[:, 2:] = q[:, 2:] * (5 / 6) ** \
            np.arange(self.D + 1).reshape((self.D + 1, 1))
        return proba
    
class JeuSequentiel(Jeu):
    """
    Classe pour représenter la version séquentielle du jeu Dice Battle.
    Contient des méthodes spécifiques pour jouer un tour du jeu, initialiser et
    réinitialiser l'attribut joueurCourant.
    
    Attributs :
        D : Nombre maximum de dés qu'un joueur peut lancer dans 1 tour du jeu.
        N : Nombre de points à atteindre pour gagner une partie. 
        probas : Tableau qui stocke P(d, k), la probabilité qu'un joueur qui 
            lance d dés obtienne k points.
        joueur1 : score du premier joueur.
        joueur2 : score du deuxième joueur.
        strategie1 : stratégie utilisée pour lancer les dés du joueur 1.
        strategie2 : stratégie utilisée pour lancer les dés du joueur 2.
        joueurCourant : détermine de quel joueur est le tour.
    """
    def __init__(self, D, N):
        super().__init__(D, N)
        self.joueurCourant = 1

    def _reset(self):
        """
        """
        super()._reset()
        self.joueurCourant = 1
        
    def _tour(self):
        """
        """
        if self.joueurCourant == 1:
            des = self.strategie1.jouerTour(self.joueur1, self.joueur2)
            self.joueur1 += self._tirageDes(des)
        else:
            des = self.strategie2.jouerTour(self.joueur2, self.joueur1)
            self.joueur2 += self._tirageDes(des)
        self.joueurCourant = 3 - self.joueurCourant

class JeuSimultanee(Jeu):
    """
    """
    def __init__(self, D, N):
        super().__init__(D, N)

    def _tour(self):
        """
        """
        des_proba = self.strategie1.jouerTour(self.joueur1, self.joueur2)[0]
        rand_val = np.random.rand()
        des = np.arange(self.D+1)[des_proba.cumsum() > rand_val][0]

        des_proba = self.strategie2.jouerTour(self.joueur2, self.joueur1)[1]

        self.joueur1 += self._tirageDes(des)

        rand_val = np.random.rand()
        des = np.arange(self.D+1)[des_proba.cumsum() > rand_val][0]
        self.joueur2 += self._tirageDes(des)

    def comparerStrategiesPourcentage(self, nbs=1000):
        """
        """
        res = np.array([0, 0, 0], dtype=int)
        for _ in tqdm(range(nbs)):
            self.joueur1 = 0
            self.joueur2 = 0
            while not self._estfini():
                self._tour()
            res[self.vainqueur()] += 1
        return res / nbs
        
class Strategie:
    """
    """
    def __init__(self, jeu):
        self.jeu = jeu

    def jouerTour(self, moi, autre):
        """
        """
        pass

class StrategieAleatoire(Strategie):
    """
    """
    def jouerTour(self, moi, autre):
        """
        """
        return np.random.randint(1, self.jeu.D + 1)
    
class StrategieAveugle(Strategie):
    """
    """
    
    def jouerTour(self, moi, autre):
        """
        ancienne EsperanceDes(D).
        """
        return min(6, self.jeu.D)
    
class StrategieOptimaleSequentielle(Strategie):
    """
    """
    
    def __init__(self, jeu):
        super().__init__(jeu)
        _, self.opt = self._esperanceGain()
        
    def _esperanceGain(self):
        """
        """
        n = self.jeu.N
        d = self.jeu.D
        eg = np.full((n + 6 * d, n + 6 * d), np.nan)
        #eg = np.zeros((n + 6 * d, n + 6 * d))
        opt = np.zeros((n, n), dtype = int)
        
        #remplissage des cas de base de l'esperance
        eg[n: , :n] = 1
        eg[:n, n: ] = -1
        
        for x in range(n - 1, -1, -1):
            for y in range(x, -1, -1):
                for i, j in {(x, y), (y, x)}:
                    #tableau des esperances pour chaque quantité de dés possible :
                    ed = - self.jeu.probas[ :, 1: ].dot(eg[j, (i + 1):(i + 6 * d + 1)])
                    opt[i, j] = ed[1: ].argmax() + 1
                    eg[i, j] =  ed[opt[i, j]]
        return eg, opt
    
    def jouerTour(self, moi, autre):
        """
        """
        return self.opt[moi, autre]
    
class StrategieHumaine(Strategie):
    """
    """
    def jouerTour(self, moi, autre):
        """
        """
        des = input("Choisissez la quantité de dés : ")
        return int(des)


class StrategieOptimaleSimultaneeTour(Strategie):

    def __init__(self, jeu):
        super().__init__(jeu)
        self._EG1 = self._esperanceGainPremier()
        self._strategies = self._calculerStrategies()

    def _esperanceGainPremier(self):
        D = self.jeu.D
        probas = self.jeu.probas.copy()
        EG1 = np.zeros((D + 1, D + 1))
        EG1[1:, 0] = 1
        EG1[0, 1:] = -1
        for d1 in range(1, D + 1):
            for d2 in range(1, D + 1):
                for j in range(1, 6 * d2 + 1):
                    EG1[d1, d2] += probas[d2, j] * np.sum(probas[d1, j + 1:6 * d1 + 1])
                for i in range(1, 6 * d1 + 1):
                    EG1[d1, d2] -= probas[d1, i] * np.sum(probas[d2, i + 1:6 * d2 + 1])

        return EG1

    def _matriceContraintePremier(self):
        D = self.jeu.D
        mres = np.zeros((D+2, D+2))
        for j in range(1, D+1):
            mres[j-1] = np.concatenate((
                [1.0, -1.0],
                -(self._EG1[:, j])[1:]
            ))
        mres[-2] = np.concatenate((
            [0.0, 0.0],
            np.ones(D)
        ))
        mres[-1] = -mres[-2].copy()

        return mres

    def _matriceContrainteDeuxieme(self):
        D = self.jeu.D
        mres = np.zeros((D+2, D+2))
        for i in range(1, D+1):
            mres[i-1] = np.concatenate((
                [-1.0, 1.0],
                self._EG1[i][1:]
            ))
        mres[-2] = np.concatenate((
            [0.0, 0.0],
            np.ones(D)
        ))
        mres[-1] = -mres[-2].copy()

        return mres

    def _calculerStrategies(self):
        D = self.jeu.D
        strategies = np.zeros((2, D+1))

        A_ub = self._matriceContraintePremier()

        b_ub = np.zeros(D+2)
        b_ub[-2] = 1.0
        b_ub[-1] = -1.0

        obj = np.zeros(D+2)
        obj[0] = 1.0
        obj[1] = -1.0

        opt_res = linprog(-obj, method='simplex', A_ub=A_ub, b_ub=b_ub)
        strategies[0, 1:] = opt_res.x[2:]

        A_ub = self._matriceContrainteDeuxieme()

        b_ub = np.zeros(D+2)
        b_ub[-2] = 1.0
        b_ub[-1] = -1.0

        obj = np.zeros(D+2)
        obj[0] = 1.0
        obj[1] = -1.0

        opt_res = linprog(obj, method='simplex', A_ub=A_ub, b_ub=b_ub)
        strategies[1, 1:] = opt_res.x[2:]

        return strategies

    def jouerTour(self, moi, autre):
        return self._strategies

class StrategieOptimaleSimultanee(Strategie):

    def __init__(self, jeu):
        super().__init__(jeu)
        self._EG1, self._strategies = self._esperanceGainPremierEtStrategies()

    def _matriceContraintePremier(self, E1_ij):
        D = self.jeu.D
        mres = np.zeros((D+2, D+2))
        for j in range(D):
            mres[j] = np.concatenate((
                [1.0, -1.0],
                -(E1_ij[:, j])
            ))
        mres[-2] = np.concatenate((
            [0.0, 0.0],
            np.ones(D)
        ))
        mres[-1] = -mres[-2].copy()

        return mres

    def _matriceContrainteDeuxieme(self, E1_ij):
        D = self.jeu.D
        mres = np.zeros((D+2, D+2))
        for i in range(D):
            mres[i] = np.concatenate((
                [-1.0, 1.0],
                E1_ij[i]
            ))
        mres[-2] = np.concatenate((
            [0.0, 0.0],
            np.ones(D)
        ))
        mres[-1] = -mres[-2].copy()

        return mres

    def _esperanceGainPremierEtStrategies(self):
        D, N = self.jeu.D, self.jeu.N
        EG1 = np.zeros((N - 1 + 6 * D + 1, N - 1 + 6 * D + 1))
        strategies = np.zeros((N - 1 + 6 * D + 1, N - 1 + 6 * D + 1, 2, D+1))
        strategies[:, :, :, 0] = 1.0
        probas = self.jeu.probas.copy()

        EG1[N:, :N] = 1
        EG1[:N, N:] = -1

        j, i = np.arange(6*D), np.arange(6*D)
        jj, ii = np.meshgrid(j, i)
        EG1[N:, N:][ii > jj] = 1
        EG1[N:, N:][ii < jj] = -1
        E1_ij = np.zeros((D, D))

        for i in tqdm(range(N-1, -1, -1)):
            for j in range(N-1, -1, -1):
                for d1 in range(1, D+1):
                    for d2 in range(1, D+1):
                        k, l = np.arange(1, 6*d1+1), np.arange(1, 6*d2+1)
                        kk, ll = np.meshgrid(k, l)
                        E1_ij[d1-1, d2-1] = np.sum(EG1[i+kk, j+ll] * probas[d1, kk] * probas[d2, ll])

                        # Pour vétifier qu'une expression NumPy est valide, on peut recalculer élément E1_ij[d1-1, d2-1]
                        # par boucles en décommentant le code ci-dessous
                        # s = 0.0
                        # for k1 in range(1, 6*d1+1):
                        #     for l1 in range(1, 6*d2+1):
                        #         s += _EG1[i + k1, j + l1] * probas[d1, k1] * probas[d2, l1]
                        # print(E1_ij[d1-1, d2-1] - s)

                A_ub = self._matriceContraintePremier(E1_ij)

                b_ub = np.zeros(D + 2)
                b_ub[-2] = 1.0
                b_ub[-1] = -1.0

                obj = np.zeros(D + 2)
                obj[0] = 1.0
                obj[1] = -1.0

                opt_res = linprog(-obj, method='simplex', A_ub=A_ub, b_ub=b_ub, options={'tol': eps})
                strategies[i, j, 0, 1:] = opt_res.x[2:]
                strategies[i, j, 0, 0] = 0.0

                A_ub = self._matriceContrainteDeuxieme(E1_ij)

                b_ub = np.zeros(D + 2)
                b_ub[-2] = 1.0
                b_ub[-1] = -1.0

                obj = np.zeros(D + 2)
                obj[0] = 1.0
                obj[1] = -1.0

                opt_res = linprog(obj, method='simplex', A_ub=A_ub, b_ub=b_ub, options={'tol': eps})
                strategies[i, j, 1, 1:] = opt_res.x[2:]
                strategies[i, j, 1, 0] = 0.0

                EG1[i, j] = np.dot(np.dot(strategies[i, j, 0, 1:], E1_ij), strategies[i, j, 1, 1:])

        return EG1, strategies

    def jouerTour(self, moi, autre):
        return np.concatenate((
            self._strategies[moi, autre, 0],
            self._strategies[autre, moi, 1]
        )).reshape(2, -1)

class StrategieAveugleAdapte(Strategie):
    """
    """

    def jouerTour(self, moi, autre):
        """
        """
        d = self.jeu.D if self.jeu.D <= 6 else 6
        strategie_mixte = np.zeros((2, self.jeu.D+1))
        strategie_mixte[:, d] = 1.0
        return strategie_mixte

class StrategieAleatoireAdapte(Strategie):
    """
    """

    def jouerTour(self, moi, autre):
        """
        """
        strategie = np.full(self.jeu.D + 1, 1 / self.jeu.D)
        strategie[0] = 0
        return strategie


def EGunCoup(D):
    """
    """
    jeu = Jeu(D, 1)
    p = jeu.probas

    res = np.zeros((D, D))

    for d1 in range(D):
        for d2 in range(D):
            for j in range(1, (d2 + 1) * 6 + 1):
                res[d1, d2] += p[d2 + 1, j] * p[d1 + 1, j + 1: (d1 + 1) * 6 + 1].sum()
            for i in range(1, (d1 + 1) * 6 + 1):
                res[d1, d2] -= p[d1 + 1, i] * p[d2 + 1, i + 1: (d2 + 1) * 6 + 1].sum()
    return res