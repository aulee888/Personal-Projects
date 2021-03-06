import pandas as pd
from random import randint, randrange
# from community_chest import community_chest


class Property:
    def __init__(self, name):
        self.name = name
        self.owner = None
        self.mortgaged = False

    def __str__(self):
        return (f'Property: {self.name} \n'
                f'Owner: {self.owner} \n'
                f'Mortgaged: {self.mortgaged}')


class Street(Property):
    def __init__(self, name, color, cost, base_rent, upgrade_cost,
                 rent1, rent2, rent3, rent4, rent5):
        super().__init__(name)
        self.color = color
        self.cost = cost
        self.base_rent = base_rent
        self.upgrade_cost = upgrade_cost
        self.rent = [base_rent, rent1, rent2, rent3, rent4, rent5]
        self.houses = 0  # Integer ranging 0 - 4
        self.hotel = False

    def get_rent(self):
        print(self.monopoly())
        if self.hotel:
            return self.rent[5]
        else:
            if self.houses == 0 and self.monopoly():  # Double on unimproved monopolized lots
                return 2 * self.rent[0]
            else:
                return self.rent[self.houses]

    def monopoly(self):
        # For determining how whether or not rent is doubled on unimproved lots
        # Or determining whether or not player can buy houses/hotels
        count = 0
        for prop in self.owner.owned:
            if prop not in railroads + utilities:
                if board[prop].color == self.color:
                    count += 1

        if self.color in ['Brown', 'Blue']:  # Need only two of each of these colors
            threshold = 2
        else:
            threshold = 3

        if count < threshold:
            return False
        else:
            return True

    def __str__(self):
        return (f'Property: {self.name} \n' \
                f'Color: {self.color} \n' \
                f'Houses: {self.houses} \n' \
                f'Hotel: {self.hotel} \n' \
                f'Owner: {self.owner} \n' \
                f'Mortgaged: {self.mortgaged}')


class RailRoad(Property):
    # Faster to search through a small list (max 4) of RRs than a potentially
    # larger list of all properties owned by a player
    rr_owners = []

    def __init__(self, name):
        super().__init__(name)
        self.cost = 200

    def get_rent(self):
        self.count = 0

        for owner in self.rr_owners:
            if owner == self.owner:
                self.count += 1

        return 25 * 2**(self.count - 1)  # Formula for 25, 50, 100, 200


class Utility(Property):
    utility_owners = []

    def __init__(self, name):
        super().__init__(name)
        self.cost = 150

    def get_rent(self, player):
        self.count = 0

        for owner in self.utility_owners:
            if owner == self.owner:
                self.count += 1

        if player.utility_chance_factor:
            x10 = 10
            player.utility_chance_factor = False
        elif not player.utility_chance_factor:
            x10 = 1

        if self.count == 1:
            return 4 * player.last_roll * x10
        elif self.count == 2:
            return 10 * player.last_roll * x10


class Chance:
    def __init__(self):
        self.name = 'Chance'

    def chance(self, player):
        chance_df = pd.read_excel('chance_data.xlsx')
        card = chance_df.iloc[randrange(16)]
        print(f"{player.name} drew [{card['number']}] {card['description']}!")

        if card['function'] == 'advance':
            self.advance(player, card['position'])
        elif card['function'] == 'pay':
            self.pay(player, card['amount'])
        else:
            self.get_card(player)

    def advance(self, player, to_position):
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
            player.utility_chance_factor = True

            if 12 <= player.position < 28:
                player.position = 28

            elif player.position >= 28:
                print(f'{player.name} passed GO! Collect $200! \n')
                player.money += 200
                player.position = 12

            else:
                player.position = 12

        elif to_position < 0:  # For move backwards chance
            player.position += to_position

        else:  # For advances to specific locations
            if to_position == 10:
                GoToJail().go_to_jail(player)

            else:
                print(to_position)
                if player.position > to_position:
                    print(f'{player.name} passed GO! Collect $200! \n')
                    player.money += 200

                player.position = to_position

        # Info
        # This last section of advance() was copied from main.py
        print(f"{player.name}'s Position: {player.position % 40} "
              f"{board[player.position % 40].name}.")
        print(f"{player.name}'s Money: {player.money} \n")

        if player.position not in chances + community_chests + taxes + misc_pos:  # These parts are still in development
            curr_loc = board[player.position]

            # If property is not owned, option to buy.
            # Made so you don't bankrupt yourself buying property.
            if not curr_loc.owner and player.money > curr_loc.cost:
                player.buy()

            # Pay rent to landlord.
            elif curr_loc.owner != player:
                player.pay_rent()

        elif player.position in taxes:
            if player.position == 4:
                IncomeTax().pay_income_tax(player)
            else:
                LuxuryTax().pay_luxury_tax(player)

        elif player.position in misc_pos:
            if player.position == 30:
                GoToJail().go_to_jail(player)

    def pay(self, player, amount):
        from player import PlayerCreation

        if amount == 'players':
            # Info
            print(f"{player.name} pays out ${(len(PlayerCreation().players) - 1) * 50}! \n")

            for other_player in PlayerCreation().players:
                if other_player != player:
                    player.money -= 50
                    other_player.money += 50

                    # Info
                    print(f"{other_player.name}'s Money: {other_player.money}")

            print(f"{player.name}'s Money: {player.money} \n")

        elif amount == 'upgrades':
            house_count = 0
            hotel_count = 0

            for prop in player.owned:
                if prop not in railroads + utilities:
                    house_count += board[prop].houses
                    hotel_count += board[prop].hotel

            general_repair_cost = 25 * house_count + 100 * hotel_count
            player.money -= general_repair_cost

            print(f"{player.name} owns {house_count} house(s).")
            print(f"{player.name} owns {hotel_count} hotel(s).")
            print(f"{player.name} pays (25 * {house_count}) + (100 * {hotel_count}) = ${general_repair_cost} in repairs!")
            print(f"{player.name}'s Money: {player.money} \n")

        else:
            player.money += amount
            print(f"{player.name}'s Money: {player.money} \n")

    def get_card(self, player):
        player.get_out_of_jail_free += 1
        print(f"{player.name} now has {player.get_out_of_jail_free} Get Out of Jail Free Card(s)! \n")


class CommunityChest:
    def __init__(self):
        self.name = 'Community Chest'

    def comm_chest(self, player):
        comm_df = pd.read_excel('comm_chest_data.xlsx')
        card = comm_df.iloc[randrange(16)]
        print(f"{player.name} drew [{card['number']}] {card['description']}!")

        if card['number'] == 0:  # Go to Jail card
            GoToJail().go_to_jail(player)
        elif card['function'] == 'pay':
            self.pay(player, card['amount'])
        else:
            self.get_card(player)

    def pay(self, player, amount):
        from player import PlayerCreation

        if amount == 'players':
            # Info
            print(f"{player.name} pays out ${(len(PlayerCreation().players) - 1) * 50}! \n")

            for other_player in PlayerCreation().players:
                if other_player != player:
                    player.money -= 50
                    other_player.money += 50

                    # Info
                    print(f"{other_player.name}'s Money: {other_player.money}")

            print(f"{player.name}'s Money: {player.money} \n")

        elif amount == 'upgrades':
            house_count = 0
            hotel_count = 0

            for prop in player.owned:
                if prop not in railroads + utilities:
                    house_count += board[prop].houses
                    hotel_count += board[prop].hotel

            general_repair_cost = 40 * house_count + 115 * hotel_count
            player.money -= general_repair_cost

            print(f"{player.name} owns {house_count} house(s).")
            print(f"{player.name} owns {hotel_count} hotel(s).")
            print(f"{player.name} pays (40 * {house_count}) + (115 * {hotel_count}) = ${general_repair_cost} in repairs!")
            print(f"{player.name}'s Money: {player.money} \n")

        else:
            player.money += amount
            print(f"{player.name}'s Money: {player.money} \n")

    def get_card(self, player):
        player.get_out_of_jail_free += 1
        print(
            f"{player.name} now has {player.get_out_of_jail_free} Get Out of Jail Free Card(s)! \n")


class IncomeTax:
    def __init__(self):
        self.name = 'Income Tax'

    def pay_income_tax(self, player):
        """
        Player pays either 10% of the income, or flat $200
        Whichever is greater
        """
        # -- TO DO -- #
        # Need to add house rule where taxes go to Free Parking
        if 0.10 * player.money > 200:
            tax = 0.10 * player.money
        else:
            tax = 200

        player.money -= tax
        print(f'{player.name} pays ${tax} in taxes!')
        print(f"{player.name}'s Money: {player.money}\n")


class LuxuryTax:
    def __init__(self):
        self.name = 'Luxury Tax'

    def pay_luxury_tax(self, player):
        # -- TO DO -- #
        # Need to add house rule where taxes go to Free Parking
        player.money -= 75

        print(f'{player.name} pays $75 in taxes!')
        print(f"{player.name}'s Money: {player.money}\n")


class Jail:
    def __init__(self):
        self.name = 'Jail'

    def jail_time(self, player):
        if player.in_jail > 3:
            player.in_jail = False
            print(f"{player.name} finished their Jail Sentence! \n")

            player.move()

        elif player.in_jail >= 1:
            use_get_out_of_jail_free = False
            print(f"{player.name} has spent {player.in_jail} turn(s) in jail! \n")

            if player.get_out_of_jail_free:
                use_card = input(f'Use Get Out of Jail Free Card? ({player.get_out_of_jail_free} Card(s)) >>> ')
                if use_card.upper() in ['Y', '1']:
                    player.in_jail = False
                    use_get_out_of_jail_free = True  # Skips bail option
                    player.get_out_of_jail_free -= 1
                    print(f"{player.name} uses a Get Out of Jail Free Card! \n")

            if not use_get_out_of_jail_free:
                bail = input('Pay $50 bail? >>> ')
                if bail.upper() in ['Y', '1']:
                    player.in_jail = False
                    player.money -= 50
                    print(f"{player.name} pays bail to leave Jail!")
                    print(f"{player.name}'s Money: {player.money} \n")
                else:
                    self.breakout(player)

            if not player.in_jail:
                player.move()  # This assumes the player broke out of jail or paid bail
            else:
                player.in_jail += 1

    def breakout(self, player):
        die1 = randint(1, 6)
        die2 = randint(1, 6)

        if die1 == die2:
            player.in_jail = False
            msg = f"{player.name} breaks out of jail! \n"
        else:
            msg = f"{player.name} fails to break out of jail! \n"

        print(f"{player.name} rolls {die1} & {die2}!")
        print(msg)


class Go:
    def __init__(self):
        self.name = 'Go'


class FreeParking:
    def __init__(self):
        self.name = 'Free Parking'
        self.money = 0


class GoToJail:
    def __init__(self):
        self.name = 'Go to Jail'

    def go_to_jail(self, player):
        player.position = 10
        player.in_jail = 1

        print(f"{player.name} was sent to Jail! \n")


board = {}

properties_df = pd.read_excel('properties_data.xlsx')
for i in range(len(properties_df)):
    curr = properties_df.loc[i]
    board[curr['position']] = Street(curr['name'], curr['color'],
                                       curr['cost'], curr['base_rent'],
                                       curr['upgrade_cost'],
                                       curr['rent1'], curr['rent2'],
                                       curr['rent3'], curr['rent4'],
                                       curr['rent5'])

railroads = [5, 15, 25, 35]
board[5] = RailRoad('Reading Railroad')
board[15] = RailRoad('Pennsylvania Railroad')
board[25] = RailRoad('B. & O. Railroad')
board[35] = RailRoad('Short Line Railroad')

utilities = [12, 28]
board[12] = Utility('Electric Company')
board[28] = Utility('Water Works')

chances = [7, 22, 36]
board[7] = Chance()
board[22] = Chance()
board[36] = Chance()

community_chests = [2, 17, 33]
board[2] = CommunityChest()
board[17] = CommunityChest()
board[33] = CommunityChest()

taxes = [4, 38]
board[4] = IncomeTax()
board[38] = LuxuryTax()

misc_pos = [0, 10, 20, 30]
board[0] = Go()
board[10] = Jail()
board[20] = FreeParking()
board[30] = GoToJail()

# Importing at the end prevents circular import error.
# Ensures that board, railroads, utilities, etc. variables are created.
# That way player.py can import them w/o error.
# Otherwise if import placed at top of script, player.py would try to import
# variables that don't exist yet.
from player import PlayerCreation
