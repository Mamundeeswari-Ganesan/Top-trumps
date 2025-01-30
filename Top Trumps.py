"""
Project name: Top Trumps
Author: M Ganesan
Date of creation: 19/12/2024
Description: This script runs a small game where players compare stats,
similar to the Top Trumps card game. Each game has 3 rounds, the player
with most numbers of rounds wins the game. The basic flow of the game
is:
1. You can choose to play Pokémon or dungeons and dragons .
2. You and your opponent are given 3 random cards with different stats.
3. You both select one of the card.
4. You get to choose heads or tails
5. Winner who won get to select the stat to compare.
6. The player with the stat higher wins that round.
7. You can choose to continue or leave the game
8. Display the result for the user.

"""

##### Import packages
import random
import requests

##### Define functions
def flip_coin():
    random_number = random.randint(1, 2)
    if random_number == 1:
        side = 'heads'
    else:
        side = 'tails'
    return side


def pokemon_card():
    # Generate 3 random numbers between 1 and 151 to use as the Pokémon ID number
    random_numbers = random.sample(range(0,152), 3)

    # Using the Pokémon API get a Pokémon based on its ID number
    # create empty list
    cards = []
    # For loop to request the information of each Pokémon
    for number in random_numbers:
        url = 'https://pokeapi.co/api/v2/pokemon/{}/'.format(number)
        response = requests.get(url)
        # check response has been successful

        pokemon = response.json()
        # Create a dictionary that contains the returned Pokémon's name, id, height and weight
        dictionary =  {
            'name': pokemon['name'],
            'id': pokemon['id'],
            'height': pokemon['height'],
            'weight': pokemon['weight'],
            }
        # append to list
        cards.append(dictionary)

    return cards


def d_and_d_cards():
    # fetch all monsters within the API
    url = 'https://www.dnd5eapi.co/api/monsters'
    response = requests.get(url)
    data = response.json()

    # Returns a list of all monsters
    all_monsters = data['results']

    # Pick 3 random monsters and get index information
    random_monsters = random.sample(all_monsters, 3)

    indexes = []
    for monster in random_monsters:
        indexes.append(monster['index'])

    # Create an empty list to storage the dictionary
    cards = []
    # For loop to request the information of each selected monster using its index
    for idx in indexes:
        url = 'https://www.dnd5eapi.co/api/monsters/{}/'.format(idx)
        response = requests.get(url)

        monster_data = response.json()

        # Create a dictionary that contains the returned monster's name, charisma, strength and intelligence
        dictionary = {
            'name': monster_data['name'],
            'charisma': monster_data['charisma'],
            'strength': monster_data['strength'],
            'intelligence': monster_data['intelligence'],
            }

        # append to list
        cards.append(dictionary)

    return cards


def top_trumps():
    theme = input('What cards do you want to play? (pokemon or D&D) ')

    # Best of 3
    user_counter = 0
    opponent_counter = 0

    for i in range(1,4):
        print('--------- ROUND {} ---------'.format(i))

        ### PLAYING WITH POKÉMON CARDS
        if theme == 'pokemon':
            # Get 3 random Pokémon for the player and print their names (output will be a list of dictionaries)
            user_cards = pokemon_card()
            print('')
            print('Fantastic! Your choices are:')
            for option in user_cards:
                print('  -> {}'.format(option['name']))

            # Ask the user to choose a Pokémon and access its data
            print('')
            option_input = str(input('Choose your pokemon\'s name: '))
            if user_cards[0]['name'] == option_input:
                user_option = user_cards[0]
            elif user_cards[1]['name'] == option_input:
                user_option = user_cards[1]
            else:
                user_option = user_cards[2]

            # Get a random Pokémon for the opponent
            opponent_cards = pokemon_card()

            while len(opponent_cards) < 3:
                opponent_cards = pokemon_card()

            random_pokemon = random.randint(0,len(opponent_cards))
            opponent_pokemon = opponent_cards[random_pokemon]

            # Show to the user the stats of the selected Pokémon
            print('')
            print('These are your stats: \n  -> id: {} '
                  '\n  -> height: {} '
                  '\n  -> weight: {}'.format(user_option['id'],
                                             user_option['height'],
                                             user_option['weight']))

            # Choose a stats and access the value
            print('')
            coin = input('Let\'s see who choose the stats - heads or tails? ')
            print('')

            side = flip_coin()

            if side == coin:
                print('It was {}. You choose.'.format(side))
                print('')
                stat_choice = input('Which stat do you want to use? (id, height, weight) ')
                user_stat = user_option[stat_choice]
            else:
                list_of_stats = ['id', 'height', 'weight']
                stat_choice = random.sample(list_of_stats, 1)
                stat_choice = stat_choice[0]
                print('It was {}. Your opponent chose {}.'.format(side, stat_choice))
                user_stat = user_option[stat_choice]

            # Print the opponent Pokémon
            print('')
            print('The opponent chose {}'.format(opponent_pokemon['name']))
            print('')
            print('These are your opponent stats: \n  -> id: {} '
                  '\n  -> height: {} '
                  '\n  -> weight: {}'.format(opponent_pokemon['id'],
                                             opponent_pokemon['height'],
                                             opponent_pokemon['weight']))
            print('')

            opponent_stat = opponent_pokemon[stat_choice]

            # Compare the player's and opponent's Pokémon on the chosen stat
            if user_stat > opponent_stat:
                user_counter += 1
                print('You win this round!')
            elif user_stat < opponent_stat:
                opponent_counter += 1
                print('You lose this round!')
            else:
                print('Draw!')

            print('')

            # Ask the user to continue
            if i < 3:
                next_round = input('Do you want to continue? (yes or no) ')
                print('')

                if next_round == 'no':
                    print('Thanks for playing. You won {} round(s). See you soon :)'.format(user_counter))
                    exit()


        ### PLAYING WITH D&D CARDS
        elif theme == 'D&D':
            user_cards = d_and_d_cards()

            # Get 3 random monsters for the player and print their names (output will be a list of dictionaries)
            print('')
            print('Great! Your choices are:')
            for options in user_cards:
                print('  -> {}'.format(options['name']))

            # Ask the user to choose a monster and access its data
            print('')
            option_input = str(input('Choose your monster\'s name: '))
            if user_cards[0]['name'] == option_input:
                user_option = user_cards[0]
            elif user_cards[1]['name'] == option_input:
                user_option = user_cards[1]
            else:
                user_option = user_cards[2]

            # Get a random monster for the opponent
            opponent_cards = d_and_d_cards()

            while len(opponent_cards) < 3:
                print(len(opponent_cards))
                opponent_cards = d_and_d_cards()

            random_monster = random.randint(0, len(opponent_cards))
            opponent_monster = opponent_cards[random_monster]

            # Show to the user the stats of the selected monster
            print('')
            print('These are your stats: \n  -> charisma: {} '
                  '\n  -> strength: {} '
                  '\n  -> intelligence: {}'.format(user_option['charisma'],
                                                   user_option['strength'],
                                                   user_option['intelligence']))

            # Choose a stats and access the value
            print('')
            coin = input('Let\'s see who choose the stats - heads or tails? ')
            print('')

            side = flip_coin()

            if side == coin:
                print('It was {}. You choose.'.format(side))
                print('')
                stat_choice = input('Which stat do you want to use? (charisma, strength, intelligence) ')
                user_stat = user_option[stat_choice]
            else:
                list_of_stats = ['charisma', 'strength', 'intelligence']
                stat_choice = random.sample(list_of_stats, 1)
                stat_choice = stat_choice[0]
                print('It was {}. Your opponent chose {}.'.format(side, stat_choice))
                user_stat = user_option[stat_choice]

            # Print the opponent monster
            print('')
            print('The opponent chose {}'.format(opponent_monster['name']))
            print('')
            print('These are your opponent stats: \n  -> charisma: {} '
                  '\n  -> strength: {} '
                  '\n  -> intelligence: {}'.format(opponent_monster['charisma'],
                                                   opponent_monster['strength'],
                                                   opponent_monster['intelligence']))
            print('')

            opponent_stat = opponent_monster[stat_choice]

            # Compare the player's and opponent's monster on the chosen stat
            if user_stat > opponent_stat:
                user_counter += 1
                print('You win this round!')
            elif user_stat < opponent_stat:
                opponent_counter += 1
                print('You lose this round!')
            else:
                print('Draw!')

            print('')

            # Ask the user to continue
            if i < 3:
                next_round = input('Do you want to continue? (yes or no) ')
                print('')

                if next_round == 'no':
                    print('Thanks for playing. You won {} round(s). See you soon :)'.format(user_counter))
                    exit()

        # If input a wrong theme
        else:
            print('Sorry, that\'s not an option')


    # After 3 rounds, decide who wins
    print('')
    if user_counter > opponent_counter:
        print('You have won {} rounds. Congratulations! You win :)'.format(user_counter))
    elif user_counter < opponent_counter:
        print('Sorry, your opponent has won {} rounds. You lose :('.format(opponent_counter))
    else:
        print('Draw!')


## run
top_trumps()