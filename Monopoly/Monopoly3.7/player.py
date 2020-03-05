import random
from board import board


class Player:
    def __init__(self, name):
        self.name = name
        self.money = 1500
        self.owned = []
        self.position = 0
        self.last_roll = 0
        self.in_jail = False

    def move(self):
        """Board must be imported to use this function.
        Function used to traverse across the board, simulates the dice rolls at
        the beginning of a player's turn.
        last_roll is used to calculate utility rent if landed on utility.
        """
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        total = die1 + die2

        self.last_roll = total
        self.position += total

        # Info
        print(f"Roll: {die1} + {die2} = {total}!")
        print(f"{self.name}'s Position: {self.position % 40} "
              f"{board[self.position % 40].name}.")
        print(f"{self.name}'s Money: {self.money} \n")

        # Collect $200 when you pass Go.
        if self.position > 39:
            self.money += 200
            self.position -= 40

            # Info
            print(f'{self.name} passed GO! Collect $200!')
            print(f"{self.name}'s Money: {self.money} \n")

    def buy(self):
        """Simulates purchasing property."""
        curr_loc = board[self.position]
        option = input(f'Purchase {curr_loc.name} for ${curr_loc.cost}? >>> ')

        if option.upper() not in ['Y', 'YES', 'N', 'NO']:
            self.buy()

        elif option.upper() in ['Y', 'YES']:
            self.owned.append(self.position)
            self.money -= curr_loc.cost
            curr_loc.owner = self

            # Info
            print(f'{self.name} buys {curr_loc.name} for ${curr_loc.cost}.')
            print(f"{self.name}'s Money: {self.money} \n")

    def pay_rent(self):
        """Pays the rent to the landlord of a property."""
        curr_loc = board[self.position]
        landlord = curr_loc.owner
        rent = curr_loc.get_rent()

        self.money -= rent
        landlord.money += rent

        # Info
        print(f'{self.name} pays {landlord.name} ${rent} in rent.')
        print(f"{self.name}'s Money: {self.money} \n")

    def upgrade(self):
        # Info
        print(f"{self.name}'s Money: {self.money}")

        selection = int(input('Upgrade which property? >>> '))

        if selection not in self.owned:

            # Info
            print(f'{self.name} does not own this property.')
            self.upgrade()

        elif selection in self.owned:

            # Info
            for i in range(board[selection].houses + 1, 6):
                if i < 5:
                    print(f'House {i}: ${board[selection].upgrade_cost * (i - board[selection].houses)}')
                elif i == 5:
                    print(f'Hotel: ${board[selection].upgrade_cost * (i - board[selection].houses)}')

            upgrades_to_buy = int(input('How many upgrades to buy? >>> '))
            cost = board[selection].upgrade_cost * upgrades_to_buy

            if cost <= self.money:

                # Info
                print(f'{self.name} does not have enough money to buy {upgrades_to_buy} upgrades.')
                self.upgrade()

            else:
                board[selection].houses += upgrades_to_buy
                self.money -= cost

                # Info
                print(f'{self.name} bought {upgrades_to_buy} for ${cost}.')
                print(f"{self.name}'s Money: {self.money} \n")


