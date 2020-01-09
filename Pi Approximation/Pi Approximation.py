import random
import numpy as np
import turtle

def drop_test(a, b, x_lines):
    cross = 0
    if a > b:
        for line in x_lines:
            if b <= line <= a:
                cross += 1
            else:
                cross += 0
        if cross:
            return True
        else:
            return False
    elif a < b:
        for line in x_lines:
            if a <= line <= b:
                cross += 1
            else:
                cross += 0
        if cross:
            return True
        else:
            return False
    else:
        for line in x_lines:
            if line == a and line == b:
                cross += 1
            else:
                cross += 0
        if cross:
            return True
        else:
            return False


def approximation(length, count, width, crossed):
    calc = (2 * length * count) / (width * crossed)
    return calc


class Pi:
    # Used to allow for uses of variables w/o having to recall them
    # their values. These reusable values were initialized in __init__.

    def __init__(self, sides, subsections, turtle):
        # Creates the lines which sticks would cross.
        # Boundaries do count as crossable lines.

        self.sides = sides
        self.lines_x_pos = []
        self.width = sides / subsections
        for i in range(subsections+1):  # +1 to include end boundary.
            self.lines_x_pos.append(i*self.width)

            # Draws boundaries and crossable lines.
            turtle.up()
            turtle.goto(i*self.width, 0)
            turtle.pencolor('blue')
            turtle.down()
            turtle.forward(100)

        # For seeing which are the crossable lines.
        print(self.lines_x_pos)

    def sticks(self, length, count, turtle):
        sticks_dict = {}
        crossed = 0  # Placeholder for returned value.
        for i in range(count):
            center_x_pos = random.randrange(self.sides + 1)
            center_y_pos = random.randrange(self.sides + 1)
            rotation = random.randrange(180)

            # Creates points (a,b) and (c,d).
            a = center_x_pos + (length / 2)*np.cos(np.deg2rad(rotation + 180))
            b = center_y_pos + (length / 2)*np.sin(np.deg2rad(rotation + 180))
            c = center_x_pos + (length / 2)*np.cos(np.deg2rad(rotation))
            d = center_y_pos + (length / 2)*np.sin(np.deg2rad(rotation))

            turtle.up()
            turtle.goto(a, b)
            turtle.down()
            turtle.pencolor('orange')
            turtle.pensize(2.5)  # A good size for the width
            turtle.goto(c, d)

            crosses = drop_test(a, c, self.lines_x_pos)
            if crosses:
                crossed += 1

            sticks_dict[i] = (crosses,
                              (round(a, 2), round(b, 2)),
                              (round(c, 2), round(d, 2)),
                              (round(a, 2), round(c, 2)))

            print(str(i) + '\t' + str(sticks_dict[i][0])
                  + '\t' + str(sticks_dict[i][1])
                  + '\t' + str(sticks_dict[i][2])
                  + '\t' + str(sticks_dict[i][3]))

        return self.width, crossed


def main():
    # length = input('Length of Stick >>> ')
    # count = input('Sticks Tossed >>> ')

    # setworldcoordinates is what enlarges the drawing size.
    # tracer adjusts the animation speed with framerate and delay.
    wn = turtle.Screen()
    wn.screensize(canvwidth=100, canvheight=100)
    wn.setworldcoordinates(-25, -25, 125, 125)
    wn.tracer(5, 0)
    alex = turtle.Turtle()
    alex.left(90)
    alex.hideturtle()

    length = 16  # Values closer to width gives really good approximations
    count = 200

    # 100 is a good screen size.
    # 6 is a pretty decent subsection number.
    width, crossed = Pi(100, 6, alex).sticks(length, count, alex)

    calc = approximation(length, count, width, crossed)
    error = np.abs((calc - np.pi) / calc * 100)

    print('\nSticks Tossed: ' + str(count))
    print('Sticks Crossed: ' + str(crossed))
    print('\nApproximation: ' + str(calc))
    print('Error: ' + str(round(error, 2)) + '%')

    wn.exitonclick()  # Close window on click


if __name__ == '__main__':
    main()
