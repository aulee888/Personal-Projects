# Make mortgage option cancel if anything else but a number is entered
# Code chance and community probabilities using probs that affect each other, after drawing a card, that card's probability goes to zero
# Code total assets.
# Code random turns in auction and turn order
# Code GUI.


import random
import re
import turtle


class Player:

    # Class Attributes
    # last_move is an attribute to help keep track of dice rolls for utilites,
    # or advance, or jail. It's convenient because it avoids having to roll
    # dice multiple times and allows you to hold onto the roll values you
    # initially wanted.
    money = 1500
    pos = 0
    in_jail = 0
    get_out_of_jail_free_card = 0
    tax = 0
    last_move = 0
    chance_factor = 0
    double_die = 0
    bid = 0
    color = ''
    move_count = 0

    def __init__(self, name):
        self.name = name
        self.prop = []
        self.community = []
        self.turtle = turtle.Turtle()

    def turtle_move(self, steps):
        for i in range(steps):
            if self.move_count == 0:
                self.turtle.forward(93.5)  # Number from end space to regular space
                self.move_count += 1
            elif self.move_count == 9:
                self.turtle.forward(93.5)  # Number from end space to regular space
                self.turtle.right(90)
                self.move_count = 0
            else:
                self.turtle.forward(61.625)  # Number between regular spaces
                self.move_count += 1


class Property:
    houses = 0
    hotel = 0

    def __init__(self, pos, name, cost):
        self.pos = pos
        self.name = name
        self.cost = cost
        self.initiative = random.randint(1,10)


class HouseHotel:
    # To be used to avoid using global and local var reference error
    houses = 32
    hotels = 12


def make_player(name):
    player = Player(name)
    return player


def make_property(pos):
    property = Property(pos, board[pos][0])
    return property


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
    houses = 0
    hotels = 0
    for i in house_list:
        if i.pos in player.prop:
            houses += i.houses
            hotels += i.hotel

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
            50 * (len(player_list)-1)),
        7: ('Holiday Fund matures -- Collect $100', 100),
        8: ('Income Tax Refund -- Collect $20', 20),
        9: ('It is your birthday -- Collect $10', 10),
        10: ('Life Insurance matures -- Collect $100', 100),
        11: ('Pay hospital fees -- Pay $100', -100),
        12: ('Pay school fees -- Pay $150', -150),
        13: ('Receive Consultancy Fee -- Collect $25', 25),
        14: ('You are assessed for street repairs -- $40 per house'
             ' -- $115 per hotel', -(40*houses + 115*hotels)),
        15: ('You won second prize in a beauty contest -- Collect $10', 10),
        16: ('You inherit $100', 100)
    }
    draw = random.randrange(17)
    if len(cards[draw]) < 3:
        print(player.name + ' draws Community Chest ' + str(draw) + ': '
              + cards[draw][0])
        community_effect = cards[draw][1]
        # Special case for 6 which doesn't follow regular rules
        if draw == 6:
            for i in player_list:
                if i != player:
                    i.money -= 50
                    print('\t{} collects $50 from {}'.format(player.name, i.name))
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
    houses = 0
    hotels = 0
    for i in house_list:
        if i.pos in player.prop:
            houses += i.houses
            hotels += i.hotel

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
            '$100 per hotel', -(25*houses + 100*hotels)),
        10: ('Pay poor tax of $15', -15),
        11: ('Take a trip to Reading Railroad -- If you pass Go, collect'
             ' $200', advance, 5),
        12: ('Take a walk on the Boardwalk -- Advance to Boardwalk',
             advance, 39),
        # Need to edit 13 for players var.
        13: ('You have been elected Chairman of the Board -- Pay each'
             ' player $50', -50*(len(player_list)-1)),
        14: ('Your building and loan matures -- Collect $150', 150),
        15: ('You have won a crossword competition -- Collect $100', 100)
    }
    draw = random.randrange(16)
    if len(cards[draw]) < 3:
        print(player.name + ' draws Chance ' + str(draw) + ': '
              + cards[draw][0])
        community_effect = cards[draw][1]
        # Special case for 13 that doesn't follow rest of rules
        if draw == 13:
            for i in player_list:
                if i != player:
                    i.money += 50
                    print('\t{} pays {} $50'.format(player.name, i.name))
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
    player.turtle.goto(-320, -320)
    player.turtle.setheading(90)  # Makes turtle face north
    player.move_count = 0
    print('{} was sent to Jail!'.format(player.name))


def jail_options(player):
    # Use last_move = 0 to indicate that the player is still stuck in jail and
    # in main():, the player doesn't move.
    # Part of the 'Movement' phase is incorporated in this function because it
    # is convenient to do so since it checks if a player is in jail.


    # Branch if player has a get out of jail free card
    if player.get_out_of_jail_free_card > 0 and 0 < player.in_jail < 4:
        print('{} is in Jail!'.format(player.name))
        print('Turn {} in Jail'.format(player.in_jail))
        print("{}'s Money: {}\n".format(player.name, player.money))
        while True:
            use_card = input('Use Get out of Jail Free Card? (Y/N) >>> ')
            if use_card.upper() in ['Y', 'YES', 'N', 'NO']:
                break

        # Branch if player uses Get Out of Jail Free Card.
        if use_card.upper() == 'YES' or use_card.upper() == 'Y':
            player.get_out_of_jail_free_card -= 1
            player.in_jail = 0
            print('{} leaves Jail for Free!\n'.format(player.name))

            player.turtle.goto(-340, -340)  # Return turtle to original track
            player.turtle.setheading(90)
            player.last_move, die1, die2 = move()

        # Branch if player doesn't use Get Out of Jail Free Card.
        else:
            while True:
                bail = input('\tPay $50 to leave jail? (Y/N) >>> ')
                if bail.upper() in ['Y', 'YES', 'N', 'NO']:
                    break

            # Branch if player pays bail.
            if bail.upper() == 'YES' or bail.upper() == 'Y':
                player.in_jail = 0
                player.money -= 50
                print('\n{} pays bail'.format(player.name))
                print("{}'s Money: {}".format(player.name, player.money))
                player.turtle.goto(-340, -340)  # Return turtle to original track
                player.turtle.setheading(90)
                player.last_move, die1, die2 = move()

            # Branch if player doesn't pay bail.
            else:
                print('')
                player.last_move, die1, die2 = move()
                if die1 == die2:
                    print('{} breaks out of Jail!\n'.format(player.name))
                    player.in_jail = 0

                    # Roll again for movement after breaking out
                    player.last_move, die1, die2 = move()

                    # Rolling Doubles
                    if die1 == die2:
                        player.double_die += 1
                    else:
                        player.double_die = 0

                else:
                    print('{} is still in Jail.\n'.format(player.name))
                    player.last_move = 0
                    player.in_jail += 1

    # Branch if player does not have get out of jail free card
    elif player.get_out_of_jail_free_card == 0 and 0 < player.in_jail < 4:
        print('{} is in Jail!'.format(player.name))
        print('Turn {} in Jail'.format(player.in_jail))
        print("{}'s Money: {}\n".format(player.name, player.money))

        while True:
            bail = input('Pay $50 to leave jail? (Y/N) >>> ')
            if bail.upper() in ['Y', 'YES', 'N', 'NO']:
                break

        # Branch if player pays bail.
        if bail.upper() == 'YES' or bail.upper() == 'Y':
            player.in_jail = 0
            player.money -= 50
            print('\n{} pays bail'.format(player.name))
            print("{}'s Money: {}\n".format(player.name, player.money))

            player.turtle.goto(-340, -340)  # Return turtle to original track
            player.turtle.setheading(90)
            player.last_move, die1, die2 = move()

        # Branch if player doesn't pay bail.
        else:
            print('')
            player.last_move, die1, die2 = move()
            if die1 == die2:
                print('{} breaks out of Jail!\n'.format(player.name))
                player.in_jail = 0
                player.turtle.goto(-340, -340)  # Return turtle to original track
                player.turtle.setheading(90)

                # Roll again for movement after breaking out
                player.last_move, die1, die2 = move()

                # Rolling Doubles
                if die1 == die2:
                    player.double_die += 1
                else:
                    player.double_die = 0

            else:
                print('{} is still in Jail.\n'.format(player.name))
                player.last_move = 0
                player.in_jail += 1

    # Branch if player has been in jail for 3 days
    elif player.in_jail == 4:
        print('{} has served his/her sentence in Jail.\n'.format(player.name))

        player.in_jail = 0
        player.turtle.goto(-340, -340)  # Return turtle to original track
        player.turtle.setheading(90)
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

    # Rolling doubles --- Go to jail.
    if player.double_die == 3:
        player.pos = 10
        player.in_jail = 1
        player.double_die = 0
        player.turtle.goto(-320, -320)
        player.turtle.setheading(90)  # Makes turtle face north
        player.move_count = 0
        player.last_move = 0
        print('{} was sent to Jail for rolling 3 Doubles!\n'.format(
            player.name))


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

            # For detrmining how far the turtle will go
            # Keep numbers positive
            steps = 12 - player.pos
            if steps < 0:
                steps = 40 - (player.pos - 12)
            player.pos = 12

        # Sends player to Water Works
        else:
            steps = 28 - player.pos
            if steps < 0:
                steps = 40 - (player.pos - 28)
            player.pos = 28
        player.turtle_move(steps)

    elif target == 'Railroad':

        # RR's are 5, 15, 25, 35
        # Send players to Reading RR
        player.chance_factor = 1
        if player.pos < 5 or player.pos >= 35:
            if player.pos >= 35:
                player.money += 200
                print('You passed Go -- Collect $200')
                print("{}'s Money: {}".format(player.name, player.money))

                steps = 5 - player.pos
                if steps < 0:
                    steps = 40 - (player.pos - 5)
                player.pos = 5

        # Send players to Pennsylvania RR
        elif player.pos >= 5 and player.pos < 15:
            steps = 15 - player.pos
            if steps < 0:
                steps = 40 - (player.pos - 15)
            player.pos = 15

        # Send players to B&O RR
        elif player.pos >= 15 and player.pos < 25:
            steps = 25 - player.pos
            if steps < 0:
                steps = 40 - (player.pos - 12)
            player.pos = 25

        # Send players to Short Line RR
        else:
            steps = 35 - player.pos
            if steps < 0:
                steps = 40 - (player.pos - 35)
            player.pos = 35
        player.turtle_move(steps)

    # For the move backwards 3 spaces Chance card
    elif target < 0:
        for i in range(3):
            if player.move_count == 0:
                player.turtle.left(90)
                player.turtle.backward(93.5)  # Number from end space to regular space
                player.move_count = 9
            elif player.move_count == 1:
                player.turtle.backward(93.5)  # Number from end space to regular space
                player.move_count -= 1
            else:
                player.turtle.backward(61.625)  # Number between regular spaces
                player.move_count -= 1
        player.pos += target

    # For all other advances
    else:
        steps = target - player.pos
        if steps <= 0:  # Accounts for when a player passes GO
            player.money += 200
            steps = 40 - (player.pos - target)
        player.pos = target
        player.turtle_move(steps)

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
    landlord = prop_owner[player.pos]
    color = board[player.pos][3]
    if color in landlord.community:
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


def print_properties(player):
    print("\n{}'s Properties:".format(player.name))
    print('-' * 60)

    color_list = []
    unnamed_list = []  # This list stores position, prop name, and color
    for i in player.prop:
        if board[i][3] in ['Railroad', 'Utility']:
            if board[i][-2]:
                status = 'Mortgaged'
            else:
                status = ' '
        else:
            for j in house_list:
                if j.pos == i:
                    if j.houses > 0:
                        status = '{} House(s)'.format(j.houses)
                    elif j.hotel == 1:
                        status = ('Hotel')
                    elif board[j.pos][-2] == True:
                        status = 'Mortgaged'
                    else:
                        status = ' '
                    break
        unnamed_list.append((i, board[i][0], board[i][3], status))
    sorted_list = sorted(sorted(
        unnamed_list, key=lambda x: x[0]), key=lambda x: x[2])

    for i in sorted_list:
        # For separating props by their colors for readability. If the
        # previously printed property has the same color, don't add a space
        # b/w them. Otherwise do add a space between them.
        if color_list == [] or i[2] == color_list[-1]:
            print('{:<4}{:<25}{:<20}{:<10}'.format(i[0], i[1], i[2], i[3]))
        else:
            print('\n{:<4}{:<25}{:<20}{:<10}'.format(i[0], i[1], i[2], i[3]))
            '''
            if len(i[1]) < 4:
                print('{}\t{}\t\t\t\t\t\t{}'.format(i[0], i[1],
                                                    i[2]))
            elif len(i[1]) < 8:
                print(
                    '{}\t{}\t\t\t\t\t{}'.format(i[0], i[1], i[2]))
            elif len(i[1]) < 12:
                print('{}\t{}\t\t\t\t{}'.format(i[0], i[1], i[2]))
            elif len(i[1]) < 16:
                print('{}\t{}\t\t\t{}'.format(i[0], i[1], i[2]))
            elif len(i[1]) < 20:
                print('{}\t{}\t\t{}'.format(i[0], i[1], i[2]))
            else:
                print('{}\t{}\t{}'.format(i[0], i[1], i[2]))
        else:
            if len(i[1]) < 4:
                print('{}\t{}\t\t\t\t\t\t{}'.format(i[0], i[1],
                                                    i[2]))
            if len(i[1]) < 8:
                print('\n{}\t{}\t\t\t\t\t{}'.format(i[0], i[1],
                                                    i[2]))
            elif len(i[1]) < 12:
                print(
                    '\n{}\t{}\t\t\t\t{}'.format(i[0], i[1], i[2]))
            elif len(i[1]) < 16:
                print('\n{}\t{}\t\t\t{}'.format(i[0], i[1], i[2]))
            elif len(i[1]) < 20:
                print('\n{}\t{}\t\t{}'.format(i[0], i[1], i[2]))
            else:
                print('\n{}\t{}\t{}'.format(i[0], i[1], i[2]))
            '''
        color_list.append(i[2])
    print('-' * 60)


def upgrades(player, available, minimum_money):
    print(
        '\nHouses Available : {}\tHotels Available: {}'.format(available.houses,
                                                               available.hotels))
    print('Monopolies: {}'.format(player.community))
    print("{}'s Money: {}".format(player.name, player.money))
    if player.money >= minimum_money:
        while True:
            buy_houses = input('\nBuy houses/hotels? (Y/N) >>> ')
            if buy_houses.upper() in ['Y', 'YES', 'N', 'NO']:
                break

    while (buy_houses.upper() == 'YES' or buy_houses.upper() == 'Y') \
            and (available.houses > 0 or available.hotels > 0) \
            and player.money > minimum_money:

        # This loop prevents ValueError for when a string is entered for
        # upgrade.
        while True:
            try:
                upgrade = int(input('\tEnter Selection by Number >>> '))
                # Ensures players only upgrade lots they have.
                # Makes it more intuitive: can't select option you can't afford
                while upgrade not in player.prop \
                        or player.money < board[upgrade][4] \
                        or board[upgrade][3] not in player.community \
                        or board[upgrade][-2]:

                    if upgrade not in player.prop:
                        print("\t\tYou don't own that property!")

                    elif board[upgrade][3] not in player.community:
                        print("\t\tYou don't have that monopoly!")

                    elif player.money < board[upgrade][4]:
                        print("\t\tYou can't afford this improvement!")

                    elif board[upgrade][-2]:
                        print('\t\tThis property has been mortgaged!')

                    upgrade = int(input('\tEnter Selection by Number >>> '))
                break  # Break here to exit the while True: loop
            except ValueError:
                print('\t\tInvalid Entry')

        # Using house_list instead of player.prop because player.prop only
        # lists the properties owned by their position. house_list is list of
        # properties as classes with their appropriate attributes.
        # Must use this 'for' function in order to access class.
        for i in house_list:
            if i.pos == upgrade and i.houses < 4 and i.hotel == 0:
                maximum_buy_houses = player.money // board[i.pos][4]
                if maximum_buy_houses > 4:
                    maximum_buy_houses = 4  # Can't own more than 4 houses

                number_of_upgrades = int(input('\t\tHow many houses? (${} each, {} maximum) >>> '.format(board[i.pos][4], maximum_buy_houses)))
                while number_of_upgrades > 4 \
                        or number_of_upgrades > maximum_buy_houses:

                    number_of_upgrades = int(input('\t\tHow many houses? (${} each, {} maximum) >>> '.format(board[i.pos][4], maximum_buy_houses)))

                i.houses += number_of_upgrades
                available.houses -= number_of_upgrades
                cost = board[i.pos][4] * number_of_upgrades
                player.money -= cost

                print('\n\t\t{} bought {} house(s) on {} for ${}!'.format(
                    player.name, number_of_upgrades, i.name, cost))
                print("\t\t{}'s Money: {}".format(player.name, player.money))

            # If there are no hotels, but 4 houses on a lot.
            # Gives this option after buying 4 houses and if there are 4 houses
            # Rules dictate when a hotel is bought, houses are returned to
            # bank.
            if i.pos == upgrade \
                    and i.houses == 4 \
                    and i.hotel == 0 \
                    and player.money >= board[i.pos][4]:

                while True:
                    answer = input('\t\tBuy hotel for ${}? (Y/N) >>> '.format(board[i.pos][4]))
                    if answer.upper() in ['Y', 'YES', 'N', 'NO']:
                        break

                if answer.upper() == 'YES' or answer.upper() == 'Y':
                    i.hotel = 1
                    available.hotels -= 1
                    available.houses += 4
                    i.houses -= 4
                    cost = board[i.pos][4]
                    player.money -= board[i.pos][4]

                    print('\n\t\t{} bought a hotel on {} for ${}!'.format(
                        player.name, i.name, cost))
                    print("\t\t{}'s Money: {}".format(player.name,
                                                      player.money))

        # This 'if' statement is prevent player's from bankrupting themselves
        # by buying more property they can't afford.
        if player.money >= minimum_money:
            print('\nHouses Available : {}\tHotels Available: {}'.format(
                available.houses, available.hotels))
            buy_houses = input('\nContinue buying houses/hotels? (Y/N) >>> ')


def auction(player, property):
    if isinstance(property, int):
        print('--Now auctioning {}--\n'.format(board[property][0]))
    else:
        print("--Now auctioning {}'s Property--\n".format(player.name))
    bidders = []  # List used only for this function to determine winner
    current_bid = 0
    bid = 0  # Placeholder so that you can run 'while' statement
    for bidder in player_list:
        bidders.append(bidder)

    while len(bidders) > 1:
        for i in player_list:
            if len(bidders) == 1:  # If everybody else passed, no need to bid again.
                break
            if i in bidders:  # If a player passes, they would not show up in bidders, but they are still in player_list
                print("{}'s Money: {}".format(i.name, i.money))

                # This while statement makes it so that your only options are
                # to pass or to bet more than the last bid.
                while True:
                    # Prevents error for entering a string
                    while True:
                        try:
                            bid = int(input('\t{}, please enter bid of at least ${} or Pass with Zero (0) >>> '.format(i.name, current_bid + 1)))
                            break
                        except ValueError:
                            print('\t\tInvalid Entry')

                    # Removes the passed player and allows others to continue
                    # bidding.
                    if bid == 0:
                        bidders.remove(i)
                        print('\t\t{} Passes'.format(i.name))
                        break

                    elif bid > current_bid:
                        current_bid = bid
                        break
                print('')

    winner = bidders[0]
    if isinstance(property, int):
        winner.prop.append(property)
        prop_owner[property] = winner
        board[property][-1] = True
        winner.money -= current_bid
        print('{} is SOLD to {} for {}!'.format(board[property][0], winner.name, current_bid))
        print("{}'s Money: {}".format(winner.name, winner.money))
    else:
        winner.prop = winner.prop + property
        player.prop = []
        for i in property:
            prop_owner[i] = winner
        winner.money -= current_bid
        print("{}'s property is SOLD to {} for {}!".format(player.name, winner.name, current_bid))
        print("{}'s Money: {}".format(winner.name, winner.money))
            

def mortgage(player, available):
    while True:
        try:
            to_mort = int(input('\tEnter selection by Number >>> '))
            if to_mort in player.prop:
                break
            else:
                print("\t\tYou don't own that property!")
        except ValueError:
            to_mort = 'exit'
            break
    #to_mort = int(to_mort)
    # If the property is owned by the player and is not mortgaged yet.
    if to_mort in player.prop and not board[to_mort][-2]:

        # Checks to see if its railroad or utility and does mortgage since they
        # don't have houses.
        if board[to_mort][-3] in ['Railroad', 'Utility']:
            value = int(
                board[to_mort][1] / 2)  # Mortgage gives 1/2 of property cost

            while True:
                are_you_sure = input(
                    '\t\tDo you want to mortage {} for ${}? (Y/N) >>> '.format(
                        board[to_mort][0], value))
                if are_you_sure.upper() in ['Y', 'YES', 'N', 'NO']:
                    break

            if are_you_sure.upper() in ['Y', 'YES']:
                player.money += value
                board[to_mort][-2] = True
                print('\n{} mortgages {} for ${}'.format(player.name,
                                                         board[to_mort][0],
                                                         value))
        for i in house_list:
            if i.pos == to_mort:
                if i.houses > 0:
                    house_value = int(board[i.pos][4] / 2)

                    # Prevents selling more houses than what's on the property
                    while True:
                        to_sell = int(input('\t\tSell how many houses? '
                                            '(${} each, {} maximum) >>> '
                                            .format(house_value, i.houses)))
                        if to_sell <= i.houses:
                            break

                    player.money += house_value * to_sell
                    i.houses -= to_sell
                    available.houses += to_sell
                    print('\n{} sells {} houses on {} for ${}'.format(player.name, to_sell, i.name, house_value * to_sell))

                # House rule: Selling a hotel entails not getting houses
                # back due to possible house conflict if there are no more
                # houses to return to lot, and a hotel investment should
                # be a risk. But hotel is worth 5 houses.
                elif i.hotel == 1:
                    hotel_value = board[i.pos][4] * 5 / 2
                    to_sell = input('\t\tSell hotel for ${}? >>> '.format(hotel_value))
                    player.money += hotel_value
                    i.hotel = 0
                    available.hotels += 1
                    print('\n{} sells a hotel on {} for ${}'.format(player.name, i.name, hotel_value))

                # Ability to mortgage property if all houses were sold or there
                # were no houses in the first place
                if i.houses == 0 and i.hotel == 0:
                    value = int(board[to_mort][1] / 2)  # Mortgage gives 1/2 of property cost
                    are_you_sure = input('\t\tDo you want to mortage {} for ${}? (Y/N) >>> '.format(board[to_mort][0], value))
                    if are_you_sure.upper() in ['Y', 'YES']:
                        player.money += value
                        board[to_mort][-2] = True
                        print('\n{} mortgages {} for ${}'.format(player.name, board[to_mort][0], value))
                break  # To speed up runtime to avoid more iterations when a match is found.

    elif to_mort in player.prop and board[to_mort][-2]:
        cost = round(board[to_mort][1] / 2 * 1.1)
        unmort_option = input('\t\tDo you want to unmortgage {} for ${}? (Y/N) >>> '.format(board[to_mort][0], cost))
        if unmort_option.upper() in ['Y', 'YES']:
            player.money -= cost
            board[to_mort][-2] = False
            print('\n{} unmortgages {} for ${}'.format(player.name, board[to_mort][0], cost))

    print("\n{}'s Money: {}".format(player.name, player.money))

    # Brown and Blue are monopolies if you own two properties.
    # If all properties in a community are mortgaged, the monopoly no longer
    # exists (no rent paid, can't buy houses/hotels).
    for i in community_colors:
        lot = 0
        mortgaged_prop = 0
        for j in player.prop:
            if board[j][3] == i:
                lot += 1
                if board[j][-2]:
                    mortgaged_prop += 1

        if i == 'Brown' or i == 'Blue':
            if lot == 2 and mortgaged_prop < 2:
                if i not in player.community:
                    player.community.append(i)
            elif lot == 2 and mortgaged_prop == 2:
                if i in player.community:
                    player.community.remove(i)
        else:
            if lot == 3 and mortgaged_prop < 3:
                if i not in player.community:
                    player.community.append(i)
            elif lot == 3 and mortgaged_prop == 2:
                if i in player.community:
                    player.community.remove(i)


def trade(player):
    patron = input('Who do you want to trade with? >>> ')
    for i in player_list:
        player_offer = []
        patron_offer = []
        if i.name == patron:
            print("\n{} --- Enter 'Done' when finished".format(player.name))

            player_trade_money = int(input('\tEnter money involved in trade >>> '))

            while True:
                player_item = input('\tEnter properties involved in trade by Number >>> ')
                if player_item.upper() == 'DONE':
                    break
                elif int(player_item) not in player.prop:
                    print("\t\tYou don't own this property!")
                else:
                    player_offer.append(int(player_item))

            print("\n{} --- Enter 'Done' when finished".format(i.name))
            while True:
                try:
                    patron_trade_money = int(input('\tEnter money involved in trade >>> '))
                    break
                except ValueError:
                    print('Enter a number')

            while True:
                patron_item = input('\tEnter properties inovlved in trade by Number >>> ')
                if patron_item.upper() == 'DONE':
                    break
                elif int(patron_item) not in i.prop:
                    print("\t\tYou don't own this property!")
                else:
                    patron_offer.append(int(patron_item))  #int() here to allow above input to be 'Done'

            if len(player_offer) >= len(patron_offer):
                list_size = len(player_offer)
            else:
                list_size = len(patron_offer)

            print('\n{:<25} \t{:<25}'.format("{}'s Offer: ".format(player.name), "{}'s Offer: ".format(i.name)))
            print('-' * 50)
            print('${:<24}|\t${:<25}'.format(player_trade_money,
                                             patron_trade_money))
            for j in range(list_size):
                try:
                    player_index = int(player_offer[j])
                except IndexError:
                    player_index = ' '
                try:
                    patron_index = int(patron_offer[j])
                except IndexError:
                    patron_index = ' '

                # Prints side by side column of what each player is playing
                # The ':<' means align left with the given space
                if patron_index == ' ':
                    print('{:<25}|\t{:<25}'.format(board[player_index][0], ' '))
                elif player_index == ' ':
                    print('{:<25}|\t{:<25}'.format(' ', board[patron_index][0]))
                else:
                    print('{:<25}|\t{:<25}'.format(board[player_index][0], board[patron_index][0]))

            while True:
                verify = input('\nDo you accept this trade? (Y/N) >>> ')
                if verify.upper() in ['Y', 'YES', 'NO', 'N']:
                    break

            if verify.upper() in ['Y', 'YES']:
                for j in player_offer:
                    player.prop.remove(j)
                    i.prop.append(j)
                    prop_owner[j] = i
                    player.money -= player_trade_money
                    i.money += player_trade_money
                for k in patron_offer:
                    i.prop.remove(k)
                    player.prop.append(k)
                    prop_owner[k] = player
                    i.money -= patron_trade_money
                    player.money += patron_trade_money

            break  # This break to increase run time


def turn(player):
    print("{}'s Position: {} {}".format(
        player.name, player.pos, board[player.pos][0]))
    print(player.name + "'s Money: ", player.money)
    property = player.pos  # Properties are labelled by index number
    # Player Options

    # If property is not owned and player has the money, gives option to buy.
    if not board[player.pos][-1] and player.money >= board[player.pos][1]:
        # Options to buy property

        buy = input('\nBuy {} for {}? (Y/N) >>> '.format(board[property][0],
                                                         board[property][1]))

        while buy.upper() not in ['YES', 'NO', 'Y', 'N']:
            buy = input('\tPlease enter (Y/N) >>> ')
        
        '''
        # For quickly testing or generating lots of data
        # Buys every property
        print('')
        buy = 'YES'
        '''
        if buy.upper() in ['Y', 'YES']:
            player.prop.append(property)
            prop_owner[property] = player
            board[property][-1] = True
            player.money -= board[property][1]

            print('{} buys {} for ${}.'.format(
                player.name, board[property][0], board[property][1]))
            print("{}'s Money: {}".format(player.name, player.money))

        elif buy.upper() == 'N' or buy.upper() == 'NO':
            print('{} did not buy {}\n'.format(player.name, board[property][0]))

            if len(player_list) < 3:
                for i in player_list:
                    if i != player and i.money > board[property][1]:
                        offer_to_other = input("{}'s money: {}\n{}, do you want to buy {}? (Y/N) >>> ".format(i.name, i.money, i.name, board[property][0]))
                        if offer_to_other.upper() in ['Y', 'YES']:
                            i.prop.append(property)
                            prop_owner[property] = i
                            board[property][-1] = True
                            i.money -= board[property][1]
                            print('{} buys {}'.format(i.name, board[property][0]))
                            print("{}'s Money: {}".format(i.name, i.money))
            else:
                auction(player, property)



    # If property is owned or is an event.
    # Below code runs if player lands on a space he doesn't own himself.
    elif board[player.pos][-1] and player.pos not in player.prop:

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

            # Runs function that handles rent for any property
            # Accounts for landing on Just Visiting, Free Parking, or GO.
            # Those spots have a rent value of 0, hence if statement.
            if board[player.pos][2] != 0:
                if board[player.pos][-2]:
                    print('\n{} is mortgaged. No rent paid.'.format(board[player.pos][0]))
                else:
                    payment(player, property)

    # If the player cannot afford the property.
    elif player.money < board[player.pos][1]:
        print('\n{} cannot afford {}'.format(
            player.name, board[player.pos][0]))
        auction(player, property)

    # Every turns checks to see if a player owns a monopoly.
    # Brown and Blue are monopolies if you own two properties.
    # If all properties in a community are mortgaged, the monopoly no longer
    # exists (no rent paid, can't buy houes/hotels).
    for i in community_colors:
        lot = 0
        mortgaged_prop = 0
        for j in player.prop:
            if board[j][3] == i:
                lot += 1
                if board[j][-2]:
                    mortgaged_prop += 1

        if i == 'Brown' or i == 'Blue':
            if lot == 2 and mortgaged_prop < 2:
                if i not in player.community:
                    player.community.append(i)
            elif lot == 2 and mortgaged_prop == 2:
                if i in player.community:
                    player.community.remove(i)
        else:
            if lot == 3 and mortgaged_prop < 3:
                if i not in player.community:
                    player.community.append(i)
            elif lot == 3 and mortgaged_prop == 2:
                if i in player.community:
                    player.community.remove(i)


def main():
    print('\n~~~ Welcome to Monopoly by Austin ~~~\n')
    global board
    # color properties: [name, buying cost, base_rent, community color,
    # house/hotel cost, house1 rent, house2 rent, house3 rent, house4 rent,
    # hotel rent, mortgaged?, owned?]
    # board will be referenced many times throughout program, easier to store
    # all information regarding the board here
    board = {
        0: ['GO', 0, 0, 0, True],
        1: ['Mediterranean Ave.', 60, 2, 'Brown', 50, 10, 30, 90, 160, 250, False, False],
        2: ['Community Chest', community_chest],
        3: ['Baltic Ave.', 60, 4, 'Brown', 50, 20, 60, 180, 320, 450, False, False],
        4: ['Income Tax', tax, True],
        5: ['Reading Railroad', 200, railroad, 'Railroad', False, False],
        6: ['Oriental Ave.', 100, 6, 'Light_Blue', 50, 30, 90, 270, 400, 550, False,
            False],
        7: ['Chance', chance],
        8: ['Vermont Ave.', 100, 6, 'Light_Blue', 50, 30, 90, 270, 400, 550, False, False],
        9: ['Connecticut Ave.', 120, 8, 'Light_Blue', 50, 40, 100, 300, 450, 600, False, False],
        10: ['Jail/Just Visiting', 0, 0, 0, True],  # Just visiting
        11: ['St. Charles Place', 140, 10, 'Purple', 100, 50, 150, 450, 625, 750, False, False],
        12: ['Electric Company', 150, utility, 'Utility',False, False],
        13: ['States Ave.', 140, 10, 'Purple', 100, 50, 150, 450, 625, 750, False, False],
        14: ['Virginia Ave.', 160, 12, 'Purple', 100, 60, 180, 500, 700, 900, False, False],
        15: ['Pennsylvania Railroad', 200, railroad, 'Railroad', False, False],
        16: ['St. James Place', 180, 14, 'Orange', 100, 70, 200, 550, 750, 950, False, False],
        17: ['Community Chest', community_chest],
        18: ['Tennessee Ave.', 180, 14, 'Orange', 100, 70, 200, 550, 750, 950, False, False],
        19: ['New York Ave.', 200, 16, 'Orange', 100, 80, 220, 600, 800, 1000, False, False],
        20: ['Free Parking', tax, True],
        21: ['Kentucky Ave.', 220, 18, 'Red', 150, 90, 250, 700, 875, 1050, False, False],
        22: ['Chance', chance],
        23: ['Indiana Ave.', 220, 18, 'Red', 150, 90, 250, 700, 875, 1050, False, False],
        24: ['Illinois Ave.', 240, 20, 'Red', 150, 100, 300, 750, 925, 1100, False, False],
        25: ['B.& O. Railroad', 200, railroad, 'Railroad', False, False],
        26: ['Atlantic Ave.', 260, 22, 'Yellow', 150, 110, 330, 800, 975, 1150, False, False],
        27: ['Ventnor Ave.', 260, 22, 'Yellow', 150, 110, 330, 800, 975, 1150, False, False],
        28: ['Water Works', 150, utility, 'Utility', False, False],
        29: ['Marvin Gardens', 280, 24, 'Yellow', 150, 120, 360, 850, 1025, 1200, False, False],
        30: ['Go To Jail', jail],  # Go to Jail
        31: ['Pacific Ave.', 300, 26, 'Green', 200, 130, 390, 900, 1100, 1275, False, False],
        32: ['North Carolina Ave.', 300, 26, 'Green', 200, 130, 390, 900, 1100, 1275, False, False],
        33: ['Community Chest', community_chest],
        34: ['Pennsylvania Ave.', 320, 28, 'Green', 200, 150, 450, 1000, 1200, 1400, False, False],
        35: ['Short Line Railroad', 200, railroad, 'Railroad', False, False],
        36: ['Chance', chance],
        37: ['Park Place', 350, 35, 'Blue', 200, 175, 500, 1100, 1300, 1500, False, False],
        38: ['Luxury Tax', tax, True],
        39: ['Boardwalk', 400, 50, 'Blue', 200, 200, 600, 1400, 1700, 2000, False, False],
    }

    # Using this to keep track how many houses/hotels a player has purchased
    global house_list
    global community_colors
    house_list = []
    community_colors = []
    available = HouseHotel()

    # List of colors for use when it come to dealing with monopolies
    for j in board.values():
        if len(j) == 12:
            if j[3] not in community_colors:
                community_colors.append(j[3])

    # For keeping track of houses and hotels for applicable properties
    for i in board.keys():
        if len(board[i]) == 12:
            house_list.append(Property(i, board[i][0], board[i][4]))

    global prop_owner
    prop_owner = {}
    # Turtle graphics setup
    # bgpic accepts gif images only. Image size is 750x750
    wn = turtle.Screen()
    wn.setup(800, 800)
    #wn.screensize(800, 800)
    turtle.bgpic('/Users/austinlee/Documents/Programming/Monopoly/Board-2.gif')

    # Use a make_player function to create player classes, designated only
    # by player.name
    '''
    global player_list
    player_list = []
    while True:
        try:
            player_no = int(input('Enter Number of Players >>> '))
            break
        except ValueError:
            print('\tEnter a number')

    for i in range(player_no):
        name = input('Player ' + str(i+1) + ' Name >>> ')
        player_list.append(make_player(name))

    # Turtle set up for each player
    turtle_colors = ['blue', 'green', 'red', 'orange']
    for j in player_list:
        j.turtle.shape('turtle')
        j.turtle.color = random.choice(turtle_colors)
        j.turtle.goto(315, -315)
    print("\n~~~~~ Let's Play ~~~~~\n")

    # This section is for testing purposes
    '''
    austin = Player('Austin')
    ben = Player('Ben')
    priscilla = Player('Priscilla')
    global player_list
    player_list = [austin, ben]

    # Turtle set up for each player
    turtle_colors = ['blue', 'green', 'red', 'orange']
    for j in player_list:
        j.turtle.shape('turtle')
        j.turtle.right(180)  # Orients turtle in correct direction

        # Ensures each player has their color
        turtle_color_choice = random.choice(turtle_colors)
        turtle_colors.remove(turtle_color_choice)
        j.turtle.color(turtle_color_choice)
        j.color = turtle_color_choice.upper()

        j.turtle.up()
        j.turtle.goto(340, -340)  # About where you would want pieces to be
    '''
    ben.prop = [39, 37]
    prop_owner[37] = ben
    prop_owner[39] = ben
    board[39][-1] = True
    board[37][-1] = True
    # house_list[21].houses = 4
    '''

    while len(player_list) > 1:
        for player in player_list:
            # First checks to see if the player is in jail.
            # While in the jail, the player rolls his movement.
            # Thus, the player moves according to his movement.
            print("~~~ {}'s ({}) Turn ~~~".format(player.name, player.color))
            jail_options(player)

            # Movement Phase
            player.pos += player.last_move
            player.turtle_move(player.last_move)


            # For when player reaches GO
            if player.pos > 39:
                player.money += 200
                player.pos = player.pos - 40
                print('You passed Go -- Collect $200')
                print("{}'s Money: {}\n".format(player.name, player.money))


            # For testing positions/events on board
            # austin.pos = 22
            # ben.pos = 7

            # This function gives players ability to buy property or pay rent
            turn(player)

            if player.prop != []:
                print_properties(player)
            while True:
                print('\nOptions:')
                print('T - Trade')  # Trade for money, no properties needed
                if player.prop != []:
                    print('M - Mortgage/Umortgage')
                    if player.community != []:
                        print('U - Upgrades')
                print('E - End Turn')

                option = input('\nSelect Option by Letter >>> ')
                if option.upper() in ['T', 'TRADE']:
                    trade(player)

                elif option.upper() in ['M', 'MORTGAGE']:
                    if player.prop != []:
                        mortgage(player, available)
                    else:
                        print("\tYou don't have any property!")

                # Enable Buying Houses/Hotels with this option
                # Below line allows a player to buy property if they have a
                # monopoly.
                # Min. money searches for monopolies a player has, if any, and
                # determines the min. money required to buy a house.
                elif option.upper() in ['U', 'UPGRADE']:
                    upgrade_costs = []
                    for lot in house_list:
                        if board[lot.pos][3] in player.community:
                            upgrade_costs.append(lot.cost)
                    minimum_money = sorted(upgrade_costs)[0]
                    if player.money >= minimum_money:
                        upgrades(player, available, minimum_money)

                elif option.upper() in ['E', 'END']:
                    break

            # When a player loses, remove the player from the list so that
            # play rotates between the remaining players
            # Checks every turn because a player can bankrupt on somebody
            # else's turn
            for i in player_list:
                if i.money < 0:
                    player_list.remove(i)
                    print('\n{} declares bankruptcy!'.format(i.name))
                    if len(player_list) > 1:
                        auction(i, i.prop)
            print('-' * 77)

    # Declaring the winner
    winner = player_list[0]
    print('\n~~~ Congratulations {}, you are the winner!!! ~~~\n'.format(
        winner.name))


if __name__ == '__main__':
    main()
