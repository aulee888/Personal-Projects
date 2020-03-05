from player import Player
from board import board

players = []
number_of_players = int(input('Enter number of players >>> '))
print('')

for i in range(1, number_of_players + 1):
    player_name = input(f"Enter Player {i}'s Name >>> ")
    players.append(Player(player_name))

print('')

while len(players) > 1:
    for player in players:

        # Info
        print(f"### {player.name}'s Turn ###")

        player.move()

        if player.position not in [7, 22, 36, 2, 17, 33, 4, 38, 0, 10, 20, 30]:
            curr_loc = board[player.position]

            # If property is not owned, option to buy.
            # Made so you don't bankrupt yourself buying property.
            if not curr_loc.owner and player.money > curr_loc.cost:
                player.buy()

            # Pay rent to landlord.
            elif curr_loc.owner != player:
                player.pay_rent()

        # Offers option to upgrade any owned properties.
        if player.owned:
            print(player.owned)
            player.upgrade()

        if player.money <= 0:
            players.remove(player)

        print('-'*35)
