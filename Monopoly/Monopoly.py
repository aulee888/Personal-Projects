# Figure out how to pull the necessary information from source code.
# Saved to programming folder.

import random


class Action:
    def move(self):
        # Simulates dice roll
        self.movement = (random.randint(1, 6) + random.randint(1, 6))
        print('Roll: ', self.movement)  # Using commas does not require object
                                        # conversion
        return self.movement

class Event:
    # To store functions in a dictionary, omit the ().
    # For the non-property things that can happen.
    def __init__(self, players, house, hotel):
        self.events = {
            # Community Chest Cards
            0: ('Advance to Go (Collect $200)', 200),
            1: ('Bank error in your favor -- Collect $200', 200),
            2: ("Doctor's Fee -- Pay $50", -50),
            3: ('From sale of you stock you get $50', 50),
            4: ('Get Out of Jail Free', Event.get_out_of_jail),
            5: ('Go to Jail', Event.jail),
            6: ('Grand Opera Night -- Collect $50 from every player',
                 50*players),
            7: ('Holiday Fund matures -- Collect $100', 100),
            8: ('Income Tax Refund -- Collect $20', 20),
            9: ('It is your birthday -- Collect $10', 10),
            10: ('Life Insurance matures -- Collect $100', 100),
            11: ('Pay hospital fees -- Pay $100', -100),
            12: ('Pay school fees -- Pay $150', -150),
            13: ('Receive Consultancy Fee -- Collect $25', 25),
            14: ('You are assessed for street repairs -- $40 per house'
                  ' -- $115 per hotel', -(40*house + 115*hotel)),
            15: ('You won second prize in a beauty contest -- Collect $10',
                  10),
            16: ('You inherit $100', 100),

            # Chance Cards
            17: ('Advance to Go (Collect $200)', 200),
            18: ('Advance to Illinois Ave. -- If you pass Go, collect $200',
                  Event.advance(self, 'Illinois Ave.')),
            19: ('Advance to St. Charles Place -- If you pass Go, '
                  'collect $200', Event.advance(self, 'St. Charles Place')),
            20: ('Advance to Utility. If unowned, you may buy it. If owned,'
                  ' throw dice and pay owner a total ten times the amount '
                  'thrown', Event.utility),
            21: ('Advance to nearest Railroad and pay ownder twice the rental'
                  ' to which he is otherwise ntitled. If Railroad is unowned, '
                  'you may buy it', Event.railroad),
            22: ('Bank pays you dividend of $50', 50),
            23: ('Get Out of Jail Free', Event.get_out_of_jail),
            24: ('Go back 3 spaces', Event.advance(self, -3)),
            25: ('Go to Jail', Event.jail),
            26: ('Make general repairs on all your property -- $25 per house'
                  ' -- $100 per hotel', -(25*house + 100*hotel)),
            27: ('Pay poor tax of $15', -15),
            28: ('Take a trip to Reading Railroad -- If you pass Go, collect'
                  ' $200', Event.advance(self, 'Reading Railroad')),
            29: ('Take a walk on the Boardwalk -- Advance to Boardwalk',
                  Event.advance(self, 'Boardwalk')),
            30: ('You have been elected Chairman of the Board -- Pay each'
                  ' player $50', -50 * players),
            31: ('Your building and loan matures -- Collect $150', 50),
            32: ('You have won a crossword competition -- Collect $100', 100),
        }

    def community_chest(self):
        card = random.randrange(17)
        print(self.events[card][0])
        community_effect = self.events[card][1]
        return community_effect

    def chance(self):
        card = random.randrange(17, 33)
        print(self.events[card][0])
        chance_effect = self.events[card][1]
        return chance_effect

    def go(self):
        return 200

    def get_out_of_jail(self):
        return True

    def advance(self, position):
        return True

    def jail(self):
        return 0

    def tax(self):
        return -250

    def utility(self):
        return -150

    def railroad(self):
        return -250


def main():
    # Use the values of the dict as lines to allow for editing
    # Properties read as [Name, Cost, Rent, Color, Owned]
    # Events read as [Name, function]
    board = {
        0: ['GO', Event.go],
        1: ['Mediterranean Ave.', 60, 2, 'Brown', False],
        2: ['Community Chest', Event.community_chest],
        #3: ['Baltic Ave.', 60, 4, 'Brown', True],
        3: ['Baltic Ave.', 60, 4, 'Brown', False],
        4: ['Income Tax', Event.tax()],
        5: ['Reading Railroad', 200, Event.railroad, 0, False],
        6: ['Oriental Ave.', 100, 6, 'Light Blue', False],
        7: ['Chance', Event.chance],
        8: ['Vermont Ave.', 100, 6, 'Light Blue', False],
        9: ['Connecticut Ave.', 120, 8, 'Light Blue', False],
        10: ['Just Visiting', 0, 0, 0, True],  # Just visiting
        11: ['St. Charles Place', 140, 10, 'Purple', False],
        12: ['Electric Company', 150, Event.utility, 0, False],
        13: ['States Ave.', 140, 10, 'Purple', False],
        14: ['Virginia Ave.', 160, 12, 'Purple', False],
        15: ['Pennsylvania Railroad', 200, Event.railroad, 0, False],
        16: ['St. James Place', 180, 14, 'Orange', False],
        17: ['Community Chest', Event.community_chest],
        18: ['Tennessee Ave.', 180, 14, 'Orange', False],
        19: ['New York Ave.', 200, 16, 'Orange', False],
        20: ['Free Parking', 0, 0, 0, True],
        21: ['Kentucky Ave.', 220, 18, 'Red', False],
        22: ['Chance', Event.chance],
        23: ['Indiana Ave.', 220, 18, 'Red', False],
        24: ['Illinois Ave.', 240, 20, 'Red', False],
        25: ['B. & O. Railroad', 200, Event.railroad, 0, False],
        26: ['Atlantic Ave.', 260, 22, 'Yellow', False],
        27: ['Ventnor Ave.', 260, 22, 'Yellow', False],
        28: ['Water Works', 150, Event.utility, 0, False],
        29: ['Marvin Gardens', 280, 24, 'Yellow', False],
        30: ['Go To Jail', Event.jail],  # Go to Jail
        31: ['Pacific Ave.', 300, 26, 'Green', False],
        32: ['North Carolina Ave.', 300, 26, 'Green', False],
        33: ['Community Chest', Event.community_chest],
        34: ['Pennsylvania Ave.', 320, 28, 'Green', False],
        35: ['Short line Railroad', 20, Event.railroad, 0, False],
        36: ['Chance', Event.chance],
        37: ['Park Place', 350, 35, 'Blue', False],
        38: ['Luxury Tax', Event.tax],
        39: ['Boardwalk', 400, 50, 'Blue', False],
    }

    player = {}
    player_money = {}
    player_pos = {}  # Board position
    player_prop = {}  # Properties owned

    '''
    player_count = int(input('Enter Number of Players >>> '))
    for i in range(1, player_count+1):
        # Dictionary Format: {Player No. : (Name, Money, Position)}
        players[i] = (input('Player ' + str(i) + ' >>> '))
        player_money[i] = 1500  # Initial starting amount
        player_position[i] = 0  # GO Spot
    '''

    # For testing purposes
    player[1] = 'Austin'
    player_money[1] = 1500
    player_pos[1] = 0
    player_prop[1] = []

    player[2] = 'Ben'
    player_money[2] = 1500
    player_pos[2] = 0
    player_prop[2] = []

    player_pos[1] += Action().move()
    if player_pos[1] > 39:
        # Accounts for the end of the board and restarts positions
        player_money[1] += Event(0, 0, 0).go()
        player_pos[1] = player_pos[1] - 40

    print(player[1] + "'s Position: " + board[player_pos[1]][0])
    print(player[1] + "'s Money: ", player_money[1], '\n')

    # Player Options
    if not board[player_pos[1]][-1]:
        # If property is not owned, gives option to buy.
        #buy = input('Buy ' + board[player_pos[1]][0] + ' for '
         #           + str(board[player_pos[1]][1]) + '? (Y/N) >>> ')
        buy = 'YES'
        if buy.upper() == 'Y' or buy.upper() == 'YES':
            player_prop[1].append(board[player_pos[1]][0])
            board[player_pos[1]][-1] = True

    ### Encountering problem where special events like tax or cards are reading
    ### as true. Need to correct.
    # If property is owned.
    # Should edit what's printed to 'Austin gains $4... Total: $1504'
    if board[player_pos[1]][-1]:
        if len(board[player_pos[1]]) == 2:
            loss = board[player_pos[1]][1]
            print(loss)
            #player_money[1] -= board[player_pos[1]][1]
        else:
            player_money[1] -= board[player_pos[1]][2]
            for i in player_prop:
                if board[player_pos[1]][0] in player_prop[i]:
                    player_money[i] += board[player_pos[1]][2]

                    print(player[1] + "'s Money: ", player_money[1])
                    print(player[i] + "'s Money: ", player_money[i])
                    print('-'*77)



if __name__ == '__main__':
    main()
