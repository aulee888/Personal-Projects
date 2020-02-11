class Property:
    def __init__(self):
        self.houses = 0
        self.hotel = 0

    def __str__(self):
        return (f'Property: {self._name} \n' \
               f'Neighborbood: {self._color} \n' \
               f'Houses: {self.houses} \n' \
               f'Hotel: {self.hotel}')


class Brown(Property):
    def __init__(self, name):
        super().__init__()
        self._name = name
        self._color = 'Brown'


class LiteBlue(Property):
    def __init__(self, name):
        super().__init__()
        self._name = name
        self._color = 'LiteBlue'


class Purple(Property):
    def __init__(self, name):
        super().__init__()
        self._name = name
        self._color = 'Purple'


class Orange(Property):
    def __init__(self, name):
        super().__init__()
        self._name = name
        self._color = 'Orange'


class Red(Property):
    def __init__(self, name):
        super().__init__()
        self._name = name
        self._color = 'Red'


class Yellow(Property):
    def __init__(self, name):
        super().__init__()
        self._name = name
        self._color = 'Yellow'


class Green(Property):
    def __init__(self, name):
        super().__init__()
        self._name = name
        self._color = 'Green'


class Blue(Property):
    def __init__(self, name):
        super().__init__()
        self._name = name
        self._color = 'Blue'


def prop_creator():
    pass


board = {}
brown_prop = ['Mediterranean Ave.', 'Baltic Ave.']
lite_blue_prop = ['Oriental Ave.', 'Vermont Ave.', 'Connecticut Ave.']
purple_prop = ['St. Charles Place', 'States Ave.', 'Virginia Ave.']
orange_prop = ['St. James Place', 'Tennessee Ave.', 'New York Ave.']
red_prop = ['Kentucky Ave.', 'Indiana Ave.', 'Illinois Ave.']
yellow_prop = ['Atlantic Ave.', 'Ventnor Ave.', 'Marvin Gardens']
green_prop = ['Pacific Ave', 'North Carolina Ave.', 'Pennsylvania Ave.']
blue_prop = ['Park Place', 'Boardwalk']

