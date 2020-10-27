from PIL import Image
import math


def most_frequent(file_name, length):
    with open(file_name) as file:
        text = file.read()
    text = text.split(' ')
    dic = {}
    for word in text:
        word = word.strip("\n")
        if len(word) >= length:
            dic[word] = dic.get(word, 0) + 1
    for word in (sorted(dic, key=dic.get, reverse=True))[:10]:
        print(word, dic[word])


def process_names(input_file, output_file):
    with open(input_file) as input_f:
        input_lines = input_f.readlines()

    with open(output_file, "w") as output:
        for name in sorted(input_lines):
            output.write(name.title())


BLACK = (0, 0, 0)
BG = (239, 236, 202)


def disk(size=150, r=50):
    img = Image.new("RGB", (size, size), BG)
    for x in range(size // 2 - r // 2, size // 2 + r // 2):
        for y in range(size // 2 - r // 2, size // 2 + r // 2):
            img.putpixel((x, y), BLACK)
    img.save("rect.png")


def gradient():
    fst = (255, 0, 255)
    snd = (160, 50, 0)
    thrd = (255, 0, 100)
    img = Image.new("RGB", (400, 400), BG)
    for x in range(img.width):
        for y in range(x + 1):
            # Find the distance to the center
            distanceToCenter = img.width - x
            # Make it on a scale from 0 to 1
            distanceToCenter = float(distanceToCenter) / img.width
            # Calculate r, g, and b values
            r = fst[0] * distanceToCenter + snd[0] * (1 - distanceToCenter)
            g = fst[1] * distanceToCenter + snd[1] * (1 - distanceToCenter)
            b = fst[2] * distanceToCenter + snd[2] * (1 - distanceToCenter)
            img.putpixel((x - y, y), (int(r), int(g), int(b)))
    for y in range(1, img.height):
        for x in range(img.width - 1, y - 1, -1):
            # Find the distance to the center
            distanceToCenter = img.width - y
            # Make it on a scale from 0 to 1
            distanceToCenter = float(distanceToCenter) / img.width
            # Calculate r, g, and b values
            r = snd[0] * distanceToCenter + thrd[0] * (1 - distanceToCenter)
            g = snd[1] * distanceToCenter + thrd[1] * (1 - distanceToCenter)
            b = snd[2] * distanceToCenter + thrd[2] * (1 - distanceToCenter)
            img.putpixel((x, y + (img.height - 1 - x)), (int(r), int(g), int(b)))
    img.save("grad.png")


def invert(color):
    return 255 - color[0], 255 - color[1], 255 - color[2]


def no_red(color):
    return 0, color[1], color[2]


def greyscale(color):
    grey = sum(color) // 3
    return grey, grey, grey


def modify_colors(file_name, modifier, prefix):
    img = Image.open(file_name)
    img.convert("RGB")
    img1 = Image.new("RGB", (img.width, img.height), BLACK)
    for x in range(img.width):
        for y in range(img.height):
            new_color = modifier(img.getpixel((x, y)))
            img1.putpixel((x, y), new_color)
    img1.save(prefix + ".jpg")


gradient()
