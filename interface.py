# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 18:28:00 2019

@author: arian
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
            
            layout2 = [[sg.Text('Jeu :')], [sg.Output(size=(88, 20))]]  
            strat1 = strats[vals1[1]](jeu)
            strat2 = strats[vals1[3]](jeu)
            jeu.setStrategies(strat1, strat2)
            win1.Hide()
            win2 = sg.Window('Dice Battle', layout2, finalize = True)  
            jeu.jouer()
        elif vals1[1] == 'Humaine' and vals1[3] != 'Humaine':
            layout2 = [[sg.Text('Jeu :')], [sg.Output(size=(88, 20))], \
                        [sg.Spin(values=[i for i in range(1, jeu.D + 1)])]]
            
            strat2 = strats[vals1[3]](jeu)
            strat2 = strats[vals1[3]](jeu)
            jeu.setStrategies(strat1, strat2)
            win1.Hide()
            win2 = sg.Window('Dice Battle', layout2, finalize = True)  
            jeu.jouer()
            
        while True:  
            ev2, vals2 = win2.Read()  
            if ev2 is None or ev2 == 'Exit':  
                win2.Close()  
                win2_active = False  
                win1.UnHide()  
                break
            
    elif ev1 == 'Jeu Séquentiel' and not win2_active:  
        win2_active = True  
        layout2 = [[sg.Text('Jeu :')], [sg.Output(size=(88, 20))]]  
        jeu = JeuSequentiel(vals1[2], vals1[0])
        strat1 = strats[vals1[1]](jeu)
        strat2 = strats[vals1[3]](jeu)
        jeu.setStrategies(strat1, strat2)
        win1.Hide()  
        win2 = sg.Window('Dice Battle', layout2, finalize = True)  
        jeu.jouer()
        
        while True:  
            ev2, vals2 = win2.Read()  
            if ev2 is None or ev2 == 'Exit':  
                win2.Close()  
                win2_active = False  
                win1.UnHide()  
                break
win1.close()