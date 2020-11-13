# for zx
from numpy import random

print("Be a good boy and eat up your foods")

import arcade
import random

SCREEN_WIDTH=800
SCREEN_HEIGHT=600

SPRITE_SMALLBUN_SCALING = 0.1
SPRITE_CHARACTER_SCALING = 0.1

class EatUp(arcade.Window):
    '''main application class'''
    def __init__(self,width, height):
        super().__init__(width,height)
        arcade.set_background_color(arcade.color.AMAZON)

        #don't display the mouse
        self.set_mouse_visible(False)
        self.scaling = SPRITE_CHARACTER_SCALING

    def setup(self):
        ''' Setup the game  and initial the variables '''
        #create sprite lists
        self.player_list = arcade.SpriteList()
        self.smallbun_list = arcade.SpriteList()

        #score
        self.score = 0

        #set up the player
        self.player_sprite = arcade.Sprite("sources/images/monster.png",self.scaling)
        self.player_sprite.center_x=50
        self.player_sprite.center_y=50
        self.player_list.append(self.player_sprite)

        #create small buns
        for i in range(100):
            smallbun = arcade.Sprite("sources/images/smallbun.jfif",SPRITE_SMALLBUN_SCALING)

            #positions of buns
            smallbun.center_x = random.randrange(SCREEN_WIDTH)
            smallbun.center_y = random.randrange(SCREEN_HEIGHT)

            #add buns to list
            self.smallbun_list.append(smallbun)

        pass

    def on_draw(self):
        arcade.start_render()
        self.player_list.draw()
        self.smallbun_list.draw()
        # drawing code
        # put text on the screen
        output=f"Score:{self.score}"
        arcade.draw_text(output,10,550,arcade.color.WHITE,14)

    def on_mouse_motion(self,x,y,dx,dy):
        """ handle mouse motion """
        self.player_sprite.center_x=x
        self.player_sprite.center_y=y

    def update(self,delta_time):
        ''' all logic to move, and the game logic '''
        #check collisions
        buns_hit_list = arcade.check_for_collision_with_list(self.player_sprite,self.smallbun_list)

        for smallbun in buns_hit_list:
            smallbun.kill()
            self.score+=1

        if self.score > 20:
            self.scaling = self.score/200;
            self.player_sprite._set_scale(self.scaling)

        pass

def main():
    game = EatUp(SCREEN_WIDTH, SCREEN_WIDTH)
    game.setup()
    arcade.run()


if __name__=="__main__":
    main()