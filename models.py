# models.py
import random
from settings import Settings
from util import get_rnd_step

class GameObject(object):
    """
    Abstract game object
    """

    def __init__(self, canvas, width, height, x, y, tag, color):
        self.canvas  = canvas
        self.width   = width
        self.height  = height
        self.obj_id  = None
        self.color   = color
        self.tag     = tag
        self.x       = x
        self.y       = y

    def draw(self):
        """
        Renders the object on the canvas
        """
        self.obj_id = self.canvas.create_rectangle(
            self.x,
            self.y,
            self.x + self.width,
            self.y + self.height,
            tag = self.tag,
            width = 0,
            fill = self.color)

    def on_update(self):
        """
        Action on each game update cycle
        """
        pass

    def on_collision(self):
        """
        Effects upon collision with the player
        """
        self.delete()
        
    def delete(self):
        """
        Removes the object from the canvas
        """
        self.canvas.remove_obj(self.get_id())

    def get_id(self):
        """
        Returns the canvas ID of the object
        Useable only once the object has been drawn
        """
        if self.obj_id == None:
            # TODO: Pick a more appropriate exception
            raise Exception("Object not yet drawn.")
        else:
            return self.obj_id

class FallingObject(GameObject):
    """
    GameObject with a "fall" functionality
    Falling is implemented in each on_update call and spawned
    on a random position on the first row
    """

    def __init__(self, canvas, width, height, tag, color, fall_velocity):
        self.y             = 0
        self.x             = get_rnd_step(width, int(canvas["width"]))
        self.fall_velocity = fall_velocity

        super().__init__(canvas, width, height, self.x, self.y, tag, color)
        self.draw()

    def on_update(self):
        """
        Action on each game update cycle
        """
        x1, y1, x2, y2 = self.canvas.bbox(self.get_id())

        # If the object hits the bottom wall
        if y2 >= int(self.canvas["height"]):
            self.delete()
        else:
            self.fall()

    def fall(self):
        """
        Moves the object down the canvas by it's fall_velocty
        """
        self.canvas.move(self.get_id(), 0, self.fall_velocity)


class Rock(FallingObject):
    """
    FallingObject that damages the player upon collision
    """
    def __init__(self, canvas):
        super().__init__(canvas, Settings.rock_width, Settings.rock_height, Settings.rock_tag, Settings.rock_color, Settings.rock_fall_velocity)

    def on_collision(self, player):
        player.loose_life()

        # Fall back to parent for destruction handling
        super().on_collision() 

class Player(object):

    def __init__(self, canvas, width = 50, height = 50, lives = 3, velocity = 50, color = "red"):
        self.canvas   = canvas
        self.lives    = lives
        self.color    = color
        self.velocity = velocity
        self.height   = height
        self.width    = width
        self.tag      = "player"
        self.x        = self.generate_x()
        self.y        = self.generate_y()
        self.draw()

    def generate_x(self):
        """
            Generates x position for the player to be drawn on
        """
        canvas_width = int(self.canvas["width"])
        positions = range(1, canvas_width + 1, self.width)
        return positions[len(positions)//2]

    def generate_y(self):
        """
            Generates y position for the player to be drawn on
        """
        return int(self.canvas["height"]) - self.height

    def draw(self):
        """
        Renders the object on the canvas
        """
        self.obj_id = self.canvas.create_rectangle(
            self.x,
            self.y,
            self.x + self.width,
            self.y + self.height,
            tag = self.tag,
            width = 0,
            fill = self.color)

    def get_id(self):
        """
        Returns the canvas ID of the object
        Useable only once the object has been drawn
        """
        if self.obj_id == None:
            # TODO: Pick a more appropriate exception
            raise Exception("Object not yet drawn.")
        else:
            return self.obj_id

    def add_life(self):
        self.lives += 1

    def loose_life(self):
        self.lives -= 1

    def move_left(self):
        velocity = -self.velocity
        x1, y1, x2, y2 = self.canvas.bbox(self.get_id())
        if x1 >= 1:
            self.canvas.move(self.get_id(), velocity, 0)

    def move_right(self):
        velocity = self.velocity
        x1, y1, x2, y2 = self.canvas.bbox(self.get_id())
        if x2 < int(self.canvas["width"]):
            self.canvas.move(self.get_id(), velocity, 0)
