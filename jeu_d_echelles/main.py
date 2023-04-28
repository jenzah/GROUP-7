
from sys import exit
import random, json, os
from time import sleep


#### SAVE
##
CURR_DIR = os.getcwd()
SAVE_DIR = os.path.join(CURR_DIR, "saved_jeu_d_echelles")
preset_save_files = ["save1.json", "save2.json", "save3.json"]

def save_game(data_to_save, save_file) :
    """
    List x Str --> None
    Saves game to a json file
    """
    with open(os.path.join(SAVE_DIR, save_file), "w") as f:
        json.dump(data_to_save, f)


def choose_save_file() :
    """
    None --> Str
    Ask player to choose which file to save in
    """
    sleep(1)
    print("Entrez un nombre pour choisir un fichier pour sauvegarder le jeu : ")
    
    existing_saves = os.listdir(SAVE_DIR)
    save_files = existing_saves
    
    nb_saves = len(save_files)
    while nb_saves < 3 :
        save_files.append(preset_save_files[nb_saves])
        nb_saves += 1

    for index, file in enumerate(save_files):
        print(f"{index+1}. {file}")

    save_as = input("> ")

    if save_as.isdigit() and 1 <= int(save_as) <= 3 :
        index = int(save_as) - 1
        return save_files[index]
    
    else :
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


def choose_load_file() :
    """
    None --> Str / None
    Ask player which file to load
    If there is no existing saved game, it starts a new one
    """
    sleep(1)
    print("Entrez un nombre pour choisir un fichier à ouvrir (1-3) :")
    for index, file in enumerate(os.listdir(SAVE_DIR)):
        print(f"{index+1}. {file}")
    loaded_file = input("> ")
    
    if loaded_file.isdigit() and 1 <= int(loaded_file) <= 3 :
        try:
            index = int(loaded_file) - 1
            filename = os.listdir(SAVE_DIR)[index]
            return filename
        except (IndexError):
            return None
    
    else: 
        print("[ERREUR] Commande invalide. Réessayez. \n")
        return choose_load_file()


def ask_to_load() :
    """
    None --> Bool
    Ask to load in a existing files
    Returns True if it's possible, False if it isn't
    """
    global data_to_save

    while True:
        load = input("Voulez-vous continuer votre jeu précédent (o/n) ? ")

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
    player_name, player_pos, count_tour = zip(*data_to_save)

    if all(x == count_tour[0] for x in count_tour):
        ordre_joueur = list(player_name)
        score_joueur = list(player_pos)

    else:
        new_ordre = []
        players = len(data_to_save)

        if len(new_ordre) != players:
            # new order of players --> those who didn't finish their round in the previous game go first
            # still according to the original order
            new_ordre = [data_to_save[n] for n in range(1, players) if count_tour[0] != count_tour[n]]
            new_ordre.extend(x for x in data_to_save if x not in new_ordre)
            new_ordre = [list(t) for t in zip(*new_ordre)]
            ordre_joueur = new_ordre[0]
            score_joueur = new_ordre[1]

    print(f"Dans votre derniere partie, {ordre_joueur} ont joué.")

    for n in range(len(ordre_joueur)):
        print(f"{ordre_joueur[n]} a été sur le case : {score_joueur[n]}")
    print()
    
    return ordre_joueur, score_joueur
##
####






#### PLAYER INITIALISATION
##
# get the name of the players
def get_noms_joueurs():
    """
    None -> Str
    Fonction retournant le nom (str) d'un joueur.
    """
    joueur_nom = None

    while not joueur_nom:
        joueur_nom = input(f"Entrez un nom du joueur {i + 1}: ")

        if joueur_nom in LISTE_JOUEUR:
            affiche("Ce nom a déjà été pris. Réessayez.")
            joueur_nom = None

    return joueur_nom


def check_user_input(input):
    """
    Str -> Bool
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


# To get the number of player and their names (game of 2 to 4 players)
def select_players():
    """
    None -> List
    Fonction retournant la liste des joueurs.
    """
    global LISTE_JOUEUR
    global i

    LISTE_JOUEUR = []

    while True:
        number = affiche("Entrez le nombre de joueur (2 à 4 joueurs): ", ask_input=True)
        if not check_user_input(number):
            affiche("[ERREUR : Vous devez entrez un nombre]")
            continue

        number_int = int(float(number))
        if 2 <= number_int <= 4:
            break

    for i in range(number_int):
        LISTE_JOUEUR.append(get_noms_joueurs())

    return LISTE_JOUEUR


def verif_doublons(pack):
    """
    List --> Bool
    Fonction retournant True si la liste comporte des doublons, False sinon.
    """
    for index, couple in enumerate(pack):
        for couple2 in pack[index + 1:]:
            if couple[1] in couple2:
                return True
    return False


def player_doublons(pack):
    """
    List --> List
    Fonction retournant la liste des joueurs avec un doublons de dé.
    """
    numbers = []
    players = []
    players_doublons = []

    # To unpack the package (player, number)
    players, numbers = zip(*pack)

    # To find players with doublons
    for index, number in enumerate(numbers):
        if number in numbers[index + 1:] or number in numbers[:index]:
            players_doublons.append(players[index])

    return players_doublons


def decide_order(player_doublons, bots=False):
    """
    List --> List
    Fonction retournant l'ordre des joueurs sur un lancé de dé.
    """
    global sorted_tuples

    dict = {}
    order = []

    for player in player_doublons:
        affiche(f"\n[{player}]")

        if bots and player == "Joueur":
            affiche("Lancez votre dé !")
            affiche("Appuyer sur ENTER pour lancer le dé : ", ask_input=True)
            dict[player] = dice_base()

        elif not bots:
            print(f"Lancez votre dé {player} !")
            affiche("Appuyer sur ENTER pour lancer le dé : ", ask_input=True)
            dict[player] = dice_base()

        else:
            affiche(f"Lancez votre dé {player} !")
            dict[player] = dice_base()

    sorted_tuples = sorted(dict.items(), key=lambda item: item[1], reverse=True)

    for key, value in sorted_tuples:
        order.append(key)

    return order


def print_player_doublons(player_doublons):
    """
    List --> None
    Prints messages when players had the same dice value when throwing to decide order
    """
    n = len(player_doublons)

    if n == 2:
        affiche(f"\n[Départagez-vous {player_doublons[0]} et {player_doublons[1]}!]")

    elif n == 3:
        affiche(f"\n[Départagez-vous {player_doublons[0]}, {player_doublons[1]} et {player_doublons[2]}!]")

    else:
        affiche(f"\n[Départagez-vous {player_doublons[0]}, {player_doublons[1]}, {player_doublons[2]} et {player_doublons[3]}!]")


def doublons_exception(player_double):
    """
    List --> List
    Fonction retournant le vrai ordre des joueurs dans le cas exceptionnel quand il y a plusieurs doublons (ex: 2, 2, 4, 4)
    """
    global sorted_tuples

    print(f"\n[Départagez-vous {player_double1[0]} et {player_double1[1]}, {player_double2[2]} et {player_double2[3]} !]")

    player_double1 = [player_double[0], player_double[1]]
    player_double2 = [player_double[2], player_double[3]]

    order_doublons1 = decide_order(player_double1)
    player_liste = sorted_tuples
    order_doublons2 = decide_order(player_double2)
    player_liste.append(sorted_tuples)
    sorted_tuples = player_liste

    return order_doublons1 + order_doublons2


def who_starts(liste_joueurs, bots = False):
    """
    List -> List
    Fonction retournant la liste de joueur dans l'ordre du joueur qui a lancé le plus grand nombre dé.
    """
    # Decide order #1
    order = decide_order(liste_joueurs, bots)

    while True:
        # Check doublons
        if verif_doublons(sorted_tuples):
            player_double = player_doublons(sorted_tuples)

            # Cas exceptionnel: quand il y a plusieurs doublons (ex: 2, 2, 4, 4)
            if len(player_double) == 4 and sorted_tuples[0][1] != sorted_tuples[-1][1] and sorted_tuples[1][1] != sorted_tuples[-2][1]:
                order = doublons_exception(player_double)
                continue

            # Decide order #2
            print_player_doublons(player_double)
            order_doublons = decide_order(player_double, bots)

            n = len(order_doublons)
            # Change order
            for i in range(len(order) - 1):
                if set(order[i: i + n]) == set(order_doublons):
                    for count, x in enumerate(order_doublons):
                        order[i + count] = x

        else:
            break

    return order
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


# starting dice
def dice_base():
    """
    None --> Int
    Retourne la valeur du dé
    """
    dice_value = random.randint(1, 6)
    affiche(f"dé : {dice_value}")

    return dice_value


def play(score_joueur, relances, bots=False):
    """
    Int x Int (x Bool) --> Int x Bool
    Executes all the conditions for moving the pawn of the player
    If the player threw a 6, they can rethrow the dice 2 more times (3 in total) 
    Retourne le score du joueur, et True si le jeu est toujours en cours, False si un joueur a gagné
    """
    running = True
    dice_value = dice_base()

    ###
    #1 Moves pion
    score_joueur += dice_value

    #2 Check win condition exacte 100
    if check_win(score_joueur):
        return score_joueur, False

    #3 If score_joueur > 100   
    if score_joueur + dice_value > 100:
        score_joueur = need_exact_win(score_joueur)
    
    #4 Effects
    score_joueur = square_effect(score_joueur, bots)
    ### 
    
    # if dice is 6 and relance < 3, then play()
    if dice_value != 6:
        return score_joueur, running
    
    if relances == 3:
        affiche("Vous avez atteint la limite de relancés")
        return score_joueur, running
    
    relances += 1

    if bots and player_name == "Joueur":
        affiche("Vous avez obtenu un 6. Vous pouvez relancer ! \nAppuyez sur ENTER pour lancer le dé : ", ask_input=True)
        score_joueur, running = play(score_joueur, relances, bots)

    elif bots:
        affiche(f"{player_name} a obtenu un 6. {player_name} va relancer le dé !")
        score_joueur, running = play(score_joueur, relances, bots)

    else:
        affiche(f"{player_name} a obtenu un 6. Vous pouvez relancer, {player_name} ! \nAppuyez sur ENTER pour lancer le dé : ", ask_input=True)
        score_joueur, running = play(score_joueur, relances)

    return score_joueur, running


### If the player throws a number that makes him go beyond the score 100 he moves back to 100 minus the number
def need_exact_win(score_joueur):
    """
    Int --> Int
    Fonction retournant le score du joueur s'il dépasse la case 100 (100 - num).
    """
    sleep(time())
    if score_joueur > 100:
        recule = score_joueur - 100
        score_joueur = 100 - (recule)
        affiche(f"Vous ne pouvez pas dépasser l'arrivée, donc vous reculez de {recule}. Vous êtes retourné(e) à la case {score_joueur}\n")
    
    return score_joueur


def check_win(score_joueur):
    """
    Int --> Bool
    Fonction retournant True si le joueur est à la case 100, False sinon.
    """

    if score_joueur == 100:
        affiche(f"Vous avez gagné {player_name}!")
        return True

    return False
##
####






#### EFFECTS
##
# when the player steps on a snake
def got_serpent(score_joueur, bots=False):
    """
    Int --> Int
    Fonction retournant le score du joueur s'il est placé sur une case serpent.
    """
    sleep(time())
    score_joueur = serpents[score_joueur]
    
    if bots and player_name == "Joueur":
        affiche(f"Vous êtes tombé(e) sur un serpent ! ")
        affiche(f"Vous descendez à la case numéro {score_joueur}. \n")
    
    else:
        affiche(f"{player_name} est tombé(e) sur un serpent ! ")
        affiche(f"{player_name} descend à la case numéro {score_joueur}. \n")

    return score_joueur


# when the player steps on a ladder
def got_echelle(score_joueur, bots=False):
    """
    Int --> Int
    Fonction retournant le score du joueur s'il est placé sur une case échelle.
    """

    sleep(time())
    score_joueur = echelles[score_joueur]
    
    if bots and player_name == "Joueur":
        affiche(f"Vous êtes tombé(e)s sur une échelle ! ")
        affiche(f"Vous montez à la case numéro {score_joueur} !\n")
    
    else:
        affiche(f"{player_name} est tombé(e) sur une échelle ! ")
        affiche(f"{player_name} monte à la case numéro {score_joueur} ! \n")
        
    return score_joueur


# function to activate the square effect
def square_effect(score_joueur, bots=False):
    """
    Int --> Int
    Active l'effet de la case sur laquelle un joueur est tombé
    Retourne le score du joueur
    """
    if bots and player_name == "Joueur":
        affiche(f"Vous avez avancé à la case {score_joueur}.")

    else:
        affiche(f"{player_name} a avancé à la case {score_joueur}.")


    if score_joueur in serpents:
        score_joueur = got_serpent(score_joueur, bots)

    elif score_joueur in echelles:
        score_joueur = got_echelle(score_joueur, bots)

    else:
        affiche("Cette case n'a pas d'effet.\n")

    return score_joueur
##
####




#### AFFICHAGE
## PLATEAU
# print score et plateau actuel
def affiche_plateau(plateau, ordre_joueur, score_joueur, pawn):
    """
    List x List x Int x Str --> None
    Procédure qui affiche le plateau avec joueurs.
    """
    # Player's name
    print("\n     ", end="")
    for pawn, player, player_case in zip(pawn, ordre_joueur, score_joueur):
        print(f"{pawn} {player}({player_case})", end="    ")

    # Plateau
    for nb, liste in enumerate(plateau):
        if nb == 0:
            print(f"\n100 | {liste[0]}", end=" ")

        elif nb % 2 == 0:
            print(f"\n {100 - nb * 10} | {liste[0]}", end=" ")

        elif nb == 9:
            print(f"\n  → | {liste[0]}", end=" ")

        else:
            print(f"\n  ↱ | {liste[0]}", end=" ")

        for colonne in liste[1:]:
            print(f"| {colonne}", end=" ")

        if nb % 2 != 0:
            print("|", 100 - nb * 10, end="")

        else:
            print("| ↰", end="")
    print()


def replace(arr, find, replace):
    """
    List x Elem x Elem --> None
    Procédure qui remplace un élément d'une liste par " ".
    """
    base = 0
    for count in range(arr.count(find)):
        offset = arr.index(find, base)
        arr[offset] = replace
        base = offset + 1


def update_plateau(plateau, player_case, pawn):
    """
    List x List x Str --> None
    Procédure qui met à jour le plateau.
    """
    for nb in range(1, 11):
        if player_case <= nb * 10:
            break

    for liste in plateau:
        replace(liste, pawn, " ")

    number = str(player_case)

    if player_case == 100:
        plateau[0][0] = pawn
        return

    if nb % 2 == 0:
        if int(number[-1]) == 0:
            plateau[10 - nb][0] = pawn
            return

        plateau[10 - nb][10 - int(number[-1])] = pawn

    else:
        plateau[10 - nb][int(number[-1]) - 1] = pawn


def update(score_joueur, player_number, player_case):
    """
    Int x Int x Int --> None
    Procédure qui met à jour le plateau et le score du joueur.
    """
    score_joueur[player_number] = player_case
    update_plateau(plateau, player_case, pawn[player_number])
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
##
####






#### Notes et problèmes ##
##
# Les éléments primaires du jeu sont: le dé, le plateau et les effets des case (serpents et échelles).
# Les éléments secondaires sont: le mouvement, la condition de victoire, sélection des personnages et les difficultés.

# Int pour la position du joueur dans le jeu dans un dictionnaire.

# variables globals: plateau, pawn, player_name, echelles, serpents, data_to_save, i, LISTE_JOUEUR, full_bot
##
####


# setup
plateau = [[" " for n in range(10)] for m in range(10)]
pawn = ["➀", "➁", "➂", "➃"]

echelles = {
    3 : 17,
    13: 28,
    18: 37,
    32: 53,
    36: 63,
    42: 61,
    65: 75,
    69: 72,
    84: 99,
    89: 94
}

serpents = {
    9: 6,
    24: 16,
    29: 10,
    39: 1,
    46: 44,
    51: 48,
    56: 47,
    67: 45,
    77: 58,
    87: 68,
    92: 85,
    97: 26,
}


#### MAIN ####
def game_no_bot(loaded_game):
    global player_name
    global data_to_save

    print("\n==================================")
    print(" JEU DES SERPENTS ET DES ECHELLES")
    print("==================================\n")

    print("[Pour sauvegarder, tapez SAVE ou SAUVEGARDER] \n[Pour afficher le plateau, tapez MAP ou PLATEAU]\n")

    # [Initialisation]
    if loaded_game:
        ordre_joueur, score_joueur = saved_game_orders()

    else:
        liste_joueurs = select_players()

        affiche("\nPour décider de l'ordre, lancez le dé. \nCeux qui ont les scores les plus élevés passent en premier.")

        sleep(time(1))
        ordre_joueur = who_starts(liste_joueurs)
        score_joueur = [0 for n in liste_joueurs]

        sleep(time(1))
        affiche(f"\nVous pouvez commencer ! Ordre : {ordre_joueur} \n")

    # counting turns and rounds for saving
    count_tour = [0 for n in ordre_joueur]
    count, round = 0, 1

    data_to_save = list(zip(ordre_joueur, score_joueur, count_tour))

    # Start
    running = True
    while running:
        for player_number, player_name in enumerate(ordre_joueur):
            
            # Set up player's score and relances = 1
            player_case = score_joueur[player_number]
            relances = 1

            sleep(time())
            affiche(f"\n[Tour de {player_name}]")

            # Select different commands
            while True:
                throw_dice = affiche("Appuyez sur ENTER pour lancer le dé : ", ask_input=True)

                if throw_dice == "":
                    player_case, running = play(player_case, relances)
                    break

                # To show the current progression / map
                elif throw_dice in ["map", "plateau"]:
                    affiche_plateau(plateau, ordre_joueur, score_joueur, pawn)

                # To save the game
                elif throw_dice in ["save", "sauvegarder"]:
                    ask_to_save(data_to_save)

                else:
                    affiche("[ERREUR : Commande introuvable]")

            # If win then break
            if running is False:
                break

            # Update score_joueur et plateau
            update(score_joueur, player_number, player_case)

            # prints the end of round and the position of each player
            count += 1
            count_tour[player_number] += 1
            data_to_save = list(zip(ordre_joueur, score_joueur, count_tour))

            if count == len(ordre_joueur):
                count = 0
                sleep(time())
                affiche(f"\n[End of round {round}]")
                round += 1

                for player, player_case in zip(ordre_joueur, score_joueur):
                    sleep(time())
                    affiche(f"{player}, vous êtes sur la case {player_case}.")
                affiche("---\n")




def game_with_bot():
    global player_name

    print("\n==================================")
    print(" JEU DES SERPENTS ET DES ECHELLES")
    print("==================================\n")    

    bots = ["Steve", "Eve", "Matt", "Kevin", "Hector", "Eris"]
    liste_joueurs = random.sample(bots, 1)
    liste_joueurs.insert(0, "Joueur")
    
    sleep(time())
    affiche(f"Vous allez jouer contre {liste_joueurs[1]}.")

    sleep(time())
    affiche("\nPour décider qui commencera, lancez le dé. \nLe joueur qui obtient le score le plus élevé commence.")

    sleep(time())
    ordre_joueur = who_starts(liste_joueurs, bots = True)
    score_joueur = [0 for n in liste_joueurs]

    sleep(time())
    affiche(f"\nVous pouvez commencer ! Ordre : {ordre_joueur}\n ")

    # Game system
    running = True
    while running:
        for player_number, player_name in enumerate(ordre_joueur):

            # Set up player's score and relances = 1
            player_case = score_joueur[player_number]
            relances = 1

            sleep(time())
            if player_name != "Joueur":
                affiche(f"[Tour de {player_name}]")   

            else:
                affiche("[Votre tour]")

            # Select different commands
            while player_name == "Joueur": 
                throw_dice = affiche("Appuyer sur ENTER pour lancer le dé : ", ask_input=True)

                if throw_dice == "":
                    player_case, running = play(player_case, relances, bots=True)
                    break

                # To show the current progression / map
                elif throw_dice in ["map", "plateau"]:
                    affiche_plateau(plateau, ordre_joueur, score_joueur, pawn)
                                
                else: 
                    affiche("[ERREUR : Commande introuvable]")

            else: # For bot
                affiche(f"{player_name} lance le dé.")
                player_case, running = play(player_case, relances, bots=True)

            # If win then break
            if running is False:
                break

            # Update score_joueur et plateau
            update(score_joueur, player_number, player_case)




def game_full_bot():
    global player_name

    print("\n==================================")
    print(" JEU DES SERPENTS ET DES ECHELLES")
    print("==================================\n") 

    # [Initialisation]
    ordre_joueur = ["bot1", "bot2", "bot3", "bot4"]
    win = [0 for n in ordre_joueur]
    coup_moyen = 0
    nb_parties = get_nb_parties()

    for nb in range(nb_parties):
        tracing_score = [[0] for n in ordre_joueur]
        score_joueur = [0 for n in ordre_joueur]

        running = True
        while running:
            for player_number, bot_name in enumerate(ordre_joueur):

                # Set up player's score and name
                player_case = score_joueur[player_number]
                player_name = bot_name
                relances = 1

                # play
                player_case, running = play(player_case, relances, bots=True)

                # add player position to list
                tracing_score[player_number].append(player_case)

                # Check win
                if running is False:
                    win[player_number] += 1 
                    break

                # Update score_joueur
                score_joueur[player_number] = player_case

        for nb in range(4) :
            if tracing_score[nb][-1] == 100:
                coup_moyen += len(tracing_score[nb]) - 1

    coup_moyen /= nb_parties
    print(f"\nNombre de partie : {nb_parties}")
    print("Pourcentage Gain : bot1  {:.0%},  bot2  {:.0%},  bot3  {:.0%},  bot4  {:.0%}.".format(win[0]/nb_parties, win[1]/nb_parties, win[2]/nb_parties, win[3]/nb_parties))
    print(f"Le coup moyen pour gagner est de {coup_moyen}.")




def choice_gamemode():
    global full_bot

    # ask if player wants to load previous game
    full_bot = False
    loaded_game = ask_to_load()
    

    if loaded_game:
        game_no_bot(loaded_game)

    # ask gamemodes
    while True:
        affiche("(1) Mode local avec joueurs\n(2) Mode solo avec bots\n(3) Mode uniquement bots")
        game_mode = input("Tapez un mode de jeu : ").strip()
         
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
