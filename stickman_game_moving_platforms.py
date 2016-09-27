#Stickman Game from Python for Kids
#With moving platforms

from Tkinter import *
import random
import time

class Coords:
    def __init__(self, x1=0, y1=0, x2=0, y2=0):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2


def within_x(co1, co2):
    if (co1.x1 > co2.x1 and co1.x1 < co2.x2) \
        or (co1.x2 > co2.x1 and co1.x2 < co2.x2)\
        or (co2.x1 > co1.x1 and co2.x1 < co1.x2)\
        or (co2.x2 > co1.x1 and co2.x2 < co1.x2): #The author changed this.
        return True
    else:
        return False

def within_y(co1, co2):
    if (co1.y1 > co2.y1 and co1.y1 < co2.y2) \
       or (co1.y2 > co2.y1 and co1.y2 < co2.y2) \
       or (co2.y1 > co1.y1 and co2.y1 < co1.y2) \
       or (co2.y2 > co1.y1 and co2.y2 < co1.y2): #The author changed this.
        return True
    else:
        return False

def collided_left(co1, co2):
    if within_y(co1, co2):
        if co1.x1 <= co2.x2 and co1.x1 >= co2.x1:
            #print("Collided_left detected.")
            return True
    return False

def collided_top(co1, co2):
    if within_x(co1, co2):
        if co1.y1 <= co2.y2 and co1.y1 >= co2.y1:
            return True
    return False

def collided_bottom(y, co1, co2):
    if within_x(co1, co2):
        y_calc = co1.y2 + y
        if y_calc >= co2.y1 and y_calc <= co2.y2:
            return True
    return False

def collided_right(co1, co2):
    if within_y(co1, co2):
        if co1.x2 >= co2.x1 and co1.x2 <= co2.x2:
            return True
    return False



class Game:
    def __init__(self):
        self.tk = Tk()
        self.tk.title("Mr. Stick Man Races for the Exit")
        self.tk.resizable(0,0)
        self.tk.wm_attributes("-topmost", 1)
        self.canvas = Canvas(self.tk, width=500, height=500, highlightthickness=0)
        self.canvas.pack()
        self.tk.update()
        self.canvas_height = 500
        self.canvas_width = 500
        self.bg = PhotoImage(file="background.gif")
        self.bg2 = PhotoImage(file="background.gif")
        self.bg3 = PhotoImage(file="background_bookshelf.gif")
        self.bg4 = PhotoImage(file="background_lamp.gif")
        self.bg5 = PhotoImage(file="background_window.gif")
        self.backgrounds = [self.bg, self.bg2, self.bg3, self.bg4, self.bg5]
        
        w = self.bg.width()
        h = self.bg.height()
        
        for x in range(5):
            for y in range(5):
                num = random.randrange(len(self.backgrounds))
                self.canvas.create_image(x*w, y*h, image=self.backgrounds[num], anchor='nw')
                
        self.sprites = []
        #His code has True here, but I added a click to start instead:
        self.running = False
        self.game_over_text = self.canvas.create_text(250, 150, \
             text='Click to start', font=("Helvetica", 40), state='hidden')

    def start_game(self, evt):
        self.running = True
        self.canvas.itemconfig(self.game_over_text, state='hidden')
        self.canvas.itemconfig(self.game_over_text, text="You won!")

    def mainloop(self):
        while 1:
            if self.running == True:
                for sprite in self.sprites:
                    sprite.move()
            else:
                
                time.sleep(0.5)
                self.canvas.itemconfig(self.game_over_text, \
                     state='normal')
            self.tk.update_idletasks()
            self.tk.update()
            time.sleep(0.01)

class Sprite:
    def __init__(self, game):
        self.game = game
        self.endgame = False
        self.coordinates = None

    def move(self):
        pass

    def coords(self):
        return self.coordinates

class DoorSprite(Sprite):
    def __init__(self, game, x=45, y=30, width=40, height=35):
        Sprite.__init__(self, game)
        self.closed_door = PhotoImage(file="door1.gif")
        self.open_door = PhotoImage(file="door2.gif")
        
        self.image = game.canvas.create_image(x, y, image=self.closed_door, \
                                              anchor = 'nw')
        # Width/2 is used so that the figure will stop in front of the door
        # Instead of before it.
        self.coordinates = Coords(x, y, x + (width/3), y + height)
        self.endgame = True

    def open_door2(self):
        print("Now you're in the open_door2 method.")
        self.game.canvas.itemconfig(self.image, image=self.open_door)
        self.game.tk.update_idletasks()

    def close_door(self):
        print("Now you're in the close_door method.")
        self.game.canvas.itemconfig(self.image, image=self.closed_door)
        self.game.tk.update_idletasks()

class PlatformSprite(Sprite):
    def __init__(self, game, photo_image, x, y, width, height):
        Sprite.__init__(self, game)
        self.photo_image = photo_image
        self.image = game.canvas.create_image(x, y, image=self.photo_image, \
                                              anchor='nw')
        self.coordinates = Coords(x, y, x + width, y + height)

class MovingPlatformSprite(PlatformSprite):
    def __init__(self, game, photo_image, x, y, width, height):
        self.x = 2
        self.width = width
        self.height = height
        self.last_time = time.time()
        self.counter = 0
        self.game = game
        self.photo_image = photo_image
        self.image = game.canvas.create_image(x, y, image=self.photo_image, \
                                              anchor='nw')
        self.coordinates = Coords(x, y, x + width, y + height)
        self.endgame = False

    def move(self):
        if time.time() - self.last_time > 0.03:
            self.last_time = time.time()
            self.game.canvas.move(self.image, self.x, 0)
            self.counter += 1
        if self.counter > 20:
            self.x *= -1
            self.counter = 0
            
    def coords(self):
        xy = self.game.canvas.coords(self.image)
        self.coordinates.x1 = xy[0]
        self.coordinates.y1 = xy[1]
        self.coordinates.x2 = xy[0] + self.width
        self.coordinates.y2 = xy[1] + self.height
        return self.coordinates
        

class StickFigureSprite(Sprite):
    def __init__(self, game):
        Sprite.__init__(self, game)
        self.images_left = [
            PhotoImage(file="figure-L1b.gif"),
            PhotoImage(file="figure-L2d.gif"),
            PhotoImage(file="figure-L3b.gif")
            ]
        self.images_right = [
            PhotoImage(file="figure-R1b.gif"),
            PhotoImage(file="figure-R2d.gif"),
            PhotoImage(file="figure-R3b.gif")
            ]
        #To check the exit, use 90 and 30:
        self.image = game.canvas.create_image(200, 470, \
                                image=self.images_left[0], anchor='nw')
        self.x = -1 #-2
        self.y = 0 #0
        self.current_image = 0
        self.current_image_add = 1
        self.jump_count = 0
        self.last_time = time.time()
        self.coordinates = Coords()
        game.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        game.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        game.canvas.bind_all('<space>', self.jump)
        #I added the line below to start the game with a mouse click:
        game.canvas.bind_all('<Button-1>', game.start_game)

    def turn_left(self, evt):
        if self.y == 0:
            self.x = -2

    def turn_right(self, evt):
        if self.y == 0:
            self.x = 2

    def jump(self, evt):
        if self.y == 0:
            self.y = -4
            self.jump_count = 0

    def animate(self):
        if self.x != 0 and self.y == 0:
            if time.time() - self.last_time > 0.1:
                self.last_time=time.time()
                self.current_image += self.current_image_add
                if self.current_image >= 2:
                    self.current_image_add = -1
                if self.current_image <= 0:
                    self.current_image_add = 1
        if self.x < 0:
            #Stick figure is moving left.
            if self.y != 0:
                #Figure is jumping.
                self.game.canvas.itemconfig(self.image, image=self.images_left[2])
            else:
                #Not jumping.
                self.game.canvas.itemconfig(self.image, image=self.images_left[self.current_image])
        elif self.x > 0:
            #Stick figure is moving right.
            if self.y != 0:
                self.game.canvas.itemconfig(self.image, image=self.images_right[2])
            else:
                self.game.canvas.itemconfig(self.image, image=self.images_right[self.current_image])

    def coords(self):
        xy = self.game.canvas.coords(self.image)
        self.coordinates.x1 = xy[0]
        self.coordinates.y1 = xy[1]
        self.coordinates.x2 = xy[0] + 27
        self.coordinates.y2 = xy[1] + 30
        return self.coordinates
                
    def end(self, sprite):
            print("Game Over")
            self.game.running = False
            sprite.open_door2()
            time.sleep(1)
            self.game.canvas.itemconfig(self.image, state='hidden')
            sprite.close_door()

    def move(self):
        self.animate()
        if self.y < 0:
            self.jump_count += 1
            if self.jump_count > 30: #20
                self.y = 4
        if self.y > 0:
            self.jump_count -= 1
            
        co = self.coords()
        left = True
        right = True
        top = True
        bottom = True
        falling = True
        
        if self.y > 0 and co.y2 >= self.game.canvas_height:
            self.y = 0
            bottom = False
        elif self.y < 0 and co.y1 <= 0:
            self.y = 0
            top = False

        if self.x > 0 and co.x2 >= self.game.canvas_width:
            self.x = 0
            right = False
        elif self.x < 0 and co.x1 <= 0:
            self.x = 0
            left = False

        for sprite in self.game.sprites:
            if sprite == self:
                continue
            sprite_co = sprite.coords()
            if top and self.y < 0 and collided_top(co, sprite_co):
                self.y = -self.y
                print("I hit my head!")
                top = False
                
            if bottom and self.y > 0 and collided_bottom(self.y, co, sprite_co):
                self.y = sprite_co.y1 - co.y2
                if self.y < 0:
                    self.y = 0
                print("I landed on something!")
                bottom = False
                top = False

            if bottom and falling and self.y == 0 and co.y2 < self.game.canvas_height and collided_bottom(1, co, sprite_co):
                falling = False
                
            if left and self.x < 0 and collided_left(co, sprite_co):
                self.x = 0
                print("I hit my left side!")
                left = False
                if sprite.endgame:
                    #self.game.running = False
                    self.end(sprite)

            if right and self.x > 0 and collided_right(co, sprite_co):
                self.x = 0
                print("I hit my right side!")
                right = False
                if sprite.endgame:
                    self.end(sprite)
                    #self.game.running = False
            
        if falling and bottom and self.y == 0 and co.y2 < self.game.canvas_height:
            self.y = 2 #4
        
        self.game.canvas.move(self.image, self.x, self.y)
        

g = Game()


platform1 = PlatformSprite(g, PhotoImage(file="platform3.gif"), 0,480,100,10)
platform2 = PlatformSprite(g, PhotoImage(file="platform3.gif"), 150,440,100, 10)

platform3 = MovingPlatformSprite(g, PhotoImage(file="platform3.gif"), 300,400,100, 10)
#platform3b = PlatformSprite(g, PhotoImage(file="platform3.gif"), 400,400,100,10)
platform4 = PlatformSprite(g, PhotoImage(file="platform3.gif"), 300,160,100, 10)
#Platform 2's: With 66
platform5 = MovingPlatformSprite(g, PhotoImage(file="platform2.gif"), 175,350, 66, 10)
platform6 = PlatformSprite(g, PhotoImage(file="platform2.gif"), 50,300, 66, 10)
platform7 = PlatformSprite(g, PhotoImage(file="platform2.gif"), 170,120,66, 10)
platform8 = PlatformSprite(g, PhotoImage(file="platform2.gif"), 45,60, 66, 10)
#Platform 1's with 32
platform9 = MovingPlatformSprite(g, PhotoImage(file="platform1.gif"), 170,250, 32, 10)
platform10 = PlatformSprite(g, PhotoImage(file="platform1.gif"), 230,200, 32, 10)

man = StickFigureSprite(g)

g.sprites.append(platform1)
g.sprites.append(platform2)
g.sprites.append(platform3)
#g.sprites.append(platform3b)
g.sprites.append(platform4)
g.sprites.append(platform5)
g.sprites.append(platform6)
g.sprites.append(platform7)
g.sprites.append(platform8)
g.sprites.append(platform9)
g.sprites.append(platform10)

g.sprites.append(man)

door = DoorSprite(g)
g.sprites.append(door)

g.mainloop()


        
    
