from turtle import Turtle

sona = Turtle()
for i in range(8):
    for j in range(8):
        sona.forward(70)
        sona.right(360 / 8)
    sona.forward(70)
    sona.left(360 / 8)
