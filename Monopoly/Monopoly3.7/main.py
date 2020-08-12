from player import Player
from board import*
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


# #  For testing purposes
player_names = ['Austin', 'Thoann']  # Add more players here
players = [Player(name) for name in player_names]

while len(players) > 1:
    for player in players:

        # Info
        print(f"### {player.name}'s Turn ###")

        player.move()

        if player.position not in chances + community_chests + taxes + misc_pos:  # These parts are still in development
            curr_loc = board[player.position]

            # If property is not owned, option to buy.
            # Made so you don't bankrupt yourself buying property.
            if not curr_loc.owner and player.money > curr_loc.cost:
                player.buy()

            # Pay rent to landlord.
            elif curr_loc.owner != player:
                player.pay_rent()

        if player.owned:
            player.print_owned()

        # -- TO DO -- #
        # Show only options that are available
        # e.g. No upgrade or trade option when a player doesn't have property
        action = input('Select Action:\n'
                       '--------------\n'
                       '[1]\t Upgrade \n'
                       '[2]\t Trade \n'
                       '[3]\t End \n'
                       '>>>\t ')

        # Offers option to upgrade any owned properties.
        if action == '1' and player.owned:
            player.upgrade()

        if player.money <= 0:
            players.remove(player)

        print('-'*35)
