
from sys import exit
from time import sleep
import json, os
from random import choice, randint
from colorama import Fore, Style
from itertools import product
import colorama
colorama.init()


#### SAVE
##
CURR_DIR = os.getcwd()
SAVE_DIR = os.path.join(CURR_DIR, "saved_qwixx")
preset_save_files = ["save1.json", "save2.json", "save3.json"]


def save_game(data_to_save, save_file):
    """
    List x Str --> None
    Saves game to a json file
    """
    with open(os.path.join(SAVE_DIR, save_file), "w") as f:
        json.dump(data_to_save, f)


def choose_save_file():
    """
    None --> Str
    Ask player to choose which file to save in
    """
    sleep(1)
    print("Entrez un nombre pour choisir un fichier pour sauvegarder le jeu : ")

    existing_saves = os.listdir(SAVE_DIR)
    save_files = existing_saves

    nb_saves = len(save_files)
    while nb_saves < 3:
        save_files.append(preset_save_files[nb_saves])
        nb_saves += 1

    for index, file in enumerate(save_files):
        print(f"{index + 1}. {file}")

    save_as = input("> ")

    if save_as.isdigit() and 1 <= int(save_as) <= 3:
        index = int(save_as) - 1
        return save_files[index]

    else:
        print("[ERREUR] Commande invalide. \n")
        return choose_save_file()
    

def ask_to_save(data_to_save):
    """
    List --> None
    Save game data and quit game 
    """
    save_file = choose_save_file()
    save_game(data_to_save, save_file)

    # rename file
    new_filename = input("Saisissez un nouveau nom pour le fichier (laissez vide pour utiliser le nom existant) : ")
    if new_filename.strip() != "":
        new_filename += ".json"
        os.rename(os.path.join(SAVE_DIR, save_file), os.path.join(SAVE_DIR, new_filename))
        save_file = new_filename
        save_game(data_to_save, save_file)

    print(f"Jeu sauvegardé ! Vos données : {data_to_save}")
    sleep(1)

    print("Merci d'avoir joué ! \n[Quitter le programme...]")
    sleep(2)
    exit()
##
####






#### LOAD
##
def load_game(save_file):
    """
    Str --> List
    Loads game from json file
    """
    with open(os.path.join(SAVE_DIR, save_file)) as f:
        data_to_save = json.load(f)
    return data_to_save


def choose_load_file():
    """
    None --> Str / None
    Ask player which file to load
    If there is no existing saved game, it starts a new one
    """
    sleep(1)
    print("Entrez un nombre pour choisir un fichier à ouvrir (1-3) :")
    for index, file in enumerate(os.listdir(SAVE_DIR)):
        print(f"{index + 1}. {file}")
    loaded_file = input("> ")

    if loaded_file.isdigit() and 1 <= int(loaded_file) <= 3:
        try:
            index = int(loaded_file) - 1
            filename = os.listdir(SAVE_DIR)[index]
            return filename
        except (IndexError):
            return None

    else:
        print("[ERREUR] Commande invalide. Réessayez. \n")
        return choose_load_file()
    

def ask_to_load():
    """
    None --> Bool
    Ask to load in a existing files
    Returns True if it's possible, False if it isn't
    """
    global data_to_save

    while True:
        load = affiche("Voulez-vous continuer votre jeu précédent (o/n) ? ", ask_input=True)

        if load in ["o", "oui", "non", "n"]:
            break

        print("[ERREUR : Commande invalide] \n")
        sleep(1)

    if load in ["n", "non"]:
        loaded_game = False
        print("Vous commencez une nouvelle partie. \n")

    # if player asks to reload game, if there is a saved game it loads it, otherwise it starts a new game
    elif load in ["o", "oui"]:
        save_file = choose_load_file()

        try:
            data_to_save = load_game(save_file)
            loaded_game = True
            print("Jeu précédent chargé avec succès.")
            print("\n[Mode local avec joueurs]")
        except:
            loaded_game = False
            print("[ERREUR : Aucun jeu précédent trouvé] \nVous commencez une nouvelle partie. \n")
            sleep(1.5)

    return loaded_game


def saved_game_orders():
    """
    None --> List x List
    Returns the order and scores from the previous game
    """
    joueurs, fiches = zip(*data_to_save)

    liste_joueurs = list(joueurs)
    fiche_joueurs = list(fiches)

    return liste_joueurs, fiche_joueurs
##
####






#### PLAYER INITIALISATION
##
# get the name of the players
def get_noms_joueurs():
    """
    None --> Str
    Fonction retournant le nom (str) d'un joueur.
    """
    joueur_nom = None

    while not joueur_nom:
        joueur_nom = input(f"Entrez le nom du joueur {i + 1}: ")

        if joueur_nom in LISTE_JOUEUR:
            print("Ce nom a déjà été pris. Réessayez.")
            joueur_nom = None

    return joueur_nom


def check_user_input(input):
    """
    Str --> Bool
    Fonction retournant True si input est un nombre, False sinon.
    """
    try:
        # Convert it into integer
        int(input)
        return True

    except ValueError:
        try:
            # Convert it into float
            float(input)
            return True

        except ValueError:
            return False


# To get the number of players and their names (game of 2 to 5 players)
def add_player():
    """
    None --> List
    Fonction retournant la liste des joueurs.
    """
    global LISTE_JOUEUR
    global i

    LISTE_JOUEUR = []

    while True:
        number = input("Entrez le nombre de joueurs (2 à 5 joueurs): ")

        if not check_user_input(number):
            print("[ERREUR: Vous devez entrer un nombre]")
            continue

        number_int = int(float(number))
        if 2 <= number_int <= 5:
            break

    for i in range(number_int):
        LISTE_JOUEUR.append(get_noms_joueurs())

    return LISTE_JOUEUR
##
####






#### BASE
##
# if in bot-only mode, it doesn't use the sleep function
def time(tempo = None):
    if full_bot:
        return 0
    
    elif tempo is not None:
        return tempo

    return 0.5
    

# Convert the color into an index number
def indice_couleur(couleur):
    """
    Str --> Int
    Fonction retournant l'indice de la couleur.
    """
    # rouge = 0, jaune = 1, bleu = 2, vert = 3
    return liste_couleur.index(couleur)


def get_dices():
    """
    None --> List
    Fonction qui renvoie une liste contenant les valeurs des dés
    """
    return [randint(1, 6) if x is not None else None for x in liste_couleur]


# active player plays at the end
def playing_order(liste_joueurs, fiche_joueurs, active_player):
    """
    List x List x Str --> List x List
    Renvoie la liste des joueurs où le joueur actif joue après les joueurs passifs
    et la liste de leurs fiches (dans le même ordre)
    """
    # Find active player
    ordre = liste_joueurs.copy()
    fiches = fiche_joueurs.copy()
    active_ind = liste_joueurs.index(active_player)

    # Remove active player
    ordre.remove(active_player)
    active_fiche = fiches.pop(active_ind)

    # Add active player at the end
    ordre.append(active_player)
    fiches.append(active_fiche)

    return ordre, fiches


# Count skip (max 2 skips for penalty)
def count_skip(player_fiche, skip):
    """
    List x Int --> None
    Procédure qui compte le nombre de skip du joueur actif.
    """

    # if active player skip twice
    if skip == 2:
        player_fiche[-1] += 1
        affiche(f"Vous avez passé votre tour 2 fois, vous obtenez une pénalité. | Pénalités: {player_fiche[-1]}.")


# If the line has the locking number in it, it removes the dice
def lock_line(fiche_joueurs):
    """
    List --> None
    Si la ligne est verrouillé, le dé de la ligne est retiré
    """
    for fiche, color_ind in product(fiche_joueurs, range(4)):
        if is_prelocked(fiche, color_ind):
            remove_dice(color_ind)


# When a line is locked, the dice of color is removed
def remove_dice(couleur_ind):
    """
    Int --> None
    Procédure qui enleve un dé de la liste de dés.
    """
    line_color = liste_couleur[couleur_ind]

    if line_color is not None:
        affiche(f"\nLe dé {colored(line_color, line_color)} est retiré du jeu.")
        liste_couleur[couleur_ind] = None


# End conditions & calculates points to announce the winner
def check_end(fiche):
    """
    List --> Bool
    Retourne True si le jeux est terminé, False sinon
    """
    # if someone has 4 penalties
    if fiche[-1] == 4:
        affiche(f"{player_name} a 4 pénalités.")
        return True

    # if 2 lines are locked/ 2 dices are removed
    nones = liste_couleur.count(None)
    if nones == 2:
        affiche("Vous avez enlevez le deuxieme dé coloré.")
        return True
    
    return False


def who_won(fiche_joueurs, noms, tracing_win = {}):
    """
    List x List (x Dict) --> None
    Compte des points et affiche le gagnant
    """
    affiche("Le jeu est terminé. \nLes points sont calculés... \n")
    sleep(time(2))

    points_joueurs = [0 for i in fiche_joueurs]

    for index, player_fiche in enumerate(fiche_joueurs):
        for line_color in player_fiche[:-1]:
            nombre_x = len(line_color)
            points_joueurs[index] += points[nombre_x]

        points_joueurs[index] -= (player_fiche[-1] * 5)

    winner_index = points_joueurs.index(max(points_joueurs))

    affiche(f"Vous avez gagné, {noms[winner_index]} avec {max(points_joueurs)} points.")
    affiche("Merci d'avoir joué ! \n[Quitter le programme...]")

    if full_bot:
        for win in tracing_win :
            if win == noms[winner_index] :
                tracing_win[win] += 1
##
####






#### PROPOSITIONS AND PLAY
## ADD TO DICTIONARIES
#
def add_to_combo_dict(line_color, combo):
    """
    List x Int --> None
    Ajoute la somme d'un dé blanc et un dé coloré dans le dict global proposition
    """
    if combo not in d_proposition[line_color]:
        d_proposition[line_color].append(combo)

def add_to_dict(Dict, key, value):
    """
    Dict x Elem x Elem --> None
    Procédure qui permet d'entrer une valeur à une clée dans un dictionnaire 
    """
    if key in Dict and value not in Dict[key]:
        Dict[key].append(value)

    elif key not in Dict:
        Dict[key] = [value]
##


## ADD TO PROPOSITIONS
# Adds 2 or 12 to the list of propositions if they can be added
def add_special(player_fiche, line_color, dice_value, type=list):
    """
    List x Str x Int (x Type) --> Str / None
    Retourne le couleur de la ligne (ou ajoute des valeurs dans le dictionnaire global proposition)
    avec des possibles placements quand la somme de dés est 2 ou 12
    """
    color_ind = indice_couleur(line_color)

    if is_premier(player_fiche, color_ind, dice_value):
        if type is list:
            return line_color

        add_to_combo_dict(line_color, dice_value)

    elif is_lockable(player_fiche, color_ind, dice_value):
        if type is list:
            return line_color

        add_to_combo_dict(line_color, dice_value)


# Somme: blanc1 + blanc2
def combine_whites(liste_dice):
    """
    List --> Int
    Retourne la somme de dés blancs
    """
    return liste_dice[-2] + liste_dice[-1]


# List of possible placements for the sum of white dices + the sum of the dices
def propose_white(player_fiche, dice_value):
    """
    List x Int --> List
    retourne une liste des couleurs oú la somme des dés blancs peut etre crochée (liste sans proposition si il n'y en a pas)
    """
    lines = []

    for line_color in liste_couleur[:-2]:
        # Check if line_color is locked
        if line_color is None:
            continue

        if dice_value in [12, 2]:
            line = add_special(player_fiche, line_color, dice_value)
            if line is not None:
                lines.append(line)

        # if it's any number {3, 4, 5, 6, 7, 8, 9, 10, 11}
        elif is_playable(player_fiche, indice_couleur(line_color), dice_value):
            lines.append(line_color)

    lines.append(dice_value)

    return lines


# Dictionary of possible placements for the combination of dices
# key = color, value = number that can be placed
def propose_combo(player_fiche, liste_dice):
    """
    List x List --> Dict
    Retourne la dictionnaire des possible placements dans les lignes colorées
    """
    global d_proposition

    d_proposition = {couleur:[] for couleur in liste_couleur[:-2]}
    index = 0

    for white_dice, color_dice in product(liste_dice[-2:], liste_dice[:-2]):
        if color_dice is None:
            index += 1
            if index == 4:
                index = 0
            continue

        line_color = liste_couleur[index]
        combo = white_dice + color_dice

        # if it's [12, 2]
        if combo in [12, 2]:
            add_special(player_fiche, line_color, combo, type=dict)

        # else if it's any other number [3, 4, 5, 6, 7, 8, 9, 10, 11]
        elif is_playable(player_fiche, indice_couleur(line_color), combo):
            add_to_combo_dict(line_color, combo)

        index += 1
        if index == 4:
            index = 0

    return d_proposition
##


## VERIFYING PLAYABILITY
# Check if the number can be crossed on a line
def is_playable(player_fiche, couleur_ind, value):
    """
    List x Int x Int --> Bool
    Fonction retournant True si la valeur est plus grande que la dernière valeur de la ligne, False sinon.
    """
    if player_fiche[couleur_ind] == []:
        return True
    
    # Lignes jaune et rouge.
    if 0 <= couleur_ind <= 1:
        return player_fiche[couleur_ind][-1] < value

    # Lignes bleue et verte.
    return player_fiche[couleur_ind][-1] > value


# If number is 2 or 12, check if it can be placed as first element of the line
def is_premier(player_fiche, couleur_ind, dice_value):
    """
    List x Int x Int --> Bool
    si le joueur veut cocher le premier numéro d'une ligne
    retourne vrai si c'est possible, faux sinon
    """
    if dice_value == 2 and 0 <= couleur_ind <= 1:
        return player_fiche[couleur_ind] == []
    
    elif dice_value == 12 and 2 <= couleur_ind <= 3:
        return player_fiche[couleur_ind] == []


# If number is 2 or 12, check if the line is lockable
def is_lockable(player_fiche, couleur_ind, dice_value):
    """
    List x Int x Int --> Bool
    si le joueur veut cocher le dernier numéro d'une ligne
    retourne vrai si c'est possible, faux sinon
    """
    if dice_value == 12 and 0 <= couleur_ind <= 1:
        return len(player_fiche[couleur_ind]) >= 5
    
    elif dice_value == 2 and 2 <= couleur_ind <= 3:
        return len(player_fiche[couleur_ind]) >= 5


# Check if the line is locked (+5 crossed numbers and lock number is crossed)
def is_prelocked(player_fiche, color_ind):
    """
    List x Int --> Bool
    Fonction retournant True si la ligne comporte 5 cases cochées et le dernier numéro coché.
    """
    # lignes jaune et rouge
    if 0 <= color_ind <= 1 and 12 in player_fiche[color_ind]:
        return True

    # lignes bleue et verte
    return 2 <= color_ind <= 3 and 2 in player_fiche[color_ind]
##


## ADD TO FICHE (PLAY)
# Add crossed number into player_fiche
def ajoute_numero(player_fiche, couleur_ind, value):
    """
    List x Int x Int --> None
    Processus qui permet d'ajouter le numéro coché sur la fiche
    """
    player_fiche[couleur_ind].append(value)


def place_x(player_fiche, propositions, couleur, dice_value=None):
    """
    List x List/Dict x Str (x Int) --> Int
    Demande au joueur de cocher un numéro, le coche si c'est possible et
    retourne skip+1 si le joueur décide de passer son tour
    """
    while True:
        # Pour tous les joueurs (après avoir choisi une ligne)
        if type(propositions) is list:
            dice_value = propositions[-1]

        # Pour joueur actif (2nd round), choisir numéro
        if type(propositions) is dict:
            while dice_value not in propositions[couleur]:
                if len(propositions[couleur]) == 1:
                    dice_value = propositions[couleur][0]
                else:
                    dice_value = affiche("Choisissez un numéro à cocher : ", ask_input=True)

                if dice_value in ["p", "pass"]:
                    affiche("Vous avez décidé de ne pas cocher de numéros.")
                    return 1 # skip + 1

                # error messages
                try:
                    dice_value = int(dice_value)
                except ValueError:
                    affiche("[ERREUR: Entrez un numéro.]")
                    continue
                
                if dice_value not in propositions[couleur]:
                    affiche("[ERREUR: Vous ne pouvez pas cocher ce numéro.]")

        # confirmer le choix
        couleur_ind = indice_couleur(couleur)
        couleur_num = f"{couleur} {dice_value}"

        confirm = affiche(f"Vous allez cocher le {colored(couleur_num, couleur)}. Etes-vous sûr (oui/non/pass) ? ", ask_input=True)

        if confirm in ["oui", "o"]:
            affiche(f"Vous avez coché le {colored(couleur_num, couleur)}.")

            # to lock line if dice_value in [2, 12]
            if dice_value in [2, 12] and is_lockable(player_fiche, couleur_ind, dice_value):
                affiche(f"Vous avez réussi à verrouiller la ligne {colored(couleur, couleur)}.")

            ajoute_numero(player_fiche, couleur_ind, dice_value)
            return 0

        elif confirm in ["pass", "p"]:
            affiche("Vous avez décidé de ne pas cocher de numéros.")
            return 1

        elif confirm in ["non", "n"]:
            if type(propositions) is list: # if is not active player
                return play_white(player_fiche, propositions, placed_x=True)
            return play_color(player_fiche, propositions, placed_x=True)


def play_white(player_fiche, prop_whites, placed_x=False, bot=False):
    """
    List x Int (x Int) --> Int
    Demande à tous les joueurs s'il veut cocher la somme de dés blancs
    Retourne skip+1 si le joueur a décidé de passer ce tour
    """
    affiche("\n[Dés blancs]")
    white_dice = prop_whites[-1]

    if placed_x:
        affiche_proposition(prop_whites)

    # si le joueur ne peut pas jouer, on quitte la fonction
    if len(prop_whites) == 1:
        if not bot or player_name == "Joueur":
            affiche(f"Vous ne pouvez pas cocher {white_dice} dans aucunes des lignes.")
        else:
            affiche(f"{player_name} ne peut pas cocher {white_dice} dans aucunes des lignes.")
        return 1

    # bot turn
    if bot and player_name != "Joueur":
        return strategie_bot(player_fiche, prop_whites)

    # human turn
    # if there is only one line available
    if len(prop_whites) == 2:
        return place_x(player_fiche, prop_whites, prop_whites[0])
    
    # otherwise
    while True:
        couleur = affiche(f"Cochez {white_dice} dans la ligne (couleur/pass) : ", ask_input=True)

        if couleur in prop_whites:
            return place_x(player_fiche, prop_whites, couleur)

        elif couleur in ["pass", "p"]:
            affiche("Vous avez décidé de ne pas cocher de numéros.")
            return 1

        #error messages
        if couleur not in liste_couleur:
            affiche("[ERREUR: Cette couleur de ligne n'existe pas]")
            continue

        elif couleur not in prop_whites:
            affiche("[ERREUR: Vous ne pouvez cocher dans cette ligne]")
            continue
        affiche("[ERREUR: Commande invalide]")


def play_color(player_fiche, prop_color, placed_x=False, bot=False):
    """
    List x Dict (x Bool x Bool) --> Int
    Demande à joueur actif s'il veut cocher la somme d'un dé blanc et d'un dé coloré
    Retourne skip+1 si le joueur a décidé de passer ce tour
    """

    affiche("\n[Dé blanc + Dé couleur]")
    if placed_x:
        affiche_proposition(prop_color)
 
    # si le joueur ne peut pas jouer, on quitte la fonction avec un skip = 1
    if prop_color == {couleur:[] for couleur in liste_couleur[:-2]}:
        if bot and player_name != "Joueur":
            affiche(f"{player_name} ne peut rien cocher dans aucunes des lignes.")
        else:
            affiche(f"Vous ne pouvez rien cocher dans aucunes des lignes.")
        return 1

    # bot turn
    if bot and player_name != "Joueur":
        return strategie_bot(player_fiche, prop_color, played_white=True)

    # human turn
    while True:
        couleur = affiche("Cochez dans la ligne (couleur/pass) : ", ask_input=True)

        if couleur in prop_color:
            return place_x(player_fiche, prop_color, couleur)

        if couleur in ["pass", "p"]:
            affiche("Vous avez décidé de ne pas cocher de numéros.")
            return 1

        #error messages
        elif couleur not in liste_couleur:
            affiche("[ERREUR: Cette couleur de ligne n'existe pas]")
            continue

        elif couleur not in prop_color:
            affiche("[ERREUR: Vous ne pouvez cocher dans cette ligne]")
            continue
        affiche("[ERREUR: Commande invalide]")
##
####






#### AFFICHAGE
## FICHES
#
def affiche_des(liste_dice):
    """
    List --> None
    affiche les valeurs des dés
    """
    # Affiche la valeur des dés blancs
    affiche(f"\nLes dés blancs: blanc1({liste_dice[-2]}) blanc2({liste_dice[-1]})")

    # Affiche la valeur des dés colorés
    affiche("Les dés colorés:", ask_end=" ")
    for couleur, dice_value in zip(liste_couleur[:-2], liste_dice):
        if couleur is not None:
            color_value = (f"{couleur}({dice_value})")
            affiche(f"{colored(color_value, couleur)}", ask_end=" ")
    affiche("")


def affiche_proposition(proposition):
    """
    List / Dict --> None
    affiche les lignes et nombres cochable
    """
    if type(proposition) is list:
        if len(proposition) == 1:
            return # on quitte la fonction
        
        aff_proposition = [colored(couleur, couleur) for couleur in proposition[:-1]]

        affiche(f"Vous pouvez cocher {proposition[-1]} dans : {', '.join(str(color) for color in aff_proposition)}.")
        
        return

    for color in proposition:
        if proposition[color] != [] and color is not None:
            print(f"Ligne {colored(color, color)} : {', '.join(map(str, proposition[color]))}")


def colored(str, color):
    """
    Int x Str --> None
    Fonction qui retourne un texte donnée en texte colorié.
    """
    # texte rouge
    if color == "rouge" or color == "r" :
        return (f"{Fore.RED}{str}{Style.RESET_ALL}")

    # texte jaune
    elif color == "jaune" or color == "j" :
        return (f"{Fore.YELLOW}{str}{Style.RESET_ALL}")

    # texte bleu
    elif color == "bleu" or color == "b" :
        return (f"{Fore.BLUE}{str}{Style.RESET_ALL}")

    # texte vert
    return (f"{Fore.GREEN}{str}{Style.RESET_ALL}")


def create_fiche(reverse=False):
    """
    Bool --> Generator
    Generateur qui crée une liste de nombre pour la fiche à afficher.
    """
    if not reverse:
        for n in range(2, 13):
            if n != 2 and n != 12:
                yield " "
            elif n == 2:
                yield "2 "
            elif n == 12:
                yield "12"

    else:
        for n in range(12, 1, -1):
            if n != 2 and n != 12:
                yield " "
            if n == 12:
                yield "12"
            if n == 2:
                yield " 2"


def update_fiche(fiche, player_fiche, index=0):
    """
    List x List (x Int) --> None
    Procédure qui ajoute des 'x' aux cases cochés dans fiche à afficher.
    """
    for fiche_couleur in player_fiche[:-1]:
        if fiche_couleur == []:
            index += 1
            continue

        for value in fiche_couleur:
            if 0 <= index <= 1:
                if value == 2:
                    fiche[index][value - 2] = "x "
                elif value == 12:
                    fiche[index][value - 2] = " x"
                else:
                    fiche[index][value - 2] = "x"

            else:
                if value == 2:
                    fiche[index][12 - value] = " x"
                elif value == 12:
                    fiche[index][12 - value] = "x "
                else:
                    fiche[index][12 - value] = "x"

        index += 1


def affiche_fiche(fiche):
    """
    List --> None
    Procédure qui affiche la fiche du joueur.
    """
    for index, fiche_couleur in enumerate(fiche):
        firstcolor_letter = LISTE_COULEUR[index][0]

        print(f"{colored(firstcolor_letter, firstcolor_letter)} |", end="")

        for case in fiche_couleur:
            print(f" {case} |", end="")

        if liste_couleur[index] == None:
            print(" fermée")
        else:
            print()
##


## TEXT
#
def affiche(texte, ask_input=False, ask_end=None):
    """
    Str (x Bool x Bool) --> Elem (si ask_input est vrai, None sinon)
    Fonction permettant l'affichage et la demande d'input.
    """
    if full_bot:
        return

    # if input()
    if ask_input:
        ask = normalise_input(input(texte))
        return ask

    # if print(str, end="")
    if ask_end is not None:
        print(texte, end=ask_end)

    # print(str) standard
    else:
        print(texte)


def normalise_input(text):
    """
    Str --> Str
    Returns the copy of 'text' in lower case and without accidental spaces
    """
    return text.strip().lower()


def affiche_texte_actif(prop_whites, prop_color, bot_message=False):
    """
    List x Dict (x Bool) --> None
    Procédure qui permet d'afficher des messages pour le joueur actif.
    """
    if bot_message:
        affiche_proposition(prop_whites)
        sleep(time())

        if len(prop_whites) > 1:
            affiche(f"En plus, {player_name} peut combiner un dé blanc avec un dé coloré.")
            affiche_proposition(prop_color)
            sleep(time())

        else:
            affiche(f"{player_name} peut combiner un dé blanc avec un dé coloré.")
            affiche_proposition(prop_color)
            sleep(time())

    else:
        affiche_proposition(prop_whites)
        sleep(time())
        if len(prop_whites) > 1:
            affiche("En plus, vous pouvez combiner un dé blanc avec un dé coloré.")
            affiche_proposition(prop_color)
            sleep(time())

        else:
            affiche(f"Vous pouvez combiner un dé blanc avec un dé coloré.")
            affiche_proposition(prop_color)
            sleep(time())
##
####






#### BOT GAME
##
# dictionnaire stockant le nom des IA
difficultes = {"facile" : ["Roland", "Paul", "Norn", "Percy", "Musashi"], "moyen" : ["Jordan", "Eris", "Aisha", "Geese", "Elinalise"]}


def get_bot_difficulty():
    """
    None --> Str x Str
    Fonction retournant la difficulté du bot et son nom
    """
    while True:
        print(f"Entrez la difficulté du bot {[niveau for niveau in difficultes]}")
        level = normalise_input(input("> "))

        if level in difficultes:
            return level

        affiche(f"Cette difficulté n'existe pas. Les difficultés disponibles sont: \n{[niveau for niveau in difficultes]}\n")


def check_placed_Xs(starting_num, placed_Xs):
    """
    Int x List -> Int 
    Fonction retournant le dernier numéro coché de la ligne
    """
    try:
        last_x = placed_Xs[-1]
    except IndexError:
        last_x = starting_num
    
    return last_x


def strategie_bot(player_fiche, proposition, white_dice=None, played_white=False):
    """
    List x List/Dict (x Int x Bool) --> Functions
    Executes all the actions of the bot
    """
    # strategie 1: random
    if level == "facile":
        if type(proposition) is list:
            return bot_facile_white(player_fiche, proposition)
        return bot_facile_color(player_fiche, proposition) 

    # strategie 2: ecart 1 ou 2
    elif level == "moyen":
        if type(proposition) is list:
            return bot_moyen_white(player_fiche, proposition)
        return bot_moyen_color(player_fiche, proposition)
    
    #strategie 3: optimal crossing for active_player (PAS CODER)
    #elif level == "difficile":
    #    if player_name == active_player:
    #        return bot_difficile_active(player_fiche, played_white, white_dice)
    #   return bot_moyen_white(player_fiche, proposition)


def place_x_bot(player_fiche, propositions, couleur, dice_value=0):
    """
    List x List/Dict x Int (x Str) --> Int
    Demande au joueur de cocher un numéro, le coche si c'est possible et
    retourne skip+1 si le joueur decide de passer son tour
    """

    # Choisir la ligne pour cocher la somme des blancs
    if type(propositions) is list:
        dice_value = propositions[-1]
        couleur_num = f"{couleur} {dice_value}"
        affiche(f"{player_name} a coché le {colored(couleur_num, couleur)}.")
        sleep(time(1))

    # Pour joueur actif in his second round, same as above
    else:
        couleur_num = f"{couleur} {dice_value}"
        affiche(f"{player_name} a coché le {colored(couleur_num, couleur)}.")

    couleur_ind = indice_couleur(couleur)

    if dice_value in [2, 12] and is_lockable(player_fiche, couleur_ind, dice_value):
        affiche(f"Vous avez réussi à verrouiller la ligne {colored(couleur, couleur)}.")

    ajoute_numero(player_fiche, couleur_ind, dice_value)


## [FACILE]
# [FACILE] chooses line and places the sum of whites
def bot_facile_white(player_fiche, prop_whites):
    """
    List x List --> Int
    Chooses into which line should the bot place an X and places it (for the sum of the white dices)
    returns the number of skips
    """
    chosen_color = choice(prop_whites[:-1] + ["pass"])

    if chosen_color in prop_whites :
        place_x_bot(player_fiche, prop_whites, chosen_color)
        return 0

    affiche(f"{player_name} a décidé de ne pas cocher de numéros.")
    return 1


# [FACILE] chooses line and places the sum of the white+color
def bot_facile_color(player_fiche, prop_color):
    """
    List x Dict --> Int
    chooses into which line should the bot place an X and places it (from the white-color combos)
    returns the number of skips
    """
    liste_couleur_dict = [couleur for couleur in prop_color if prop_color[couleur] != []]
    chosen_color = choice(liste_couleur_dict + ["pass"])

    if chosen_color in prop_color :
        choosen_number = choice(prop_color[chosen_color]) #choice un nombre possible sur la ligne
        place_x_bot(player_fiche, prop_color, chosen_color, choosen_number)
        return 0
    
    affiche(f"{player_name} a décidé de ne pas cocher de numéros.")
    return 1
##


## [MOYEN]
# [MOYEN] chooses line color for sum of whites
def white_line_bot_moyen(player_fiche, prop_whites, dice_value):
    """
    List x List x Int --> Str
    Chooses which line the sum of the white dices should be placed on
    Returns the colour of the line
    """
    proposition_valable = []

    for color in prop_whites[:-1]:
        if color in ["rouge", "jaune"]:
            color_ind = indice_couleur(color)
            placed_Xs = player_fiche[color_ind]
            last_x = check_placed_Xs(2, placed_Xs)

            # best choice
            if (placed_Xs == [] and dice_value == 2) or (placed_Xs != [] and last_x == dice_value - 1): 
                return color
                
            elif (placed_Xs == [] and dice_value == 3) or (placed_Xs != [] and last_x == dice_value - 2):
                proposition_valable.append(color)
            continue
        
        # bleu et vert
        color_ind = indice_couleur(color)
        placed_Xs = player_fiche[color_ind]
        last_x = check_placed_Xs(12, placed_Xs)

        # best choice
        if (placed_Xs == [] and dice_value == 12) or (placed_Xs != [] and last_x == dice_value + 1): 
            return color
            
        elif (placed_Xs == [] and dice_value == 11) or (placed_Xs != [] and last_x == dice_value + 2):
            proposition_valable.append(color)
    
    # if no good options, then pass
    if proposition_valable == []:
        return "pass"
    
    return choice(proposition_valable)


# [MOYEN] chooses line color for combos 
def combo_line_bot_moyen(player_fiche, prop_color):
    """
    List x Dict --> Str x Int
    Fonction retournant le meilleur la meilleur ligne et le meilleur numéro de la ligne.
    """
    proposition_valable = dict()

    for color in prop_color:
        color_index = indice_couleur(color)
        placed_Xs = player_fiche[color_index]
        possible_Xs = prop_color[color]

        for dice_value in possible_Xs:
            if color in ["rouge", "jaune"]:    
                last_x = check_placed_Xs(2, placed_Xs)

                # best choice
                if (placed_Xs == [] and dice_value == 2) or (placed_Xs != [] and last_x == dice_value - 1): 
                    return color, dice_value
                    
                elif (placed_Xs == [] and dice_value == 3) or (placed_Xs != [] and last_x == dice_value - 2):
                    add_to_dict(proposition_valable, color, dice_value)
                continue
        
            # vert et bleu
            last_x = check_placed_Xs(12, placed_Xs)

            # best choice
            if (placed_Xs == [] and dice_value == 12) or (placed_Xs != [] and last_x == dice_value + 1): 
                return color, dice_value
            
            elif (placed_Xs == [] and dice_value == 11) or (placed_Xs != [] and last_x == dice_value + 2):
                add_to_dict(proposition_valable, color, dice_value)

    # if no good options, pass
    if proposition_valable == {}:
        return "pass", None
    
    couleur = choice(list(proposition_valable.keys()))
    dice_value = proposition_valable[couleur][0]
    return couleur, dice_value


# [MOYEN] places the sum of whites in chosen line
def bot_moyen_white(player_fiche, prop_whites):
    """
    List x List --> Int
    Places the sum of white dices in the chosen color
    Returns the number of skips
    """
    dice_value = prop_whites[-1]
    chosen_color = white_line_bot_moyen(player_fiche, prop_whites, dice_value)
    
    if chosen_color in prop_whites:
        place_x_bot(player_fiche, prop_whites, chosen_color)
        return 0
    
    affiche(f"{player_name} a décidé de ne pas cocher de numéros.")
    return 1


# [MOYEN] places the chosen sum (of combo) in the chosen line
def bot_moyen_color(player_fiche, prop_color):
    """
    List x Dict --> Int
    Places an X on the chosen line and number (from the white-color combos)
    Returns the number of skips
    """
    chosen_color, chosen_number = combo_line_bot_moyen(player_fiche, prop_color)
    
    if chosen_color == "pass" :
        affiche(f"{player_name} a décidé de ne pas cocher de numéros.")
        return 1
    
    place_x_bot(player_fiche, prop_color, chosen_color, chosen_number)
    return 0
##
####





#### STATISTIQUES
##
def get_nb_parties():
    """
    None --> Int
    Tests if the input for the number of games was integer and returns the value 
    """
    while True:
        nb_parties = input("Entrez le nombre de parties que les bots vont jouer : ")

    # error messages
        try:
            nb_parties = int(nb_parties)
        except ValueError:
            print("[ERREUR: Entrez un numéro.]")
            continue
        
        return nb_parties


def most_line_lock(line_lock):
    """
    Dict --> List
    Retourne la liste des couleurs les plus verrouillées
    """
    max = line_lock["rouge"]
    for value in line_lock.values():
        if value > max:
            max = value

    if max != 0:
        return [key for key, val in line_lock.items() if val == max]
        

def most_cause_final(penalite, ligne_verrouille) :
    """
    :param penalite: int
    :param ligne_verrouille: int
    :return: str
    Retourne la fin le plus probable
    """
    if max(penalite, ligne_verrouille) == ligne_verrouille :
        return "La fin la plus probable est dû aux verrouillages de lignes."
    return "La fin la plus probable est dû aux pénalités."


def average_round(tours_moyen, nb_parties):
    """
    :param liste_nb_tours: int
    :return: float
    Retourne le moyen de tours
    """
    return tours_moyen / nb_parties
##
####






#### Notes et problèmes ####
##
# Les éléments primaires sont: la fiche du joueur, les dés (2w, 1r, 1g, 1b, 1y),
# Les éléments secondaires sont: les conditions d'arrêt, cocher une case de la fiche, les conditions pour pouvoir cocher une case, sélection de personnage, tour par tour, pénalités, active_player

# fiche_player: liste de listes, chaque liste correspond à une ligne de la fiche, dans chacune de ces liste on trouve les numéros déjá cochés. La pénalité (int) est le dernier élément de la liste.

# variables globals: active_player, player_name, proposition, LISTE_JOUEUR, i, level, full_bot, data_to_save, LISTE_COULEUR, points

# mode_dev: for inputting dice values manually
## input 6 numbers divided by space

##
####


def mode_dev():
    """
    None --> List
    Fonction qui permet d'obtenir la liste de dé souhaitée
    """
    dice_value = [int(x) for x in input("Entrez 6 dés (rjbv/b1b2): ").split(" ")]
    return dice_value


# setup
LISTE_COULEUR = ["rouge", "jaune", "bleu", "vert", "blanc1", "blanc2"]

points = {
    0: 0,
    1: 1,
    2: 3,
    3: 6,
    4: 10,
    5: 15,
    6: 21,
    7: 28,
    8: 36,
    9: 45,
    10: 55,
    11: 66,
    12: 75
}


#### MAIN ####
def game_no_bot(loaded_game):
    global active_player, player_name, liste_couleur
    global data_to_save

    print("\n======================")
    print("     JEU DU QWIXX")
    print("======================\n")

    affiche("[Pour sauvegarder, tapez SAVE ou SAUVEGARDER avant de lancer les dé.]\n")
    sleep(time())

    # [Initialisation]
    if loaded_game:
        liste_joueurs, fiche_joueurs = saved_game_orders()

    else:
        liste_joueurs = add_player()
        fiche_joueurs = [[[], [], [], [], 0] for joueur in liste_joueurs]
    
    data_to_save = list(zip(liste_joueurs, fiche_joueurs))
    liste_couleur = LISTE_COULEUR.copy()

    affiche(f"\nVous pouvez commencer! Ordre de lancer: {liste_joueurs} \n")

    # Start
    mode = affiche("mode dev (o/n)? ", ask_input=True)

    running = True
    while running:
        for active_player in liste_joueurs:
            affiche(f"\n\n[Tour de lancer: {active_player}]")

            # Trow dice
            if mode == "o":
                liste_dice = mode_dev()

            else:
                start_round = affiche("Appuyer sur ENTER pour lancer le dé: ", ask_input=True)
                # to save game
                if start_round in ["save", "sauvegarder"]:
                    ask_to_save(data_to_save)

                liste_dice = get_dices()

            # Additionner les dés blancs et affiche la valeur des dés
            affiche_des(liste_dice)
            white_dice = combine_whites(liste_dice)

            # set up ordre_joueur
            ordre_joueur, ordre_fiche = playing_order(liste_joueurs, fiche_joueurs, active_player)
            sleep(time(1))

            # Play
            for player_num, player_name in enumerate(ordre_joueur):
                if player_name == active_player:
                    print(f"\n\n  [ actif: {player_name} ]")
                else:
                    print(f"\n\n  [ passif: {player_name} ]")

                # set up player_fiche
                player_fiche = ordre_fiche[player_num]
                fiche = [list(create_fiche()) for i in range(2)] + [list(create_fiche(reverse=True)) for i in range(2)]

                # update and affiche fiche
                update_fiche(fiche, player_fiche)
                affiche_fiche(fiche)

                # propositions white and color combo
                prop_whites = propose_white(player_fiche, white_dice)
                prop_color = propose_combo(player_fiche, liste_dice)

                if player_name == active_player :
                    affiche_texte_actif(prop_whites, prop_color)

                    nb_skip = play_white(player_fiche, prop_whites)

                    if nb_skip == 0 :
                        prop_color = propose_combo(player_fiche, liste_dice)
                        placed_x = True
                    else:
                        placed_x = False

                    nb_skip += play_color(player_fiche, prop_color, placed_x)

                else :
                    sleep(time())
                    affiche_proposition(prop_whites)
                    nb_skip = play_white(player_fiche, prop_whites)

                # check penalties
                count_skip(player_fiche, nb_skip)

            # if a line was locked, remove its dice
            lock_line(fiche_joueurs)

            # check end conditions
            if check_end(player_fiche):
                running = False
                break

            data_to_save = list(zip(ordre_joueur, ordre_fiche))

    # Calcul et affiche le vainqueur
    who_won(fiche_joueurs, ordre_joueur)
    sleep(time(3))
    exit()




def game_with_bot():
    global active_player, player_name, level, liste_couleur
    
    print("\n======================")
    print("     JEU DU QWIXX")
    print("======================\n")

    # [Initialisation]
    level = get_bot_difficulty()
    bot_name = choice(difficultes[level])
    liste_joueurs = ["Joueur", bot_name]
    fiche_joueurs = [[[], [], [], [], 0] for joueur in liste_joueurs]
    liste_couleur = LISTE_COULEUR.copy()

    affiche(f"Vous allez jouer contre {liste_joueurs[1]}.")
    affiche(f"\nVous pouvez commencer! Ordre de lancer: {liste_joueurs} \n")

    # Start
    mode = affiche("mode dev (o/n)? ", ask_input=True)

    running = True
    while running:
        for active_player in liste_joueurs :
            affiche(f"\n\n[Tour de lancer: {active_player}]")

            # Trow dice

            if mode == "o":
                liste_dice = mode_dev()

            else:
                if active_player == "Joueur" :
                    input("Appuyer sur ENTER pour lancer le dé: ")
                liste_dice = get_dices()
                sleep(time())

            # Addition les dés blancs et affiche la valeur des dés
            affiche_des(liste_dice)
            white_dice = combine_whites(liste_dice)

            # set up ordre_joueur
            ordre_joueur, ordre_fiche = playing_order(liste_joueurs, fiche_joueurs, active_player)
            sleep(time(1))

            # Play
            for player_num, player_name in enumerate(ordre_joueur):
                if player_name == active_player:
                    print(f"\n\n  [ actif: {player_name} ]")
                else:
                    print(f"\n\n  [ passif: {player_name} ]")

                # set up player_fiche
                player_fiche = ordre_fiche[player_num]
                fiche = [list(create_fiche()) for i in range(2)] + [list(create_fiche(reverse=True)) for i in range(2)]

                # update et affiche fiche
                update_fiche(fiche, player_fiche)
                affiche_fiche(fiche)

                # propositions
                prop_whites = propose_white(player_fiche, white_dice)
                prop_color = propose_combo(player_fiche, liste_dice)
                
                if player_name == active_player :
                    if player_name == "Joueur":
                        affiche_texte_actif(prop_whites, prop_color)

                    else:
                        affiche_texte_actif(prop_whites, prop_color, bot_message=True)

                    nb_skip = play_white(player_fiche, prop_whites, prop_color, bot=True)

                    if nb_skip == 0 :
                        prop_color = propose_combo(player_fiche, liste_dice)
                        placed_x = True
                    else:
                        placed_x = False

                    nb_skip += play_color(player_fiche, prop_color, placed_x, bot=True)

                else: 
                    sleep(time())
                    affiche_proposition(prop_whites)
                    nb_skip = play_white(player_fiche, prop_whites, bot=True)

                # check penalties
                count_skip(player_fiche, nb_skip)

            # if a line was locked, remove its dice
            lock_line(fiche_joueurs)

            # check end conditions
            if check_end(player_fiche):
                running = False
                break

    # Calcul et affiche le vainqueur
    who_won(fiche_joueurs, ordre_joueur)
    sleep(time())
    exit()




def game_full_bot():
    global active_player, player_name, level, liste_couleur

    print("\n======================")
    print("     JEU DU QWIXX")
    print("======================\n")

    # [Initialisation]
    liste_joueurs = ["bot1", "bot2", "bot3", "bot4", "bot5"]
    nb_parties = get_nb_parties()
    tracing_win = {}

    for i in liste_joueurs :
        tracing_win[i] = 0

    level = get_bot_difficulty()
    print()

    line_lock = {"rouge" : 0, "jaune" : 0, "bleu" : 0, "vert" : 0}
    nb_tours = 0
    penalite = 0
    ligne_verrouillee = 0
    
    for nb in range(nb_parties):
        fiche_joueurs = [[[], [], [], [], 0] for joueur in liste_joueurs]
        liste_couleur = LISTE_COULEUR.copy()
        locked_lines_in_round = 0

        # Start
        running = True
        while running:
            for active_player in liste_joueurs:
                # count rounds
                nb_tours += 1

                # Trow dice
                liste_dice = get_dices()

                # Addition les dés blancs et affiche la valeur des dés
                white_dice = combine_whites(liste_dice)

                # set up ordre_joueur
                ordre_joueur, ordre_fiche = playing_order(liste_joueurs, fiche_joueurs, active_player)

                # Play
                for player_num, player_name in enumerate(ordre_joueur):
                    # set up player_fiche
                    player_fiche = ordre_fiche[player_num]

                    # propositions
                    prop_whites = propose_white(player_fiche, white_dice)
                    prop_color = propose_combo(player_fiche, liste_dice)

                    if player_name == active_player:
                        nb_skip = play_white(player_fiche, prop_whites, bot=True)

                        if nb_skip == 0:
                            prop_color = propose_combo(player_fiche, liste_dice)
                        nb_skip += play_color(player_fiche, prop_color, bot=True)
                    
                    else: 
                        nb_skip = play_white(player_fiche, prop_whites, bot=True)

                    # check penalties
                    count_skip(player_fiche, nb_skip)

                # if a line was locked, remove its dice
                lock_line(fiche_joueurs)

                # check end conditions
                if check_end(player_fiche):
                    running = False
                    break
        
        # verify number of locked lines
        # count +1 if the game ended bc 2 lines were closed
        for index, color in enumerate(liste_couleur[:-2]):
            if color is None:
                og_color = LISTE_COULEUR[index]
                line_lock[og_color] += 1
                locked_lines_in_round += 1
        if locked_lines_in_round >= 2:
            ligne_verrouillee += 1
        #print(f"nb of locked lines in round: {locked_lines_in_round}")
        #print(f"lock_line counter: {ligne_verrouillee}")
        #print(f"colours to check locked lines: {liste_couleur[:-2]}")

        # count penalities
        # counts 1 at the first penality
        for fiche in fiche_joueurs:
            #print(f"fiches check penalty: {fiche}") # to verify the player_fiches: if penality was really 4 and/or number of locked lines add up
            if fiche[-1] == 4:
                penalite += 1
                break
        

        # Calcul et affiche le vainqueur
        who_won(fiche_joueurs, ordre_joueur, tracing_win)

    for bot in tracing_win :
        print(f"Nombre de partie gagnée {bot}: {tracing_win[bot]}")

    # line with the most locks
    #print(f"\ndict of which line was locked how many times: {line_lock}") # to verify that most_line_lock has the right output
    if most_line_lock(line_lock) is not None:
        print(f"\nLa ligne la plus verrouillée est la/les ligne/s {most_line_lock(line_lock)}. \n")
    
    else:
        print("Aucune des lignes n'a été verrouillées. \n")

    # penality vs lines locked
    print(f"Nombre de matchs qui se sont terminés à cause de pénalités: {penalite}")
    print(f"Nombre de jeux qui se sont terminés parce que les lignes étaient verrouillées: {ligne_verrouillee}")
    print(most_cause_final(penalite, ligne_verrouillee))
    print()

    print(f"Le nombre de tour moyen est de {average_round(nb_tours, nb_parties)} tours.")

    exit()


## choose game mode
def choice_gamemode():
    global full_bot

    # ask if player wants to load previous game
    full_bot = False
    loaded_game = ask_to_load()

    if loaded_game:
        affiche("\n")
        game_no_bot(loaded_game)

    # ask gamemodes
    while True:
        affiche("(1) Mode local avec joueurs\n(2) Mode solo avec bots\n(3) Mode uniquement bots")

        game_mode = input("Entrez un mode de jeu : ").strip()

        if game_mode in ["1", "2", "3"]:
            break

        affiche("[ERREUR : Ce mode ne fait pas partie des modes de jeu]\n")

    sleep(time(1))
    if game_mode == "1":
        affiche("\n\n[Mode local avec joueurs]")
        game_no_bot(loaded_game)

    elif game_mode == "2":
        affiche("\n\n[Mode solo avec bots]")
        game_with_bot()

    else:
        affiche("\n\n[Mode uniquement bots]")
        full_bot = True
        game_full_bot()


# Commandes start
choice_gamemode()