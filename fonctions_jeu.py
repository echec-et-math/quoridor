#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 30 17:29:31 2025

@author: GrandLatapon

Fonctions de jeu

Représentation du jeu:
    grille -> graphe qui code le plateau et les cases adjacentes ;
                implanté par un dictionnaire d'adjacence de clé (i,j) (cases)
                où les valeurs sont les listes de cases voisines de (i,j)
    taille -> contient la taille du côté de la grille (noté n)
    joueur1, joueur2 -> identifiant des joueurs
    pos1, pos2 -> position des joueurs 1 et 2
    nbmurs1, nbmurs2 -> nombre de murs restants pour les joueurs 1 et 2
    joueur_courant -> 1 ou 2, c'est selon
    partie ->  liste des coups joués 
    
    coup -> 1er cas (déplacement) : case atteinte par le joueur courant format tuple (i,j) d'entiers 
        avec 1<=i,j<=n et n=9 par défaut
            2eme cas (pose de mur) : tuple au format (i,j,'dir') 


Variation par rapport à la règle officielle :
    - si un joueur est adjacent à son adversaire, il peut se déplacer sur 
    n'importe quelle case voisine de l'adversaire - sauf rester sur place
    - Les murs peuvent se croiser perpendiculairement : en fait, on coupe deux 
    arêtes parallèles voisines. 
    
"""
from representation_quoridor import *
from copy import deepcopy

#%%
def prochain_joueur(Game):
    """ Entrée : état de jeu
        Sortie : renvoie l'état du jeu où le joueur courant a changé """
    p = Game['joueur_courant']
    Game['joueur_courant'] = 3-p
    return Game

#%%    
#####################
### Fonction de test de coup licite
######################   

def test_deplacement_licite(coup, Game):
    """ Entrée : case où se déplace le joueur courant, sa position et celle de l'adversaire
        On suppose que coup est ici une case
        Sortie : booléen True si le coup est licite et False sinon """
    joueur_courant = Game['joueur_courant']
    grille = Game['grille']
    if joueur_courant == 1:
        pos_joueur, pos_adversaire = Game['pos1'], Game['pos2']
    else: 
        pos_joueur, pos_adversaire = Game['pos2'], Game['pos1']
    
    # premier cas : les joueurs ne se cotoient pas
    if pos_adversaire not in grille[pos_joueur]:
        return (coup in grille[pos_joueur])   # on teste si la case coup est atteignable 
    
    # second cas : les joueurs se cotoient
    else:
        if pos_adversaire in grille[pos_joueur]:
            return (coup in grille[pos_adversaire] and coup != pos_joueur)
        # un coup est licite s'il est voisin de l'adversaire, sauf la case actuelle
        

# Pour placer un mur, il faut vérifier que l'adversaire aura toujours un chemin 
# pour arriver à une de ses cases objectif. On choisit de tester l'existence d'un chemin 
# par une variante booléenne de Floyd-Warshall -> seule utilisation de la matrice d'adjacence

def sontConnectes(grille, n):
    """ Entrée : dictionnaire d'adjacence d'un graphe non orienté,
                n le nombre de sommets
        Sortie : une matrice carrées n*n de booléens dont la case d'indice (x,y) 
                indique s'il existe un chemin du sommet x au sommet y """
    # on créé un tableau de booléen qui indique les sommets liés
    A = matrice_adjacence(grille)
    N = []
    for i in range(n):
        N.append([A[i][j] == 1 for j in range(n)])
    # on applique le procédé ci-dessus
    for i in range(n):
        for j in range(n):
            for k in range(n):
                N[i][j] = N[i][j] or (N[i][k] and N[k][j])
    return N

def test__mur_presents(coup, Game):
    """ Entrée : coup de placement de mur de la forme (i,j,'orientation') et la grille
        Sortie : booléen True si les arêtes à enlever sont présentes et False sinon """
    # NE PREND PAS EN COMPTE POUR L'INSTANT L'EXISTENCE D'UN CHEMIN VERS LA SORTIE !!
    grille = Game['grille']
    (i, j, orientation) = coup
    if orientation == 'v':
        return( (i+1,j) in grille[ (i,j) ] and (i+1,j+1) in grille[ (i,j+1) ])
    elif orientation == 'h':
        return( (i,j+1) in grille[ (i,j) ] and (i+1,j+1) in grille[ (i+1,j) ])

    
def objectif_accessible(case, coup, Game):
    """ Entrée : une case sous la forme (i,j), un coup de placement de mur, l'état du jeu
        Sortie : booléen True si au moins une case objectif du joueur courant
            est atteignable après avoir retiré le mur """
    G = deepcopy(Game)
    joueur_courant = G['joueur_courant']
    n = G['taille']
    assert test__mur_presents(coup, G), 'pose de mur illicite'
    G = maj_placement_mur(coup, G)
    Tableau_bool = sontConnectes(G['grille'], n)
    if joueur_courant == 2:
        boole = False
        for b in Tableau_bool[0]:
            boole = boole or b
        return boole
    elif joueur_courant == 1:
        boole = False
        for b in Tableau_bool[-1]:
            boole = boole or b
        return boole          


def test_placement_mur_licite(coup, Game):
    """ Entrée : coup de placement de mur de la forme (i,j,'orientation') et la grille
        Sortie : booléen selon que le coup est licite ou pas """
    joueur_courant = Game['joueur_courant']
    if joueur_courant == 1: 
        assert Game['nbmurs1']>0
    elif joueur_courant == 2: 
        assert Game['nbmurs2']>0
    grille = Game['grille']
    (i, j, orientation) = coup
    if orientation == 'v':
        return( (i+1,j) in grille[ (i,j) ] and (i+1,j+1) in grille[ (i,j+1) ])
    elif orientation == 'h':
        return( (i,j+1) in grille[ (i,j) ] and (i+1,j+1) in grille[ (i+1,j) ])
        
def test_coup_licite(coup, Game):
    """ Entrée : clair
        Sortie : booléen """
    try:
        assert(len(coup)>1 and len(coup)<4) # ajouter test de type -> devrait être 
                                            # tuple (int, int, str)
        #grille = Game['grille']
        if len(coup) == 3:
            i,j,orientation = coup
            return test_placement_mur_licite(coup, Game)
        elif len(coup) == 2:
            return test_deplacement_licite(coup, Game)
    except AssertionError:
        return False

#%%
#####################
### Fonction de l'état de la partie - intégration des coups 
######################


def maj_deplacement(coup, Game):
    """ Entrée : case où se déplace le joueur courant, sa position et celle de l'adversaire
        Sortie : Game mis à jour ; présuppose que le coup est licite """
    if Game['joueur_courant'] == 1:
        Game['pos1'] = coup
    else: 
        Game['pos2'] = coup
    Game['partie'].append(coup)
    return Game

def maj_placement_mur(coup, Game):
    """ Entrée : coup de placement de mur de la forme (i,j,'orientation') état de jeu
        Sortie : Game mis à jour
        Effet de bord : modifie le tableau partie des coups joués """
    assert test_placement_mur_licite(coup, Game)
    grille = Game['grille']
    (i, j, orientation) = coup
    if orientation == 'v':
        grille[ (i,j) ].remove( (i+1,j) )
        grille[ (i+1,j) ].remove( (i,j) )
        grille[ (i,j+1) ].remove( (i+1,j+1) )
        grille[ (i+1,j+1) ].remove( (i,j+1) )            
    elif orientation == ('h'):
        grille[ (i,j) ].remove( (i,j+1) )
        grille[ (i,j+1) ].remove( (i,j) )
        grille[ (i+1,j) ].remove( (i+1,j+1) )
        grille[ (i+1,j+1) ].remove( (i+1,j) )
    joueur_courant = Game['joueur_courant']
    if joueur_courant == 1: 
        Game['nbmurs1'] -= 1
    elif joueur_courant == 2: 
        Game['nbmurs2'] -= 1
    Game['grille'] = grille
    Game['partie'].append(coup)
    return Game

def maj_etat_jeu(coup, Game):
    """ Entrée : coup, état du jeu
        Sortie : renvoie Game modifié  et modifie partie si le coup est licite"""
    assert test_coup_licite(coup, Game)
    joueur_courant = Game['joueur_courant']
    if len(coup) == 3:
        Game = maj_placement_mur(coup, Game)
    else:
        Game = maj_deplacement(coup, Game)
    if test_position_gagnante(Game):
        Game['gagnant'] = joueur_courant
        Game['fini'] = True
    Game = prochain_joueur(Game)
    return Game
    
#%%
#####################
### Fonction de l'état de la partie - position gagnante  
######################
    
def test_position_gagnante(Game):
    """ Entrée : état du jeu (Game) 
        Sortie : True si le joueur courant est sur une position gagnante, False sinon"""
    joueur_courant = Game['joueur_courant']
    n = Game['taille']
    if joueur_courant == 1:
        return Game['pos1'][1] == n
    elif joueur_courant == 2:
        return Game['pos2'][1] == 1
    

#%%%  Test d'une partie simple complète
Game = creation_partie(3)
Game
#%%
Game = maj_etat_jeu((1,1,'h'), Game)
Game
#%%
Game = maj_etat_jeu((2,2), Game)
Game
#%%
Game = maj_etat_jeu((3,1), Game)
Game
#%%
Game = maj_etat_jeu((2,2,'h'), Game)
Game
#%%
Game = maj_etat_jeu((3,2), Game)
Game
#%%
Game = maj_etat_jeu((3,1), Game)
Game











