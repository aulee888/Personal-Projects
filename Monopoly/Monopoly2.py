import random


class Player:

    # Class Attributes
    money = 1500
    pos = 0
    prop = []
    get_out_of_jail_free_card = 0

    def __init__(self, name):
        self.name = name


def move():
    # Simulates dice roll
    # Using commas in print does not require type conversions
    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)
    movement = (die1 + die2)
    print('Roll: ', die1, ' + ', die2, ' = ', movement)
    return movement


def community_chest(player):
    print('')
    cards = {
        # Community Chest Cards
        # Special Events have 3 elements.
        # Normal events have 2 elements.
        0: ('Advance to GO -- Collect $200', advance, 0),
        1: ('Bank error in your favor -- Collect $200', 200),
        2: ("Doctor's Fee -- Pay $50", -50),
        3: ('From sale of you stock you get $50', 50),
        4: ('Get Out of Jail Free', jail_card, 0),
        5: ('Go to Jail', jail, 0),
        # Need to edit 6 for players var.
        6: ('Grand Opera Night -- Collect $50 from every player',
            50),
        7: ('Holiday Fund matures -- Collect $100', 100),
        8: ('Income Tax Refund -- Collect $20', 20),
        9: ('It is your birthday -- Collect $10', 10),
        10: ('Life Insurance matures -- Collect $100', 100),
        11: ('Pay hospital fees -- Pay $100', -100),
        12: ('Pay school fees -- Pay $150', -150),
        13: ('Receive Consultancy Fee -- Collect $25', 25),
        # Need to edit 14 to include house and hotel prices
        14: ('You are assessed for street repairs -- $40 per house'
             ' -- $115 per hotel', -(40 + 115)),
        15: ('You won second prize in a beauty contest -- Collect $10',
             10),
        16: ('You inherit $100', 100)
    }
    draw = random.randrange(17)
    if len(cards[draw]) < 3:
        print(player.name + ' draws Community Chest ' + str(draw) + ': '
              + cards[draw][0])
        community_effect = cards[draw][1]
        return community_effect
    else:
        # For when the draw is an advance
        # These have two arguments
        if cards[draw][1] == advance:
            print(player.name + ' draws Community Chest ' + str(draw) + ': '
                  + cards[draw][0])
            cards[draw][1](player, cards[draw][2])

        # For when the draw is an event not advance
        # These only have one argument
        else:
            print(player.name + ' draws Community Chest ' + str(draw) + ': '
                  + cards[draw][0])
            cards[draw][1](player)


def chance(player):
    print('')
    cards = {
        # Chance Cards
        0: ('Advance to Go (Collect $200)', advance, 0),
        1: ('Advance to Illinois Ave. -- If you pass Go, collect $200', advance
            , 24),
        2: ('Advance to St. Charles Place -- If you pass Go, collect $200',
            advance, 11),
        3: ('Advance to Utility. If unowned, you may buy it. If owned, throw '
            'dice and pay owner a total ten times the amount thrown', utility,
            0),
        4: ('Advance to nearest Railroad and pay owner twice the rental to '
            'which he is otherwise entitled. If Railroad is unowned, you may '
            'buy it', railroad, 0),
        5: ('Bank pays you dividend of $50', 50),
        6: ('Get Out of Jail Free', jail_card, 0),
        7: ('Go back 3 spaces', advance, -3),
        8: ('Go to Jail', jail, 0),
        9: ('Make general repairs on all your property -- $25 per house -- '
            '$100 per hotel', -(25 + 100)),
        10: ('Pay poor tax of $15', -15),
        11: ('Take a trip to Reading Railroad -- If you pass Go, collect'
             ' $200', advance, 5),
        12: ('Take a walk on the Boardwalk -- Advance to Boardwalk',
             advance, 39),
        # Need to edit 30 for players var.
        13: ('You have been elected Chairman of the Board -- Pay each'
             ' player $50', -50),
        14: ('Your building and loan matures -- Collect $150', 50),
        15: ('You have won a crossword competition -- Collect $100', 100)
    }
    draw = random.randrange(16)
    if len(cards[draw]) < 3:
        print(player.name + ' draws Chance ' + str(draw) + ': '
              + cards[draw][0])
        community_effect = cards[draw][1]
        return community_effect
    else:
        # For when the draw is an advance
        # These have two arguments
        if cards[draw][1] == advance:
            print(player.name + ' draws Chance ' + str(draw) + ': '
                  + cards[draw][0])
            cards[draw][1](player, cards[draw][2])

        # For when the draw is an event not advance
        # These only have one argument
        else:
            print(player.name + ' draws Chance ' + str(draw) + ': '
                  + cards[draw][0])
            cards[draw][1](player)


def turn(player):
    print(player.name + "'s Position: ", player.pos, board[player.pos][0])
    print(player.name + "'s Money: ", player.money)
    property = board[player.pos][0]  #
    # Player Options

    # If property is not owned, gives option to buy.
    if not board[player.pos][-1]:
        print('')
        buy = input('Buy ' + board[player.pos][0] + ' for ' +
                    str(board[player.pos][1]) + '? (Y/N) >>> ')
        # buy = 'YES'

        if buy.upper() == 'Y' or buy.upper() == 'YES':
            player.prop.append(property)
            prop_owner[property] = player
            board[player.pos][-1] = True

            player.money -= board[player.pos][1]
            print('{} buys {} for ${}.'.format(
                player.name, board[player.pos][0], board[player.pos][1]))
            print("{}'s Money: {}".format(player.name, player.money))

    # If property is owned or is an event.
    # Should edit what's printed to 'Austin gains $4... Total: $1504'
    else:
        print('')
        # For events
        if len(board[player.pos]) == 2:
            # The end of this line calls the function with the argv.
            # i.e this one could call community_chest(player) even though
            # community_chest doesn't have the () in the board
            draw = board[player.pos][1](player)
            if isinstance(draw, int):  # Checks to see if draw is type int
                player.money += draw
                print("{}'s Money: {}".format(player.name, player.money))

        # For properties
        else:
            # Accounts for landing on Just Visiting, Free Parking, or GO
            if board[player.pos][2] != 0:
                try:
                    # Pay and earned rent statements if not a railroad or utility
                    player.money -= board[player.pos][2]
                    prop_owner[property].money += board[player.pos][2]

                    print('{} pays ${} in rent'.format(
                        player.name, board[player.pos][2]))
                    print("{}'s Money: {}".format(player.name, player.money))
                    print('\n{} gains ${} from rent'.format(
                        prop_owner[property].name, board[player.pos][2]))
                    print("{}'s Money: {}".format(
                        prop_owner[property].name, prop_owner[property].money))
                except TypeError:
                    player.money -= utility(player)


def tax(player):
    player.money -= 250
    #tax_collection += 250
    print('{} paid $250 in taxes'.format(player.name))


def jail(player):
    player.pos = 10
    print('{} was sent to Jail'.format(player.name))


def jail_card(player):
    player.get_out_of_jail_free_card += 1
    print('{} received (1) Get Out of Jail Free Card'.format(player.name))


def advance(player, target):
    # For when a chance or community chest says to move backwards
    if target < 0:
        player.pos += target

    else:
        steps = target - player.pos
        if steps <= 0:  # Accounts for when a player passes GO
            player.money += 200
        player.pos = target

    turn(player)


def railroad(player):
    return 50


def utility(player):
    return 50


def main():
    global board
    board = {
        0: ['GO', 0, 0, 0, True],
        1: ['Mediterranean Ave.', 60, 2, 'Brown', False],
        2: ['Community Chest', community_chest],
        3: ['Baltic Ave.', 60, 4, 'Brown', False],
        4: ['Income Tax', tax],
        5: ['Reading Railroad', 200, railroad, 0, False],
        6: ['Oriental Ave.', 100, 6, 'Light Blue', False],
        7: ['Chance', chance],
        8: ['Vermont Ave.', 100, 6, 'Light Blue', False],
        9: ['Connecticut Ave.', 120, 8, 'Light Blue', False],
        10: ['Just Visiting', 0, 0, 0, True],  # Just visiting
        11: ['St. Charles Place', 140, 10, 'Purple', False],
        12: ['Electric Company', 150, utility, 0, False],
        13: ['States Ave.', 140, 10, 'Purple', False],
        14: ['Virginia Ave.', 160, 12, 'Purple', False],
        15: ['Pennsylvania Railroad', 200, railroad, 0, False],
        16: ['St. James Place', 180, 14, 'Orange', False],
        17: ['Community Chest', community_chest],
        18: ['Tennessee Ave.', 180, 14, 'Orange', False],
        19: ['New York Ave.', 200, 16, 'Orange', False],
        20: ['Free Parking', 0, 0, 0, True],
        21: ['Kentucky Ave.', 220, 18, 'Red', False],
        22: ['Chance', chance],
        23: ['Indiana Ave.', 220, 18, 'Red', False],
        24: ['Illinois Ave.', 240, 20, 'Red', False],
        25: ['B. & O. Railroad', 200, railroad, 0, False],
        26: ['Atlantic Ave.', 260, 22, 'Yellow', False],
        27: ['Ventnor Ave.', 260, 22, 'Yellow', False],
        28: ['Water Works', 150, utility, 0, False],
        29: ['Marvin Gardens', 280, 24, 'Yellow', False],
        30: ['Go To Jail', jail],  # Go to Jail
        31: ['Pacific Ave.', 300, 26, 'Green', False],
        32: ['North Carolina Ave.', 300, 26, 'Green', False],
        33: ['Community Chest', community_chest],
        34: ['Pennsylvania Ave.', 320, 28, 'Green', False],
        35: ['Short line Railroad', 200, railroad, 0, False],
        36: ['Chance', chance],
        37: ['Park Place', 350, 35, 'Blue', False],
        38: ['Luxury Tax', tax],
        39: ['Boardwalk', 400, 50, 'Blue', False],
    }

    global prop_owner
    prop_owner = {}
    #global tax_collection
    #tax_collection = 0

    '''
    player_list = []
    player_no = int(input('Enter Number of Players >>> '))
    for i in range(player_no):
        name = input('Player ' + str(i) + ' Name >>> ')
        i = Player(name)
        player_list.append[i]
    '''

    austin = Player('Austin')
    ben = Player('Car')
    global player_list
    player_list = [austin, ben]

    '''
    while austin.money > 0:
        austin.pos += move()
        if austin.pos > 39:
            austin.money += 200
            austin.pos = austin.pos - 40
        turn(austin)
        print('-' * 77)
    '''

    while austin.money > 0 and ben.money > 0:
        for player in player_list:
            print("~~~ {}'s Turn ~~~".format(player.name))
            player.pos += move()
            if player.pos > 39:
                # Accounts for when player reaches GO
                player.money += 200
                player.pos -= 40
                print('\nYou passed Go -- Collect $200')
                print("{}'s Money: {}\n".format(player.name, player.money))

    # For testing events on board
    #prop_owner['Boardwalk'] = ben
    #board[39][4] = True
    #austin.pos = 39

            turn(player)
            print('-' * 77)


if __name__ == '__main__':
    main()
