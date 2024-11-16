#!/usr/bin/python
# Rraspberry.link-tech.de/doku.php?d=mcp23017
# Haupt Menu/Manuel Control/ AND Einzellsteuerung
"""
"""

#import smbus
import time
#import os
#import sys
from tkinter import *
#from tkinter as tk
# Objekt der Klasse Tk erstellt und self.WinMasterüberschrift

#(in cfg) from Hardware import *

#?from tkinter import messagebox

from Meter import *

"""
    HW-Simulation
"""
sim_porta = 0
sim_portb = 0

tmp_vorgang_dauer = 19      #"01:00"
tmp_vorgang_countdown = -1  #0
tmp_countdown_mode = 0      # gestoppt

NOT_AUS = False

Condition_Auto = True  # ok

Kanal_Druck_Vorrat = 0

"""
    Ablauf-Steuerung
"""

"""
    automatische Funktionen / Vorgänge
"""
Vorgang_Inaktiv = 0
Vorgang_Sequenzel = 1
Vorgang_Wäsche = 2
Vorgang_Spuelung = 3
Vorgang_SpTrocknung = 4
Vorgang_WaWasserentleeren = 5
Vorgang_SpWasserentleeren = 6
Vorgang_Druckluft = 7

Vorgang = Vorgang_Inaktiv

Vorgang_Name = [
    "Inaktiv",      # = 0
    "Sequenzel",
    "Wäsche",
    "Spuelung",
    "SpTrocknung",
    "WaWasserentleeren",
    "SpWasserentleeren",
    "Druckluft "
]

#X Ablauf = 0
#-> Vorgang

Ablaufplan = []     #[1, 2, 3, 4, 5]    # (...)

#?Ablaufplan[1] = [
"""
Innenbeleuchtung;Wasser-Auslaßmotor;Wasser-Einlaßmotor;Trocknenluft-Motor;Wasser-Heizung;Trockenluft-Heizung;Druckluft-Einl.-Ventil;Wasser-Auslaß-Ventil;Wasser-Einlaß-Ventil;Trockenluft-Ventil;Euro-6-Ventil;Betriebsanzeige;Warnsignal;Waschwasser-Einlaß-Ventil;Spülwasser-Einlaß-Ventil;Waschwasser-Abpump-Motor
Port B, Bit                                 Port A, Bit                         
    7   6   5   4   3   2   1   0       0   1   2   3   4   5   6   7
    Innenbeleuchtung
                Wasser-Auslaßmotor
                        Wasser-Einlaßmotor
                                Trocknenluft-Motor
                                        Wasser-Heizung
                                                Trockenluft-Heizung
                                                        Druckluft-Einl.-Ventil
                                                                Wasser-Auslaß-Ventil
                                                                                Wasser-Einlaß-Ventil
                                                                                        Trockenluft-Ventil
                                                                                                Euro-6-Ventil
                                                                                                        Betriebsanzeige
                                                                                                                Warnsignal
                                                                                                                        Waschwasser-Einlaß-Ventil
                                                                                                                                Spülwasser-Einlaß-Ventil
                                                                                                                                        Waschwasser-Abpump-Motor
"""
#! Ablaufplan_Vorwäsche = [
    #Vorgang;Funktion;Text;Dauer;Wiederholung;Bedingung;Innenbeleuchtung;Wasser-Auslaßmotor;Wasser-Einlaßmotor;Trocknenluft-Motor;Wasser-Heizung;Trockenluft-Heizung;Druckluft-Einl.-Ventil;Wasser-Auslaß-Ventil;Wasser-Einlaß-Ventil;Trockenluft-Ventil;Euro-6-Ventil;Betriebsanzeige;Warnsignal;Waschwasser-Einlaß-Ventil;Spülwasser-Einlaß-Ventil;Waschwasser-Abpump-Motor
    #;;;;;;;;;;;;;;;;;;;;;
    #Vorwäsche;;;;;;;;;;;;;;;;;;;;;
"""
                                       Innenbeleuchtung
                                           | Wasser-Auslaßmotor
                                           |   Wasser-Einlaßmotor
                                           |     Trocknenluft-Motor
                                           |       Wasser-Heizung
                                           |         Trockenluft-Heizung
                                           |           Druckluft-Einl.-Ventil
                                           |             Wasser-Auslaß-Ventil
                                           |             | Wasser-Einlaß-Ventil
                                           |             |   Trockenluft-Ventil
                                           |             |     Euro-6-Ventil
                                           |             |       Betriebsanzeige
                                           |             |         Warnsignal
                                           |             |           Waschwasser-Einlaß-Ventil
                                           |             |             Spülwasser-Einlaß-Ventil
                                           |             |               Waschwasser-Abpump-Motor
                                           |             |               |
"""
    #Index: Sequenzel\nLuft Druck Wäsche
    #0                       1   2       3 4 5 6 7 8 9 10111213141516171819
    #                                      |Innenbeleuchtung             |Waschwasser-Abpump-Motor
Ablaufplan_Sequenzel = [  #Luftdruck Waäsche
#    "Start + Warnsignal OFF","", 0.5,    0,2,2,2,2,2,2,2,2,2,2,2,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2, #
    "Betriebsanzeige ON","", 0.5,        0,2,2,2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
                                         # (12) Wiederholungen:
    "Druckluft-In ON", "",       7,    4,2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2, #   Luft-Einlaß (neu: druckgeregelt)
    "Druckluft-In OFF",  "",     0.5,    0,2,2,2,2,2,2,2,2,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Druckluft Ventil ON","",    2,      0,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2, #   Luft-Auslaß
    "Druckluft Ventil OFF","",   0.5,    0,2,2,2,2,2,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,#
    "Wasser-Auslaßmotor XX","",  0.5,   -1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,     #   ???

    "Wasser-Auslaß-Ventil ON","",0.5,    0,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Wasser-Auslaßmotor ON","", 10,      0,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Wasser-Auslaßmotor OFF","", 0.5,    0,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Wasser-Auslaß-Ventil OFF","",0.5,   0,2,2,2,2,2,2,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,

    "Warnsignal","", 0,                  0,2,2,2,2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2

]
    #Index:
    #0                       1   2       3 4 5 6 7 8 9 10111213141516171819
    #                                      |Innenbeleuchtung             |Waschwasser-Abpump-Motor
Ablaufplan_Wäsche = [
# Start (Haupt Program Begin)
    "Start + Warnsignal OFF","",  0.5,  0,2,2,2,2,2,2,2,2,2,2,2,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2, #
    "Betriebsanzeige ON","",      0.5,  0,2,2,2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Wasser-Heizung ON","",       0.5,  0,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Wasser-Einlaß-Ventil ON","", 0.5,  0,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Wasser-Einlaßmotor ON","",  25,    0,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Wasser-Auslaß-Ventil ON","", 0.5,  0,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Wasser-Auslaßmotor ON","",   1,    0,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
# Start (Haupt Program Ende)
    
# Haupt Program Begin    
    "Druckluft Ventil ON",     "", 2, 180,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,   # 6= 1. Min   30 ist 5 Min
    "Druckluft Ventil OFF",  "", 0.5,   0,2,2,2,2,2,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Druckluft-In ON",         "", 7,   0,2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Drukluft-In OFF",        "",0.5,   0,2,2,2,2,2,2,2,2,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Wasser-Auslaßmotor ON","  ",0.5,  -1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
# Haupt Program Ende
    
# End Programm (Auslauf Begin)
    "Wasser-Einlaßpumpe OFF",  "", 1,   0,2,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Wasser-Einlaß-Ventil OFF", "",1,   0,2,2,2,2,2,2,2,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Druckluft-In ON",          "",7,   4,2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2, #   Luft-Einlaß (neu: druckgeregelt)
    "Druckluft-In OFF",        "", 0.5, 0,2,2,2,2,2,2,2,2,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Druckluft Ventil ON",     "", 2,   0,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2, #   Luft-Auslaß
    "Druckluft Ventil OFF",    "", 0.5, 0,2,2,2,2,2,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,#
    "Zürück zur Wiederholung", "", 0.5,-1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,     #   ???
    "Wasser-Auslaß-Ventil ON ", "",15,  0,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Wasser-Auslaß-Motor OFF",  "",0.5, 0,2,0,2,2,2,2,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Wasser-Auslaß-Ventil OFF", "",0.5, 0,2,2,2,2,2,2,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Warnsignal","", 0,                 0,2,2,2,2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2
# End Programm (Auslauf Ende)
]
"""
Ablaufplan_Spuelung = [
    
    "Betriebsanzeige ON",      "", 1,   0,2,2,2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Wasser-Heizung OFF",      "", 1,   0,2,2,2,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Wasser-Einlaßmotor ON",  "", 15,   0,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Wasser-Auslaßmotor ON",  "", 40,   0,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Wasser-Einlaßpumpe OFF", "", 10,   0,2,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Wasser-Auslaß-Motor OFF", "",1,    0,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,

    "Druckluft-In ON",          "",7,   4,2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2, #   Luft-Einlaß (neu: druckgeregelt)
    "Druckluft-In OFF",         "",1,   0,2,2,2,2,2,2,2,2,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Druckluft Ventil ON",      "",2,   0,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2, #   Luft-Auslaß
    "Druckluft Ventil OFF",     "",1,   0,2,2,2,2,2,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,#
    "Wasser-Auslaßmotor ON",    "",1,  -1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,     #   ???

    "Wasser-Auslaßmotor ON",   "",10,   0,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Wasser-Auslaßmotor OFF",  "", 1,   0,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Warnsignal",              "", 1,   0,2,2,2,2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2
]
"""

    #                                      |Innenbeleuchtung             |Waschwasser-Abpump-Motor
Ablaufplan_Spuelung = [
 #   "Start + Warnsignal OFF","", 0.5,    0,2,2,2,2,2,2,2,2,2,2,2,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2, #
    "Betriebsanzeige ON","",     0.5,  0,2,2,2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Wasser-Heizung OFF","",     1,    0,2,2,2,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Wasser-Einlaßmotor ON","", 15,    0,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,

    "Wasser-Auslaß-Ventil ON","", 0.5,  0,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    
    "Wasser-Auslaßmotor ON","", 40,    0,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Wasser-Einlaßpumpe OFF","",10,    0,2,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Wasser-Auslaß-Motor OFF","",1,    0,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
#    "Betriebsanzeige OFF",""   , 0.5,    0,2,2,2,2,2,2,2,2,2,2,2,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2, #
                                        # (3) Wiederholungen:
    "Druckluft-In ON", "",       7,    4,2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2, #   Luft-Einlaß (neu: druckgeregelt)
    "Druckluft-In OFF",  "",     0.5,  0,2,2,2,2,2,2,2,2,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Druckluft Ventil ON","",    2,    0,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2, #   Luft-Auslaß
    "Druckluft Ventil OFF","",   0.5,  0,2,2,2,2,2,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,#
    "Wasser-Auslaßmotor ON","",  0.5,- 1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,     #   ???

    "Wasser-Auslaßmotor ON","", 15,    0,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Wasser-Auslaßmotor OFF","", 0.5,  0,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,

    "Wasser-Auslaß-Ventil OFF","", 0.5,  0,2,2,2,2,2,2,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    
    "Warnsignal","", 0,                0,2,2,2,2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2
]


# Sequenzel luft Trocknung nach Spülung
Ablaufplan_SpTrocknung = [

    "Betriebsanzeige ON","", 0.5,        0,2,2,2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    # (12) Wiederholungen:
    "Druckluft-In ON", "",       7,     4,2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2, #   Luft-Einlaß (neu: druckgeregelt)
    "Druckluft-In OFF",  "",     0.5,    0,2,2,2,2,2,2,2,2,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Druckluft Ventil ON","",    2,      0,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2, #   Luft-Auslaß
    "Druckluft Ventil OFF","",   0.5,    0,2,2,2,2,2,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,#
    "Wasser-Auslaßmotor ON","",  0.5,   -1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,     #   ???
                                        # Ende Wiederholungs-Schleife
    "Wasser-Auslaß-Ventil ON","",0.5,    0,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Wasser-Auslaßmotor ON","",   10,    0,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Wasser-Auslaßmotor OFF","", 1,      0,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Wasser-Auslaß-Ventil OFF","", 1,    0,2,2,2,2,2,2,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Warnsignal","", 0,                  0,2,2,2,2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2
]

Ablaufplan_WaWasserentleeren = [
    "Start + Warnsignal OFF","", 0.5,    0,2,2,2,2,2,2,2,2,2,2,2,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2, #
#    "Wasser-Heizung ON ","", 1,          0,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Betriebsanzeige ON","", 0.5,        0,2,2,2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,  # Betriebsanzeige    ON  -12
    "Wasser-Auslaß-Ventil ON","", 1,     0,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Wasser-Auslaßmotor ON","", 20,      0,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Wasser-Auslaßmotor OFF","", 3,      0,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Wasser-Auslaß-Ventil OFF","", 1,    0,2,2,2,2,2,2,2,2,0,2,2,2,2,2,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
#    "Betriebsanzeige OFF",""   , 0.5,    0,2,2,2,2,2,2,2,2,2,2,2,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2, #
    "Warnsignal","", 0,                  0,2,2,2,2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2
]

#SpWasserentleeren
Ablaufplan_SpWasserentleeren = [
    "Start + Warnsignal OFF","", 0.5,    0,2,2,2,2,2,2,2,2,2,2,2,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2, #
#    "Wasser-Heizung ON ","", 1,          0,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Betriebsanzeige ON","",     0.5,    0,2,2,2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,  # Betriebsanzeige    ON  -12
    "Wasser-Einlaßmotor ON","", 15,      0,2,0,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Wasser-Auslaßmotor ON","",  1,      0,2,0,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,    
    "Wasser-Auslaß-Ventil ON","",0.5,    0,2,1,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Wasser-Auslaßmotor ON","",  1,      0,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,


#    "Wasser-Auslaß-Ventil ON","",0.5,    0,2,1,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Wasser-Auslaßmotor OFF","",30,      0,2,1,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Wasser-Auslaßmotor OFF","", 0.5,    0,2,0,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Wasser-Auslaß-Ventil OFF","",0.5,   0,2,2,2,2,2,2,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,

#    "Spülwa Abpump Motor ON","", 10,     0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
#    "Spülwa Abpump Motor OFF","", 1,     0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Warnsignal","", 0,                  0,2,2,2,2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2
]

Ablaufplan_Druckluft = [
    "Start + Warnsignal OFF","", 0.5,    0,2,2,2,2,2,2,2,2,2,2,2,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2, # Start
    "Betriebsanzeige ON","",     0.5,    0,2,2,2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,

    "Druckluft-In ON", "",       7,      8,2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2, #   Luft-Einlaß (neu: druckgeregelt)
    "Druckluft-In OFF",  "",     0.5,    0,2,2,2,2,2,2,2,2,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
    "Druckluft Ventil ON","",    4,      0,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2, #   Luft-Auslaß
    "Druckluft Ventil OFF","",   0.5,    0,2,2,2,2,2,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,#
    "Wasser-Auslaßmotor ON","",  0.5,   -1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,     #   ???
    "Warnsignal","", 0,                  0,2,2,2,2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2

]


Ablaufplan.append(0)                         # 0
Ablaufplan.append(Ablaufplan_Sequenzel)      # 1
Ablaufplan.append(Ablaufplan_Wäsche)         # 2
Ablaufplan.append(Ablaufplan_Spuelung)       # 3
Ablaufplan.append(Ablaufplan_SpTrocknung)      # 4
Ablaufplan.append(Ablaufplan_WaWasserentleeren)# 5
Ablaufplan.append(Ablaufplan_SpWasserentleeren)# 6
Ablaufplan.append(Ablaufplan_Druckluft)      # 7


ablaufplan_breite = 36  # Anzahl Spalten pro Reihe  ###! -> 36 !

ablauf_schritt = 0 #-1     # stop
ablauf_schritt_dauer = 0
ablauf_schritt_wdh = 0
ablauf_schritt_wdhpos = 0  # 

HaltAblauf = False          # Taste "Halt/Weiter", Ablaufsteuerung anhalten
WarteTemperatur = True      # Ablaufstart nach Erreichen der Regel-Temperatur


def berechne_ablaufdauer():
    schritt = 0
    summe = 0
    wdh = 0
    wdhpos = 0
    #while Ablaufplan_Vorwäsche[schritt*ablaufplan_breite + 2] > 0:
    while Ablaufplan[Vorgang][schritt*ablaufplan_breite + 2] > 0:
        # noch ein Schritt
        ablwdh = Ablaufplan[Vorgang][schritt*ablaufplan_breite + 3]
        #print("Schritt-Dauer: ", Ablaufplan_Vorwäsche[schritt*ablaufplan_breite + 2])
        ##print("Schritt-Dauer: ", Ablaufplan[Vorgang][schritt*ablaufplan_breite + 2])
        ##print("Schritt-Wiederholung: ", ablwdh)
        if ablwdh > 0:
            wdh = ablwdh
            wdhpos = schritt
        elif ablwdh < 0:
            wdh -= 1
            if wdh > 0:
                schritt = wdhpos
        #summe += Ablaufplan_Vorwäsche[schritt*ablaufplan_breite + 2]
        summe += Ablaufplan[Vorgang][schritt*ablaufplan_breite + 2] #* ablwdh
        ##print("Summe: ", summe)
        schritt += 1
        #wdh = Ablaufplan[Vorgang][(ablauf_schritt-1)*ablaufplan_breite + 3]

    summe += 1     ### TEST !!!!    XXX!
    print("Dauer: ", summe)
    return summe        # Summe [s]


def Ablauf_SchrittWeiter():
    global Ablaufplan_Sequenzel
    global ablaufplan_breite
    global ablauf_schritt
    global ablauf_schritt_dauer
    global ablauf_schritt_wdh
    global ablauf_schritt_wdhpos
    if ablauf_schritt > 0:
        print("  # Ablauf-Schritt: ", ablauf_schritt)
        #for sp in range(ablaufplan_breite):
        #    #print(Ablaufplan_Vorwäsche[(ablauf_schritt-1)*ablaufplan_breite + sp], end="; ")
        #    print(Ablaufplan[Vorgang][(ablauf_schritt-1)*ablaufplan_breite + sp], end="; ")
        #print(".")
        #Show_Info("Vorwäsche\r\n[", Ablaufplan_Vorwäsche[(ablauf_schritt-1)*ablaufplan_breite + 0], "]")
        #if Ablaufplan_Vorwäsche[(ablauf_schritt-1)*ablaufplan_breite + 2] == 0:     # (0-basiert!)
        if Ablaufplan[Vorgang][(ablauf_schritt-1)*ablaufplan_breite + 2] > 0:     # (0-basiert!)
            #!     ablauf_schritt = -1 #0
            #! else:
            #if ablauf_schritt > 1:
            ablauf_schritt += 1
            ablauf_schritt_dauer = Ablaufplan[Vorgang][(ablauf_schritt-1)*ablaufplan_breite + 2]
            wdh = Ablaufplan[Vorgang][(ablauf_schritt-1)*ablaufplan_breite + 3]
            if wdh > 0:                             # neue Wiederholung, Start
                ablauf_schritt_wdh = wdh                # Anzahl Wdh.
                ablauf_schritt_wdhpos = ablauf_schritt  # Wdh.-Start merken
            elif wdh < 0:                           # Ende Wiederholungsschleife
                ablauf_schritt_wdh -= 1                 # nächste Wdh.
                if ablauf_schritt_wdh > 0:
                    ablauf_schritt = ablauf_schritt_wdhpos  # zurück zum Wdh.-Start
                    ablauf_schritt_dauer = Ablaufplan[Vorgang][(ablauf_schritt-1)*ablaufplan_breite + 2]    # holen!
            print("SD: ", ablauf_schritt_dauer, " SW: ", ablauf_schritt_wdh)


def Ablauf_Start():
    global NOT_AUS
    if not NOT_AUS:
        global ablauf_schritt
        global ablauf_schritt_dauer
        global tmp_vorgang_dauer
        global tmp_vorgang_countdown
        #global Ablaufplan
        #global Vorgang
        print("vorgang", Vorgang)
        print("breite", ablaufplan_breite)
        print("AP:", Ablaufplan[Vorgang][0*ablaufplan_breite + 2])
        zeit = berechne_ablaufdauer()
        tmp_vorgang_dauer = zeit
        tmp_vorgang_countdown = int(tmp_vorgang_dauer)
        ablauf_schritt = 1 #0  # start #1
        #?:
        ablauf_schritt_dauer = Ablaufplan[Vorgang][(ablauf_schritt-1)*ablaufplan_breite + 2]
        print("SD: ", ablauf_schritt_dauer)


def Ablauf_Stop():
    global ablauf_schritt
    global tmp_vorgang_dauer
    global tmp_vorgang_countdown
    tmp_countdown_mode = 0
    tmp_vorgang_countdown = -1
    ablauf_schritt = 0 #-1     # stop #0


"""
"""
BtnAusgangNamen = [
    "Innenbeleuchtung",         #1
    "Wasserauslaß-Pumpe",
    "Wassereinlaß-Pumpe",
    "Trockenluft-Motor",        #4

    "Wasserheizung",
    "Trockenluft-Heizung",
    "Drucklufteinlaß-Ventil",
    "Wasserauslaß-Ventil",      #8

    "Wassereinlaß-Ventil",
    "Druckluftauslaß-Ventil",
    "Euro-6-Ventil",
    "Betriebsanzeige",          #12

    "Warnsignalgeber",
    "Waschwa.-Einlaß-Ventil",
    "Spülwa.-Einlaß-Ventil" ,
    "Waschw.-Abpump-Motor" , #16
    
    "Nicht Belegt",         #17
    "Nicht Belegt",
    "Nicht Belegt",
    "Nicht Belegt",        #20

    "Nicht Belegt",
    "Nicht Belegt",
    "Nicht Belegt",
    "WNicht Belegt",      #24

    "Nicht Belegt",
    "Nicht Belegt",
    "Nicht Belegt",
    "Nicht Belegt",          #28

    "Nicht Belegt",
    "Nicht Belegt",
    "Nicht Belegt",
    "Nicht Belegt"  #32
]


#bus = smbus.SMBus(1) # Rev 2 Pi
bus = False


#   MCP23017
#---------------------------------------------------
# 1 CHIP AUSGANGS CONFIGRATION
DEVICEA = 0x20 # DEVICEAA Adresse (A0-A2)
IODIRAA = 0x00 # Pin Register fuer die Richtung
IODIRBA = 0x01 # Pin Register fuer die Richtung
OLATBA = 0x14  # Register fuer Ausgabe (GPA)
OLATAA = 0x15  # Register fuer Ausgabe (GPB)

zeit = ''   # ()
zeitcode = time.localtime()
timelast = 0

temp_lese_zeit = 0

temp_control = False
temp_ctrl_on = False

Heizung_Aus = False     # Schalter "Heizung aus"

auszeit = -1    # sleep timer
sekteiler = 2

"""
"""
class AutomaticControl:

    #self.hw = False
    #self.WinMaster = 0
    #self.cfg = 0
    #self.active = False

    def __init__(self, config):
        self.cfg = config
        self.win_PartMenueName = "Automatische Steuerung"
        self.zeit = ''
        #? self.bus = smbus.SMBus(1) # Rev 2 Pi
        self.hw = self.cfg["hw_Interface"]
        self.active = False
        global bus
        global temp_control
        global temp_ctrl_on
        temp_control = True     #   ?!?     immer starten
        temp_ctrl_on = False #True     #   ?!?
        if Condition_Auto == False:
            temp_control = False

        global WarteTemperatur
        WarteTemperatur = True  # auf Regeltemperatur warten

        self.load_settings()    # (Druck-)Einstellungen holen

        self.restart_sleeptimer()

    def load_settings(self):
        #...global Condition_Auto
        self.press_wash = self.cfg["settings"].get_setting("press_wash")
        press_air = self.cfg["settings"].get_setting("press_air")
        self.press_air_list = press_air.split(", ")
        print("PressList", self.press_air_list)

    def isactive(self):
        return self.active

    def restart_sleeptimer(self):
        global auszeit
        # print("ReSleep")
        auszeit = int(self.cfg["settings"].get_setting("auto_heat_off")) * 60   # Min. -> Sek.
        # print("  ausz=", auszeit)
        if auszeit <= 0:
            auszeit = -1    # aus, ohne Sleep-Timer

    def Show_Info(self, text, mode=0):
        self.Lbl_Info["text"] = text
        if mode == 0:
            # normal, zentriert
            self.Lbl_Info["anchor"] = CENTER
            self.Lbl_Info["bg"] = self.cfg["win_InfoMode0Farbe"] #grau
        elif mode == 1:
            # multiline, links oben
            self.Lbl_Info["anchor"] = NW
            self.Lbl_Info["bg"] = self.cfg["win_InfoMode1Farbe"]
        elif mode == 2:
            # rotl, zentriert
            self.Lbl_Info["anchor"] = CENTER
            self.Lbl_Info["bg"] = self.cfg["win_InfoMode2Farbe"] #(rot)
            
        elif mode == 3:
            # multiline, links oben
            self.Lbl_Info["anchor"] = CENTER
            self.Lbl_Info["bg"] = self.cfg["win_InfoMode3Farbe"] #(Grün)
        elif mode == 4:
            # rotl, zentriert
            self.Lbl_Info["anchor"] = CENTER
            self.Lbl_Info["bg"] = self.cfg["win_InfoMode4Farbe"] #(Blau)

    """
        Hardware!
    """
    def SchalteAusgang(self, ausgang, pegel):
        #
        #   ausgang: 0 .. 15
        #   pegel: 0 / 1 (!)
        #
        #? bus = self.bus

        """
        ... hw !!!
        """
        self.hw.SchalteAusgang(ausgang, pegel)
        self.show_output(ausgang, pegel)
        return -1


    def LiesAusgang(self, ausgang):
        #
        #   ausgang: 0 .. 15
        #
        """
        ...hw!!!
        """
        return self.hw.LiesAusgang(ausgang)


    def SchalteAlleAusgaenge(self, pegel):
        #
        #   pegel: 0 / 1 (!)
        #
        print("Ausgänge : ", pegel)
        """
        ...
        """
        self.hw.SchalteAlleAusgaenge(pegel)
        for aus in range(16):                   # (...??)   ###! -> 32 !
            self.show_output(aus, pegel)


    def ablauf_schritt_ausgabe(self):
        global Ablaufplan_Sequenzel
        global ablaufplan_breite
        global ablauf_schritt

        global ablauf_schritt_wdh   # Wdh.-Durchlauf, absteigend

        for sp in range(16):    ###! -> 32 !
            #val = Ablaufplan_Vorwäsche[(ablauf_schritt-1)*ablaufplan_breite + 3+sp]
            val = Ablaufplan[Vorgang][(ablauf_schritt-1)*ablaufplan_breite + 4+sp]
            if val == 0:
                self.SchalteAusgang(sp, 0)
                #in schalteausgang! self.show_output(sp, 0)
            elif val == 1:
                self.SchalteAusgang(sp, 1)
                # self.show_output(sp, 1)
            # ['2' = unverändert]


    def show_outputs(self):
        """
            Labels
        """
        """
        self.WinMaster.grid_rowconfigure(index=3, weight=1)     # anpassende Reihen
        self.WinMaster.grid_rowconfigure(index=4, weight=1)
        self.WinMaster.grid_rowconfigure(index=5, weight=1)
        self.WinMaster.grid_rowconfigure(index=6, weight=1)
        """

        lf = LabelFrame(master=self.WinMaster, text="Ausgänge", font="arial 13", labelanchor=N) #, width=25
        lf.grid(row=3, column=3, rowspan=3, sticky=N+S+E+W, padx=5, pady=10)

        self.label = []
        row = 0
        
        for idx in range(16):
            print("Idx:", idx)

            l = Label(master=lf, text="{0:2d}".format(idx+1) +" " + BtnAusgangNamen[idx], font="arial 13", justify=LEFT, anchor=W) #, bg="cyan", width=22
            l.pack(anchor=W, fill=X, pady=1) #, expand=1  #, side=LEFT    #sticky=N+S+E+W, padx=5, pady=10)

            #if self.LiesAusgang(idx) == 1:    # aktuellen Zustand übernehmen!
            if self.hw.LiesAusgang(idx) == 1:    # aktuellen Zustand übernehmen!
                l["bg"] = self.cfg["win_SchaltFarbeAn"]

            self.label.append(l)    # innerhalb LabelFrame!
            ###################################################### 21.04.2021 keine Funktion
#            if len(sim_invalues) <= 32:     # (2 B.) nur einmal!
#            self.label.append(l)
            ######################################################
#            lf = Frame(lf) #, width=25
#            lf.pack(anchor=E, pady=20) #, expand=1  #, side=LEFT    #sticky=N+S+E+W, padx=5, pady=10)

#        for idx in range(16):
#            print("Idx:", idx)

#            lg = Label(master=lg, text="{0:2d}".format(16+idx+1) +" " + BtnAusgangNamen[idx], font="arial 13", justify=LEFT, anchor=W) #, bg="cyan", width=22
#            lg.pack(anchor=W, fill=X, pady=1) #, expand=1  #, side=LEFT    #sticky=N+S+E+W, padx=5, pady=10)

            #if self.LiesAusgang(idx) == 1:    # aktuellen Zustand übernehmen!
#            if self.hw.LiesAusgang(idx) == 1:    # aktuellen Zustand übernehmen!
#                l["bg"] = self.cfg["win_SchaltFarbeAn"]

#            self.label.append(l)    # innerhalb LabelFrame!

    def show_output(self, output, level=0):

        l = self.label[output]

        if level == 1:
            l["bg"] = self.cfg["win_SchaltFarbeAn"]    #"yellow"
        else:
            l["bg"] = "#d8d8d8" #self.cfg["win_InfoMode0Farbe"]    #win_HgFarbe    # "win_SchaltFarbeAus"


    def Show(self):

        self.WinMaster = Toplevel()     #Tk()
        self.WinMaster.title(self.cfg["win_Titel"])
        self.WinMaster.geometry(self.cfg["win_Geometrie"])
        self.WinMaster['bg'] = self.cfg["win_HgFarbe"]

        self.WinMaster.grid_columnconfigure(index=0, weight=1)
        self.WinMaster.grid_columnconfigure(index=1, weight=1)
        self.WinMaster.grid_columnconfigure(index=2, weight=1)
        self.WinMaster.grid_columnconfigure(index=3, weight=1)
        self.WinMaster.grid_columnconfigure(index=4, weight=1)

        #0
        Label(master=self.WinMaster, text=self.cfg["win_Bezeichnung"], font=self.cfg["win_TopSchrift"], bg=self.cfg["win_TextHgFarbe"], fg='red').grid(row=0, column=1, columnspan=2, pady=3, sticky=W+E)

        uhr = Label(master=self.WinMaster, font=('Arial',15), bg=self.cfg["win_HgText"], fg=self.cfg["win_UhrTextFarbe"])   #, width=25, height = 3
        uhr.grid(row=0, column=3)

        #2
        Label(self.WinMaster, text=self.win_PartMenueName, font=self.cfg["win_PartMenueSchrift"], bg=self.cfg["win_TextHgFarbe"], fg=self.cfg["win_TextFarbe"], pady=15).grid(row=2, column=1, columnspan=2, sticky=W+E) #.pack() #.place(x=150,y=110)


        def Btn_NotAus_click():
            self.SchalteAlleAusgaenge(0)
            buttons_normal()
            Ablauf_Stop()
            global NOT_AUS
            NOT_AUS = True
            self.Show_Info("NOT-AUS!", 2)
            
            
        def Btn_Back_click():
            self.SchalteAlleAusgaenge(0)   # Yeni 18.04.2020
            Ablauf_Stop()       #   !?!
            self.active = False
            self.WinMaster.quit()
            self.WinMaster.destroy()

        #
        #noch grid 2
        btn = Button(self.WinMaster, text="zurück", 
            width=8, height=2, background="#c0c0c0", command=Btn_Back_click,   #self.cfg["win_TextFarbe"]
            font=self.cfg["win_SchaltSchrift"] , bd=5)   #, relief="ridge"
        btn.grid(row=2, column=0)#, stick=W)

        #--- Schalter Heizung aus
        def HeizungAus_click():
            print("H-off:", varho.get())
            global temp_control
            global Heizung_Aus
            if  Btn_Hoff.var.get() == 1:
                Heizung_Aus = True
                # Abschaltung
                temp_control = False
                self.SchalteAusgang(4, 0)   # aus!
                #?! temp_ctrl_on = False
                self.Show_Info("Heizungsregelung ausgeschaltet!", 1)
            else:
                Heizung_Aus = False
                # einschalten
                temp_control = True
                self.SchalteAusgang(4, 1)   # ein   (!?)
                temp_ctrl_on = True
                self.Show_Info("Heizungsregelung eingeschaltet!", 3)

        varho = IntVar()
        Btn_Hoff = Checkbutton(self.WinMaster, text="Heizung\naus", font=self.cfg["win_Button2Schrift"], pady=15, bg=self.cfg["win_HgText"], 
            width=10, height=1, bd=5, relief=RIDGE, command=HeizungAus_click,
            selectcolor=self.cfg["win_SchaltFarbeAn"], indicatoron=OFF, variable=varho)
        Btn_Hoff.var = varho
        Btn_Hoff.grid(row=4, column=0, pady=15, sticky=S) 


        btn = Button(self.WinMaster, text="Not-Aus", 
            width=6, height=2, background=self.cfg["win_NotFarbe"], command=Btn_NotAus_click,
            #font=self.cfg["win_SchaltSchrift"], bd=5)   #, relief="ridge"
            font=self.cfg["win_MenueSchrift"], bd=5)   #, relief="ridge"
        btn.grid(row=2, column=3 ) #,sticky=E

        #3
        Lbl_TempID = Label(self.WinMaster, text="Wasser-Temp.", font=self.cfg["win_SchaltSchrift"], pady=10, bg=self.cfg["win_HgText"], 
            width=16, height=1)
        Lbl_TempID.grid(row=3, column=0, sticky=N, pady=0)   #, pady=15
        
        Lbl_Temp = Label(self.WinMaster, text="Temperatur", font=self.cfg["win_MenueSchrift"], pady=10, bg=self.cfg["win_HgText"], 
            width=10, height=1)
        Lbl_Temp.grid(row=3, column=0, sticky=N, pady=30)   #, pady=50

        Lbl_TempSoll = Label(self.WinMaster, text="Soll-Temp.", font=self.cfg["win_SchaltSchrift"], pady=10, bg=self.cfg["win_HgText"], 
            width=16, height=1)
        Lbl_TempSoll.grid(row=4, column=0, sticky=N, pady=10)   #, pady=15
        
        st = float(self.cfg["settings"].get_setting("proc_temp_wash"))
        
        Lbl_TempSoll = Label(self.WinMaster, text="{0}".format(st) + "°C", font=self.cfg["win_MenueSchrift"], pady=10, bg=self.cfg["win_HgText"], 
            width=10, height=1)
        Lbl_TempSoll.grid(row=4, column=0, sticky=N, pady=0)   #, pady=15 sticky=N, 

        # Meßinstrument
        #?? self.WinMaster.wm_attributes("-transparent", True)
        #?? root.config(bg='systemTransparent')
        self.gauge = Meter(self.WinMaster, width=190, indicatorlen=95,  # indicatorarrow="5 10 3",
                           textupper="Cem-Tuning", textlower="Wasser-\n  Temp.",
                           upper=100, lower=0)
        # "grünen Bereich" einstellen auf Soll-Temperatur-Bereich
        self.gauge.colorrange(1, 0, st - float(self.cfg["settings"].get_setting("proc_temp_wash_thresh")))
        self.gauge.colorrange(2, st - float(self.cfg["settings"].get_setting("proc_temp_wash_thresh")), st)
        self.gauge.colorrange(3, st, 100)
        self.gauge.grid(row=5, column=0, pady=0)   #, pady=15 sticky=N, 

        """
        knopf30 = Button(fenster, text=" VORWÄSCHE ",font="arial 30",relief="groove" ,bd=5,width=17 ,command=ausgabe30) .place(x=250,y=210)
        knopf31 = Button(fenster, text=" WASCHVORGANG ",font="arial 30",relief="groove" ,bd=5,width=17 ,command=ausgabe31).place(x=250,y=300)
        knopf32 = Button(fenster, text=" SPÜLUNG ",font="arial 30",relief="groove" ,bd=5 ,width=17 ,command=ausgabe32).place(x=250,y=390)
        knopf33 = Button(fenster, text=" TROCKNEN ",relief="groove" ,font="arial 30" ,width=17, bd=5,command=ausgabe33).place(x=250,y=480)
        """
        def buttons_off():
            Btn_Sequenzel["bg"] = self.cfg["win_HgText"]
            Btn_Wäsche["bg"] = self.cfg["win_HgText"]
            Btn_Spuelung["bg"] = self.cfg["win_HgText"]
            Btn_SpTrocknung["bg"] = self.cfg["win_HgText"]
            Btn_WaWasserentleeren["bg"] = self.cfg["win_HgText"]
            Btn_SpWasserentleeren["bg"] = self.cfg["win_HgText"]
            Btn_Druckluft ["bg"] = self.cfg["win_HgText"]
#            Btn_Trocknung["bg"] = self.cfg["win_HgText"]  Druckluft 
        def buttons_state(state=NORMAL, button_enable=None):
            Btn_Sequenzel["state"] = state
            Btn_Wäsche["state"] = state
            Btn_Spuelung["state"] = state
            Btn_SpTrocknung["state"] = state
            Btn_WaWasserentleeren["state"] = state
            Btn_SpWasserentleeren["state"] = state
            Btn_Druckluft ["state"] = state
#            Btn_Trocknung["bg"] = self.cfg["win_HgText"]

        def buttons_normal():
            buttons_off()
            buttons_state()

        def Sequenzel_click():
            print(Btn_Sequenzel["text"])
            buttons_off()
            if not NOT_AUS and Condition_Auto:
                buttons_state(DISABLED)
                Btn_Sequenzel["bg"] = self.cfg["win_SchaltFarbeAn"]
                Btn_Sequenzel.flash()
                self.Show_Info("Sequenzel läuft", 1)
                #temp_control = True     # Heizung an    ?!?
                #global tmp_vorgang_countdown
                #global tmp_vorgang_dauer
                #oben! tmp_vorgang_countdown = tmp_vorgang_dauer   # Countdown starten
                global Vorgang
                global Vorgang_Sequenzel
                Vorgang = Vorgang_Sequenzel
                Ablauf_Start()
            
        Btn_Sequenzel = Button(self.WinMaster, text="Sequenzel\nLuft Druck Wäsche", font=self.cfg["win_MenueSchrift"], pady=10, bg=self.cfg["win_HgText"], 
            width=self.cfg["win_Button1Breite"], height=2, bd=12, relief=RIDGE, command=Sequenzel_click)
        Btn_Sequenzel.grid(row=3, column=2, pady=5 ,sticky=N)
#Btn_Wäsche.grid(row=3, column=1, sticky=N, pady=5)

        def Wäsche_click():
            print(Btn_Wäsche["text"])
            buttons_off()
            if not NOT_AUS and Condition_Auto:
                buttons_state(DISABLED)
                Btn_Wäsche["bg"] = self.cfg["win_SchaltFarbeAn"]
                Btn_Wäsche.flash()
                self.Show_Info("Wäsche läuft", 1)
                temp_control = True     # Heizung an    ?!?
                global Vorgang
                global Vorgang_Wäsche
                Vorgang = Vorgang_Wäsche
                Ablauf_Start()

        Btn_Wäsche = Button(self.WinMaster, text="WÄSCHE", font=self.cfg["win_MenueSchrift"], pady=10, bg=self.cfg["win_HgText"], 
            width=self.cfg["win_Button1Breite"], height=2, bd=12, relief=RIDGE, command=Wäsche_click)
        Btn_Wäsche.grid(row=3, column=1, sticky=N, pady=5)
        #() (row=4, column=1, pady=5)

        #4
        def Spuelung_click():
            print(Btn_Spuelung["text"])
            buttons_off()
            if not NOT_AUS and Condition_Auto:
                buttons_state(DISABLED)
                Btn_Spuelung["bg"] = self.cfg["win_SchaltFarbeAn"]
                Btn_Spuelung.flash()
                self.Show_Info("Spülung läuft", 1)
                #?global temp_control
                #?temp_control = False     # Heizung aus
                #global WarteTemperatur
                #WarteTemperatur = False
                global HaltAblauf
                HaltAblauf = False
                global Vorgang
                global Vorgang_Spuelung
                Vorgang = Vorgang_Spuelung
                Ablauf_Start()
        Btn_Spuelung = Button(self.WinMaster, text="SPÜLUNG", font=self.cfg["win_MenueSchrift"], pady=10, bg=self.cfg["win_HgText"], 
            width=self.cfg["win_Button1Breite"], height=2, bd=12, relief=RIDGE, command=Spuelung_click)
        Btn_Spuelung.grid(row=4, column=1, pady=5) #, sticky=N
        #(row=4, column=1, pady=5)
#        Btn_Vorwäsche.grid(row=3, column=1, sticky=N, pady=5)

        def SpTrocknung_click():
            print(Btn_SpTrocknung["text"])
            buttons_off()
            if not NOT_AUS:
                buttons_state(DISABLED)
                Btn_SpTrocknung["bg"] = self.cfg["win_SchaltFarbeAn"]
                Btn_SpTrocknung.flash()
                self.Show_Info("SpTrocknung läuft", 1)
                #temp_control = False     # Heizung an    ?!?
                self.SchalteAusgang(4, 0)  # Heizung OFF
                #global WarteTemperatur
                #WarteTemperatur = False
                global HaltAblauf
                HaltAblauf = False
                global Vorgang
                global Vorgang_SpTrocknung
                Vorgang = Vorgang_SpTrocknung
                Ablauf_Start()

        Btn_SpTrocknung = Button(self.WinMaster, text="Sequenzel\nLuft Druck Spülung", font=self.cfg["win_MenueSchrift"], pady=10, bg=self.cfg["win_HgText"], 
            width=self.cfg["win_Button1Breite"], height=2, bd=12, relief=RIDGE, command=SpTrocknung_click)
        Btn_SpTrocknung.grid(row=4, column=2, pady=5)    #, sticky=N
        #Btn_Trocknung["state"] = DISABLED

        def WaWasserentleeren_click():
            print(Btn_WaWasserentleeren["text"])
            buttons_off()
            if not NOT_AUS:
                buttons_state(DISABLED)
                Btn_WaWasserentleeren["bg"] = self.cfg["win_SchaltFarbeAn"]
                Btn_WaWasserentleeren.flash()
                self.Show_Info("WaWasserentleeren läuft", 1)
                self.SchalteAusgang(4, 0)  # Heizung OFF
                #global WarteTemperatur
                #WarteTemperatur = False
                global HaltAblauf
                HaltAblauf = False
                global Vorgang
                global Vorgang_WaWasserentleeren
                Vorgang = Vorgang_WaWasserentleeren
                Ablauf_Start()
      
        Btn_WaWasserentleeren = Button(self.WinMaster, text="Waschwasser\nentleeren", font=self.cfg["win_Button2Schrift"], pady=10, bg=self.cfg["win_HgText"], 
            width=9, height=1, bd=5, relief=RIDGE, command=WaWasserentleeren_click)  #win_SchaltSchrift
        Btn_WaWasserentleeren.grid(row=5, column=2, padx=5, pady=15, sticky=NW) #
#        Btn_X1["state"] = DISABLED

        def SpWasserentleeren_click():
            print(Btn_SpWasserentleeren["text"])
            buttons_off()
            if not NOT_AUS:
                buttons_state(DISABLED)
                Btn_SpWasserentleeren["bg"] = self.cfg["win_SchaltFarbeAn"]
                Btn_SpWasserentleeren.flash()
                self.Show_Info("SpWasserentleeren läuft", 1)
                self.SchalteAusgang(4, 0)  # Heizung OFF
                #global WarteTemperatur
                #WarteTemperatur = False
                global HaltAblauf
                HaltAblauf = False
                global Vorgang
                global Vorgang_SpWasserentleeren
                Vorgang = Vorgang_SpWasserentleeren
                Ablauf_Start()

        Btn_SpWasserentleeren = Button(self.WinMaster, text="Spülwasser\nEntleeren", font=self.cfg["win_Button2Schrift"], pady=10, bg=self.cfg["win_HgText"], 
            width=9, height=1, bd=5, relief=RIDGE, command=SpWasserentleeren_click)  #win_SchaltSchrift
        Btn_SpWasserentleeren.grid(row=5, column=2, padx=5, pady=15, sticky=NE) #

        def Druckluft_click():
            print(Btn_Druckluft["text"])
            buttons_off()
            if not NOT_AUS:
                buttons_state(DISABLED)
                Btn_Druckluft["bg"] = self.cfg["win_SchaltFarbeAn"]
                Btn_Druckluft.flash()
                self.Show_Info("Druckluft  läuft", 1)
                self.SchalteAusgang(4, 0)  # Heizung OFF
                #global WarteTemperatur
                #WarteTemperatur = False
                global HaltAblauf
                HaltAblauf = False
                global Vorgang
                global Vorgang_Druckluft 
                Vorgang = Vorgang_Druckluft 
                Ablauf_Start()
        Btn_Druckluft = Button(self.WinMaster, text="Druckluft", font=self.cfg["win_Button2Schrift"], pady=10, bg=self.cfg["win_HgText"], 
            width=8, height=2, bd=5, relief=RIDGE, command=Druckluft_click)
        Btn_Druckluft.grid(row=5, column=1, padx=5, pady=33, sticky=SW)
        #Btn_X2["state"] = DISABLED

        def SummerAus_click():
            #print(Btn_Vorwäsche["text"])
            #?buttons_off()
            #?buttons_state(DISABLED)
            #()Btn_X3["bg"] = self.cfg["win_SchaltFarbeAn"]
            Btn_X3.flash()
            #()self.Show_Info("Vorwäsche läuft", 1)
            self.SchalteAusgang(12, 0)
            """
            #global tmp_vorgang_countdown
            #global tmp_vorgang_dauer
            #oben! tmp_vorgang_countdown = tmp_vorgang_dauer   # Countdown starten
            Vorgang = Vorgang_Vorwäsche
            Ablauf_Start()
            """
        Btn_X3 = Button(self.WinMaster, text="Alarm\naus", font=self.cfg["win_Button2Schrift"], pady=10, bg=self.cfg["win_HgText"], 
            width=8, height=2, bd=5, relief=RIDGE, command=SummerAus_click)
        Btn_X3.grid(row=5, column=2, padx=5, pady=33, sticky=SW)

        def HaltWeiter_click():
            print("H/W:", var.get())
            global HaltAblauf
            if  Btn_X4.var.get() == 1:
                HaltAblauf = True
            else:
                HaltAblauf = False
        """
                btn = Checkbutton(master=lf, text="0 / Aus", command=Btn_click, variable=var, 
                    width=8, height=3, indicatoron=OFF, selectcolor=self.cfg["win_SchaltFarbeAn"], background=self.cfg["win_SchaltFarbeAus"],
                    font= self.cfg["win_SchaltSchrift"], relief="ridge", bd=5)  #self.cfg["win_SchaltText"]
                btn.var = var
                self.btn_out[idx].select()
                self.btn_out[idx].config(text='1 / An')
        """
        var = IntVar()
        Btn_X4 = Checkbutton(self.WinMaster, text="Halt/\nweiter", font=self.cfg["win_Button2Schrift"], pady=10, bg=self.cfg["win_HgText"], 
            width=8, height=2, bd=5, relief=RIDGE, command=HaltWeiter_click,
            selectcolor=self.cfg["win_SchaltFarbeAn"], indicatoron=OFF, variable=var)
        Btn_X4.var = var
        Btn_X4.grid(row=5, column=2, padx=5, pady=33, sticky=SE)
        
        #
        self.show_outputs()     # (über Reihen 3 bis 5)

        self.Lbl_Press1 = Label(master=self.WinMaster, text="[Druck]", font=self.cfg["win_TopSchrift"], bg=self.cfg["win_HgText"])
        self.Lbl_Press1.grid(row=5, column=1, sticky=SW)

        self.Lbl_Press2 = Label(master=self.WinMaster, text="[Druck]", font=self.cfg["win_TopSchrift"], bg=self.cfg["win_HgText"])
        self.Lbl_Press2.grid(row=5, column=2, sticky=SW)
    
        #6
        l6a = Label(master=self.WinMaster, text="Information", font=self.cfg["win_LabelSchrift"]) #, bg=self.cfg["win_HgText"]
        l6a.grid(row=6, column=1, columnspan=2, sticky=N+S+E+W, padx=1)
        l6b = Label(master=self.WinMaster, text="Restzeit", font=self.cfg["win_LabelSchrift"], bg=self.cfg["win_HgText"])
        l6b.grid(row=6, column=3, sticky=N+S+E+W, padx=1)

        #X, Rest nach unten
        self.WinMaster.grid_rowconfigure(index=7, weight=1)

        self.Lbl_Press = Label(master=self.WinMaster, text="[Druck]", font=self.cfg["win_TopSchrift"], bg=self.cfg["win_HgText"])
        self.Lbl_Press.grid(row=7, column=0, sticky=N)

        Label(master=self.WinMaster, text="Ver.52 Automatic",bg=self.cfg["win_HgText"],).grid(row=7, column=0, sticky=S)

        self.Lbl_Info = Label(master=self.WinMaster, text="Info", font=self.cfg["win_TopSchrift"], bg=self.cfg["win_HgText"], justify=LEFT)
        self.Lbl_Info.grid(row=7, column=1, columnspan=2, sticky=N+S+E+W, padx=1)

        self.Lbl_Countdown = Label(master=self.WinMaster, text="00:00",
            font=self.cfg["win_CountdownSchrift"], fg=self.cfg["win_CountdownAusFarbe"], bg=self.cfg["win_HgText"])
        self.Lbl_Countdown.grid(row=7, column=3, sticky=N+S+E+W, padx=1)

        """
        """
        #global zeit = ''
        #global zeitcode = time.localtime()

        global temp_control
        temp_control = True     # immer an ?!

        def Check_BedinertastenA():# Zusatz tasten
            if self.hw.LiesEingang(25-1) == 1:  # Taste "Wasserheizung"
                HeizungAus_click()
#            if self.hw.LiesEingang(18-1) == 1:  # Taste "Vorwäsche"
#                Sequenzel_click()
            if self.hw.LiesEingang(22-1) == 1:  # Taste "Wäsche"
                Wäsche_click()
            if self.hw.LiesEingang(23-1) == 1:  # Taste "Spülung"  Führer 23
                Spuelung_click()
#            if self.hw.LiesEingang(21-1) == 1:  # Taste "SpTrocknung"
#                SpTrocknung_click()
            if self.hw.LiesEingang(23-1) == 1:  # Taste "Sezwenzel Luft druck 31 WaWasserentleeren"
                Sequenzel_click()
            if self.hw.LiesEingang(30-1) == 1:  # Taste "Sezwenzel Luft Druck Spülwassr entleeren"
                SpTrocknung_click()
            if self.hw.LiesEingang(28-1) == 1:  # Taste "Alarm Aus"
                SummerAus_click()
            if self.hw.LiesEingang(29-1) == 1:  # Taste "Zürück"
                Btn_Back_click()


        def Check_Autocondition(): # eingang prüfung abgefragt .vor automatic ablauf
            global Condition_Auto
            txtinfo = ""
            
            conda = self.cfg["settings"].get_setting("input_auto_cond_a")
            if conda != "" and int(conda) > 0:
                if self.hw.LiesEingang(int(conda)-1) == 0: #1
                    txtinfo += self.cfg["settings"].get_setting("text_auto_cond_a") + "!\n"

            condb = self.cfg["settings"].get_setting("input_auto_cond_b")
            if condb != "" and int(condb) > 0:
                if self.hw.LiesEingang(int(condb)-1) == 0: #1
                    txtinfo += self.cfg["settings"].get_setting("text_auto_cond_b") + "!\n"
                    
            condc = self.cfg["settings"].get_setting("input_auto_cond_c")
            if condc != "" and int(condc) > 0:
                if self.hw.LiesEingang(int(condc)-1) == 0: #1
                    txtinfo += self.cfg["settings"].get_setting("text_auto_cond_c") + "!\n"
                    
            if txtinfo != "":
                self.Show_Info(txtinfo, 2)
                Condition_Auto = False
                #print("CS F")
            else:
                self.Show_Info("OK")
                Condition_Auto = True
                #print("CS T")
            return Condition_Auto

        Check_Autocondition()   # Eingänge nur am Anfang testen
        if Condition_Auto == False:
            temp_control = False

            """
                val = self.hw.LiesAnalog(0)
                print("Analog:", val)
                u = self.Konv_Spannung(val)
                korr = float(self.cfg["settings"].get_setting("press_cal_uoffset"))
                uk = u + korr
                p = self.Konv_Druck(uk)
                #Lbl_Analog["text"] = "{0}".format(val)
                self.Lbl_Info["text"] = "{0} = {1:1.3f} V => {2:> 3.3f} kPa = {3:> 3.3f} Bar".format(val, u, p, p/100)
            """
        def Konv_ADC_Druck(adc):
            #   Wert des ADC in Spannung umrechnen
            f = 4.096 / 32768   # ADC-Faktor 1 ( +/- 4,096 V) / 15 Bit
            u = adc * f
            korr = float(self.cfg["settings"].get_setting("press_cal_uoffset"))
            uk = u + korr
            #   Spannung in Druck umrechnen
            #   Vout = Vs * (0,009 * P + 0,04) (ohne Fehler); Vs = 5 V
            #   -> P = (Vo / Vs - 0,04) / 0,009
            p = (uk / 5 -0.04) / 0.009
            p = p/100
            return p


        def Check_Pressure(press_target, press_is=-999):
            ret = False
            if press_is > -999:     # Druck angegeben?
                p = press_is        # (Zeit/Konvertierung sparen)
            else:
                global Kanal_Druck_Vorrat
                adc = self.hw.LiesAnalog(Kanal_Druck_Vorrat)     # Sensor einlesen
                print("Analog:", adc)
                p =  Konv_ADC_Druck(adc)
            # Vergleich:
            if p - press_target >= 0:
                ret = True      # Soll-Druck erreicht/überschritten
            return ret

            
        def tick( ):
            #global zeit
            global zeitcode
            global tmp_vorgang_countdown
            global tmp_countdown_mode
            global HaltAblauf
            global timelast

            global temp_lese_zeit
            global temp_control
            global temp_ctrl_on
            global WarteTemperatur
            
            global auszeit
            global sekteiler
            
            ##neuezeit = time.strftime('%H:%M:%S - %d.%m.%Y')
            zeitcodeneu = time.localtime()
            # print("*TICK*: {0}".format(zeitcodeneu.tm_sec))
            ##if neuezeit != zeit:
            if True: #!!! zeitcodeneu.tm_sec != zeitcode.tm_sec:
                #?print(" - ", time.time()) #timelast, 
                #!print("* s *", "{0:12.3f}-{1:12.3f}".format(timelast, time.time()))
                # (1/s)
                ##self.zeit = neuezeit
                ##self.zeit = zeitcodeneu.strftime('%H:%M:%S - %d.%m.%Y')
                self.zeit = time.strftime('%H:%M:%S - %d.%m.%Y')
                uhr.config(text = self.zeit)

                if temp_lese_zeit >= self.cfg["hw_TempLeseInterval"]:
                    ## arr = HoleTemperatur()  #   !!! ~1s     !!! !!! !!!
                    ## temp=arr[0]
                    temp = self.hw.AktuelleTemperatur()
                    #print(temp)
                    ## Lbl_TempID["text"] = "Sensor-ID\n" + arr[1]
                    #? Lbl_TempID["text"] = "Sensor-ID\n" + TempSensor1
                    Lbl_Temp["text"] = "{0:3.1f} °C".format(temp)
                    temp_lese_zeit = 0
                    self.gauge.updateValue(temp)
                temp_lese_zeit += 1

                if auszeit > 0:
                    sekteiler -= 1
                    ##print("sekt:", sekteiler)
                    if sekteiler <= 0:
                        auszeit -= 1    # - 1 Sek.
                        sekteiler = 2   # 2 pro Sek.

                    ##print("ausz:", auszeit)
                    #? if (auszeit >= 0) and (auszeit <= 60):
                    #?     # 1 Min. vor Abschaltung
                    if auszeit <= 0:
                        # Abschaltung
                        temp_control = False
                        self.SchalteAusgang(4, 0)   # aus!
                        temp_ctrl_on = False
                        self.Show_Info("Heizung wurde automatisch ausgeschaltet!", 1)
                    
                print("?TC?", temp_control)
                ##print("?Warte?", WarteTemperatur)
                if temp_control:
                    tact = self.hw.AktuelleTemperatur()
                    ttarg = float(self.cfg["settings"].get_setting("proc_temp_wash"))
                    tdiff = float(self.cfg["settings"].get_setting("proc_temp_wash_thresh"))
                    tupper = ttarg          # Temp.-Fenster
                    tlower = ttarg - tdiff  #
                    #! if temp_ctrl_on:    # ist an
                    if tact >= tupper:
                        self.SchalteAusgang(4, 0)   # Temp. erreicht, aus!
                        self.Show_Info("Betriebstemperatur erreicht.", 3)
                        temp_ctrl_on = False
                        if WarteTemperatur:     # wird Teparatur erwartet?
                            HaltAblauf = False      # Halt beenden
                            WarteTemperatur = False # (nur einmal)
                            self.Show_Info("Betriebstemperatur erreicht.", 3)
                    #! else:               # ist aus
                    if tact < tlower:
                        self.SchalteAusgang(4, 1)   # Temp. unterschritten, an!
                        self.Show_Info("Betriebstemperatur noch nicht erreicht!", 2)
                        temp_ctrl_on = True
                        if WarteTemperatur:     # wird Teparatur erwartet?
                            HaltAblauf = True       # Halt erzwingen
                            self.Show_Info("Betriebstemperatur noch nicht erreicht!", 2)
                    """ Kopie
                    if temp_ctrl_on:    # ist an
                        if tact >= ttarg:
                            self.SchalteAusgang(4, 0)   # Temp. erreicht, aus!
                            temp_ctrl_on = False
                            if WarteTemperatur:     # wird Teparatur erwartet?
                                HaltAblauf = False      # Halt beenden
                                WarteTemperatur = False # (nur einmal)
                                self.Show_Info("Betriebstemperatur erreicht.")
                    else:               # ist aus
                        if tact < (ttarg - tdiff):
                            self.SchalteAusgang(4, 1)   # Temp. unterschritten, an!
                            temp_ctrl_on = True
                            if WarteTemperatur:     # wird Teparatur erwartet?
                                HaltAblauf = True       # Halt erzwingen
                                self.Show_Info("Betriebstemperatur noch nicht erreicht!", 1)
                    """
                if self.cfg["cond_start"] == False:
                    # Start-/Lauf-Bedingung nicht erfüllt!
                    Btn_NotAus_click()
                
                global Kanal_Druck_Vorrat
                pr =  Konv_ADC_Druck(self.hw.LiesAnalog(Kanal_Druck_Vorrat))    * 10  # SIM!!!
                self.Lbl_Press["text"] = "{:> 3.3f} Bar".format(pr)
                pr2 =  Konv_ADC_Druck(self.hw.LiesAnalog(1))    * 10  # SIM!!!
                self.Lbl_Press1["text"] = "{:> 3.3f} Bar".format(pr2)
                pr3 =  Konv_ADC_Druck(self.hw.LiesAnalog(2))    * 10  # SIM!!!
                self.Lbl_Press2["text"] = " {:> 3.3f} Bar".format(pr3)
                ##print("?NOT?", NOT_AUS)
                ##print("?HALT?", HaltAblauf)
                if not NOT_AUS:
                    if not HaltAblauf:
                        if tmp_vorgang_countdown >= 0:
                            # noch Restzeit
                            self.restart_sleeptimer()
                            if tmp_countdown_mode == 0:
                                print("TSTART")
                                # aktiv schalten
                                self.Lbl_Countdown["fg"] = self.cfg["win_CountdownAktivFarbe"]
                                tmp_countdown_mode = 1
                            mins, secs = divmod(tmp_vorgang_countdown, 60)      # Quotient, Rest
                            #!print("m,s: ", mins, secs)
                            ts = '{:02d}:{:02d}'.format(int(mins), int(secs))
                            self.Lbl_Countdown["text"] = ts     # anzeigen
                            tmp_vorgang_countdown -= 0.5    #0.25   #1
                            #(unten) Ablauf_SchrittWeiter()
                            self.ablauf_schritt_ausgabe()           #   Ausgänge schalten!
                            global Ablaufplan_Sequenzel
                            global ablaufplan_breite
                            global ablauf_schritt
                            global ablauf_schritt_dauer
                            global ablauf_schritt_wdh
                            global Vorgang
                            #Ablaufplan[Vorgang][(ablauf_schritt-1)*ablaufplan_breite + 3] > 0:
                            if ablauf_schritt_wdh > 0:
                                tmpstr = " wiederholt ({:0})".format(ablauf_schritt_wdh)
                            else:
                                tmpstr = ""
                                
                            #--- spezial: Druckregelung (bei "Druckluft")
                            #global Kanal_Druck_Vorrat
                            #pr =  Konv_ADC_Druck(self.hw.LiesAnalog(Kanal_Druck_Vorrat))    * 100  # SIM!!!
                            #self.Lbl_Press["text"] = "{:> 3.3f} Bar".format(pr)
                            #pr2 =  Konv_ADC_Druck(self.hw.LiesAnalog(1))    * 100  # SIM!!!
                            #self.Lbl_Press1["text"] = "{:> 3.3f} Bar".format(pr2)
                            #pr3 =  Konv_ADC_Druck(self.hw.LiesAnalog(2))    * 100  # SIM!!!
                            #self.Lbl_Press1["text"] += " {:> 3.3f} Bar".format(pr3)
                            prstr = ""
#  29.04.23 gändert                          if int(Ablaufplan[Vorgang][(ablauf_schritt-1)*ablaufplan_breite + 13]) == 1: # Druck ON
#                                prstr = "\nDruck: " + self.press_air_list[12 - ablauf_schritt_wdh] + "?" # self.press_wash + "?"
#                                if Check_Pressure(float(self.press_air_list[12 - ablauf_schritt_wdh]), pr):
#                                    prstr += " ok"              # Druck erreicht
#                                    self.SchalteAusgang(9, 0)       # Ventil zu!    ??
#                                    tmp_vorgang_countdown -= ablauf_schritt_dauer   # Teil-Restdauer abziehen
#                                    ablauf_schritt_dauer = 0        # diesen Teilschritt vorzeitig beenden! ??
                            
                            self.Show_Info(Vorgang_Name[Vorgang] + "\n" +
                                           #Ablaufplan_Vorwäsche[(ablauf_schritt-1)*ablaufplan_breite + 0] +
                                           Ablaufplan[Vorgang][(ablauf_schritt-1)*ablaufplan_breite + 0] +
                                           " [" + "{:.1f}".format(Ablaufplan[Vorgang][(ablauf_schritt-1)*ablaufplan_breite + 2]) +
                                           " s" + tmpstr + "]" + prstr, 1)
                            ablauf_schritt_dauer -= 0.5
                            print("ASD", ablauf_schritt_dauer)
                            if ablauf_schritt_dauer <= 0:
                                Ablauf_SchrittWeiter()
                        else:
                            if tmp_countdown_mode > 0:
                                print("TEND")
                                # inaktiv schalten
                                self.Lbl_Countdown["fg"] = self.cfg["win_CountdownAusFarbe"]
                                buttons_normal()
                                Vorgang = Vorgang_Inaktiv
                                self.SchalteAusgang(6, 0)   # Zwangs-Aus (Druck-Ventil)
                                self.Show_Info("beendet")
                                tmp_countdown_mode = 0

                    Check_BedinertastenA() # Externe bedinteil Bedine Fronttasten
                
                zeitcode = zeitcodeneu
                timelast = time.time()     # (weiter oben!?!)
                    
            #uhr.after(200, tick)
            #uhr.after(250, tick)
            uhr.after(500, tick)


        tick()      # Start!
        self.active = True

        self.WinMaster.mainloop()
