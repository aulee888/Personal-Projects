import random
from board import board, railroads, utilities


class Player:
    def __init__(self, name):
        self.name = name
        self.money = 1500
        self.owned = []
        self.position = 0
        self.last_roll = 0
        self.in_jail = False

    def print_owned(self):
        # Formatting and Info
        print(f"{'Number':<8}{'Property Name':<20}{'Type':<10}{'Houses':<7}")
        print('-'*7, '-'*19, '-'*9, '-'*7)  # Should be -1 from below formatting

        # -- TO DO -- #
        # Need to sort the self.owned list by color and then by number
        for prop in sorted(self.owned):
            number_for_selection = f'[{prop}]'

            if prop not in railroads + utilities:
                house_or_hotel = 'Hotel' if board[prop].hotel else board[prop].houses  # Shows that a hotel exists on prop if fully upgraded
                print(f"{number_for_selection:<8}{board[prop].name:<20}{board[prop].color:<10}{house_or_hotel:>7}")

            elif prop in railroads:
                print(f"{number_for_selection:<8}{board[prop].name:<20}{'Railroad':<10}{'N/A':>7}")

            else:
                print(f"{number_for_selection:<8}{board[prop].name:<20}{'Utility':<10}{'N/A':>7}")

        print('')  # End all print sections with new line

    def move(self, cheat=False):
        """
        Board must be imported to use this function.
        Function used to traverse across the board, simulates the dice rolls at
        the beginning of a player's turn.
        last_roll is used to calculate utility rent if landed on utility.

        Cheat is used for testing purposes, allows the player to move a desired
        location on the board.
        """
        if not cheat:
            die1 = random.randint(1, 6)
            die2 = random.randint(1, 6)
            total = die1 + die2

            self.last_roll = total
            self.position += total

        else:
            die1 = die2 = total = 'Cheat'

            self.last_roll = cheat
            self.position = cheat

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

        if option.upper() not in ['Y', 'YES', 'N', 'NO', '1', '2']:
            self.buy()

        elif option.upper() in ['Y', 'YES', '1']:
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
        # -- TO DO -- #
        # Need to add houses back into circulation if upgrading to a hotel

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

            if cost >= self.money:

                # Info
                print(f'{self.name} does not have enough money to buy {upgrades_to_buy} upgrades.')
                self.upgrade()

            else:
                board[selection].houses += upgrades_to_buy
                self.money -= cost

                # Info
                print(f'{self.name} bought {upgrades_to_buy} for ${cost}.')
                print(f"{self.name}'s Money: {self.money} \n")
