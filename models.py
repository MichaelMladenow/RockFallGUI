# models.py
import random
from settings import Settings
from util import get_rnd_step
from time import sleep

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

    def on_deletion(self):
        """
        Effects upon destruction
        """
        pass

    def delete(self):
        """
        Removes the object from the canvas
        """
        self.canvas.remove_obj(self.get_id())
        self.on_deletion()

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

    def get_player(self):
        return self.canvas.get_player_obj()

class FallingObject(GameObject):
    """
    GameObject with a "fall" functionality
    Falling is implemented in each on_update call and spawned
    on a random position on the first row
    """

    def __init__(self, canvas, width, height, tag, color, fall_velocity):
        self.y             = 0
        self.x             = get_rnd_step(width, int(canvas["width"]))
        self.collided      = False
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
        super().__init__(canvas, Settings.rock_width, Settings.rock_height, Settings.rock_tag,
                        Settings.rock_color, Settings.rock_fall_velocity)

    def on_collision(self, player):
        """
        Damages player upon collision
        """
        self.collided = True
        player.loose_life()

        # Fall back to parent for destruction handling
        super().on_collision()

    def on_deletion(self):
        """
        Action upon object deletion
        """
        if not self.collided:
            self.get_player().add_score(Settings.rock_miss_score)

        super().on_deletion()

class InsanityBonus(FallingObject):
    """
    Bonus - Increases score generation but also increases game speed and rock spawn rate
    """
    def __init__(self, canvas):
        super().__init__(canvas, Settings.bonus_width, Settings.bonus_height, Settings.bonus_tag,
                        Settings.bonus_color, Settings.bonus_fall_velocity)

    def on_collision(self, player):
        self.orig_score_multiplier  = player.score_multiplier
        self.orig_rock_spawn_rate   = self.canvas.rock_spawn_interval
        self.orig_game_speed        = Settings.game_delay
        self.bonus_duration         = Settings.bonus_insanity_duration
        self.player                 = player

        bonus_score_multiplier      = Settings.bonus_insanity_score_mult
        bonus_rock_spawn_rate       = Settings.bonus_insanity_spawn_rate
        bonus_game_speed            = Settings.bonus_insanity_game_delay
        
        self._set_bonus_game_props(player, bonus_score_multiplier, bonus_rock_spawn_rate, bonus_game_speed)
        self.canvas.after(self.bonus_duration, self._return_orig_game_props)

        super().on_collision()

    def _set_bonus_game_props(self, player, score_multiplier, rock_spawn_rate, game_speed):
        player.score_multiplier         = score_multiplier
        self.canvas.rock_spawn_interval = rock_spawn_rate
        Settings.game_delay             = game_speed

    def _return_orig_game_props(self):
        self.player.score_multiplier    = self.orig_score_multiplier
        self.canvas.rock_spawn_interval = self.orig_rock_spawn_rate
        Settings.game_delay             = self.orig_game_speed


class Player(object):
    """
    Handles player movement, actions, rendering and stores player info(lives/score)
    """

    def __init__(self, canvas, width=Settings.player_width, height=Settings.player_height,
                 lives=Settings.player_lives, velocity=Settings.player_velocity, color=Settings.player_color):
        self.canvas           = canvas
        self.lives            = lives
        self.score            = 0
        self.color            = color
        self.velocity         = velocity
        self.height           = height
        self.width            = width
        self.tag              = "player"
        self.score_multiplier = Settings.game_score_multiplier
        self.x                = self.generate_x()
        self.y                = self.generate_y()
        self.vulnerable       = True
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
        """
        Increments the player's lives
        """
        self.lives += 1

    def loose_life(self):
        """
        Decrements the player's lives
        """
        if self.vulnerable:
            self.lives -= 1
            self.make_invulnerable(Settings.player_ghost_dur)

    def make_invulnerable(self, timer):
        """
        Make player invulnerable for @timer ms
        """
        self.vulnerable = False
        self.canvas.itemconfigure(self.obj_id, fill=Settings.player_ghost_color)
        self.canvas.after(timer, self.make_vulnerable)

    def make_vulnerable(self):
        self.vulnerable = True
        self.canvas.itemconfigure(self.obj_id, fill=Settings.player_color)

    def add_score(self, score):
        self.score += (score * self.score_multiplier)

    def loose_score(self, score):
        self.score -= score

    def move_left(self):
        """
        Moves the player left by their velocity
        """
        velocity = -self.velocity
        x1, y1, x2, y2 = self.canvas.bbox(self.get_id())
        if x1 >= 1:
            self.canvas.move(self.get_id(), velocity, 0)

    def move_right(self):
        """
        Moves the player right by their velocity
        """
        velocity = self.velocity
        x1, y1, x2, y2 = self.canvas.bbox(self.get_id())
        if x2 < int(self.canvas["width"]):
            self.canvas.move(self.get_id(), velocity, 0)

