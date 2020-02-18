import random
import pandas as pd


def chance(player):
    def advance(to_position):
        if to_position == 'railroad':  # For move to nearest railroad chance
            if player.position >= 35:
                player.money += 200
                player.position = 5

            elif player.position < 5:
                player.position = 5

            elif player.position >= 25:
                player.position = 35

            elif player.position >= 15:
                player.position = 25

            elif player.position >= 5:
                player.position = 15

        elif to_position == 'utility':  # For move to nearest utility chance
            if 12 <= player.position < 28:
                player.position = 28

            elif player.position >= 28:
                player.money += 200
                player.position = 12

            else:
                player.position = 12

        elif to_position < 0:  # For move backwards chance
            player.position += to_position

        else:  # For advances to specific locations
            if player.position > to_position:
                player.money += 200

            player.position = to_position

    def pay(amount):
        if amount == 'players':
            pass

        elif amount == 'upgrades':
            pass

        player.money += amount

    chance_df = pd.read_excel('chance_data.xlsx')

    card = chance_df.iloc[random.randrange(16)]
    if card['function'] == 'advance':
        advance(card['position'])

    elif card['function'] == 'pay':
        pay(card['amount'])
