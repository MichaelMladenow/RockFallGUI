from tkinter import *

SETTINGS = {
    "window_title": "RockFall",
    "window_height": "480",
    "window_width": "600",
    "window_bg_color": "gray",
    "player_height": "20",
    "player_width": "10",
    "player_color": "red"
}

class Board(Canvas):

    def __init__(self):
        super().__init__(width=SETTINGS["window_width"],
            height=SETTINGS["window_height"],
            background=SETTINGS["window_bg_color"])
        
        self.pack()

class Player(Frame):

    def __init__(self):
        super().__init__()
                
        self.master.title('Player')
        self.board = Board()
        self.pack()

def main():

    root = Tk()
    player = Player()
    root.mainloop()  


if __name__ == '__main__':
    main()