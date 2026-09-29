import pygame  as pg
import numpy as np
from scipy.signal import savgol_filter
pg.init()

# Setting window size
win_x = 1000
win_y = 600

sidebar_width = 100

can_x = win_x - sidebar_width

win = pg.display.set_mode((win_x, win_y))
win.fill((255, 255, 255))
pg.display.set_caption('Live Derivatives')

class button(object):

    def __init__(self, x, y, width, height, color, index, outline=0, action=0, text=''):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.color = color
        self.outline = outline
        self.index = index
        self.action = action
        self.text = text
        
# Class for drawing buttons
    def draw(self, win):

        pg.draw.rect(win, self.color, (self.x, self.y,
                                           self.width, self.height), self.outline)
        font = pg.font.SysFont('calibri', 30)
        text = font.render(self.text, 1, self.color)
        win.blit(text, (int(self.x+self.width/2-text.get_width()/2),
                        int(self.y+self.height/2-text.get_height()/2)))

redButton = button(can_x + 53, 30, 40, 40, (255, 0, 0), 0)
blueButton = button(can_x + 7, 30, 40, 40, (0, 0, 255), 1)
greenButton = button(can_x + 7, 76, 40, 40, (0, 255, 0), 2)
clearButton = button(can_x + 7, 120, 90, 40, (0, 0, 0),3, 3, text="CLEAR")

buttons = [redButton, blueButton, greenButton, clearButton]

class drawing(object):

    def __init__(self):
        '''constructor'''
        self.color = (255, 0, 0)
        self.rad = 3
        self.points = [{},{},{}]
        self.smooth = [[],[],[]]
        self.index = 0

    def draw(self, win, pos):
        pg.draw.circle(win, self.color, (pos[0], pos[1]), self.rad)

    def click(self, win):
        pos = pg.mouse.get_pos()

        if pg.mouse.get_pressed() == (1, 0, 0) and pos[0] < can_x and pos[1] > win_y/2:
            self.draw(win, pos)
            self.points[self.index][pos[0]] = pos[1]

        elif pg.mouse.get_pressed() == (1, 0, 0):
            for button in buttons:
                if pos[0] > button.x and pos[0] < button.x + button.width:
                    if pos[1] > button.y and pos[1] < button.y + button.height:
                        if button.index == 3:
                            self.points = [{}, {},{}]
                            self.smooth = [[],[],[]]
                            win.fill((255, 255, 255))
                            
                        else:
                            self.color = button.color
                            self.index = button.index


canvas = drawing()

scale = 30

def draw(win):
    canvas.click(win)
    pg.draw.rect(win, (0, 0, 0), (can_x, 0, sidebar_width, win_y),
                     2)  # Drawing button space
    # pg.draw.rect(win, (255, 255, 255), (can_x, 0, 100, 500),)
    pg.draw.rect(win, (0, 0, 0), (0, win_y/2, can_x, win_y/2),
                     2)  # Drawing canvas space

    for button in buttons:
        button.draw(win)

    if len(canvas.points[canvas.index]) > 1 :
        pg.draw.rect(win, (255, 255, 255), (0, 0, can_x, win_y/2),0)
        pg.draw.line(win, (0,0,0), (0,win_y/4), (can_x,win_y/4))
        x = np.array(list(canvas.points[canvas.index].keys()))
        y = win_y - np.array(list(canvas.points[canvas.index].values()))
        # p = np.polynomial.polynomial.Polynomial.fit(y/10, x/10, 10)
        winlen = min(30,len(canvas.points[canvas.index]))
        polyorder = min(1,len(canvas.points[canvas.index])-1)
        p = savgol_filter(y, winlen, polyorder)
        # d = p.deriv(1)
        # grad = np.gradient(p(x/10),(x/10))
        grad = np.gradient(p/scale, x/scale)
        d = win_y/4 - grad*scale
        winlen = min(20,len(canvas.points[canvas.index]))
        d = savgol_filter(d, winlen, polyorder)
        canvas.smooth[canvas.index] = d

        for j in range(3):
            if len(canvas.points[j]) > 1 :
                x = np.array(list(canvas.points[j].keys()))
                y = np.array(list(canvas.smooth[j]))
                for i in range(len(y)):
                    if x[i] < can_x and y[i] < win_y/2:
                        pg.draw.circle(win, buttons[j].color,(x[i], y[i]) , canvas.rad)

    pg.display.update()




def main_loop():
    run = True
    while run: 
        keys = pg.key.get_pressed()  
        for event in pg.event.get():
            if event.type == pg.QUIT or keys[pg.K_ESCAPE]:
                run = False

        draw(win)

main_loop()