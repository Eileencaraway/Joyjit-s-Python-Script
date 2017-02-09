import turtle
import random

#turtle=turtle()
#turtle.shape('turtle')


for i in range(100):
    step=random.uniform(10,100)
    turtle.forward(step)
    direction=random.randint(0,360)
    turtle.left(direction)

turtle.done()
