# Code houses and hotels.
# Code mortgage and bankrupted players.
# Code property trading.
# Cod auctioning on properties that are not bought.
# Code total assets.
# Code GUI.
# Code graphics.


import random
import re


class Player:

    # Class Attributes
    money = 1500
    pos = 0
    in_jail = 0
    get_out_of_jail_free_card = 0
    tax = 0
    last_move = 0
    chance_factor = 0
    double_die = 0

    def __init__(self, name):
        self.name = name
        self.prop = []


class Property:
    houses = 0
    hotel = 0

    def __init__(self, pos, name):
        self.pos = pos
        self.name = name


def make_player(name):
    player = Player(name)
    return player


def make_property(pos):
    property = Property(pos, board[pos][0])
    return property


def color_sort():
    return board[3]


def move():
    # Simulates dice roll
    # Using commas in print does not require type conversions
    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)
    movement = (die1 + die2)
    print('Roll: ', die1, ' + ', die2, ' = ', movement)
    return movement, die1, die2


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
        1: ('Advance to Illinois Ave. -- If you pass Go, collect $200',
            advance, 24),
        2: ('Advance to St. Charles Place -- If you pass Go, collect $200',
            advance, 11),
        3: ('Advance to Utility. If unowned, you may buy it. If owned, \n'
            'throw dice and pay owner a total ten times the amount thrown.',
            advance, 'Utility'),
        4: ('Advance to nearest Railroad and pay owner twice the rental \nto '
            'which he is otherwise entitled. If Railroad is unowned, you may '
            'buy it.', advance, 'Railroad'),
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
        # Need to edit 13 for players var.
        13: ('You have been elected Chairman of the Board -- Pay each'
             ' player $50', -50),
        14: ('Your building and loan matures -- Collect $150', 150),
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


def tax(player):
    tax_collection = 0

    # Luxury Tax
    if player.pos == 38:
        player.money -= 75
        player.tax += 75
        print('\n{} paid $75 in Luxury Tax'.format(player.name))
        for i in player_list:
            tax_collection += i.tax
        print('Tax Collected: {}'.format(tax_collection))
        print("{}'s Money: {}".format(player.name, player.money))

    # Income Tax
    # Either 10% of all cash, or $200, whichever is greater
    elif player.pos == 4:
        if player.money < 2000:
            taxable = round(player.money * 0.1)
            player.money -= taxable
            player.tax += taxable
            print('\n{} paid ${} in Income Tax'.format(
                player.name, taxable))
            for i in player_list:
                tax_collection += i.tax
            print('Tax Collected: {}'.format(tax_collection))
            print("{}'s Money: {}".format(player.name, player.money))
        else:
            player.money -= 200
            player.tax += 200
            print('\n{} paid $200 in Income Tax'.format(player.name))
            for i in player_list:
                tax_collection += i.tax
            print('Tax Collected: {}'.format(tax_collection))
            print("{}'s Money: {}".format(player.name, player.money))

    # Free Parking House Rule
    else:
        for i in player_list:
            tax_collection += i.tax
            i.tax = 0

        # There's no point in printing redundant messages.
        # If tax collected is 0, no gain.
        if tax_collection != 0:
            player.money += tax_collection
            print('\n{} gains ${} from Free Parking'.format(
                player.name, tax_collection))
            print("{}'s Money: {}".format(player.name, player.money))


def jail(player):
    player.in_jail += 1
    player.pos = 10
    print('{} was sent to Jail!'.format(player.name))


def jail_options(player):

    # Branch if player has a get out of jail free card
    if player.get_out_of_jail_free_card > 0 and 0 < player.in_jail < 4:
        print('{} is in Jail!'.format(player.name))
        print('Turn {} in Jail'.format(player.in_jail))
        print("{}'s Money: {}\n".format(player.name, player.money))
        use_card = input('Use Get out of Jail Free Card? (Y/N) >>> ')

        # Branch if player uses Get Out of Jail Free Card.
        if use_card.upper() == 'YES' or use_card.upper() == 'Y':
            player.get_out_of_jail_free_card -= 1
            player.in_jail = 0
            print('{} leaves Jail for Free!\n'.format(player.name))
            player.last_move, die1, die2 = move()

        # Branch if player doesn't use Get Out of Jail Free Card.
        else:
            bail = input('Pay $50 to leave jail? (Y/N) >>> ')

            # Branch if player pays bail.
            if bail.upper() == 'YES' or bail.upper() == 'Y':
                player.in_jail = 0
                player.money -= 50
                print('\n{} pays bail'.format(player.name))
                print("{}'s Money: {}".format(player.name, player.money))
                player.last_move, die1, die2 = move()

            # Branch if player doesn't pay bail.
            else:
                print('')
                player.last_move, die1, die2 = move()
                if die1 == die2:
                    print('{} breaks out of Jail!\n'.format(player.name))
                    player.in_jail = 0
                    player.last_move, die1, die2 = move()
                else:
                    print('{} is still in Jail.\n'.format(player.name))
                    player.last_move = 0
                    player.in_jail += 1

    # Branch if player does not have get out of jail free card
    elif player.get_out_of_jail_free_card == 0 and 0 < player.in_jail < 4:
        print('{} is in Jail!'.format(player.name))
        print('Turn {} in Jail'.format(player.in_jail))
        print("{}'s Money: {}\n".format(player.name, player.money))
        bail = input('Pay $50 to leave jail? (Y/N) >>> ')

        # Branch if player pays bail.
        if bail.upper() == 'YES' or bail.upper() == 'Y':
            player.in_jail = 0
            player.money -= 50
            print('\n{} pays bail'.format(player.name))
            print("{}'s Money: {}\n".format(player.name, player.money))
            player.last_move, die1, die2 = move()

        # Branch if player doesn't pay bail.
        else:
            print('')
            player.last_move, die1, die2 = move()
            if die1 == die2:
                print('{} breaks out of Jail!\n'.format(player.name))
                player.in_jail = 0
                player.last_move, die1, die2 = move()
            else:
                print('{} is still in Jail.\n'.format(player.name))
                player.last_move = 0
                player.in_jail += 1

    # Branch if player has been in jail for 3 days
    elif player.in_jail == 4:
        print('{} has served his/her sentence in Jail.\n'.format(player.name))
        player.in_jail = 0
        player.last_move, die1, die2 = move()

        # Rolling Doubles
        if die1 == die2:
            player.double_die += 1
        else:
            player.double_die = 0

    # Branch if player is not in jail
    else:
        player.in_jail = 0
        player.last_move, die1, die2 = move()

        # Rolling Doubles
        if die1 == die2:
            player.double_die += 1
        else:
            player.double_die = 0


def jail_card(player):
    player.get_out_of_jail_free_card += 1
    print('{} received (1) Get Out of Jail Free Card'.format(player.name))


def advance(player, target):
    # For when a chance or community chest says to move backwards
    if target == 'Utility':
        player.chance_factor = 1
        player.last_move = move()[0]

        # Utilities are 12 and 28
        # Sends player to Electric Company
        if player.pos >= 28 or player.pos < 12:
            if player.pos >= 28:
                player.money += 200
                print('You passed Go -- Collect $200')
                print("{}'s Money: {}".format(player.name, player.money))

            player.pos = 12

        # Sends player to Water Works
        else:
            player.pos = 28

    elif target == 'Railroad':

        # RR's are 5, 15, 25, 35
        # Send players to Reading RR
        player.chance_factor = 1
        if player.pos < 5 or player.pos >= 35:
            if player.pos >= 35:
                player.money += 200
                print('You passed Go -- Collect $200')
                print("{}'s Money: {}".format(player.name, player.money))

                player.pos = 5

        # Send players to Pennsylvania RR
        elif player.pos >= 5:
            player.pos = 15

        # Send players to B&O RR
        elif player.pos >= 15:
            player.pos = 25

        # Send players to Short Line RR
        else:
            player.pos = 35

    # For the move backwards 3 spaces Chance card
    elif target < 0:
        player.pos += target

    # For all other advances
    else:
        steps = target - player.pos
        if steps <= 0:  # Accounts for when a player passes GO
            player.money += 200
        player.pos = target

    turn(player)


def railroad(player):
    # RR's are on positions 5, 15, 25, 35.
    RR = 0
    property = player.pos
    landlord = prop_owner[property]
    for i in landlord.prop:
        if i in [5, 15, 25, 35]:
            RR += 1
    rent = 25 * 2**(RR-1)  # Formula for 25, 50, 100, 200
    print('\n{} owns {} Railroad(s)'.format(landlord.name, RR))
    if player.chance_factor == 1:
        rent = 2 * rent
        player.chance_factor = 0
    return rent


def utility(player):
    # Utilities on positions 12, 28
    uti = 0
    property = player.pos
    landlord = prop_owner[property]
    for i in landlord.prop:
        if i in [12, 28]:
            uti += 1
    if player.chance_factor == 1 or uti == 2:  # Chance factor from chance card
        rent = 10 * player.last_move
        player.chance_factor = 0
    else:
        rent = 4 * player.last_move
    return rent


def monopoly(player):
    color = board[player.pos][3]
    community_prop = 0
    landlord = prop_owner[player.pos]

    # If the property is Just Visiting, GO, or Free Parking
    # The above properties have a 0 for color.
    if color == 0:
        monopoly_bonus = 1

    # For colored properties
    else:
        for i in landlord.prop:
            if board[i][3] == color:
                community_prop += 1

        # There are only two properties in the Brown and Blue communities.
        # Having both will grant a monopoly_bonus multiplier.
        if color == 'Brown' or color == 'Blue':
            if community_prop == 2:
                monopoly_bonus = 2
            else:
                monopoly_bonus = 1

        # All other colored properties
        else:
            if community_prop == 3:
                monopoly_bonus = 2
            else:
                monopoly_bonus = 1
    return monopoly_bonus


def payment(player, property):

    # Paying and earning rent on owned properties
    # Normal properties have a non-zero rent value.
    if isinstance(board[player.pos][2], int):
        rent = board[player.pos][2]

        # For granting a monopoly bonus
        monopoly_bonus = monopoly(player)
        if monopoly_bonus == 2:
            print('\n{} owns all {} properties!'.format(
                prop_owner[property].name, board[player.pos][3]))

        # For rent on houses/hotels
        for i in house_list:
            if property == i.pos:
                if i.houses == 0 and i.hotel == 0:
                    rent = rent * monopoly_bonus
                else:
                    improvements = i.houses + i.hotel
                    rent = board[property][4 + improvements]

    # For utilities or railroads.
    # Checks to see if variable is a function.
    elif callable(board[player.pos][2]):
        rent = board[player.pos][2](player)

    player.money -= rent
    prop_owner[property].money += rent

    print('\n{} pays ${} in rent'.format(
        player.name, rent))
    print("{}'s Money: {}".format(player.name, player.money))
    print('\n{} gains ${} from rent'.format(
        prop_owner[property].name, rent))
    print("{}'s Money: {}".format(
        prop_owner[property].name, prop_owner[property].money))


def turn(player):
    print("{}'s Position: {} {}".format(
        player.name, player.pos, board[player.pos][0]))
    print(player.prop)
    print(player.name + "'s Money: ", player.money)
    property = player.pos  # Properties are labelled by index number
    # Player Options

    # If property is not owned, gives option to buy.
    if not board[player.pos][-1] and player.money >= board[player.pos][1]:

        # buy = input('\nBuy ' + board[player.pos][0] + ' for '
        #            + str(board[player.pos][1]) + '? (Y/N) >>> ')

        # For quickly testing or generating lots of data
        # Buys every property
        print('')
        buy = 'YES'

        if buy.upper() == 'Y' or buy.upper() == 'YES':
            player.prop.append(property)
            prop_owner[property] = player
            board[player.pos][-1] = True

            player.money -= board[player.pos][1]
            print('{} buys {} for ${}.'.format(
                player.name, board[player.pos][0], board[player.pos][1]))
            print("{}'s Money: {}".format(player.name, player.money))

        elif buy.upper() == 'N' or buy.upper() == 'NO':
            print('{} did not buy {}'.format(player.name, board[property][0]))

    # If property is owned or is an event.
    elif board[player.pos][-1]:

        # For Community Chest or Chance events
        # The above events have values of length 2 in their dict.
        # The end of this line calls the function with the argv.
        # i.e this one could call community_chest(player) even though
        # community_chest doesn't have the () in the board
        if len(board[player.pos]) == 2:
            draw = board[player.pos][1](player)
            if isinstance(draw, int):  # Checks to see if draw is type int
                player.money += draw
                print("\n{}'s Money: {}".format(player.name, player.money))

        # For tax event
        # Tax event values have a length of 3 in the board dict.
        elif len(board[player.pos]) == 3:
            tax(player)

        # For owned properties
        elif board[player.pos][-1]:

            # Accounts for landing on Just Visiting, Free Parking, or GO.
            # The above spots have a rent value of 0, hence if statement.
            if board[player.pos][2] != 0:
                payment(player, property)

    # If the player cannot afford the property
    else:
        print('\n{} cannot afford {}'.format(
            player.name, board[player.pos][0]))

    print("\n{}'s Properties:".format(player.name))
    print('-' * 25)
    for i in sorted(player.prop):
        #if board[i-1][3] == board[i][3]:
        print('{}\t{}\t\t{}'.format(i, board[i][0], board[i][3]))
        #else:
        # print('\n{}\t{}\t{}'.format(i, board[i][0], board[i][3]))


def main():
    print('\n~~~ Welcome to Monopoly by Austin ~~~\n')
    global board
    # color properties: [name, buying cost, base_rent, community color,
    # house/hotel cost, house1 rent, house2 rent, house3 rent, house4 rent,
    # hotel rent, owned?]
    # board will be referenced many times throughout program, easier to store
    # all information regarding the board here
    board = {
        0: ['GO', 0, 0, 0, True],
        1: ['Mediterranean Ave.', 60, 2, 'Brown', 50, 10, 30, 90, 160, 250, False],
        2: ['Community Chest', community_chest],
        3: ['Baltic Ave.', 60, 4, 'Brown', 50, 20, 60, 180, 320, 450, False],
        4: ['Income Tax', tax, True],
        5: ['Reading Railroad', 200, railroad, 0, False],
        6: ['Oriental Ave.', 100, 6, 'Light Blue', 50, 30, 90, 270, 400, 550,
            False],
        7: ['Chance', chance],
        8: ['Vermont Ave.', 100, 6, 'Light Blue', 50, 30, 90, 270, 400, 550, False],
        9: ['Connecticut Ave.', 120, 8, 'Light Blue', 50, 40, 100, 300, 450, 600, False],
        10: ['Jail/Just Visiting', 0, 0, 0, True],  # Just visiting
        11: ['St. Charles Place', 140, 10, 'Purple', 100, 50, 150, 450, 625, 750, False],
        12: ['Electric Company', 150, utility, 0, False],
        13: ['States Ave.', 140, 10, 'Purple', 100, 50, 150, 450, 625, 750, False],
        14: ['Virginia Ave.', 160, 12, 'Purple', 100, 60, 180, 500, 700, 900, False],
        15: ['Pennsylvania Railroad', 200, railroad, 0, False],
        16: ['St. James Place', 180, 14, 'Orange', 100, 70, 200, 550, 750, 950, False],
        17: ['Community Chest', community_chest],
        18: ['Tennessee Ave.', 180, 14, 'Orange', 100, 70, 200, 550, 750, 950, False],
        19: ['New York Ave.', 200, 16, 'Orange', 100, 80, 220, 600, 800, 1000, False],
        20: ['Free Parking', tax, True],
        21: ['Kentucky Ave.', 220, 18, 'Red', 150, 90, 250, 700, 875, 1050, False],
        22: ['Chance', chance],
        23: ['Indiana Ave.', 220, 18, 'Red', 150, 90, 250, 700, 875, 1050, False],
        24: ['Illinois Ave.', 240, 20, 'Red', 150, 100, 300, 750, 925, 1100, False],
        25: ['B. & O. Railroad', 200, railroad, 0, False],
        26: ['Atlantic Ave.', 260, 22, 'Yellow', 150, 110, 330, 800, 975, 1150, False],
        27: ['Ventnor Ave.', 260, 22, 'Yellow', 150, 110, 330, 800, 975, 1150, False],
        28: ['Water Works', 150, utility, 0, False],
        29: ['Marvin Gardens', 280, 24, 'Yellow', 150, 120, 360, 850, 1025, 1200, False],
        30: ['Go To Jail', jail],  # Go to Jail
        31: ['Pacific Ave.', 300, 26, 'Green', 200, 130, 390, 900, 1100, 1275, False],
        32: ['North Carolina Ave.', 300, 26, 'Green', 200, 130, 390, 900, 1100, 1275, False],
        33: ['Community Chest', community_chest],
        34: ['Pennsylvania Ave.', 320, 28, 'Green', 200, 150, 450, 1000, 1200, 1400, False],
        35: ['Short Line Railroad', 200, railroad, 0, False],
        36: ['Chance', chance],
        37: ['Park Place', 350, 35, 'Blue', 200, 175, 500, 1100, 1300, 1500, False],
        38: ['Luxury Tax', tax, True],
        39: ['Boardwalk', 400, 50, 'Blue', 200, 200, 600, 1400, 1700, 2000, False],
    }

    # Using this to keep track how many houses/hotels a player has purchased
    global house_list
    global house_buyable
    global hotel_buyable
    house_buyable = 32
    hotel_buyable = 12
    house_list = []
    for i in board.keys():

        # For keeping track of houses and hotels for applicable properties
        if len(board[i]) == 11 and not board[i][-1]:
            house_list.append(Property(i, board[i][0]))
            # board[i][0] = Property(i, board[i][0])
    # print(house_list[21].name)

    global prop_owner
    prop_owner = {}

    '''
    # Use a make_player function to create
    global player_list
    player_list = []
    player_no = int(input('Enter Number of Players >>> '))
    for i in range(player_no):
        name = input('Player ' + str(i) + ' Name >>> ')
        player_list.append(make_player(name))

    print("\n~~~~~ Let's Play ~~~~~\n")
    '''
    # This section is for testing purposes

    austin = Player('Austin')
    ben = Player('Ben')
    priscilla = Player('Priscilla')
    global player_list
    player_list = [austin, ben]

    # ben.prop = [39]
    # prop_owner[39] = ben
    # board[39][-1] = True
    # house_list[21].houses = 4


    while austin.money > 0 and ben.money > 0:
    # while len(player_list) > 1:
        for player in player_list:
            print("~~~ {}'s Turn ~~~".format(player.name))
            jail_options(player)
            player.pos += player.last_move

            # Rolling doubles
            if player.double_die == 3:
                player.pos = 10
                player.in_jail = 1
                player.double_die = 0
                print('{} was sent to Jail for rolling 3 Doubles!\n'.format(
                    player.name))

            # For when player reaches GO
            if player.pos > 39:
                player.money += 200
                player.pos = player.pos - 40
                print('You passed Go -- Collect $200')
                print("{}'s Money: {}\n".format(player.name, player.money))


            # For testing positions/events on board
            # austin.pos = 39
            # ben.pos = 7

            turn(player)
            if player.money < 0:
                player_list.remove(player)
                print('\n{} declares bankruptcy!'.format(player.name))
            print('-' * 77)

    # Declaring the winner
    winner = player_list[0]
    print('\n~~~ Congratulations {}, you are the winner!!! ~~~\n'.format(
        winner.name))


if __name__ == '__main__':
    main()
