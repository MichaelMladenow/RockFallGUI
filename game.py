import random
from tkinter import *

SETTINGS = {
    "window_title": "RockFall",
    "window_height": 700,
    "window_width": 600,
    "window_bg_color": "gray",
    "player_height": 50,
    "player_width": 50,
    "player_initial_pos_x": 251,
    "player_initial_pos_y": 650,
    "player_color": "red",
    "player_velocity": 50,
    "rock_height": 50,
    "rock_width": 50,
    "rock_velocity": 5,
    "rock_color": "black",
    "rock_fall_delay": 10,
    "rock_spawn_delay": 500,
    "game_delay": 100,
}

class Board(Canvas):

    def __init__(self):
        super().__init__(width=SETTINGS["window_width"],
            height=SETTINGS["window_height"],
            background=SETTINGS["window_bg_color"], highlightthickness=0)

        # TODO: Create settings for the player rect
        # TODO: Export into a method
        player_height  = SETTINGS["player_height"]
        player_width   = SETTINGS["player_width"]
        player_x_start = SETTINGS["player_initial_pos_x"]
        player_y_start = SETTINGS["player_initial_pos_y"]
        player_x_end   = player_x_start + player_width
        print (player_x_start,player_x_end)
        player_y_end   = player_y_start + player_height
        self.create_rectangle(player_x_start, player_y_start, player_x_end, player_y_end, fill=SETTINGS["player_color"], tag='player', width=0)
        self.pack()

        # TODO: Don't bind all keys
        self.bind_all("<Key>", self.on_keypress)

        # Periodical actions
        self.after(SETTINGS["game_delay"], self.on_tick)
        self.after(SETTINGS["rock_spawn_delay"], self.rock_spawn_cycle)
        self.after(SETTINGS["rock_fall_delay"], self.rock_fall_cycle)

    def on_keypress(self, e): 
    
        key = e.keysym

        if key == "Left":
            self.move_player_left()
        if key == "Right":
            self.move_player_right()

    def move_player_left(self):
        # TODO: Boundary check
        velocity = SETTINGS["player_velocity"] * - 1
        x1, y1, x2, y2 = self.bbox(self.get_player())
        if x1 >= 1:
            self.move("player", velocity, 0)

    def move_player_right(self):
        velocity = SETTINGS["player_velocity"]
        x1, y1, x2, y2 = self.bbox(self.get_player())
        if x2 < SETTINGS["window_width"]:
            self.move("player", SETTINGS["player_velocity"], 0)

    def fall_rock(self, rock):
        self.move(rock, 0, SETTINGS["rock_velocity"])

    def on_tick(self):
        # TODO: Game update cycle
        #   - Check for collisions
        #   - Spawn rocks
        #   - Move rocks down
        self.check_for_collisions()
        self.after(SETTINGS["game_delay"], self.on_tick)

    def spawn_rock(self):
        rock_height  = SETTINGS["rock_height"]
        rock_width   = SETTINGS["rock_width"]
        rock_x_max   = SETTINGS["window_width"] - SETTINGS["rock_width"]
        rock_x_start = random.choice(range(1,rock_x_max+1, rock_width))
        rock_y_start = 1
        rock_x_end   = rock_x_start + rock_width
        rock_y_end   = rock_y_start + rock_height
        self.create_rectangle(rock_x_start, rock_y_start, rock_x_end, rock_y_end, fill=SETTINGS["rock_color"], tag='rock', width=0)
        
    def drop_rocks(self):
        rocks = self.find_withtag("rock")
        for rock in rocks:
            # TODO: If rock is on the bottom border - delete it
            x1, y1, x2, y2 = self.bbox(rock)
            if y2 >= SETTINGS["window_height"]:
                self.delete(rock)
            else:
                self.fall_rock(rock)

    def rock_spawn_cycle(self):
        self.spawn_rock()
        self.after(SETTINGS["rock_spawn_delay"], self.rock_spawn_cycle)

    def rock_fall_cycle(self):
        self.drop_rocks()
        self.after(SETTINGS["rock_fall_delay"], self.rock_fall_cycle)

    def check_for_collisions(self):
        
        rocks = self.find_withtag("rock")
        x1, y1, x2, y2 = self.coords(self.get_player())
        overlap = self.find_overlapping(x1, y1, x2, y2)
        for ovr in overlap:
            ovr_tags = self.gettags(ovr)
            if "rock" in ovr_tags:
                # TODO: Dwayne Johnson assaulted Milko! Call 112
                print("You hit a rock!")
                

    def get_player(self):
        return self.find_withtag("player")

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