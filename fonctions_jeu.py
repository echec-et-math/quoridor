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
 #####################
 ### Fonction de test de coup licite
 ######################   

def test_deplacement_licite(coup, Game, joueur_courant):
    """ Entrée : case où se déplace le joueur courant, sa position et celle de l'adversaire
        On suppose que coup est ici une case
        Sortie : booléen True si le coup est licite et False sinon """
    
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
        if coup in Game[pos_joueur]:
            return (coup in grille[pos_adversaire] and coup != pos_joueur)
        # un coup est licite s'il est voisin de l'adversaire, sauf la case actuelle
        

# Pour placer un mur, il faut vérifier que l'adversaire aura toujours un chemin 
# pour arriver à une de ses cases objectif. On choisit de tester l'existence d'un chemin 
# par une variante booléenne de Floyd-Warshall

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

    
def objectif_accessible(case, coup, Game, joueur_courant):
    """ Entrée : une case sous la forme (i,j), un coup de placement de mur, l'état du jeu, joueur_courant
        Sortie : booléen True si au moins une case objectif du joueur courant
            est atteignable après avoir retiré le mur """
    G = deepcopy(Game)
    n = G['taille']
    assert test__mur_presents(coup, G), 'pose de mur illicite'
    G = maj_placement_mur(coup, G, joueur_courant)
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

    grille = Game['grille']
    (i, j, orientation) = coup
    if orientation == 'v':
        return( (i+1,j) in grille[ (i,j) ] and (i+1,j+1) in grille[ (i,j+1) ])
    elif orientation == 'h':
        return( (i,j+1) in grille[ (i,j) ] and (i+1,j+1) in grille[ (i+1,j) ])
        
def test_coup_licite(coup, Game, joueur_courant):
    """ Entrée : clair
        Sortie : booléen """
    assert(len(coup)>1 and len(coup)<4) # ajouter test de type -> devrait être 
                                        # tuple (int, int, str)
    #grille = Game['grille']
    if len(coup) == 3:
        i,j,orientation = coup
        return test_placement_mur_licite(coup, Game)
    elif len(coup) == 2:
        return test_deplacement_licite(coup, Game, joueur_courant)

#%%
#####################
### Fonction de l'état de la partie - intégration des coups 
######################

""" L'état du jeu est codé par un dictionnaire Game de clés 
    - 'grille' qui contient le graphe du jeu sous forme lui-même de dictionnaire de liste d'adjacence 
    - 'nbmurs1' et 'nbmurs2' qui correspondent aux nombres de murs à jouer
    - 'pos1' et 'pos2' qui contiennent la case (i,j) du joueur 1 (resp2) avec 1<= i,j <=n 
    - 'partie' qui contient la liste des coups joués et est une variable globale indépendante de Game """
    
def creation_partie(n):
    """ Initialise les variables de jeu en créant un dictionnaire contenant l'état du jeu (Game) et 
        la liste des coups dans le tableau Partie"""
    Game = {}
    Game['grille'] = Graphe(n)
    Game['taille'] = n
    Game['partie'] = []
    Game['nbmurs1'] = 10
    Game['nbmurs2'] = 10
    Game['pos1'] = (1, (n+1)//2 )
    Game['pos2'] = (n, (n+1)//2 )
    #Game['joueur1'] = joueur1
    #Game['joueur2'] = joueur2
    Game['joueur_courant'] = 1
    Game['gagnant'] = 0 # vaudra 1 ou 2 
    Game['fini'] = False # True quand la partie est finie 
    return Game 


def maj_deplacement(coup, Game):
    """ Entrée : case où se déplace le joueur courant, sa position et celle de l'adversaire
        Sortie : Game mis à jour ; présuppose que le coup est licite """
    #grille = Game['grille']
    joueur_courant = Game['joueur_courant']
    if joueur_courant == 1:
        pos_joueur = Game['pos1']
    else: 
        pos_joueur = Game['pos2']

    Game[pos_joueur] = coup
    Game['partie'].append(coup)
    return Game

def maj_placement_mur(coup, Game,):
    """ Entrée : coup de placement de mur de la forme (i,j,'orientation') état de jeu
        Sortie : Game mis à jour
        Effet de bord : modifie le tableau partie des coups joués """
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
    Game['grille'] = grille
    Game['partie'].append(coup)
    return Game

def maj_etat_jeu(coup, Game):
    """ Entrée : coup, état du jeu
        Sortie : renvoie Game modifié  et modifie partie si le coup est licite"""
    if test_coup_licite(coup, Game, joueur_courant):
        if len(coup) == 3:
            Game = maj_placement_mur(coup, Game, joueur_courant)
        else:
            Game = maj_deplacement(coup, Game, joueur_courant)
        Game['joueur_courant'] = 1 if Game['joueur_courant'] == 2 else 1
    return Game
    
#%%
#####################
### Fonction de l'état de la partie - position gagnante  
######################
    
def test_position_gagnante(Game):
    """ Entrée : état du jeu (Game) 
        Sortie : True si le joueur courant est sur une position gagnante, False sinon"""
    n = Game['taille']
    if joueur_courant == 1:
        return Game['pos1'][1] == n
    elif joueur_courant == 2:
        return Game['pos2'][1] == 1


    
