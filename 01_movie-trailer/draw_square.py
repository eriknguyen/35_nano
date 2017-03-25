import turtle
from turtle import *


def draw_square(t):
    for i in range(0, 4):
        t.forward(100)
        t.right(90)


def draw():
    window = turtle.Screen()
    window.bgcolor('#dedede')

    me = turtle.Turtle()
    me.color('red')
    me.shape('turtle')
    me.speed(10)

    me.color('red', 'yellow')

    for i in range(0, 36):
        me.begin_fill()
        draw_square(me)
        me.right(10)
        me.end_fill()

    you = turtle.Turtle()
    # you.shape('arrow')
    you.color('blue')
    you.circle(100)

    window.exitonclick()


def draw_sun():
    color('red', 'yellow')
    begin_fill()
    while True:
        forward(200)
        left(170)
        if abs(pos()) < 1:
            break
    end_fill()
    done()


def draw_triangle(t, size, fill_color):
	t.color('black', fill_color)
	t.begin_fill()
	for i in range(0,3):
		t.forward(size)
		t.right(120)
	t.end_fill()


def draw_multitri():
	t = turtle.Turtle()
	size = 128
	for i in range(1,5):
		draw_triangle(t, size, '#fecb3c')


window = turtle.Screen()
draw_multitri()
window.exitonclick()
# draw_sun()
# draw()
