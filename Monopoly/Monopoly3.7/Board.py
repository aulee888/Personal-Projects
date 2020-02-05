class Property:
    def __init__(self):
        self.houses = 0
        self.hotel = 0

    def __str__(self):
        return (f'Property: {self.name} \n' \
               f'Neighborbood: {self.color} \n' \
               f'Houses: {self.houses} \n' \
               f'Hotel: {self.hotel}')

class Brown(Property):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.color = 'Brown'

class LiteBlue(Property):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.color =  'LiteBlue'

class Purple(Property):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.color = 'Purple'

class Orange(Property):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.color = 'Orange'

class Red(Property):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.color = 'Red'

class Yellow(Property):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.color = 'Yellow'

class Green(Property):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.color = 'Green'

class Blue(Property):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.color = 'Blue'

board = {}
lite_blue_property = ['Mediterranean Ave.', 'Baltic Ave.', 'Oriental Ave.']
for property in lite_blue_property:
    board[property].append(LiteBlue(property))

for property in board:
    print(board[property])
    print('')