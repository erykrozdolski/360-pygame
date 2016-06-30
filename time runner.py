__author__ = 'Eryk'
#!/usr/bin/python
#-*-coding: utf-8-*-
import pygame
import random
from math import radians,cos,sin,sqrt
from colors import *
from pygame import gfxdraw
pygame.mixer.init()
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
window_size = window_width,window_height = 400,717
window = pygame.display.set_mode(window_size,False)
pygame.display.set_caption('')
# icon=pygame.image.load('360 icon-01.jpg')
sound_icon=pygame.image.load('sound_icon.png')
music_icon=pygame.image.load('music_icon.png')
# pygame.display.set_icon(icon)




clock = pygame.time.Clock()
fps=70
sound_on_off = True
speed_time = 0
direction_time = 0
score= 0
time=0
false_or_true=[True,False]
pygame.mixer.music.load('360soundogg.ogg')
win_sound=pygame.mixer.Sound('360soundwin.ogg')
lose_sound=pygame.mixer.Sound('360losesound.ogg')
click_sound=pygame.mixer.Sound('360clicksound.ogg')
highscore_file= open('highscore.txt','r')
actual_highscore = highscore_file.readline()
highscore_file.close()
class simple_circle:
    def __init__(self,dest,radius,color):
        self.color = color
        pygame.gfxdraw.aacircle(window,dest[0],dest[1],radius,color)
        pygame.gfxdraw.filled_circle(window,dest[0],dest[1],radius,color)

class Button:
    def __init__(self,x,y,radius,color,text=None,text_color=None,text_size=None):
        self.x =x
        self.y=y
        self.radius = radius
        self.first_color = grey
        self.second_color = carrot_color
        self.color = self.first_color
        self.text = text

        if self.text != None:
            self.script = Text(text,text_color,text_size)

    def draw(self):
        x,y = pygame.mouse.get_pos()
        if self.x - self.radius <= x <= self.x + self.radius:
            if self.y - self.radius <= y <= self.y + self.radius:
                self.color = self.second_color
            else:
                self.color = self.first_color
        else:
            self.color = grey
        pygame.gfxdraw.aacircle(window,self.x,self.y,self.radius,self.color)
        pygame.gfxdraw.filled_circle(window,self.x,self.y,self.radius,self.color)
        if self.text != None:
            self.script.draw([self.x,self.y],True)
    def clicked(self,action=None):
        x,y = pygame.mouse.get_pos()
        if self.x - self.radius <= x <= self.x + self.radius:
            if self.y - self.radius <= y <= self.y + self.radius and pygame.mouse.get_pressed()[0]:
                if action != None:
                    if sound_on_off == True:
                        click_sound.play()
                    eval(action)
                if sound_on_off == True:
                    click_sound.play()
                return True
class MusicButton:
    def __init__(self,x,y,radius):
        self.x =x
        self.y=y
        self.radius = radius
        self.on_off = 'on'
        self.color = carrot_color
    def clicked(self):
        x,y = pygame.mouse.get_pos()
        if self.x - self.radius <= x <= self.x + self.radius:
            if self.y - self.radius <= y <= self.y + self.radius and pygame.mouse.get_pressed()[0] :
                if self.on_off == 'on':
                    self.on_off = 'off'
                    self.color = grey
                    pygame.mixer.music.stop()
                else:
                    self.color = carrot_color

                    pygame.mixer.music.play(-1)
                    self.on_off = 'on'
    def draw(self):
        pygame.gfxdraw.aacircle(window,self.x,self.y,self.radius,self.color)
        pygame.gfxdraw.filled_circle(window,self.x,self.y,self.radius,self.color)
class SoundButton:
    def __init__(self,x,y,radius):
        self.x =x
        self.y=y
        self.radius = radius
        self.on_off = 'on'
        self.color = carrot_color
    def clicked(self):
        global sound_on_off
        x,y = pygame.mouse.get_pos()
        if self.x - self.radius <= x <= self.x + self.radius:
            if self.y - self.radius <= y <= self.y + self.radius and pygame.mouse.get_pressed()[0]:
                if self.on_off == 'on':
                    self.on_off = 'off'
                    self.color = grey
                    sound_on_off = False
                else:
                    self.color = carrot_color

                    sound_on_off = True
                    self.on_off = 'on'
    def draw(self):
        pygame.gfxdraw.aacircle(window,self.x,self.y,self.radius,self.color)
        pygame.gfxdraw.filled_circle(window,self.x,self.y,self.radius,self.color)

class Circle(pygame.sprite.Sprite):
    def __init__(self,cx,cy,radius,font_size):
        self.font_size = font_size
        self.x = cx
        self.y = cy
        self.radius = radius
        self.was_position = []
        self.is_full = False
        self.position_list=[]
        self.text = ''
        self.asteriks_text = Text("*",carrot_color,font_size)
        self.asteriks = False
        self.rect = pygame.Rect(self.x-self.radius,self.y-self.radius,self.radius*2,self.radius*2)
        for position in range(0,360):
            self.fi = radians(position)
            x = int(self.x + (self.radius + 30) * cos(self.fi))
            y = int(self.y - (self.radius + 30)* sin(self.fi))
            self.position_list.append((x,y))
    def draw(self):
        pygame.gfxdraw.aacircle(window,self.x,self.y,self.radius,carrot_color)
        pygame.gfxdraw.filled_circle(window,self.x,self.y,self.radius,carrot_color)
        pygame.gfxdraw.aacircle(window,self.x,self.y,self.radius//2,ai_color)
        pygame.gfxdraw.filled_circle(window,self.x,self.y,self.radius//2,ai_color)


class Player(pygame.sprite.Sprite):
    def __init__(self,enemies_circle_list):
        self.radius = 10
        self.degree = 0
        self.fi = 0
        self.actual_circle = middle_circle
        self.new_actual_circle = middle_circle
        self.change_direction = True
        self.speed = 2
        self.position = 180
        self.kill = False
        self.position_list= self.actual_circle.position_list
        self.x,self.y  = self.position_list[self.position]
        self.enemies_circle_list = enemies_circle_list
        self.rect = pygame.Rect(self.x-self.radius*2,self.y-self.radius*2,self.radius*4,self.radius*4)

    def set_position(self):
        if self.change_direction == True:
            if self.position < len(self.position_list)-self.speed:
                self.position += self.speed
            else:
                self.position = 0
        else:
            if self.position > 0:
                self.position -= self.speed
            else:
                self.position = len(self.position_list)-self.speed
        self.x,self.y  = self.position_list[self.position]


    def set_circle(self):

        if self.x > self.actual_circle.x - self.radius*3 and self.x < self.actual_circle.x + self.radius*3 :
            if self.actual_circle == middle_circle:
                if self.y < self.actual_circle.y:
                    self.new_actual_circle = up_circle
                elif self.y > self.actual_circle.y:
                    self.new_actual_circle = down_circle
            if self.actual_circle == down_circle:
                if self.y < self.actual_circle.y:
                    self.new_actual_circle = middle_circle
            if self.actual_circle == up_circle:
                if self.y > self.actual_circle.y:
                    self.new_actual_circle = middle_circle
        if self.new_actual_circle != self.actual_circle:
            self.actual_circle = self.new_actual_circle
            if self.actual_circle == middle_circle:
                if self.y > self.actual_circle.y:
                    self.position = int(abs(self.position - len(self.position_list)))
                if self.y < self.actual_circle.y:
                    self.position = int(abs(self.position - len(self.position_list)))
            if self.actual_circle == up_circle:
                if self.y > self.actual_circle.y:
                    self.position = int(abs(self.position - len(self.position_list)))
            if self.actual_circle == down_circle:
                if self.y < self.actual_circle.y:
                    self.position = int(abs(self.position - len(self.position_list)))

            self.change_direction = not self.change_direction

        self.position_list= self.actual_circle.position_list

    def draw(self):

        pygame.gfxdraw.aacircle(window,self.x,self.y,self.radius,white)
        pygame.gfxdraw.filled_circle(window,self.x,self.y,self.radius,white)
    def do_kill(self):
        global actual_highscore, score
        for i in self.enemies_circle_list:
            distance = sqrt((i.x-self.x)**2+(i.y-self.y)**2)
            if distance <= self.radius + i.radius:
                if score > float(actual_highscore):
                    actual_highscore = score
                if sound_on_off == True:
                    lose_sound.play()
                self.kill = True
                self.actual_circle =  middle_circle
                self.position_list = middle_circle.position_list
                self.x,self.y = middle_circle.position_list[self.position]
                for i in enemies_circle_list:
                    i.speed = 0
                game_over_panel()


    def update(self):
        print(self.position)
        self.set_position()
        self.rect = pygame.Rect(self.x-self.radius*2,self.y-self.radius*2,self.radius*4,self.radius*4)
        self.do_kill()




class Enemy(pygame.sprite.Sprite):
    def __init__(self,actual_circle):
        self.radius = 10
        self.degree = 0
        self.fi = 0
        self.speed = 1
        self.min_speed = 1
        self.max_speed = 1
        self.local_speed_time = 0
        self.local_dir_time = 0
        self.actual_circle = actual_circle
        self.change_direction = True

        self.position_list=[]

        self.position = 50
        self.position_list= self.actual_circle.position_list
        self.x,self.y  = self.position_list[self.position]
        self.rect = pygame.Rect(self.x - self.radius*2,self.y-self.radius*2,self.radius*4,self.radius*4)
    def set_position(self):
        if self.change_direction == True:
            if self.position < len(self.position_list)-self.speed:
                self.position += self.speed
            else:
                self.position = 0
        else:
            if self.position > 0:
                self.position -= self.speed
            else:
                self.position = len(self.position_list)-1
        self.x,self.y  = self.position_list[self.position]
    def change_speed(self):
        if self.min_speed != self.max_speed:
            self.speed = random.randrange(self.min_speed,self.max_speed)
    def update(self):
        global speed_time, direction_time
        self.set_position()

        if speed_time > self.local_speed_time and false_or_true[random.randint(0,1)] and self.local_speed_time != 0:
            self.change_speed()
            speed_time = 0
        if direction_time > self.local_dir_time and false_or_true[random.randint(0,1)] and self.local_dir_time != 0:
            if self.change_direction == False:
                    self.change_direction = True
            else:
                self.change_direction = False
            direction_time = 0
        self.rect = pygame.Rect(self.x - self.radius*2,self.y-self.radius*2,self.radius*4,self.radius*4)


    def draw(self):

        pygame.gfxdraw.aacircle(window,self.x,self.y,self.radius,grey)
        pygame.gfxdraw.filled_circle(window,self.x,self.y,self.radius,grey)


class Text:
    def __init__(self,message,color,size,font="montserratsemi"):
        self.my_font = pygame.font.SysFont(font,size)
        self.font_surface = self.my_font.render(message,True,color)
    def draw(self,dest,center=False):
        if center == True:
            textrect = self.font_surface.get_rect()
            textrect.center = dest
            window.blit(self.font_surface,[textrect.x,textrect.y])
        else:
            window.blit(self.font_surface,dest)
class Block_Text:
    def __init__(self,color,size,leading,font,message_list):
        self.my_font = pygame.font.SysFont(font,size)
        self.draw_list =[]
        self.leading = leading
        self.color = color
        for i in message_list:
            text_surface = self.my_font.render(i,True,self.color)
            self.draw_list.append(text_surface)
    def draw(self,dest):
        lead = 0
        for i in self.draw_list:
            window.blit(i,[dest[0],dest[1]+lead])
            lead += self.leading


score_text = Text(str(score),white,30)

space_text = Text("space to change direction",grey,20)
shift_text = Text("left shift to change circle",grey,20)
game_name = Text("360",white,30)
game_name2 = Text("360",white,20)
game_asteriks2 = Text("*",carrot_color,20)
game_asteriks = Text("*",carrot_color,30)
play_text = Text("play",white,20)
space_word = Text("space",carrot_color,20)
shift_word = Text("shift",carrot_color,20)
how_to_play_text1 = Text("how to play",white,20)
how_to_play_text2 = Text("how to play",grey,20)

quit_text = Text("quit",white,20)


middle_circle = Circle(int(window_width/2),int(window_height/2),70,20)
up_circle = Circle(int(window_width/2 ),int(window_height/2-180),50,15)
down_circle = Circle(int(window_width/2 ),int(window_height/2+180),50,15)

middle_enemy = Enemy(middle_circle)
up_enemy = Enemy(up_circle)
down_enemy = Enemy(down_circle)

enemies_circle_list = [middle_enemy,up_enemy,down_enemy]
circle_list = [middle_circle,up_circle,down_circle]
player_circle = Player(enemies_circle_list)

update_list=[middle_enemy,up_enemy,down_enemy,player_circle]

all_list=[middle_enemy,up_enemy,down_enemy,middle_circle,up_circle,down_circle,player_circle]
message_list2 =['To change circle, which','around you rotate, just press left','          when your circle is inside','this tunnel, between circles.']
message_list3=['You score a point by full lap','- 360  in all circles']
message_list4 =['The game ends, when you hit','the grey circle, avoid collisions','and make full laps to score points' ]
message_list1=['To change direction of your', 'circle simply press']


how_to_play_block1 = Block_Text(white,20,20,"montserratsemi",message_list1)
how_to_play_block3 = Block_Text(white,20,20,"montserratsemi",message_list2)
how_to_play_block2 = Block_Text(white,20,23,"montserratsemi",message_list4)
how_to_play_block4 = Block_Text(white,20,20,"montserratsemi",message_list3)



music_button = MusicButton(int(window_width-50),25,17)
sound_button = SoundButton(int(window_width-90),25,17)

middle_score_rect = pygame.Rect(middle_circle.x - 20,middle_circle.y - 20,50,50)
up_score_rect = pygame.Rect(up_circle.x-20,up_circle.y-20,40,42)
down_score_rect = pygame.Rect(down_circle.x-20,down_circle.y-20,40,42)
main_score_rect = pygame.Rect(window_width-70,22,70,30)

def game_text():

    space_text.draw([20,window_height - 65])
    shift_text.draw([20,window_height - 40])
    game_name.draw([10,10])
    game_asteriks.draw([65,10])
    for i in circle_list:
        i.text.draw([i.x,i.y],True)
        if i.asteriks == True:
            i.asteriks_text.draw([int(i.x+i.radius/3.5),i.y-i.radius/5])
def is360(player,all=True,sound=True):
    global score
    if player.position not in player.actual_circle.was_position:
        player.actual_circle.was_position.append(player.position)
        if (len(player.actual_circle.was_position)) == len(player.actual_circle.position_list)/2:
            player.actual_circle.is_full = True
            player.actual_circle.asteriks = True
            score +=1
            if sound == True:
                win_sound.play()
    if all == True:
        if middle_circle.is_full and up_circle.is_full and down_circle.is_full:
            score +=3
            for i in circle_list:
                i.was_position = []
                i.is_full = False
                i.asteriks = False
    else:
        if middle_circle.is_full:
            middle_circle.was_position =[]
            middle_circle.is_full = False
            middle_circle.asteriks = False


def game():

    global gameOver,speed_time,direction_time,time,score

    while not player_circle.kill:

        score_text = Text("score "+str(round(score,2)),white,30)
        for i in circle_list:
            i.text = Text(str(len(i.was_position)*2),white,i.font_size)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if player_circle.change_direction == False:
                        player_circle.change_direction = True
                    else:
                        player_circle.change_direction = False
                elif event.key == pygame.K_LSHIFT:
                    player_circle.set_circle()





        for i in update_list:
            i.update()


        window.fill(ai_color)
        for i in all_list:
            i.draw()


        game_text()
        score_text.draw([window_width-150,20])
        if time < 5:
            pygame.display.update()
        else:
            pygame.display.update([middle_score_rect,up_score_rect,down_score_rect,main_score_rect,player_circle.rect,middle_enemy.rect,up_enemy.rect,down_enemy.rect])

        clock.tick(fps)
        speed_time += 1
        direction_time +=1
        time += 1
        is360(player_circle)

        raise_level()


def restart():
    global speed_time,direction_time,score,time,enemies_circle_list,fps
    player_circle.kill = False
    fps=70
    speed_time=0
    direction_time=0
    score=0
    time=0
    player_circle.actual_circle,player_circle.new_actual_circle=middle_circle,middle_circle
    player_circle.x,player_circle.y  = player_circle.position_list[player_circle.position]
    for i in enemies_circle_list:
        i.position = 0
        i.speed = 1

    for i in circle_list:
        i.was_position=[]
        i.is_full = False
        i.asteriks=False




    player_circle.change_direction = True
    player_circle.speed = 2
    player_circle.position = 180
    for i in enemies_circle_list:
        i.local_dir_time = 0
        i.max_speed = 1
        i.local_speed_time = 0

def raise_level():
    global score,fps
    if score > 6:
        fps = 75
        for i in enemies_circle_list:
            i.local_dir_time = 450
    if score > 12:
        fps =82
        for i in enemies_circle_list:
            i.local_dir_time = 350
    if score > 24:
        fps =90
        for i in enemies_circle_list:
            i.local_dir_time = 300

    if score > 36:
        fps =99
        for i in enemies_circle_list:
            i.local_dir_time = 250


    if score > 48:
        fps = 110
        for i in enemies_circle_list:
            i.local_dir_time = 200


    if score > 60:
        fps= 120
        for i in enemies_circle_list:
            i.local_dir_time = 150

    if score > 72:
        fps= 130
        for i in enemies_circle_list:
            i.local_dir_time = 110
    if score > 84:
        fps= 140
        for i in enemies_circle_list:
            i.local_dir_time = 100
    if score > 96:
        fps= 150
        for i in enemies_circle_list:
            i.local_dir_time = 80


def how_to_play():
    screen = 0
    next_button = Button(int(window_width/2+90),90,35,grey,'next',white,20)
    previous_button = Button(int(window_width/2-90),90,35,grey,'previous',white,20)
    def simple_screen():
        window.fill(ai_color)
        middle_circle.draw()


        game_name.draw([10,10])
        game_asteriks.draw([65,10])
        how_to_play_text2.draw([window_width-150,20])


        how_to_play_circle.draw()



    how_to_play_middle_enemy = Enemy(middle_circle)
    how_to_play_enemies_list = [how_to_play_middle_enemy]
    how_to_play_circle = Player([])
    how_to = False
    how_to_time = 0
    for i in circle_list:
        i.was_position = []


    trigger = True
    while not how_to:
        for i in circle_list:
            i.text = Text(str(len(i.was_position)*2),white,i.font_size)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                highscore_file = open('C:/Users\Eryk\Desktop/360\highscore.txt','w')
                highscore_file.write(str(actual_highscore))
                highscore_file.close()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if how_to_play_circle.change_direction == False:
                        how_to_play_circle.change_direction = True
                    else:
                        how_to_play_circle.change_direction = False
                if screen == 2 or screen == 3:

                    if event.key == pygame.K_LSHIFT:
                        how_to_play_circle.set_circle()

        if how_to_time > 20:
            if next_button.clicked():
                screen +=1
                how_to_time = 0
            if previous_button.clicked():
                if screen != 0:
                    restart()
                    screen -=1
                    how_to_time = 0
        if screen == 4:
            how_to = True


        if screen == 0:
            simple_screen()
            how_to_play_block1.draw([50,window_height-220])
            space_word.draw([window_width/2 + 45,window_height-200])
            game_name2.draw([middle_circle.x,middle_circle.y],True)
            game_asteriks2.draw([int(middle_circle.x+middle_circle.radius/3.5),middle_circle.y-middle_circle.radius/5])
            next_button.draw()


        if screen == 1:

            simple_screen()
            how_to_play_block2.draw([30,window_height-220])
            how_to_play_middle_enemy.update()
            how_to_play_middle_enemy.draw()
            game_name2.draw([middle_circle.x,middle_circle.y],True)
            game_asteriks2.draw([int(middle_circle.x+middle_circle.radius/3.5),middle_circle.y-middle_circle.radius/5])
            next_button.draw()
            previous_button.draw()
            how_to_play_circle.new_actual_circle = middle_circle
            how_to_play_circle.actual_circle = middle_circle
            how_to_play_circle.position_list = middle_circle.position_list
        if screen == 2:

            simple_screen()

            pygame.draw.aaline(window,grey,(int(down_circle.x-player_circle.actual_circle.radius/2),up_circle.y+up_circle.radius),(int(down_circle.x-player_circle.actual_circle.radius/2),middle_circle.y-middle_circle.radius))
            pygame.draw.aaline(window,grey,(int(down_circle.x+player_circle.actual_circle.radius/2),up_circle.y+up_circle.radius),(int(down_circle.x+player_circle.actual_circle.radius/2),middle_circle.y-middle_circle.radius))
            pygame.draw.aaline(window,grey,(int(down_circle.x-player_circle.actual_circle.radius/2),down_circle.y-up_circle.radius),(int(down_circle.x-player_circle.actual_circle.radius/2),middle_circle.y+middle_circle.radius))
            pygame.draw.aaline(window,grey,(int(down_circle.x+player_circle.actual_circle.radius/2),down_circle.y-up_circle.radius),(int(down_circle.x+player_circle.actual_circle.radius/2),middle_circle.y+middle_circle.radius))

            how_to_play_block3.draw([30,window_height-100])
            up_circle.draw()
            down_circle.draw()
            shift_word.draw([30,window_height - 60])
            game_name2.draw([middle_circle.x,middle_circle.y],True)
            game_asteriks2.draw([int(middle_circle.x+middle_circle.radius/3.5),middle_circle.y-middle_circle.radius/5])
            pygame.gfxdraw.hline(window,0,window_width,middle_circle.y+middle_circle.radius,grey)
            pygame.gfxdraw.hline(window,0,window_width,middle_circle.y-middle_circle.radius,grey)
            pygame.gfxdraw.hline(window,0,window_width,up_circle.y+up_circle.radius,grey)
            pygame.gfxdraw.hline(window,0,window_width,down_circle.y-down_circle.radius,grey)
            next_button.draw()
            previous_button.draw()


        if screen == 3:

            if trigger:
                for i in circle_list:
                    i.asteriks = False
                    i.was_position=[]
                    i.is_full = False
                trigger = False
            simple_screen()
            up_circle.draw()
            down_circle.draw()
            next_button.draw()
            previous_button.draw()


            how_to_play_block4.draw([20,window_height-100])

            is360(how_to_play_circle)
            for i in circle_list:

                i.text.draw([i.x,i.y],True)
                if i.asteriks == True:
                    i.asteriks_text.draw([int(i.x+i.radius/3.5),i.y-i.radius/5])

        how_to_play_circle.update()
        pygame.display.update()
        clock.tick(fps)
        how_to_time +=1

def game_menu():
    global player_circle,middle_circle,actual_highscore,sound_button, music_button

    menu_player=Player([])

    shift_text = Text("shift to change circle",grey,20)
    space_text = Text("space to choose circle",grey,20)
    middle_circle.was_position = []

    while True:
        middle_circle.text = Text(str(len(middle_circle.was_position)*2),white,middle_circle.font_size)

        play_choice_circle = Button(int(window_width/2),75,17,grey)
        how_to_play_choice_circle = Button(int(window_width/2),135,17,grey)
        quit_choice_circle = Button(int(window_width/2),195,17,grey)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                highscore_file = open('C:/Users\Eryk\Desktop/360/360highscore.txt','w')
                highscore_file.write(str(actual_highscore))
                highscore_file.close()
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                music_button.clicked()
                sound_button.clicked()

        window.fill(ai_color)

        middle_circle.draw()

        middle_circle.text.draw([middle_circle.x,middle_circle.y],True)
        is360(menu_player,False,False)




        menu_player.update()
        menu_player.draw()

        game_name.draw([10,10])
        game_asteriks.draw([65,10])

        play_choice_circle.draw()
        how_to_play_choice_circle.draw()
        quit_choice_circle.draw()
        music_button.draw()
        sound_button.draw()
        window.blit(sound_icon,[int(window_width-96),4])
        window.blit(music_icon,[int(window_width-60),17])


        play_choice_circle.clicked('restart(),game()')
        how_to_play_choice_circle.clicked('how_to_play()')
        quit_choice_circle.clicked('quiter()')
        play_text.draw([int(window_width/2)+30,60])
        how_to_play_text1.draw([int(window_width/2)+30,120])
        quit_text.draw([int(window_width/2)+30,180])

        pygame.display.update()
        clock.tick(fps)
def quiter():
    highscore_file = open('C:/Users\Eryk\Desktop/360/highscore.txt','w')
    highscore_file.write(str(actual_highscore))
    highscore_file.close()
    pygame.quit()
    exit()
def game_over_panel():
    game_over_words = Text('game over',white,40)
    best_word = Text('best',white,20)
    score_word = Text('score',white,20)
    again_button = Button(int(window_width/2),int(window_height/2),70,grey,'again',white,40)
    menu_button = Button(int(window_width/2+125),int(window_height/2+125),40,grey,'menu',white,25)

    while True:

        global score,actual_highscore
        score_text = Text(str(round(score,2)),white,25)
        actual_highscore_text = Text(str(actual_highscore),white,25)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


        window.fill(ai_color)
        score_text.draw([window_width-100,int(window_height/2 - 195)])
        actual_highscore_text.draw([window_width-100,int(window_height/2 - 160)])
        game_over_words.draw([int(window_width/2),int(window_height/2 - 250)],True)
        orange_button = simple_circle([50,int(window_height/2 - 140)],10,carrot_color)
        grey_button = simple_circle([50,int(window_height/2 - 175)],10,grey)
        best_word.draw([90,int(window_height/2 - 140)],True)
        score_word.draw([97,int(window_height/2 - 175)],True)
        game_name.draw([10,10])
        game_asteriks.draw([65,10])
        again_button.draw()
        menu_button.draw()
        again_button.clicked('restart(),game()')
        menu_button.clicked('game_menu()')
        pygame.display.update()



pygame.mixer.music.play(-1)


game_menu()






