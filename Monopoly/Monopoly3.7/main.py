from board import*
from player import PlayerCreation


PlayerCreation().player_creation()


while len(PlayerCreation().players) > 1:
    for player in PlayerCreation().players:

        # Info
        print(f"### {player.name}'s Turn ###")

        # Cheating is for testing properties and monitoring behavior
        # Enter an position number to move to that location on the board
        print('')

        force = input('Cheat? [E / #]\n'
                      '>>>\t')
        print('')

        if force.upper() in ['E', ''] and not player.in_jail:  # Entering a blank skips to cheating
            player.move()

        elif player.in_jail:
            Jail().jail_time(player)

        else:
            player.move(int(force))  # End of cheating section

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

        elif player.position in chances:
            Chance().chance(player)

        if player.owned:
            player.print_owned()

        # -- TO DO -- #
        # Show only options that are available
        # e.g. No upgrade or trade option when a player doesn't have property
        while True:
            action = input('Select Action:\n'
                           '--------------\n'
                           '[1]\t Upgrade \n'
                           '[2]\t Trade \n'
                           '[3]\t End \n'
                           '>>>\t ')

            print('')  # Spacing after selecting an action for aesthetics

            # Offers option to upgrade any owned properties.
            if action == '1' and player.owned:
                player.upgrade()

            elif action in ['3', '']:
                break

        if player.money <= 0:
            PlayerCreation().players.remove(player)

        print('-'*70)  # Line to show end of turn
