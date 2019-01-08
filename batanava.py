#!/usr/bin/python3

'''
SD - Projet Bataille Navale
DUPOND Samuel, LAURENT Valentin (groupe C)
'''

# Utilisé pour l'affichage
from time import sleep

# Importer l'OS utilisé, utilisé pour la réactualisation
from sys import platform

# Importer la bibliothèque aléatoire
import random

# Importer la fonction de commande bash/shell
from os import system

# Message à afficher suite à un tir
message = ""

def initialiser_grille(valInitiale):
        return [ [valInitiale] * 10 for i in range(10) ]

def afficher_grille(grille):
        '''
        Afficher le jeu
        '''
        for i in range(11):
                if (i > 0):
                        print(i, end=' ') # Chiffres
                else:
                        print('', end='  ')
        print()
        for i in range(10):
                for j in range(11):
                        if (j == 0):
                                print(chr(65+i), end=' ') # Lettres
                        elif (j < 10):
                                print(grille[i][j-1], end=' ') # Contenu du carré
                        else:
                                print(grille[i][j-1]) # Contenu du dernier carré de la ligne
                                
def placer_bateaux(grilleBateaux):
        '''
        1 porte-avions (5 cases)
        1 croiseur (4 cases)
        1 contre-torpilleur (3 cases)
        1 sous-marin (3 cases)
        1 torpilleur (2 cases)
        '''
        # id pour chaque bateau
        bid = 0
        
        for n in [5,4,3,3,2]:
                # Incrémenter l'id bateau
                bid += 1
                
                # 1 pour placer un bateau horizontal, vertical sinon
                horz = random.randint(0, 1)
                
                # Générer des coordonnées aléatoires, en prenant en compte la taille
                if (horz == 1):
                        x = random.randint(0, 9-n)
                        y = random.randint(0, 9)
                else:
                        x = random.randint(0, 9)
                        y = random.randint(0, 9-n)
                # S'il y a un problème de placement, alors regénérer des coordonnées
                while (not verif_bateaux(grilleBateaux, x, y, n, horz)):
                        if (horz == 1):
                                x = random.randint(0, 9-n)
                                y = random.randint(0, 9)
                        else:
                                x = random.randint(0, 9)
                                y = random.randint(0, 9-n)
                
                # Ajouter les morceaux du bateau
                if (horz == 1):
                        for i in range(n):
                                grilleBateaux[x+i][y] = bid
                                
                else:
                        for i in range(n):
                                grilleBateaux[x][y+i] = bid
                        
def verif_bateaux(grilleBateaux, x, y, n, horz):
                '''
                Vérifier qu'il n'y a pas déjà un bateau collé
                dans un masque de collision qui englobe le bateau
                et tous les carrés adjacents
                
                args:
                grille -> tableau
                x, y -> coordonnées de la tête du bateau
                n -> taille du bateau
                horz -> 1 pour horizontal, vertical sinon
                '''
                
                # Prendre le carré en haut à gauche de la tête du bateau
                xMin=x-1
                yMin=y-1
                if (xMin==-1):
                        xMin=0
                if (yMin==-1):
                        yMin=0
                
                # Prendre las coordonnées dépendant de la taille
                if (horz==1):
                        xMax=xMin + n + 1
                        yMax=yMin + 2
                else:
                        yMax = yMin + n + 1
                        xMax = xMin + 2
                        
                if (xMax > 9):
                        xMax = 9
                if (yMax > 9):
                        yMax = 9
                        
                # Retourner FAUX si un bateau est détecté
                for i in range(xMin, xMax+1):
                        for j in range(yMin, yMax+1):
                                if (grilleBateaux[i][j] != 0):
                                        return False
                                
                # Sinon vrai
                return True
                
def tir_valide(grilleTirs, x, y):
        if (x < 0 or y < 0 or x > 9 or y > 9):
                return False
        return (grilleTirs[x][y] == '.')
        
def prochain_coup():
        coords = input("Saisissez la position du prochain tir: ")
        # Parser l'entrée
        
        try:
                x = ord(coords[0]) - 65
                if (len(coords) == 2):
                        y = int(coords[1]) - 1
                else:
                        y = int(coords[1] + coords[2]) - 1
        except IndexError:
                return (-1, -1)
        except ValueError:
                return (-1, -1)
        return (x, y)
        
def resultat_tir(grilleBateaux, x, y):
        return (grilleBateaux[x][y] > 0)
        
def tirer(grilleBateaux, grilleTirs, x, y):
        global message
        if (resultat_tir(grilleBateaux, x, y)):
                grilleTirs[x][y] = '+'
                message = "Touché!"
        else:
                grilleTirs[x][y] = '*'
                message = "Dans l'eau..."

        # Pour chaque bateau (bid)
        for bid in [1, 2, 3, 4, 5]:
                cpt = 0
                for i in range(len(grilleBateaux)): # Parcourir la grille
                        for j in range(len(grilleBateaux[0])):
                                if (grilleBateaux[i][j] == bid and grilleTirs[i][j] != '+'):
                                        cpt += 1 # Ajouter 1 pour chaque partie de bateau non-touché
                if (cpt == 0): # Si tous les carrés ont été touchés
                        message = "Coulé!"
                        for i in range(len(grilleBateaux)):
                                for j in range(len(grilleBateaux[0])):
                                        if (grilleBateaux[i][j] == bid):
                                                grilleTirs[i][j] = 'X' # Placer le symbol 'coulé' sur les carrés du bateau

def partie_finie(grilleTirs):
        c = 0 # Initialiser le compteur
        for i in grilleTirs:
                for j in i: # Parcourir tous les éléments
                        if (j == 'X'):
                                c += 1 # Ajouter un au compteur pour chaque carré coulé
        return (c == 17) # Si le compteur est égal au nombre total de carrés à couler, alors c'est gagné

# Grille des bateaux de l'IA
grilleBateauxIA = initialiser_grille(0)
placer_bateaux(grilleBateauxIA)

# Grille des bateaux du joueur
grilleBateauxJoueur = initialiser_grille(0)
placer_bateaux(grilleBateauxJoueur)

'''
Une grille de tir contient les valeurs suivantes:
'.' ->  carré valide
'*' ->  dans l'eau
'+' ->  touché
'X' ->  coulé
'''

# Grille des tirs du joueur
grilleTirsJ = initialiser_grille('.')
gagne = False

# Grille des tirs de l'IA
grilleTirsIA = initialiser_grille('.')
gagneIA = False

# Afficher l'introduction
if platform == "linux":
        system("clear")
else:
        system("cls")
print("Bienvenue dans la Bataille navale!\nEssayez de couler tous les bateaux ennemis!\nPour cela, entrez les coordonnées de vos tirs. Exemple: A7")
n=input("Appuyez sur Entrer pour continuer.")

# Codes spéciaux dans l'input
view="Heart of the sunrise"
# La grille ennemie ne sera visible qu'à l'entrée du string ci-dessus.
b="Brain Salad Surgery"
# Désactive l'autre joueur.
f="Stairway to heaven"
# Fait jouer l'IA deux fois.
m="Dynamite and laser beams"
# Donne la main obligatoirement

# Décide de la main:
priorite = True
if m not in n:
        priorite = random.randint(0,1)
# Boucle principale tant qu'aucun des deux joueurs ne gagne.
if priorite or m in n:
    while (gagne == False) and (gagneIA == False):
        # Nettoyer l'affichage
        if platform == "linux":
                system("clear")
        else:
                system("cls")
        print("Vous avez la main!")
        # Affichage du jeu
        if view in n:
                print("Vision de la grille ennemie activée.")
                afficher_grille(grilleBateauxIA)
                print()
        print("Eaux ennemies:")
        afficher_grille(grilleTirsJ)
        print("Votre Grille:")
        afficher_grille(grilleBateauxJoueur)
        print("Dont partie découverte:")
        afficher_grille(grilleTirsIA)

        # Demander les coordonnées du prochain tir
        (x, y) = prochain_coup()
        while (not tir_valide(grilleTirsJ, x, y)):
                print("Tir invalide!")
                (x, y) = prochain_coup()

        # Effectuer le tir s'il est valide
        tirer(grilleBateauxIA, grilleTirsJ, x, y)
        print("Joueur: ", message)
        sleep(2)
        # Tester les conditions de victoire
        if(partie_finie(grilleTirsJ)):
                gagne = True
                break

        if b not in n:
                k = 1
                if f in n:
                        k = 2
                for i in range(k):

                        # L'IA décide ensuite de son coup, de façon aléatoire (utiliser la fonction maximisant les chances, "le tir croisé", rends le jeu trop dur)
                        (x, y) = random.randint(0, 9), random.randint(0, 9)
                        while (not tir_valide(grilleTirsIA, x, y)):
                                (x, y) = random.randint(0, 9), random.randint(0, 9)

                        # Effectuer le tir s'il est valide
                        tirer(grilleBateauxJoueur, grilleTirsIA, x, y)
                        print("IA: ", message)
                        sleep(2)
                        # Tester les conditions de victoire
                        if(partie_finie(grilleTirsJ)):
                                gagne = True
                                break
else:
    while (gagne == False) and (gagneIA == False):
        # Nettoyer l'affichage
        if platform == "linux":
                system("clear")
        else:
                system("cls")
        print("L'IA a la main")

        if b not in n:
                k = 1
                if f in n:
                        k = 2
                for i in range(k):

                        # L'IA décide ensuite de son coup, de façon aléatoire (utiliser la fonction maximisant les chances, "le tir croisé", rends le jeu trop dur)
                        (x, y) = random.randint(0, 9), random.randint(0, 9)
                        while (not tir_valide(grilleTirsIA, x, y)):
                                (x, y) = random.randint(0, 9), random.randint(0, 9)

                        # Effectuer le tir s'il est valide
                        tirer(grilleBateauxJoueur, grilleTirsIA, x, y)

                        # Tester les conditions de victoire
                        if(partie_finie(grilleTirsJ)):
                                gagne = True
                                break
        # Affichage du jeu
        if view in n:
                print("Vision de la grille ennemie activée.")
                afficher_grille(grilleBateauxIA)
                print()
        print("Eaux ennemies:")
        afficher_grille(grilleTirsJ)
        print("Votre Grille:")
        afficher_grille(grilleBateauxJoueur)
        print("Dont partie découverte:")
        afficher_grille(grilleTirsIA)
        print("IA: ", message)
        sleep(2)
        # Demander les coordonnées du prochain tir
        (x, y) = prochain_coup()
        while (not tir_valide(grilleTirsJ, x, y)):
                print("Tir invalide!")
                (x, y) = prochain_coup()

        # Effectuer le tir s'il est valide
        tirer(grilleBateauxIA, grilleTirsJ, x, y)
        print("Joueur: ", message)
        sleep(2)
        # Tester les conditions de victoire
        if(partie_finie(grilleTirsJ)):
                gagne = True
                break

# En cas de victoire
if gagne:
        print("Vous avez gagné!")
if gagneIA:
        print("Vous avez réussi à perdre!")