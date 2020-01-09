import random
import re


class Block:
    # Initial values, before AB Score Improvements and CON bonuses
    def __init__(self):
        self.ab_list = ['STR', 'DEX', 'CON', 'WIS', 'INT', 'CHR']
        self.LV = 1

        self.HP = dice_rolls(1, 6)[0]  # Can balance by changing the which die
        self.STR = random.randint(8, 15)
        self.DEX = random.randint(8, 15)
        self.CON = random.randint(8, 15)
        self.WIS = random.randint(8, 15)
        self.INT = random.randint(8, 15)
        self.CHR = random.randint(8, 15)

    def improvement(self, LV):
        for level in range(2, LV+1):
            # 2 ptns of improvement every 4th level
            # Randomly assigned
            if (level % 4 == 0 and level != 20) or level == 19:
                for j in range(2):
                    # Syntax does not allow self.chosen to be the same as
                    # self.STR for example. Must use setattr() to change an
                    # attribute from within the function.
                    # Therefore, cannot access an attribute through an alias.
                    # But the object can be accessed through an alias.
                    chosen = random.choice(self.ab_list)
                    ab_value = getattr(self, chosen)
                    setattr(self, chosen, ab_value + 1)

            # Handles rolling hit dice and CON modifiers
            HP_roll = dice_rolls(1, 6)[0]
            self.HP += HP_roll
            if level >= 20:
                mod = 5
            elif level >= 18:
                mod = 4
            elif level >= 16:
                mod = 3
            elif level >= 14:
                mod = 2
            elif level >= 12:
                mod = 1
            else:
                mod = 0

            self.HP += mod
            self.LV += 1

            # For seeing behavior of improvement function
            #print_block(self)
            #print('\tHP Rolled: {} + ({})'.format(HP_roll, mod))


def dice_rolls(cast, die):
    results = []
    sum = 0
    for die_cast in range(cast):
        roll = random.randint(1, die)
        sum += roll
        results.append(roll)
    return sum, results


def print_block(block):
    print('LV: \t{}'.format(block.LV))
    print('HP: \t{}'.format(block.HP))
    print('STR:\t{}'.format(block.STR))
    print('DEX:\t{}'.format(block.DEX))
    print('CON:\t{}'.format(block.CON))
    print('WIS:\t{}'.format(block.WIS))
    print('INT:\t{}'.format(block.INT))
    print('CHR:\t{}'.format(block.CHR))


def balance(block):
    #Point Cost dict setup
    ab_points = 27
    ab_point_cost = {8: 0, 9: 1, 10: 2, 11: 3, 12: 4, 13: 5, 14: 7, 15: 9}

    for ability in block.ab_list:
        ab_value = getattr(block, ability)  # Returns value of attribute
        ab_points -= ab_point_cost[ab_value]
    return ab_points
    # Negative AB represents strong stats
    # Positive AB represents weak stats
    # Zero represents the perfectly balanced character


def main():
    while True:
        # \D matches non-digit characters, so anything not 0-9, AKA [^0-9]
        # Represents the number of dice cast or blocks created...
        # Must be int() so it can be used in functions
        user_input = input('\nEnter Dice Roll (xdy) or Stat Block (xLVy) >>> ')
        if user_input.upper() in ['EXIT', 'E', 'DONE', 'N']:
            break

        match = re.search(r'(\d+)(\D+)(\d+)', user_input)
        x = int(match.group(1))
        y = int(match.group(3))

        # For dice rolls
        if match.group(2).upper() == 'D':
            print('')
            count = 1
            sum, results = dice_rolls(x, y)
            for i in results:
                print('{:<10}{}'.format('Roll {}:'.format(count), i))
                count += 1
            print('\n{:<10}{}'.format('Total: ', sum))

        # For stat blocks
        # Prints AB first before applying improvement to see stat balance
        elif match.group(2).upper() == 'LV':
            block_list = []
            for i in range(x):
                block_list.append(Block())
            count = 1
            for j in block_list:
                print('\n{:<10}'.format('Block {}'.format(count)))
                print('{:>10}'.format('AB: {}'.format(balance(j))))
                print('-' * 10)
                j.improvement(y)
                print_block(j)
                count += 1


if __name__ == '__main__':
    main()
