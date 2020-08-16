import pandas as pd
# from community_chest import community_chest
# from chance import chance


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
        if self.hotel:
            return self.rent[5]

        else:
            return self.rent[self.houses]

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

    def get_rent(self):
        self.count = 0

        for owner in self.utility_owners:
            if owner == self.owner:
                self.count += 1

        if self.count == 1:
            return 4 * last_move

        elif self.count == 2:
            return 10 * last_move


class Chance:
    def __init__(self):
        self.name = 'Chance'


class CommunityChest:
    def __init__(self):
        self.name = 'Community Chest'


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
