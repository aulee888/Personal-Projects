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
                f'Owned: {self.owner} \n'
                f'Mortgaged: {self.mortgaged}')


class Street(Property):
    def __init__(self, name, color, cost, base_rent, upgrade_cost,
                 rent1, rent2, rent3, rent4, rent5):
        super().__init__(name)
        self.color = color
        self.cost = cost
        self.base_rent = base_rent
        self.upgrade_cost = upgrade_cost
        self.rent1 = rent1
        self.rent2 = rent2
        self.rent3 = rent3
        self.rent4 = rent4
        self.rent5 = rent5
        self.houses = 0
        self.hotel = 0

    def get_rent(self):
        if self.hotel == 1:
            return self.rent5

        if self.houses == 0:
            return self.base_rent
        elif self.houses == 1:
            return self.rent1
        elif self.houses == 2:
            return self.rent2
        elif self.houses == 3:
            return self.rent3
        elif self.houses == 4:
            return self.rent4

    def __str__(self):
        return (f'Property: {self.name} \n' \
                f'Color: {self.color} \n' \
                f'Houses: {self.houses} \n' \
                f'Hotel: {self.hotel} \n' \
                f'Owned: {self.owner} \n' \
                f'Mortgaged: {self.mortgaged}')


class RailRoad(Property):
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


class LuxuryTax:
    def __init__(self):
        self.name = 'Luxury Tax'


class Jail:
    def __init__(self):
        self.name = 'Jail'


class Go:
    def __init__(self):
        self.name = 'Go'


class FreeParking:
    def __init__(self):
        self.name = FreeParking
        self.money = 0


def setup():
    board = {}

    properties_df = pd.read_excel('Properties_Data.xlsx')
    for i in range(len(properties_df)):
        curr = properties_df.loc[i]
        board[curr['position']] = Street(curr['name'], curr['color'],
                                           curr['cost'], curr['base_rent'],
                                           curr['upgrade_cost'],
                                           curr['rent1'],curr['rent2'],
                                           curr['rent3'], curr['rent4'],
                                           curr['rent5'])

    board[5] = RailRoad('Reading Railroad')
    board[15] = RailRoad('Pennsylvania Railroad')
    board[25] = RailRoad('B. & O. Railroad')
    board[35] = RailRoad('Short Line Railroad')

    board[12] = Utility('Electric Company')
    board[28] = Utility('Water Works')

    board[7] = Chance()
    board[22] = Chance()
    board[36] = Chance()

    board[2] = CommunityChest()
    board[17] = CommunityChest()
    board[33] = CommunityChest()

    board[4] = IncomeTax()
    board[38] = LuxuryTax()

    board[0] = Go()
    board[10] = Jail()
    board[20] = FreeParking()

    return board