from kivy.config import Config
Config.set('graphics', 'resizable', False)
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.lang import Builder
from functools import partial
from kivy.core.window import Window
from kivy.graphics import *
from multiprocessing import Process
import threading
import board_generator
import time
from kivy.config import Config

Builder.load_file("design.kv")
Window.size = (720,790)
# Config.set('input', 'mouse', 'mouse,disable_multitouch')
# Config.set('graphics','resizable', False)
 #0 being off 1 being on as in true/false


mines = 21

length = 15
timer = None
started = False
current_time = None
buttons = []
remove_mine = False
cells = []
colors = [(34/255, 41/255, 51/255, 0), (0,0,1,1), (0,128/255,0,1), (1,0,0,1),(75/255,0,130/255,1),(139/255, 0, 0, 1)]
run = True

class Game(Screen):    
    def start(self):
        #threading.Thread(target = self.game_timer).start()
        self.ids.main_layout.clear_widgets()
        self.ids.status.text = "Game in progress..."
        self.ids.mine_id.text=str(mines)

        global board
        global current_time
        global buttons
        global started
        global cells
        board = board_generator.generate_matrix(length, mines)
        buttons = []
        cells = []
        started = False
        if not started:
            for i in range(length):
                layout = GridLayout(cols = length)
                for j in range(length):
                    #button = Button(text="",on_release=partial(self.show_text,i,j))
                    button = Button(text="",on_release=partial(self.cancel_timer,i,j),on_press=partial(self.start_timer, i,j), background_color=(34/255, 41/255, 51/255,0.5),  width=10, height=10)
                    layout.add_widget(button)
                self.ids.main_layout.add_widget(layout)
        started = True

        for i in range(len(self.ids.main_layout.children)):
            temp = []
            for j in range(len(self.ids.main_layout.children[i].children)):
                temp.append(self.ids.main_layout.children[i].children[j])
            buttons.append(temp)
        current_time = time.time()

    def start_timer(self, i, j, button):
        global timer
        if timer:
            timer.cancel()
        timer = Clock.schedule_once(partial(self.put_flag,i,j), 0.5)
    def cancel_timer(self,i,j, button):
        global timer
        global remove_mine
        if timer:
            timer.cancel()
        if remove_mine is False:
            self.show_text(i, j, buttons[length-i-1][length-j-1])
        remove_mine = False

    def put_flag(self, i, j, timer):
        global buttons
        global remove_mine
        global unrevealed_cells
        global run
        if self.ids.status.text != "You lost." and self.ids.status.text != "You win!":
            if buttons[length-i-1][length-j-1].text == "#":
                buttons[length-i-1][length-j-1].text = ""
                # buttons[length-i-1][length-j-1].background_color = (34/255, 41/255, 51/255, 0.5)
                buttons[length-i-1][length-j-1].background_normal = "bg2.png"
                buttons[length-i-1][length-j-1].background_color = (34/255, 41/255, 51/255, 0.405)
                self.ids.mine_id.text = str(int(self.ids.mine_id.text) +1)
                #buttons[length-i-1][length-j-1].background_color = (34/255, 41/255, 51/255, 0.5)
                # btn = Button(text="", background_color = (34/255, 41/255, 51/255, 0.5))
                
                cells.remove((i,j))
                print(len(set(cells)))
                remove_mine = True
            elif buttons[length-i-1][length-j-1].text == "":
                buttons[length-i-1][length-j-1].text = "#"
                buttons[length-i-1][length-j-1].color = (0,0,0,0)
                buttons[length-i-1][length-j-1].background_normal = "flag.png"
                buttons[length-i-1][length-j-1].background_color = (1,0,0,1)
                if int(self.ids.mine_id.text) >0:
                    self.ids.mine_id.text = str(int(self.ids.mine_id.text) -1)
                cells.append((i,j))
                if len(set(cells)) == length**2:
                    if self.win():
                        self.ids.status.text = "You win!"
                        run = False
                        # self.ids.time.text =  str(round(time.time()-current_time)//60)+"m"+" "+str(round(time.time()-current_time)%60)+"s"
                print(len(set(cells)))
                remove_mine = False
    def show_text(self, x, y, button):
        global board     
        global set_mine
        global unrevealed_cells
        global lost
        global run
        if buttons[length-x-1][length-y-1].text == "" and buttons[length-x-1][length-y-1].text!="#" and self.ids.status.text != "You lost.":
            set_mine = False
            if board[x][y] == 0:
                self.flood_fill(x,y)
            else:
                if board[x][y] == "X":
                    if set_mine == False:
                        for i in range(len(board)):
                            for j in range(len(board[i])):
                                if board[i][j] == "X":
                                    buttons[length-i-1][length-j-1].background_color = (1,0,0,1)
                        self.ids.status.text = "You lost."
                        run = False
                        #self.ids.time.text =str(round(time.time()-current_time)//60)+"m"+" "+str(round(time.time()-current_time)%60)+"s"
                else:
                    try:
                        button.text = str(board[x][y])
                    except: 
                        pass
                    button.background_color = (34/255, 41/255, 51/255, 1)
                    try:
                        button.color = colors[board[x][y]]
                    except:
                        pass
                    cells.append((x,y))
                    print(len(set(cells)))
        if len(set(cells)) == length**2:
            if self.win():
                self.ids.status.text = "You win!"
                run = False
                #self.ids.time.text =  str(round(time.time()-current_time)//60)+"m"+" "+str(round(time.time()-current_time)%60)+"s"
    def win(self):
        for i in range(len(board)):
            for j in range(len(board[i])):
                if str(board[i][j]) != buttons[length-i-1][length-j-1].text:
                    if ((board[i][j] == "#" and buttons[length-i-1][length-j-1].text != "0") or (board[i][j] != "#" and buttons[length-i-1][length-j-1].text=="0")) or ((board[i][j] == "X" and buttons[length-i-1][length-j-1].text != "#") or (board[i][j] != "X" and buttons[length-i-1][length-j-1].text == "#")):
                        return False
        return True
    def flood_fill(self, x, y):
        global buttons
        global board
        global unrevealed_cells
        global run
        q = []
        q.append([x, y])
        indices = []
        while len(q):
            [new_x,new_y] = q.pop()
            indices.append((new_x, new_y))
            board[new_x][new_y] = "#"
            if new_x +1 < length and new_x+1>=0 and new_y >= 0 and new_y < length:
                if board[new_x+1][new_y] == 0:
                    q.append([new_x+1, new_y])
                    indices.append((new_x+1, new_y))
            if new_x-1 >= 0 and new_x-1 < length and new_y >= 0 and new_y < length:
                if board[new_x-1][new_y] == 0:
                    q.append([new_x-1, new_y])
                    indices.append((new_x-1, new_y))
            if new_x >=0 and new_x < length and new_y+1>=0 and new_y+1<length:
                if board[new_x][new_y+1] == 0:
                    q.append([new_x, new_y+1])
                    indices.append((new_x, new_y+1))
            if new_x >= 0 and new_x < length and new_y-1 >=0 and new_y-1<length:
                if board[new_x][new_y-1] == 0:
                    q.append([new_x, new_y-1]) 
                    indices.append((new_x, new_y-1))
            if new_x +1 >= 0 and new_x+1 <length and new_y+1>=0 and new_y+1 <length:
                if board[new_x+1][new_y+1] == 0 :
                    q.append([new_x+1, new_y+1])
                    indices.append((new_x+1, new_y+1))
            if new_x+1 >= 0 and new_x+1 < length and new_y-1 >= 0  and new_y-1 < length:
                if board[new_x+1][new_y-1] == 0 :
                    q.append([new_x+1, new_y-1])
                    indices.append((new_x+1, new_y-1))
            if new_x -1>= 0 and new_x-1 < length and new_y +1 >= 0 and new_y+1 < length:
                if board[new_x-1][new_y+1] == 0:
                    q.append([new_x-1, new_y+1])
                    indices.append((new_x-1, new_y+1))
            if new_x - 1>= 0 and new_x-1 < length and new_y-1 >= 0 and new_y-1 < length:
                if board[new_x-1][new_y-1] == 0:
                    q.append([new_x-1, new_y-1])
                    indices.append((new_x-1,new_y-1))
        final_indices = set(indices)
        for i in final_indices:
            cells.append(i)
            print(len(set(cells)))
        for index in final_indices:
            i = index[0]
            j = index[1]
            if buttons[length-i-1][length-j-1].text != "#" and buttons[length-i-1][length-j-1].background_normal != "flag.png":
                buttons[length-i-1][length-j-1].text = "0"
                buttons[length-i-1][length-j-1].background_color = (34/255, 41/255, 51/255, 1)
                buttons[length-i-1][length-j-1].color = colors[0]
                if len(set(cells)) == length**2:
                    if self.win():
                        print("You won")
                        run = False
                directions = [
                    [i, j-1],
                    [i, j+1],
                    [i-1, j],
                    [i+1, j],
                    [i+1, j+1],
                    [i+1, j-1],
                    [i-1, j+1],
                    [i-1, j-1]
                ]
                for dir in directions:
                    
                    if dir[0] >= 0 and dir[0] < length and dir[1] >= 0 and dir[1] < length:
                        if board[dir[0]][dir[1]] != '#' and str(board[dir[0]][dir[1]]) != "0" and buttons[length-dir[0]-1][length-dir[1]-1].text != "#" :
                            buttons[length-dir[0]-1][length-dir[1]-1].text = str(board[dir[0]][dir[1]])
                            buttons[length-dir[0]-1][length-dir[1]-1].color = colors[board[dir[0]][dir[1]]]
                            buttons[length-dir[0]-1][length-dir[1]-1].background_color = (34/255, 41/255, 51/255, 1)
                            cells.append((dir[0], dir[1]))
                            if len(set(cells)) == length**2:
                                if self.win():
                                    self.ids.status.text = "You win!"
                                    run = False
                                   # self.ids.time.text = str(round(time.time()-current_time)//60)+"m"+" "+str(round(time.time()-current_time)%60)+"s"
                            print(len(set(cells)))
                        elif str(board[dir[0]][dir[1]]) == 0:
                            buttons[length-dir[0]-1][length-dir[1]-1].background_color = (34/255, 41/255, 51/255, 1)

class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__ == "__main__":
    MainApp().run()