""" Les fonctions de base de structure du Quoridor 

On crée ici les fonctions d'initialisations de la grille, codée sous forme de dictionnaire de liste d'adjacence. 
Les sommets sont les cases représentées par des couples (i,j) ; les fonctions sur les arêtes prennent en arguments les 
4 coordonnées des sommets. Le graphe est non-orienté, c'est-à-orientatione que si a->b est une arête, b-> a aussi. 



L'état du jeu est codé par un dictionnaire Game de clés :
    - 'grille' qui contient le graphe du jeu sous forme lui-même de dictionnaire de liste d'adjacence 
    - 'taille' qui stocke le côté de la grille (n=9 par défaut - voir GAMEBOARD_DIMENSION dans quoridor_server_constants.py)
    - 'nbmurs1' et 'nbmurs2' qui correspondent aux nombres de murs à jouer
    - 'pos1' et 'pos2' qui contiennent la case (i,j) du joueur 1 (resp2) avec 1<= i,j <=n 
    - 'partie' qui contient la liste des coups joués
    - 'joueur_courant' qui continet le numéro du joueur courant (1 ou 2) ; 1 commence 
    - 'gagnant' qui contient 1 ou 2, gagnant de la partie - et 0 tant qu'elle n'est pas finie
    - 'fini' : booléen qui passe à True dès que la partie est finie """
    
def creation_partie(n):
    """ Initialise les variables de jeu en créant un dictionnaire contenant l'état du jeu (Game) et 
        la liste des coups dans le tableau Partie"""
    Game = {}
    Game['grille'] = Graphe(n)
    Game['taille'] = n
    Game['partie'] = []
    Game['nbmurs1'] = 10
    Game['nbmurs2'] = 10
    Game['pos1'] = ( (n+1)//2 , 1 )
    Game['pos2'] = ((n+1)//2 , n )
    Game['partie'] = [] 
    #Game['joueur1'] = joueur1
    #Game['joueur2'] = joueur2
    Game['joueur_courant'] = 1
    Game['gagnant'] = 0 # vaudra 1 ou 2 
    Game['fini'] = False # True quand la partie est finie 
    return Game 


def Graphe(n=9) :
    """ Entrée : taille du plateau - un entier 
        Sortie : graphe des cases du plateau sous forme de dictionnaire ; 
        clés case (i,j) ; valeurs = listes des voisins """
    G = {}
    for a in range (1,n+1) :
        for b in range (1,n+1) :
                G[(a,b)] =  []
    for (i,j) in G.keys() :
        for (k,l) in G.keys() :
            if cases_voisines((i,j),(k,l),n) :
                G[(i,j)].append( (k,l) )
    return G

def cases_voisines(case1, case2, n):
    """ teste les cases voisines """
    i,j = case1
    k,l = case2
    if abs(i-k) == 1 and j == l :
        return True
    elif abs(j-l) == 1 and i == k :
        return True
    else : 
        return False

# # Semble obosolète... 
# def Aretes(G):
#     """ Entrée : G dictionnaire d'adjacence de la grille vide
#         Sortie : Liste des arêtes a->b sous forme de couple de tuple ((xa,ya),(xb,yb)) """
#     A = []
#     for k in G.keys() :
#         (x,y) = k
#         for v in G[k] :
#             (p,q) = v
#             A.append( (x,y,p,q) )
#     return A
# #

def sommet2numero(i,j,n):
    """ Entrée : entier t >= 1 côté de la grille (i,j) case de [1,n]^2 
        Sortie : énumeration des couples (i,j) - la première ligne est 0-1-2..."""
    return (j-1)*n + i-1

def numero2sommet(num_case, grille):
    """ Entrée : entier entre 0 et n^2-1 et la grille sous forme de dictionnaire 
                de listes d'adjacence
        Sortie : le couple (i,j) qui correspond au numéro num_case """
    n = round(len(grille)**0.5)
    return (num_case % n + 1, num_case // n +1 )
        

def matrice_adjacence(grille):
    """ Entrée : grille sous forme de dictionnaire d'adjacence 
        Sortie : matrice d'adjacence sous forme de liste de liste du graphe
                non orienté grille """
    t = len(grille) # nb de sommets = côté de la matrice d'adjacence
    A = [[0]* t for _ in range(t)]
    for i in range(t):
        for j in range(t):
            (a,b) = numero2sommet(i, grille)
            (c,d) = numero2sommet(j, grille)
            if (c,d) in grille[(a,b)]:
                A[i][j] = 1
    return A
            
# def aretes_a_enlever(mur):
#     """ Entrées : un mur sous la forme (i,j,orientation) avec (i,j) une case et orientation = 'h' ou 'v' 
#         Sorties : liste Aretes contenant les couples de cases déconnectées par le mur (les 4 arêtes orientées) """
#     assert(len(mur) == 3)
#     (i,j,orientation) = mur
#     if orientation == 'h' : Aretes = [(i,j,i,j+1), (i+1,j,i+1,j+1), (i,j+1,i,j), (i+1,j+1,i+1,j)]
#     elif orientation == 'v' : Aretes = [(i,j,i+1,j), (i,j+1,i+1,j+1)]
#     return Aretes
    
# def Plaquette_licite_numeros(x,y,p,q,n) :
#     """ Entrée : deux cases (x,y) et (p,q) 
#         Sortie : booléen """
#     if y-x == n :
#         return (q-p==n) and (q==y+1 or q==y-1)
#     elif y-x == 1 :
#         return (q-p==1) and (q==y+n or q==y-n)
#     else : return False
    
    
# def numero(i,j,n) :
#     """ numérotation des cases par des entiers, ici de 1 à n**2 """
#     return (i-1)*n + j

# def supprime_arete(i,j,k,l, G) :
#     """ Entrée : dico G et deux sommets a et b
#         Sortie : None 
#         Effet de bord : modifie le dico G en supprimant l'arête a->b """
#     L = []
#     for c in G[(i,j)]:
#         if c != (k,l) :
#             L.append(c)
#     G[(i,j)] = L

# def Pose_Plaquette(mur, G) :
#     """ Entrée : un mur et le graphe du jeu 
#         Sorties :  None 
#         Effet de bord : supprime les arêtes coupées par le mur """
#     Aretes = aretes_a_enlever(mur)
#     for a in Aretes :
#         (i,j,k,l) = a
#         supprime_arete(i,j,k,l,G)

