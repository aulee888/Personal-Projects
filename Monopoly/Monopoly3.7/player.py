from random import randint
from board import board, railroads, utilities


class PlayerCreation:
    players = []

    def player_creation(self):
        # # For actually playing the game
        # players = []
        # number_of_players = int(input('Enter number of players >>> '))
        # print('')
        #
        # for i in range(1, number_of_players + 1):
        #     player_name = input(f"Enter Player {i}'s Name >>> ")
        #     players.append(Player(player_name))
        #
        # print('')

        #  For testing purposes
        player_names = ['Austin', 'Thoann']  # Add more players here
        for player in player_names:
            self.players.append(Player(player))


class Player:
    def __init__(self, name):
        self.name = name
        self.money = 1500
        self.owned = []
        self.position = 0
        self.last_roll = 0  # Used for utility rent
        self.utility_chance_factor = False  # For x10 on Chance card
        self.in_jail = False  # Integer is turns in jail; False is not in jail

    def print_owned(self):
        # Column Names and formatting
        print(f"{'Number':<8}"
              f"{'Property Name':<23}"
              f"{'Type':<10}"
              f"{'Houses':<7}")
        print('-'*7, '-'*22, '-'*9, '-'*7)  # Should be -1 from above padding

        # -- TO DO -- #
        # Need to sort the self.owned list by color and then by number
        for prop in sorted(self.owned):
            number_for_selection = f'[{prop}]'

            if prop not in railroads + utilities:
                house_or_hotel = 'Hotel' if board[prop].hotel else board[prop].houses  # Shows that a hotel exists on prop if fully upgraded
                prop_type = board[prop].color

            elif prop in railroads:
                house_or_hotel = 'N/A'
                prop_type = 'Railroad'

            else:
                house_or_hotel = 'N/A'
                prop_type = 'Utility'

            print(f"{number_for_selection:<8}"
                  f"{board[prop].name:<23}"
                  f"{prop_type:<10}"
                  f"{house_or_hotel:>7}")

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
            die1 = randint(1, 6)
            die2 = randint(1, 6)
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

        # -- TO DO -- #
        # Display the prop info such as rent/upgrade/color before purchase

        curr_loc = board[self.position]
        while True:
            option = input(f'Purchase {curr_loc.name} for ${curr_loc.cost}? >>> ')

            if option.upper() in ['Y', 'YES', '1']:
                self.owned.append(self.position)
                self.money -= curr_loc.cost
                curr_loc.owner = self  # Points to player object instead of player.name; prevents case if >=2 players have the same name

                if self.position in railroads:
                    curr_loc.rr_owners.append(self)  # Same idea as above

                if self.position in utilities:
                    curr_loc.utility_owners.append(self)  # Same idea as above

                # Info
                print(f'{self.name} buys {curr_loc.name} for ${curr_loc.cost}.')
                print(f"{self.name}'s Money: {self.money} \n")
                break

            elif option.upper() in ['N', 'NO', '2']:
                print('')
                break

    def pay_rent(self):
        """Pays the rent to the landlord of a property."""
        curr_loc = board[self.position]
        landlord = curr_loc.owner

        if self.position in utilities:
            rent = curr_loc.get_rent(self)  # Rent rules for utilities are slightly different; need to incorporate last_move
        else:
            rent = curr_loc.get_rent()  # Every other prop not require last_move

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

        while True:
            selection = input('Upgrade which property? >>> ')
            if selection.upper() in ['NO', 'N', 'E', '']:
                upgrading = False
                print('')
                break
            else:
                selection = int(selection)

            if selection not in self.owned:
                print(f'{self.name} does not own this property. \n')
            elif selection in railroads + utilities:
                print('Railroad and Utility upgrades cannot be purchased. \n')
            elif not board[selection].monopoly():
                print(f'{self.name} does not have a monopoly on {board[selection].color}! \n')
            else:
                upgrading = True
                break

        if upgrading:
            # Column Names and formatting
            print(f"{'Option':<8}"
                  f"{'Description':<13}"
                  f"{'Rent':<6}"
                  f"{'Upgrade Cost':<14}")
            print('-'*7, '-'*12, '-'*5, '-'*13)  # Lines; should be -1 from above padding

            # Shows only available options
            # i.e. if own 2 houses, shows only option buy house 3/4/hotel
            for i in range(board[selection].houses + 1, 6):
                number_for_selection = f'[{i}]'

                if i < 5:
                    description = f'House {i}'
                else:
                    description = 'Hotel'

                # 4 houses must be purchased before a hotel can be bought
                # One house upgrade costs the upgrade_cost based on prop color
                # i.e. Brown upgrade cost is $50 >>> 2 houses costs $100
                # To go from 2 houses to 3 houses costs $50
                # 3 houses to 4 houses costs $50
                # 4 houses to hotel costs $50
                # Hence the strange math in the last print line
                print(f"{number_for_selection:<8}"
                      f"{description:<13}"
                      f"{board[selection].rent[i]:>5}"
                      f"{board[selection].upgrade_cost * (i - board[selection].houses):>13}")

            print('')  # Spacing

            while True:
                # Prevents entering breaking values:
                # i.e. More than 4 houses and a hotel
                # i.e. A number of houses that currently exist on the prop
                upgrades_to_buy = input('Upgrade Option >>> ')

                if upgrades_to_buy in ['N', 'NO', 'E', '']:
                    print('')
                    break
                else:
                    upgrades_to_buy = int(upgrades_to_buy)
                    cost = board[selection].upgrade_cost \
                                * (upgrades_to_buy - board[selection].houses)

                if upgrades_to_buy <= board[selection].houses \
                        or upgrades_to_buy > 6:
                    print('Select another option. \n')
                else:
                    if cost >= self.money:
                        # Info
                        print(
                            f'{self.name} does not have enough money to buy this upgrade. \n')

                    else:
                        if upgrades_to_buy == 5:
                            board[selection].hotel = True
                            self.money -= cost
                            purchase = 'a hotel'

                        else:
                            board[selection].houses += upgrades_to_buy
                            self.money -= cost
                            purchase = f'{upgrades_to_buy} house(s)'

                        # Info
                        print(f'{self.name} bought {purchase} for ${cost}.')
                        print(f"{self.name}'s Money: {self.money} \n")
                    break
