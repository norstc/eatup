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

SPRITE_FOOD_SCALING = 0.3
SPRITE_CHARACTER_SCALING = 0.3

MUSIC_VOLUME = 0.2

# how big the foods
FOOD_WIDTH = 256 * SPRITE_FOOD_SCALING
FOOD_HEIGHT = 256 * SPRITE_FOOD_SCALING

# dishes
DISH_PERCENTAGE_OVERSIZE = 1.25
DISH_WIDTH = int(FOOD_WIDTH * DISH_PERCENTAGE_OVERSIZE)
DISH_HEIGHT = int(FOOD_HEIGHT * DISH_PERCENTAGE_OVERSIZE)

# how much spaces for each dish
VERTICAL_MARGIN_PERCENT = 0.1
HORIZONTAL_MARGIN_PERCENT = 0.1

FOOD_START_X = SCREEN_WIDTH / 12
FOOD_START_Y = SCREEN_HEIGHT / 3 + DISH_HEIGHT
FOOD_X_SPACING = SCREEN_WIDTH / 6
FOOD_Y_SPACING = FOOD_HEIGHT + FOOD_HEIGHT * VERTICAL_MARGIN_PERCENT

# food contants
FOOD_CLASSIC = ["fruit", "vege", "food"]
FOOD_VALUES = ["1", "2", "3", "4", "5", "6"]

# dish constants
# four top dishes
DISH_START_Y = SCREEN_HEIGHT / 3 - FOOD_HEIGHT / 2
DISH_START_X = SCREEN_WIDTH / 8
DISH_X_SPACING = SCREEN_WIDTH / 4


class Food(arcade.Sprite):
    """ food """

    def __init__(self, classic, value, scale=1):
        self.classic = classic
        self.value = value

        # images for food
        self.image_file_name = f"sources/images/{self.classic}{self.value}.png"

        # if this food has been selected
        self.chosen = False


        # call the parent
        super().__init__(self.image_file_name, scale)

    def set_chosen(self, chosen):
        self.chosen = chosen

    def get_chosen(self):
        return self.chosen

    def get_energy(self):
        if self.classic == "vege":
            return 20
        elif self.classic == "fruit":
            return 20
        else:
            return 40


class TextButton:
    """ Text-based button """

    def __init__(self,
                 center_x, center_y,
                 width, height,
                 text,
                 font_size=18,
                 font_face="Arial",
                 face_color=arcade.color.LIGHT_GRAY,
                 highlight_color=arcade.color.WHITE,
                 shadow_color=arcade.color.GRAY,
                 button_height=2):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size
        self.font_face = font_face
        self.pressed = False
        self.face_color = face_color
        self.highlight_color = highlight_color
        self.shadow_color = shadow_color
        self.button_height = button_height

    def draw(self):
        """ Draw the button """
        arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width,
                                     self.height, self.face_color)

        if not self.pressed:
            color = self.shadow_color
        else:
            color = self.highlight_color

        # Bottom horizontal
        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y - self.height / 2,
                         color, self.button_height)

        # Right vertical
        arcade.draw_line(self.center_x + self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        if not self.pressed:
            color = self.highlight_color
        else:
            color = self.shadow_color

        # Top horizontal
        arcade.draw_line(self.center_x - self.width / 2, self.center_y + self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        # Left vertical
        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x - self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        x = self.center_x
        y = self.center_y
        if not self.pressed:
            x -= self.button_height
            y += self.button_height

        arcade.draw_text(self.text, x, y,
                         arcade.color.BLACK, font_size=self.font_size,
                         width=self.width, align="center",
                         anchor_x="center", anchor_y="center")

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.pressed = False


def check_mouse_press_for_buttons(x, y, button_list):
    """ Given an x, y, see if we need to register any button clicks. """
    for button in button_list:
        if x > button.center_x + button.width / 2:
            continue
        if x < button.center_x - button.width / 2:
            continue
        if y > button.center_y + button.height / 2:
            continue
        if y < button.center_y - button.height / 2:
            continue
        button.on_press()


def check_mouse_release_for_buttons(_x, _y, button_list):
    """ If a mouse button has been released, see if we need to process
        any release events. """
    for button in button_list:
        if button.pressed:
            button.on_release()


class StartTextButton(TextButton):
    def __init__(self, center_x, center_y, action_function):
        super().__init__(center_x, center_y, 100, 40, u"OK", 18, "Arial")
        self.action_function = action_function

    def on_release(self):
        super().on_release()
        self.action_function()


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
        game_view = OrderWise()
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
        game_view = OrderWise()
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
        game_view = OrderWise()
        game_view.setup()
        self.window.show_view(game_view)


class OrderWise(arcade.View):
    """main application class"""

    def __init__(self):
        super().__init__()
        self.scaling = SPRITE_CHARACTER_SCALING

        # score
        self.score = 0

        # sprite list
        self.foodie_list = arcade.SpriteList()
        self.food_list = None
        self.button_list = arcade.SpriteList()
        self.dish_list = None

        # list of foods  we are dragging  with the mouse
        self.held_foods = None

        # original location of cards  we are dragging with mouse  in case they have to go back
        self.held_foods_original_location = None

        # background
        arcade.set_background_color(arcade.color.AMAZON)

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
        # set up the player
        player_sprite = arcade.Sprite("sources/images/20130224100445921.png", self.scaling)
        player_sprite.center_x = 400
        player_sprite.center_y = 50
        self.foodie_list.append(player_sprite)

        # create food list
        self.food_list = arcade.SpriteList()

        # create every food
        for food_classic in FOOD_CLASSIC:
            for food_value in FOOD_VALUES:
                food = Food(food_classic, food_value, SPRITE_FOOD_SCALING)
                food.position = FOOD_START_X + FOOD_VALUES.index(food_value) * FOOD_X_SPACING, \
                                FOOD_START_Y + FOOD_CLASSIC.index(food_classic) * FOOD_Y_SPACING
                self.food_list.append(food)

        # list of  foods we are dragging with mouse
        self.held_foods = []
        # original position of the dragging foods if they need to go back
        self.held_foods_original_location = []

        # create dishes
        self.dish_list: arcade.SpriteList = arcade.SpriteList()
        for i in range(4):
            #dish = arcade.SpriteSolidColor(DISH_WIDTH, DISH_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
            dish = arcade.Sprite("sources/images/dish.jpeg",SPRITE_FOOD_SCALING)
            dish.position = DISH_START_X + i * DISH_X_SPACING, DISH_START_Y
            self.dish_list.append(dish)

    def pull_to_top(self, food):
        """ pull food to the top of rending order, means it will be rendered at last """
        # find the index of food
        index = self.food_list.index(food)
        # loop and pull all the other  foods  down towards the zero end
        for i in range(index, len(self.food_list) - 1):
            self.food_list[i] = self.food_list[i + 1]
        # put this food to the right-side/top of the food list
        self.food_list[len(self.food_list) - 1] = food

    def level_2(self):
        pass

    def level_3(self):
        pass

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
        self.total_time = 30.0

        # level set up
        self.level = 1
        self.level_1()

        # buttons, all levels need this button
        self.button_list = []
        play_button = StartTextButton(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50, self.check_result)
        self.button_list.append(play_button)

    def on_draw(self):
        arcade.start_render()
        self.dish_list.draw()
        self.food_list.draw()
        self.foodie_list.draw()

        # drawing code
        # put text on the screen
        output = f"Score:{self.score}"
        arcade.draw_text(output, 20, SCREEN_HEIGHT - 32, arcade.color.BLACK, 16)

        # draw timer
        minutes = int(self.total_time) // 60
        seconds = int(self.total_time) % 60
        total_timer = f"{minutes:02d}:{seconds:02d}"
        arcade.draw_text(total_timer, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 32, arcade.color.RED, 16)

        # draw buttons
        for button in self.button_list:
            button.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        """ handle mouse motion """
        # move foods with mouse
        for food in self.held_foods:
            food.center_x += dx;
            food.center_y += dy;
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """ when use press the mouse """
        # check buttons
        check_mouse_press_for_buttons(x, y, self.button_list)

        # check food
        foods = arcade.get_sprites_at_point((x, y), self.food_list)
        # have we chosen some food
        if len(foods) > 0:
            # might be a stack of foods, get the top one
            primary_food = foods[-1]
            primary_food.set_chosen(True)
            self.held_foods = [primary_food]
            # save the position
            self.held_foods_original_location = [self.held_foods[0].position]
            # put it the top of render list
            self.pull_to_top(self.held_foods[0])

    def on_mouse_release(self, x, y, button, key_modifiers):
        """ when mouse release """
        # check the button
        check_mouse_release_for_buttons(x, y, self.button_list)

        # check the foods
        if len(self.held_foods) == 0:
            return
        else:
            # snap the food into dish
            # find the closest dish
            dish, distance = arcade.get_closest_sprite(self.held_foods[0], self.dish_list)
            reset_position = True
            # if we have contact between the food and the dish
            if arcade.check_for_collision(self.held_foods[0], dish):
                self.bite_sound.play()
                for i, dropped_food in enumerate(self.held_foods):
                    dropped_food.position = dish.center_x, dish.center_y
                # success, don't reset
                reset_position = False
            if reset_position:
                # if we dropped the food somewhere else, return it to the original position
                for food_index, food in enumerate(self.held_foods):
                    food.position = self.held_foods_original_location[food_index]

        self.held_foods = []

    def check_result(self):
        self.stop_song()
        for food in self.food_list:
            if food.get_chosen():
                self.score += food.get_energy()
                food.set_chosen(False)
        if self.score > 120 or self.score < 80:
            self.game_over_sound.play()
            game_view = GameOverView()
            self.window.show_view(game_view)
        else:
            self.you_win_sound.play()
            game_view = YouWinView()
            self.window.show_view(game_view)

        pass

    def update(self, delta_time):
        """ all logic to move, and the game logic """

        # call update of all sprites
        self.food_list.update()
        self.foodie_list.update()

        # change to the game over view
        if self.score == 3 and self.total_time > 0:
            self.stop_song()
            self.you_win_sound.play()
            game_view = YouWinView()
            self.window.show_view(game_view)

        if self.total_time < 0:
            self.stop_song()
            if self.score == 3:
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
