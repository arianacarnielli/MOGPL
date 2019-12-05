# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 18:28:00 2019

@author:Ariana Carnielli \\ Ivan Kachaikin
Interface graphique pour le projet de MOGPL 2019-2020
"""

import PySimpleGUI as sg  

from jeu import JeuSequentiel, JeuSimultane
from strategie import StrategieAveugle, StrategieOptimaleSequentielle,\
 StrategieAleatoire, StrategieHumaine, StrategieOptimaleSimultaneeTour,\
 StrategieOptimaleSimultanee

strats = {'Aléatoire': StrategieAleatoire,\
          'Aveugle': StrategieAveugle,\
          'Humaine': StrategieHumaine,\
          'Optimale Séq': StrategieOptimaleSequentielle,\
          'Optimale 1 tour': StrategieOptimaleSimultaneeTour,\
          'Optimale': StrategieOptimaleSimultanee}

sg.change_look_and_feel('BluePurple')

#Columns
col1 = [[sg.Text('N'), sg.Spin(values=[i for i in range(1, 1000)],\
                 initial_value = 100, size=(6, 1))],
        [sg.Text('Joueur 1')],
        [sg.InputOptionMenu(('Aléatoire', 'Aveugle', 'Humaine', 'Optimale Séq',\
                             'Optimale 1 tour', 'Optimale'))],
        [sg.Button('Jeu Simultané')]]
       
col2 = [[sg.Text('D'), sg.Spin(values=[i for i in range(1, 100)],\
                 initial_value = 10, size=(6, 1))],
        [sg.Text('Joueur 2')],
        [sg.InputOptionMenu(('Aléatoire', 'Aveugle', 'Humaine', 'Optimale Séq',\
                             'Optimale 1 tour', 'Optimale'))],
        [sg.Button('Jeu Séquentiel')]]
        
layout = [[sg.Column(col1, element_justification = 'center'), \
           sg.Column(col2, element_justification = 'center')]]  

win1 = sg.Window('Dice Battle', layout, finalize = True)  

win2_active = False 
 
while True:  
    ev1, vals1 = win1.Read(timeout=100)  
    if ev1 is None:  
        break  

    if ev1 == 'Jeu Simultané' and not win2_active:  
        win2_active = True
        jeu = JeuSimultane(vals1[2], vals1[0])
        if vals1[1] != 'Humaine' and vals1[3] != 'Humaine':   
            
            layout2 = [[sg.Text('Jeu :')], [sg.Output(size=(50, 20))]]  
            strat1 = strats[vals1[1]](jeu)
            strat2 = strats[vals1[3]](jeu)
            jeu.setStrategies(strat1, strat2)
            win1.Hide()
            win2 = sg.Window('Dice Battle', layout2, finalize = True)  
            jeu.jouer()
            
        elif vals1[1] == 'Humaine' and vals1[3] != 'Humaine':
            layout2 = [[sg.Text('Jeu :')], [sg.Output(size=(50, 20))]]
            strat2 = strats[vals1[3]](jeu)
            win1.Hide()
            win2 = sg.Window('Dice Battle', layout2, finalize = True) 
            
            #on recrée le jeu à la main, pas à pas :
            print ("La partie commence :")
            print("Joueur 1 | Joueur 2")

            while not jeu._estfini():
                layout3 = [[sg.Text('Joueur 1 :')],\
                        [sg.Spin(values=[i for i in range(1, jeu.D + 1)],\
                                initial_value = 1, size = (5, 1))],\
                        [sg.Button('jouer dés')]]
                win3 = sg.Window('Dés', layout3, finalize = True)
                while True:
                    ev3, vals3 = win3.Read(timeout=100)  
                    if ev3 is None:  
                        break  
                    if ev3 == 'jouer dés':
                        des1 = vals3[0]
                        win3.Close()
                        break
                if ev3 is None:
                    break
                des2 = strat2.jouerTour(jeu.joueur2, jeu.joueur1)
                
                jeu.joueur1 += jeu._tirageDes(des1)
                jeu.joueur2 += jeu._tirageDes(des2)
    
                print("{:8d} | {:8d}".format(jeu.joueur1, jeu.joueur2))
            if jeu.vainqueur() == 0:
                print("Match nul")    
            else:
                print("La partie est finie, le joueur", jeu.vainqueur(), \
                      "a gagné")
        elif vals1[1] != 'Humaine' and vals1[3] == 'Humaine':
            layout2 = [[sg.Text('Jeu :')], [sg.Output(size=(50, 20))]]
            strat1 = strats[vals1[1]](jeu)
            win1.Hide()
            win2 = sg.Window('Dice Battle', layout2, finalize = True) 
            
            #on recrée le jeu à la main, pas à pas :
            print ("La partie commence :")
            print("Joueur 1 | Joueur 2")
            
            while not jeu._estfini():
                layout3 = [[sg.Text('Joueur 2 :')],\
                        [sg.Spin(values=[i for i in range(1, jeu.D + 1)],\
                                initial_value = 1, size = (5, 1))],\
                        [sg.Button('jouer dés')]]
                win3 = sg.Window('Dés', layout3, finalize = True)
                while True:
                    ev3, vals3 = win3.Read(timeout=100)  
                    if ev3 is None:  
                        break  
                    if ev3 == 'jouer dés':
                        des2 = vals3[0]
                        win3.Close()
                        break
                if ev3 is None:
                    break
                des1 = strat1.jouerTour(jeu.joueur1, jeu.joueur2)
                
                jeu.joueur1 += jeu._tirageDes(des1)
                jeu.joueur2 += jeu._tirageDes(des2)
    
                print("{:8d} | {:8d}".format(jeu.joueur1, jeu.joueur2))
            if jeu.vainqueur() == 0:
                print("Match nul")    
            else:
                print("La partie est finie, le joueur", jeu.vainqueur(), \
                      "a gagné")
        else:
            layout2 = [[sg.Text('Jeu :')], [sg.Output(size=(50, 20))]]
            win1.Hide()
            win2 = sg.Window('Dice Battle', layout2, finalize = True) 
            
            #on recrée le jeu à la main, pas à pas :
            print ("La partie commence :")
            print("Joueur 1 | Joueur 2")
            
            while not jeu._estfini():
                layout3 = [[sg.Text('Joueur 1 :')],\
                        [sg.Spin(values=[i for i in range(1, jeu.D + 1)],\
                                initial_value = 1, size = (5, 1))],\
                        [sg.Button('jouer dés')]]
                win3 = sg.Window('Dés', layout3, finalize = True)
                while True:
                    ev3, vals3 = win3.Read(timeout=100)  
                    if ev3 is None:  
                        break  
                    if ev3 == 'jouer dés':
                        des1 = vals3[0]
                        win3.Close()
                        break
                if ev3 is None:  
                    break  
                layout3 = [[sg.Text('Joueur 2 :')],\
                        [sg.Spin(values=[i for i in range(1, jeu.D + 1)],\
                                initial_value = 1, size = (5, 1))],\
                        [sg.Button('jouer dés')]]
                win3 = sg.Window('Dés', layout3, finalize = True)
                while True:
                    ev3, vals3 = win3.Read(timeout=100)  
                    if ev3 is None:  
                        break  
                    if ev3 == 'jouer dés':
                        des2 = vals3[0]
                        win3.Close()
                        break
                if ev3 is None:  
                    break  
                jeu.joueur1 += jeu._tirageDes(des1)
                jeu.joueur2 += jeu._tirageDes(des2)
    
                print("{:8d} | {:8d}".format(jeu.joueur1, jeu.joueur2))
            if jeu.vainqueur() == 0:
                print("Match nul")    
            else:
                print("La partie est finie, le joueur", jeu.vainqueur(), \
                      "a gagné")
        while True:  
            ev2, vals2 = win2.Read()  
            if ev2 is None or ev2 == 'Exit':  
                win2.Close()  
                win2_active = False  
                win1.UnHide()  
                break
            
    elif ev1 == 'Jeu Séquentiel' and not win2_active:  
        win2_active = True  
        jeu = JeuSequentiel(vals1[2], vals1[0])
        if vals1[1] != 'Humaine' and vals1[3] != 'Humaine':   
            layout2 = [[sg.Text('Jeu :')], [sg.Output(size=(50, 20))]]  
            strat1 = strats[vals1[1]](jeu)
            strat2 = strats[vals1[3]](jeu)
            jeu.setStrategies(strat1, strat2)
            win1.Hide()  
            win2 = sg.Window('Dice Battle', layout2, finalize = True)  
            jeu.jouer()
         
        elif vals1[1] == 'Humaine' and vals1[3] != 'Humaine':
            layout2 = [[sg.Text('Jeu :')], [sg.Output(size=(50, 20))]]
            strat2 = strats[vals1[3]](jeu)
            win1.Hide()
            win2 = sg.Window('Dice Battle', layout2, finalize = True) 
            
            #on recrée le jeu à la main, pas à pas :
            print ("La partie commence :")
            print("Joueur 1 | Joueur 2")
            joueurCourant = 1
            
            while not jeu._estfini():
                if joueurCourant == 1:
                    layout3 = [[sg.Text('Joueur 1 :')],\
                            [sg.Spin(values=[i for i in range(1, jeu.D + 1)],\
                                    initial_value = 1, size = (5, 1))],\
                            [sg.Button('jouer dés')]]
                    win3 = sg.Window('Dés', layout3, finalize = True)
                    while True:
                        ev3, vals3 = win3.Read(timeout=100)  
                        if ev3 is None:  
                            break  
                        if ev3 == 'jouer dés':
                            des1 = vals3[0]
                            win3.Close()
                            joueurCourant = 2
                            break
                    if ev3 is None:  
                        break  
                    jeu.joueur1 += jeu._tirageDes(des1)
                    print("Le joueur 1 joue :")
                    print("{:8d} | {:8d}".format(jeu.joueur1, jeu.joueur2))
                else:
                    des2 = strat2.jouerTour(jeu.joueur2, jeu.joueur1)
                    jeu.joueur2 += jeu._tirageDes(des2)
                    print("Le joueur 2 joue :")
                    print("{:8d} | {:8d}".format(jeu.joueur1, jeu.joueur2))
                    joueurCourant = 1
                
            if jeu.vainqueur() == 0:
                print("Match nul")    
            else:
                print("La partie est finie, le joueur", jeu.vainqueur(), \
                      "a gagné")
        elif vals1[1] != 'Humaine' and vals1[3] == 'Humaine':
            layout2 = [[sg.Text('Jeu :')], [sg.Output(size=(50, 20))]]
            strat1 = strats[vals1[1]](jeu)
            win1.Hide()
            win2 = sg.Window('Dice Battle', layout2, finalize = True) 
            
            #on recrée le jeu à la main, pas à pas :
            print ("La partie commence :")
            print("Joueur 1 | Joueur 2")
            joueurCourant = 1
            
            while not jeu._estfini():
                if joueurCourant == 1:
                    des1 = strat1.jouerTour(jeu.joueur1, jeu.joueur2)
                    jeu.joueur1 += jeu._tirageDes(des1)
                    joueurCourant = 2
                    print("Le joueur 1 joue :")
                    print("{:8d} | {:8d}".format(jeu.joueur1, jeu.joueur2))
                else:
                    layout3 = [[sg.Text('Joueur 2 :')],\
                            [sg.Spin(values=[i for i in range(1, jeu.D + 1)],\
                                    initial_value = 1, size = (5, 1))],\
                            [sg.Button('jouer dés')]]
                    win3 = sg.Window('Dés', layout3, finalize = True)
                    while True:
                        ev3, vals3 = win3.Read(timeout=100) 
                        if ev3 is None:  
                            break  
                        if ev3 == 'jouer dés':
                            des2 = vals3[0]
                            win3.Close()
                            joueurCourant = 1
                            break
                    if ev3 is None:  
                        break  
                    jeu.joueur2 += jeu._tirageDes(des2)
                    print("Le joueur 2 joue :")
                    print("{:8d} | {:8d}".format(jeu.joueur1, jeu.joueur2))
                
            if jeu.vainqueur() == 0:
                print("Match nul")    
            else:
                print("La partie est finie, le joueur", jeu.vainqueur(), \
                      "a gagné")
        else:
            layout2 = [[sg.Text('Jeu :')], [sg.Output(size=(50, 20))]]
            win1.Hide()
            win2 = sg.Window('Dice Battle', layout2, finalize = True) 
            
            #on recrée le jeu à la main, pas à pas :
            print ("La partie commence :")
            print("Joueur 1 | Joueur 2")
            joueurCourant = 1
            
            while not jeu._estfini():
                if joueurCourant == 1:
                    layout3 = [[sg.Text('Joueur 1 :')],\
                            [sg.Spin(values=[i for i in range(1, jeu.D + 1)],\
                                    initial_value = 1, size = (5, 1))],\
                            [sg.Button('jouer dés')]]
                    win3 = sg.Window('Dés', layout3, finalize = True)
                    while True:
                        ev3, vals3 = win3.Read(timeout=100)
                        if ev3 is None:  
                            break  
                        if ev3 == 'jouer dés':
                            des1 = vals3[0]
                            win3.Close()
                            break
                    joueurCourant = 2
                    if ev3 is None:  
                        break  
                    jeu.joueur1 += jeu._tirageDes(des1)
                    print("Le joueur 1 joue :")
                    print("{:8d} | {:8d}".format(jeu.joueur1, jeu.joueur2))
                else:
                    layout3 = [[sg.Text('Joueur 2 :')],\
                            [sg.Spin(values=[i for i in range(1, jeu.D + 1)],\
                                    initial_value = 1, size = (5, 1))],\
                            [sg.Button('jouer dés')]]
                    win3 = sg.Window('Dés', layout3, finalize = True)
                    while True:
                        ev3, vals3 = win3.Read(timeout=100)  
                        if ev3 is None:  
                            break  
                        if ev3 == 'jouer dés':
                            des2 = vals3[0]
                            win3.Close()
                            break
                    joueurCourant = 1
                    if ev3 is None:  
                        break
                    jeu.joueur2 += jeu._tirageDes(des2)
                    print("Le joueur 2 joue :")
                    print("{:8d} | {:8d}".format(jeu.joueur1, jeu.joueur2))

            if jeu.vainqueur() == 0:
                print("Match nul")    
            else:
                print("La partie est finie, le joueur", jeu.vainqueur(), \
                      "a gagné")     
        
        while True:  
            ev2, vals2 = win2.Read()  
            if ev2 is None or ev2 == 'Exit':  
                win2.Close()  
                win2_active = False  
                win1.UnHide()  
                break
        
win1.close()