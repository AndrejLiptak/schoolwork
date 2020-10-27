import math, random


class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def get_perimeter(self):
        return math.pi * (self.radius ** 2)

    def get_area(self):
        return 2 * math.pi * self.radius

    def __str__(self):
        return "Circle at " + str(self.center) + " with radius " + str(self.radius)


class Book:
    def __init__(self, name, author, ISBN, price):
        self.name = name
        self.author = author
        self.ISBN = ISBN
        self.price = price


class Turtle:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.direction = 0
        self.lines = []
        self.color = "black"

    def left(self, angle):
        self.direction -= angle

    def right(self, angle):
        self.direction += angle

    def forward(self, distance):
        nx = self.x + distance * math.cos(self.direction * math.pi / 180)
        ny = self.y + distance * math.sin(self.direction * math.pi / 180)

        self.lines.append((self.x, self.y, nx, ny))
        self.x, self.y = nx, ny

    def get_lines_svg(self):
        svg = ""
        for x1, y1, x2, y2 in self.lines:
            svg += """\t<line x1='{}' y1='{}' x2='{}' y2='{}'
                style='stroke: {}; stroke-width:2' />\n""".format(x1, y1, x2, y2, self.color)
        return svg

    def save(self, filename):
        with open(filename, "w") as f:
            f.write(
                '<svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" xmlns:xlink= "http://www.w3.org/1999/xlink">\n')
            f.write(self.get_lines_svg())
            f.write("\n</svg>")

    def polygon(self, n, dis):
        for _ in range(n):
            self.forward(dis)
            self.right(360 // n)

    def set_color(self, color):
        self.color = color

    def random_step(self, dis):
        self.right(random.randint(0,360))
        self.forward(dis)


julia = Turtle()
julia.polygon(3,50)
julia.forward(100)
julia.set_color("red")
julia.polygon(4,50)
julia.save("trt")
julia.random_step(100)
