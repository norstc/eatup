# -*-coding:utf-8-*-
# for zx
__author__ = "Youda"
from numpy import random

print("Be a good boy and eat up your foods")

import arcade
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = u"光盘行动"

SPRITE_SMALLBUN_SCALING = 0.1
SPRITE_CHARACTER_SCALING = 0.1

class InstructionView(arcade.View):
    def on_show(self):
        """ this is run once when we change to this view """
        arcade.set_background_color(arcade.color.DARK_BLUE)

        """ reset the viewport , necessary if we have a scrolling game and we 
        need to reset the viewport to the start point so we can see what we draw
        """
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_draw(self):
        """ draw this view """
        arcade.start_render()
        arcade.draw_text("I will eat them up.", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Click to begin", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 75,
                         arcade.color.WHITE, font_size=50, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ if the user click mouse, start the game """
        game_view = EatUp()
        game_view.setup()
        self.window.show_view(game_view)


class GameOverView(arcade.View):
    """ view to show game over """
    def __init__(self):
        """ this is run once when we change to this view """
        super().__init__()
        self.game_over_texture = arcade.load_texture("sources/images/game_over.jpg")

        """ reset the viewport """
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_draw(self):
        arcade.start_render()
        self.game_over_texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ if user presses the mouse, restart the game """
        game_view = EatUp()
        game_view.setup()
        self.window.show_view(game_view)


class EatUp(arcade.View):
    '''main application class'''

    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.AMAZON)

        # don't display the mouse
        self.window.set_mouse_visible(False)
        self.scaling = SPRITE_CHARACTER_SCALING

    def setup(self):
        """ Setup the game  and initial the variables """
        # create sprite lists
        self.player_list = arcade.SpriteList()
        self.smallbun_list = arcade.SpriteList()

        # score
        self.score = 0

        # set up the player
        self.player_sprite = arcade.Sprite("sources/images/monster.png", self.scaling)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        # create small buns
        for i in range(20):
            smallbun = arcade.Sprite("sources/images/smallbun.jfif", SPRITE_SMALLBUN_SCALING)

            # positions of buns
            smallbun.center_x = random.randrange(SCREEN_WIDTH)
            smallbun.center_y = random.randrange(SCREEN_HEIGHT)

            # add buns to list
            self.smallbun_list.append(smallbun)

        pass

    def on_draw(self):
        arcade.start_render()
        self.player_list.draw()
        self.smallbun_list.draw()
        # drawing code
        # put text on the screen
        output = f"Score:{self.score}"
        arcade.draw_text(output, 10, 550, arcade.color.WHITE, 14)

    def on_mouse_motion(self, x, y, dx, dy):
        """ handle mouse motion """
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def update(self, delta_time):
        """ all logic to move, and the game logic """
        # check collisions
        buns_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.smallbun_list)

        for smallbun in buns_hit_list:
            smallbun.kill()
            self.score += 1

        if self.score > 10:
            self.scaling = self.score / 100
            self.player_sprite._set_scale(self.scaling)

        """ change to the game over view """
        if self.score  == 20:
            game_view = GameOverView()
            self.window.show_view(game_view)
        pass


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT,SCREEN_TITLE)
    start_view = InstructionView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
