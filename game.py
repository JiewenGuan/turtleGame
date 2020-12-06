import turtle
import time
import random
SIDELENGTH = 300
PEDDING = 40


class Player:
    def __init__(self):
        self.moveSpeed = 5
        self.avatar = turtle.Turtle()
        self.avatar.speed(0)
        self.avatar.shape('tank')
        self.avatar.penup()
        self.avatar.setpos(SIDELENGTH, 0)
        self.avatar.left(90)

    def getHight(self):
        return self.avatar.ycor()

    def up(self):
        self.avatar.forward(self.moveSpeed)

    def down(self):
        self.avatar.backward(self.moveSpeed)


class Balloon:
    def __init__(self):
        self.goUp = random.randint(0, 1) == 1
        self.countDown = random.randint(0, 10)
        self.moveSpeed = 2
        self.avatar = turtle.Turtle()
        self.avatar.speed(0)
        self.avatar.shape('circle')
        self.avatar.pencolor(141, 159, 92)
        self.avatar.fillcolor(158, 188, 71)
        self.avatar.turtlesize(2, 2, 2)
        self.avatar.penup()
        self.avatar.setpos(-SIDELENGTH, 0)
        self.avatar.left(90)

    def reset(self):
        self.goUp = random.randint(0, 1) == 1
        self.countDown = random.randint(20, 100)

    def move(self):
        if(self.goUp):
            self.avatar.forward(self.moveSpeed)
        else:
            self.avatar.backward(self.moveSpeed)
        self.countDown -= 1
        if(self.countDown == 0):
            self.reset()
        if(self.avatar.ycor() > SIDELENGTH):
            self.avatar.sety(-SIDELENGTH)
        if(self.avatar.ycor() < -SIDELENGTH):
            self.avatar.sety(SIDELENGTH)

    def getHight(self):
        return self.avatar.ycor()


class Bullet:
    def __init__(self, height):
        self.moveSpeed = 3
        self.avatar = turtle.Turtle()
        self.avatar.hideturtle()
        self.avatar.speed(0)
        self.avatar.shape('square')
        self.avatar.penup()
        self.avatar.setpos(SIDELENGTH, height)
        self.avatar.color('gray')
        self.avatar.showturtle()

    def move(self):
        self.avatar.backward(self.moveSpeed)

    def getHight(self):
        return self.avatar.ycor()

    def explowed(self):
        self.avatar.color('red')
        self.avatar.shape('circle')
        self.avatar.turtlesize(2, 2, 2)

    def delete(self):
        self.avatar.hideturtle()
        del self


class Window:

    def drawBorder(self):
        border = SIDELENGTH+PEDDING
        mypen = turtle.Turtle()
        mypen.speed(0)
        mypen.penup()
        mypen.setpos(-border, -border)
        mypen.pendown()
        mypen.pensize(3)

        for side in range(4):
            mypen.forward(border*2)
            mypen.left(90)
        mypen.hideturtle()

        del mypen

    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.colormode(255)
        #self.register_shape('tank', ((20,-30), (20,40), (-20,40), (-20,-30), (-10,-30), (-10,-60), (10, -60), (10, -30)))
        self.screen.register_shape('tank', ((-30, -20), (40, -20), (40, 20),
                                            (-30, 20), (-30, 10), (-60, 10), (-60, -10), (-30, -10)))
        self.drawBorder()

    def clear(self):
        self.screen.clear()


class Game:
    def __init__(self):
        self.flying_bullets = []
        self.missed = 0
        self.playing = True
        self.window = Window()
        self.player = Player()
        self.balloon = Balloon()
        turtle.listen()
        turtle.onkeypress(self.player.up, 'Up')
        turtle.onkeypress(self.player.down, 'Down')
        turtle.onkey(self.fire, 'space')

    def win(self):
        self.window.clear()
        turtle.write(("Missed shots: " + str(self.missed)), move = False, font = ("Arial", 20, "normal"))

    def dealBullet(self):
        for bullet in self.flying_bullets:
            bullet.move()
            if (bullet.avatar.xcor() < -SIDELENGTH):
                bullet.explowed()
                if(bullet.getHight() > self.balloon.getHight() - 20 and bullet.getHight() < self.balloon.getHight() + 20):
                    self.playing = False
            if (bullet.avatar.xcor() < -(SIDELENGTH+PEDDING)):
                self.flying_bullets.remove(bullet)
                self.missed += 1
                bullet.delete()

    def fire(self):
        if(len(self.flying_bullets)>0):
            return
        bullet = Bullet(self.player.getHight())
        self.flying_bullets.append(bullet)

    def play(self):
        while self.playing == True:
            self.balloon.move()
            self.dealBullet()
        self.win()




game = Game()
game.play()
time.sleep(5)
