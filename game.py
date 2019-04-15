import random
from tkinter import *
from settings import Settings
from models import Rock, Player


class Board(Canvas):

    def __init__(self):
        super().__init__(width=Settings.window_width,
            height=Settings.window_height,
            background=Settings.window_bg_color,
            highlightthickness=0)

        self.game_objects = []
        self.score        = 0
        # self.lives        = Settings.player_lives
        self.pack()
        self.create_player()

        # TODO: Don't bind all keys
        self.bind_all("<Key>", self.on_keypress)

        # Info Screen
        self.create_text(30, 30, tag="score", fill="white")
        self.create_text(30, 10, tag="lives", fill="white")

        # Periodical actions
        self.rock_spawn_cycle()
        self.update_cycle()

    def rock_spawn_cycle(self):
        """
        Action on each rock spawn cycle
        """
        rock = Rock(self)
        self.game_objects.append(rock)
        self.after(Settings.rock_spawn_interval, self.rock_spawn_cycle)

    def update_cycle(self):
        """
        Action of each game update cycle
        """
        self.check_for_collisions()

        for obj in self.game_objects:
            obj.on_update()

        self.update_info()
        self.after(Settings.game_delay, self.update_cycle)

    def create_player(self):
        self.player = Player(self)

    def on_keypress(self, e): 
        """
        Handle game inputs
        """    
        key = e.keysym

        if key == "Left":
            self.player.move_left()
        if key == "Right":
            self.player.move_right()

    def update_info(self):
        """
        Updates the info text (score/lives)
        """
        lives = self.find_withtag("lives")
        score = self.find_withtag("score")
        self.itemconfigure(lives, text="Lives: {0}".format(self.player.lives))
        self.itemconfigure(score, text="Score: {0}".format(self.score))

    def check_for_collisions(self):
        """
        Check for collisions and pass them to the player object
        """
        x1, y1, x2, y2 = self.coords(self.get_player())
        overlap        = self.find_overlapping(x1, y1, x2, y2)

        for ovr in overlap:
            obj = self.get_game_obj(ovr)
            if obj:
                obj.on_collision(self.player)
            if self.player.lives <= 0:
                # TODO: Game over
                pass

    def get_player(self):
        return self.find_withtag("player")

    def remove_obj(self, obj_id):
        """
        Removes an object from the canvas and game_objects
        """
        obj       = self.get_game_obj(obj_id)
        obj_index = self.game_objects.index(obj)

        self.delete(obj.get_id())
        del self.game_objects[obj_index]

    def get_game_obj(self, obj_id):
        for obj in self.game_objects:
            if obj.get_id() == obj_id:
                return obj
        return None


class Game(Frame):

    def __init__(self):
        super().__init__()
                
        self.master.title(Settings.window_title)
        self.board = Board()
        self.pack()

def main():

    root = Tk()
    game = Game()
    root.mainloop()  


if __name__ == '__main__':
    main()