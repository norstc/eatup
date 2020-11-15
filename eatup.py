# -*-coding:utf-8-*-
# for zx
__author__ = "Youda"

from numpy import random

print("Be a good child and eat up your foods")

import arcade
import random
import time

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = u"光盘行动"

SPRITE_SMALLBUN_SCALING = 0.2
SPRITE_CHARACTER_SCALING = 0.2

MUSIC_VOLUME = 0.2


class FallingBun(arcade.Sprite):
    """ falling down buns """
    def update(self):
        """ move the buns """
        # fall down
        self.center_y -= 2

        # if it go off the screen move it back to the top
        if self.top < 0:
            self.top = SCREEN_HEIGHT


class RisingBun(arcade.Sprite):
    def update(self):
        self.center_y += 2
        if self.top > SCREEN_HEIGHT:
            self.top = 0


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
        self.game_over_texture = arcade.load_texture("sources/images/game_over_1.png")

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


class YouWinView(arcade.View):
    """ winner is the one eat them up """

    def __init__(self):
        """ this is run once when we change to this view """
        super().__init__()
        self.you_win_texture = arcade.load_texture("sources/images/you_win.jpg")

        """ reset the viewport """
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_draw(self):
        arcade.start_render()
        self.you_win_texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = EatUp()
        game_view.setup()
        self.window.show_view(game_view)


class EatUp(arcade.View):
    """main application class"""

    def __init__(self):
        super().__init__()
        self.scaling = SPRITE_CHARACTER_SCALING
        self.player_sprite = arcade.Sprite("sources/images/20130224100445921.png", self.scaling)

        # score
        self.score = 0

        # sprite list
        self.player_list = arcade.SpriteList()
        self.smallbun_list = arcade.SpriteList()

        # background
        arcade.set_background_color(arcade.color.WHITE)

        # don't display the mouse
        self.window.set_mouse_visible(False)
        self.scaling = SPRITE_CHARACTER_SCALING

        # timer
        self.total_time = 20.0

        # music
        # from Anttis:
        # https: // www.soundclick.com / artist / default.cfm?bandid = 1277008 & content = songs
        # https: // www.reddit.com / r / gameassets / comments / ewo5iu / i_have_released_my_2000_instrumental_pieces_free /
        self.music_list = []
        self.current_song = 0
        self.music = None

        # sound
        self.bite_sound = arcade.load_sound("sources/sounds/coin1.wav")
        self.you_win_sound = arcade.load_sound("sources/sounds/upgrade1.wav")
        self.game_over_sound = arcade.load_sound("sources/sounds/gameover1.wav")

        # levels control
        self.level = 1

    def level_1(self):
        # create small buns
        for i in range(10):
            smallbun = arcade.Sprite("sources/images/chicken.png", SPRITE_SMALLBUN_SCALING)

            # positions of buns
            smallbun.center_x = random.randrange(SCREEN_WIDTH)
            smallbun.center_y = random.randrange(SCREEN_HEIGHT - 100)

            # angles of buns
            smallbun.angle = random.randrange(30)
            smallbun.change_angle = random.randrange(-5, 6)

            # add buns to list
            self.smallbun_list.append(smallbun)

    def level_2(self):
        """ falling """
        for i in range(10):
            smallbun = FallingBun("sources/images/pizza.png", SPRITE_SMALLBUN_SCALING)
            smallbun.center_x = random.randrange(SCREEN_WIDTH)
            smallbun.center_y = random.randrange(SCREEN_HEIGHT, SCREEN_HEIGHT * 2)
            self.smallbun_list.append(smallbun)

    def level_3(self):
        """ rising """
        for i in range(10):
            smallbun = RisingBun("sources/images/sausage.png", SPRITE_SMALLBUN_SCALING)
            smallbun.center_x = random.randrange(SCREEN_WIDTH)
            smallbun.center_y = random.randrange(-SCREEN_HEIGHT, 0)
            self.smallbun_list.append(smallbun)

    def advanced_song(self):
        """ advanced our pointer to next song, but doesn't start it"""
        self.current_song += 1
        if self.current_song >= len(self.music_list):
            self.current_song = 0

    def play_song(self):
        """ play the current song """
        # stop if already playing
        if self.music:
            self.music.stop()

        # play next song
        self.music = arcade.Sound(self.music_list[self.current_song], streaming=True)
        self.music.play(MUSIC_VOLUME)
        # this is a delay for update, if we don't do this,
        # update will think the music is over and advance us to next song
        time.sleep(0.03)

    def stop_song(self):
        """ stop the song """
        if self.music:
            self.music.stop()

    def setup(self):
        """ Setup the game  and initial the variables """
        # list of musics
        self.music_list = ["sources/music/funkyrobot.mp3"]
        self.current_song = 0
        self.play_song()

        # create sprite lists

        # score
        self.score = 0
        # timer reset
        self.total_time = 20.0

        # set up the player
        self.player_sprite.center_x = random.randrange(SCREEN_WIDTH)
        self.player_sprite.center_y = random.randrange(SCREEN_HEIGHT - 100)
        self.player_list.append(self.player_sprite)

        # level set up
        self.level = 1
        self.level_1()

    def on_draw(self):
        arcade.start_render()
        self.player_list.draw()
        self.smallbun_list.draw()
        # drawing code
        # put text on the screen
        output = f"Score:{self.score}"
        arcade.draw_text(output, 20, SCREEN_HEIGHT - 32, arcade.color.BLACK, 16)

        # draw timer
        minutes = int(self.total_time) // 60
        seconds = int(self.total_time) % 60
        total_timer = f"{minutes:02d}:{seconds:02d}"
        arcade.draw_text(total_timer, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 32, arcade.color.RED, 16)

    def on_mouse_motion(self, x, y, dx, dy):
        """ handle mouse motion """
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def update(self, delta_time):
        """ all logic to move, and the game logic """

        # call update of all sprites
        self.smallbun_list.update()
        self.player_list.update()

        # check collisions
        buns_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.smallbun_list)

        for smallbun in buns_hit_list:
            smallbun.remove_from_sprite_lists()
            self.bite_sound.play()
            self.score += 1

        # check levels
        if len(self.smallbun_list) == 0 and self.level == 1:
            self.level += 1
            self.level_2()
            self.scaling = (self.level + 1) / 10
            self.player_sprite._set_scale(self.scaling)

        if len(self.smallbun_list) == 0 and self.level == 2:
            self.level += 1
            self.level_3()
            self.scaling = (self.level + 1) / 10
            self.player_sprite._set_scale(self.scaling)




        # change to the game over view
        if self.score == 30 and self.total_time > 0:
            self.stop_song()
            self.you_win_sound.play()
            game_view = YouWinView()
            self.window.show_view(game_view)

        if self.total_time < 0:
            self.stop_song()
            if self.score == 30:
                self.you_win_sound.play()
                game_view = YouWinView()
                self.window.show_view(game_view)
            else:
                self.game_over_sound.play()
                game_view = GameOverView()
                self.window.show_view(game_view)

        # timer update
        self.total_time -= delta_time

        # music update
        position = self.music.get_stream_position()
        # the position pointer is reset to  0 right after  we finish the song,
        # This make it very difficult  to figure out if we just started playing or we have done playing


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = InstructionView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
