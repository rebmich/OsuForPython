# Osu. The Game
# Import
# from curses import KEY_UP
# from email.mime import image
import pygame
import sys

from os import listdir
from os.path import isfile, join

import os.path

from pygame.constants import K_ESCAPE

import random

pygame.init()
clock = pygame.time.Clock()
width=1920
height=1080
pygame.display.set_caption("No internet")
screen= pygame.display.set_mode((0,0),pygame.FULLSCREEN)

# Different screen variables
main_screen = True
create_screen = False
map_pick = False
play_map = False

# Some mouse click variables
mouse_prev = [False,False,False]
mouse_flag = [False,False,False]

# Mouse click functions
def mouse_inputs(pre,flag):
    # Variable for the actual inputs
    clicks=[]
    for x in range(len(pre)):
        # Checks if the button state has change and where it changed to on or off
        if pre[x] != flag[x] and pre[x] == False:
            clicks.append(True)
        else:
            clicks.append(False)
    return clicks

# We may not neet keyboard functions

# # Keyboard variables
# k_up_pre = False
# k_up_flag = False

# # Keyboard functions
# def keyboard_inputs(var1,var2):
#     if var1 != var2 and var1 == False:
#         return True

# Still need a few keyboard friends

k_up = False
k_down = False
k_enter = False      

c_click = False
z_click = False

# Cursor makage
cursor = pygame.image.load("skin/Skin_1/cursor@2x.png").convert_alpha()
cursor = pygame.transform.scale(cursor,(150,150))
cursor_rect = cursor.get_rect()

# Other cursor variables
pygame.mouse.set_visible(False)

# Title screen
play = pygame.image.load("Assets/Main_play.png")
play = pygame.transform.scale(play,(560,140))
play_rect = play.get_rect()
play_rect.center = (width/2,height/2-100)

make = pygame.image.load("Assets/Main_create.png")
make = pygame.transform.scale(make,(560,140))
make_rect = make.get_rect()
make_rect.center = (width/2,height/2+100)

bg = pygame.image.load("Assets/corn.png")
bg = pygame.transform.scale(bg,(width,height))

# Title screen functions*********************************************************************
def mouse_hover(mousex,mousey,rect):
    if rect.collidepoint(mousex,mousey):
        return True
    else:
        return False
    
def mouse_click(mousex,mousey,rect, button):
    if rect.collidepoint(mousex,mousey) and button:
        return True
    else:
        return False

# Map selection parts******************************************************************************

# main image calls
map_select_back = pygame.image.load("Skin/Skin_1/selection-mode@2x.png").convert_alpha()
map_select_back = pygame.transform.scale(map_select_back,(1600,1080))
map_select_rect = map_select_back.get_rect()
map_select_rect.topright = (width,0)

menu_layer = pygame.image.load("Skin/Skin_1/mode-osu-small@2x.png").convert_alpha()
# idk why 1.45 lines it up just go with it
menu_layer = pygame.transform.scale(menu_layer,(4400/1.43,2900/1.43))
menu_layer_rect = menu_layer.get_rect()
menu_layer_rect.topright = (width,0)

menu_back = pygame.image.load("Skin/Skin_1/menu-back-0.png").convert_alpha()
# 1.4 just works again (quazy)
menu_back = pygame.transform.scale(menu_back,(256*1.4,91*1.4))
menu_back_rect = menu_back.get_rect()
menu_back_rect.bottomleft = (0,height)

level_button = pygame.image.load("Skin/Skin_1/menu-button-background@2x.png").convert_alpha()
# now its 0.7 :O
level_button = pygame.transform.scale(level_button,(1380*0.7,192*0.7))
level_button_rect = level_button.get_rect()
level_button_rect.center = (width-100,height/2)

# Reads all the current maps the player has
maps = [f for f in listdir("Maps")]

# map selection variables
fontTitle = pygame.font.Font("Assets/Aller_Rg.ttf", 40)
fontStat = pygame.font.Font("Assets/Aller_Rg.ttf", 30)
new_map = True
first_map = random.randint(0,len(maps)-1)
stats = []
stat_text = ""

# Function for loading the map that player if looking at (map screen)
def new_load(maps,num):
    background = pygame.image.load(f"Maps/{maps[num]}/bg.jpg")
    background = pygame.transform.scale(background,(width,height))
    darken_percent = .25
    dark = pygame.Surface(background.get_size()).convert_alpha()
    dark.fill((0, 0, 0, darken_percent*255))
    background.blit(dark,(0,0))
    return background

# This is for new text to be printed onto the screen
def new_text(text,colour):
    text = fontTitle.render(f"{text}", True, colour)
    text_rect = text.get_rect()
    return text, text_rect

rule_im, rule_rect = new_text("Click Create for Rules/How to Play! ;O", (255,255,255))
rule_rect.center = (width/5, height/2)

# Bro.... I don't even know with this stuff man. I had a very eligant solution before but "\n" doesn't work when creating text objects so instead i did this
def stat_maker(slw):
    sl = sorted(slw)
    st_list = []
    st_list.append([fontTitle.render("Top 5",True,(0,0,0)),0])
    st_list[0][1] = st_list[0][0].get_rect()
    st_list[0][1].left = 5
    st_list[0][1].centery = height/4
    st_list.append([fontTitle.render("Top 5",True,(0,255,0)),0])
    st_list[1][1] = st_list[1][0].get_rect()
    st_list[1][1].center = (st_list[0][1].centerx-2,st_list[0][1].centery-2)

    for x in range(len(sl)):
        x+=1
        if x >=6:
            break
        st_list.append([fontStat.render(f"Score: {sl[-x][0]} Combo: {sl[-x][1]}     300: {sl[-x][2]} 100: {sl[-x][3]} 50: {sl[-x][4]} Miss: {sl[-x][5]}",True,(0,0,0)),0])
        st_list[-1][1] = st_list[-1][0].get_rect()
        st_list[-1][1].left = 5
        st_list[-1][1].centery = (st_list[-3][1].centery+((st_list[-3][1].height/2)+10))
        st_list.append([fontStat.render(f"Score: {sl[-x][0]} Combo: {sl[-x][1]}     300: {sl[-x][2]} 100: {sl[-x][3]} 50: {sl[-x][4]} Miss: {sl[-x][5]}",True,(255,255,255)),0])
        st_list[-1][1] = st_list[-1][0].get_rect()
        st_list[-1][1].center = (st_list[-2][1].centerx-2,st_list[-2][1].centery-2)

    st_list.append([fontTitle.render(f"Recent",True,(0,0,0)),0])
    st_list[-1][1] = st_list[-1][0].get_rect()
    st_list[-1][1].left = 5
    st_list[-1][1].centery = (st_list[-3][1].centery+((st_list[-3][1].height/2)+10))
    st_list.append([fontTitle.render(f"Recent",True,(0,255,0)),0])
    st_list[-1][1] = st_list[-1][0].get_rect()
    st_list[-1][1].center = (st_list[-2][1].centerx-2,st_list[-2][1].centery-2)

    if len(sl) > 0: 
        st_list.append([fontStat.render(f"Score: {slw[-1][0]} Combo: {slw[-1][1]}     300: {slw[-1][2]} 100: {slw[-1][3]} 50: {slw[-1][4]} Miss: {slw[-1][5]}",True,(0,0,0)),0])
        st_list[-1][1] = st_list[-1][0].get_rect()
        st_list[-1][1].left = 5
        st_list[-1][1].centery = (st_list[-3][1].centery+((st_list[-3][1].height/2)+10))
        st_list.append([fontStat.render(f"Score: {slw[-1][0]} Combo: {slw[-1][1]}     300: {slw[-1][2]} 100: {slw[-1][3]} 50: {slw[-1][4]} Miss: {slw[-1][5]}",True,(255,255,255)),0])
        st_list[-1][1] = st_list[-1][0].get_rect()
        st_list[-1][1].center = (st_list[-2][1].centerx-2,st_list[-2][1].centery-2)
    return st_list

# THESE ARE PLAYING GAME VARIAVLES AND FUN******************************************************************************************************************************
test_box = pygame.Rect(0,0,512*2,384*2)
test_box.center = (width/2,height/2)

# playing variables
# td = ThingDuration
td = 500
map_startup = True
three_sec = 0
map_objects = []
place_rect = pygame.Rect(0,0,0,0)
start=0
start_music = True
on_screen = []
clicked = []
hit_timing = []
combo_update = False
score=0
combo=0
blunders = []
max_combo = []

b100 = pygame.image.load("Skin/Skin_1/hit100-0@2x.png").convert_alpha()
# b100 = pygame.transform.scale(b100,(256*1.4,91*1.4))

b50 = pygame.image.load("Skin/Skin_1/hit50-0@2x.png").convert_alpha()
# b50 = pygame.transform.scale(b50,(256*1.4,91*1.4))

b0 = pygame.image.load("Skin/Skin_1/hit0-0@2x.png").convert_alpha()
# b0 = pygame.transform.scale(b0,(256*1.4,91*1.4))

click = pygame.mixer.Sound("Skin/Skin_1/normal-hitnormal.ogg")
pygame.mixer.Sound.set_volume(click, 0.02)

# Function for level startup
def music_peeper(maps,num,start):
    pygame.mixer.music.load(f"Maps/{maps[num]}/audio.ogg")
    pygame.mixer.music.set_volume(0.02)
    pygame.mixer.music.play(0,start/1000,0)
    return

# 229588/60

def object_reading(maps,num,file):
    objects=[]
    ob_file = open(f"Maps/{maps[num]}/{file}.txt", "r")
    for lines in ob_file:
        objects.append(lines.split(","))
    try:
        for x in range(len(objects)):
            objects[x][0] = int(objects[x][0])
            objects[x][1] = int(objects[x][1])
            objects[x][2] = int(objects[x][2])
    except:
        pass
    return objects

# This function has lots of colours in vscode (pretty)
def diff_reading(maps,num): 
    diff=[]
    diff_file = open(f"Maps/{maps[num]}/difficulty.txt", "r")
    for lines in diff_file:
        diff.append(lines.split(":"))
    for x in range(len(diff)):
        if "\n" in diff[x][1]:
            diff[x][1]=diff[x][1].replace("\n","")
        diff[x][1] = float(diff[x][1])
    return diff

def image_load(cs):
    inner = pygame.image.load("Skin/Skin_1/hitcircleselect.png").convert_alpha()
    inner = pygame.transform.scale(inner,(186-((cs-2)*10),186-((cs-2)*10)))
    inner_rect = inner.get_rect()

    out = pygame.image.load("Skin/Skin_1/hitcircleoverlay@2x.png").convert_alpha()
    out = pygame.transform.scale(out,(186-((cs-2)*10),186-((cs-2)*10)))
    out_rect = out.get_rect()

    ac = pygame.image.load("Skin/Skin_1/approachcircle@2x.png").convert_alpha()
    ac = pygame.transform.scale(ac,(186-((cs-2)*40),186-((cs-2)*40)))
    ac_rect = ac.get_rect()

    return inner,inner_rect,out,out_rect,ac,ac_rect

# um...
def python_sucks(start):
    return

# RULES VARY'S (THIS IS VEYR LAST MINUTE)
rules = False
rules_startup = False

# Pause vary's
pause = False
pause_startup = False
work = True

# IMAGES I NEED FOR PLAYING THE LEVELS
# game loop***********************************************************************************************************************************************************************
main = True
while main:
    work = True
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            main=False
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                if main_screen:
                    main=False
                elif map_pick:
                    map_pick=False
                    main_screen=True
                    new_map=True
                elif play_map:
                    pause = True
                    pause_startup = True
                    play_map = False
                elif pause:
                    pause = False
                    play_map = False
                    map_pick = True
                    # print(score)
                    # print(hit_timing)
                    # variables
                    map_startup = True
                    three_sec = 0
                    map_objects = []
                    start=0
                    start_music = True
                    on_screen = []
                    clicked = []
                    hit_timing = []
                    combo_update = False
                    score=0
                    combo=0
                    blunders = []
                    max_combo = []
                    new_map = True

                elif rules:
                    main_screen=True
                    rules=False
            if event.key == pygame.K_UP:
                k_up = True
                
            if event.key == pygame.K_DOWN:
                k_down = True

            if event.key == pygame.K_RETURN:
                k_enter = True
                if pause:
                    pause=False
                    play_map = True
                    work = False
                    pygame.mixer.music.unpause()
            if event.key == pygame.K_c:
                c_click = True
            
            if event.key == pygame.K_z:
                z_click = True
                

    clock.tick_busy_loop(100)

    screen.fill(0)

    # May not need this
    # # THIS PART IS FOR KEYBOARD INPUTS***************************************************************************************************************
    # # UP arrow for swapping maps
    # k_up = keyboard_inputs(k_up_pre, k_up_flag)
    # k_up_pre = k_up_flag

    # gets the mouse area
    mousex, mousey = pygame.mouse.get_pos()

    cursor_rect.center = mousex,mousey

    # Blit the curosr behind everything else

    # THIS IS COMPLEX SO THE BUTTON ONLY GETS PRESSED ONCE IF YOU HOLD IT
    # Saves the last mouse state
    mouse_prev = mouse_flag.copy()
    # Sets a flag if you clicked the button
    mouse_flag = list(pygame.mouse.get_pressed())
    # Puts in the magic function
    left, middle, right = mouse_inputs(mouse_prev,mouse_flag)

    # Does the main screen code
    if main_screen:
        # screen.blit(bg,(0,0))
        # Put the tings on the screen
        screen.blit(play,play_rect)
        screen.blit(make,make_rect)
        screen.blit(rule_im,rule_rect)

        # Puts you to the next part depending on what you hit
        if mouse_click(mousex,mousey,play_rect,left):
            map_pick = True
            main_screen = False
            first_map = random.randint(0,len(maps)-1)

        if mouse_click(mousex,mousey,make_rect,left):
            rules = True
            rules_startup = True
            main_screen = False
    # THis for rules n stuff
    if rules:
        if rules_startup:
            line1, l1 = new_text("This Game is basicaly just Osu without sliders",(255,255,255))
            line2, l2 = new_text("Firstly If you press play on the main screen then you will be taken to a map picking stage",(255,255,255))
            line3, l3 = new_text("From there you can press the up and down arrow to cycle through the maps",(255,255,255))
            line4, l4 = new_text("Once you found a map you want to play, hit enter and the map will start",(255,255,255))
            line5, l5 = new_text("When the map start circle will start to appear on the screen to the beat of a song",(255,255,255))
            line6, l6 = new_text("Your job is to click the circles when the outer circle reaches the middle",(255,255,255))
            line7, l7 = new_text("To click you can either press z or c on your keyboard, and you aim simply with your mouse",(255,255,255))
            line8, l8 = new_text("Thats the basics completly, im sure you can figure the rest out on your own :)",(255,255,255))
            line9, l9 = new_text("If you have anymore questions email me at:",(255,255,255))
            line10, l10 = new_text("michjfisher@gmail.com",(0,255,0))
            line11, l11 = new_text("Excuse any grammer/spelling mistakes, Its late at night",(255,255,255))
            line12, l12 = new_text("Lastly, press esc on the main screen to exit", (255,255,255))
        
            l1.center = (width/2, 200)
            l2.center = (width/2, l1.centery+(l1.height/2)+30)
            l3.center = (width/2, l2.centery+(l2.height/2)+30)
            l4.center = (width/2, l3.centery+(l3.height/2)+30)
            l5.center = (width/2, l4.centery+(l4.height/2)+30)
            l6.center = (width/2, l5.centery+(l5.height/2)+30)
            l7.center = (width/2, l6.centery+(l6.height/2)+30)
            l8.center = (width/2, l7.centery+(l7.height/2)+30)
            l9.center = (width/2, l8.centery+(l8.height/2)+30)
            l10.center = (width/2, l9.centery+(l9.height/2)+30)
            l11.center = (width/2, l10.centery+(l10.height/2)+30)
            l12.center = (width/2, l11.centery+(l11.height/2)+30)
            rules_startup=False


        screen.blit(line1,l1)
        screen.blit(line2,l2)
        screen.blit(line3,l3)
        screen.blit(line4,l4)
        screen.blit(line5,l5)
        screen.blit(line6,l6)
        screen.blit(line7,l7)
        screen.blit(line8,l8)
        screen.blit(line9,l9)
        screen.blit(line10,l10)
        screen.blit(line11,l11)
        screen.blit(line12,l12)



    if map_pick:
        # If a new map is picked then load a map (sounds/bg/stats)
        if new_map:
            stat_text = ""
            map_back = new_load(maps,first_map) 
            stats = object_reading(maps,first_map,"scores")
            stat_list = stat_maker(stats)
            # st, st_r = new_text(stat_text, (255,255,255))
            # stb, stb_r = new_text(stat_text, (0,0,0))

            text, text_rect = new_text(f"{maps[first_map]}", (255,255,255))
            textbd, textbd_rect = new_text(f"{maps[first_map]}", (0,0,0))
            new_map = False
        
        # If the person wants to go to the next map
        if k_up:
            first_map+=1
            new_map=True
            if first_map >= len(maps):
                first_map=0

        # Next map but in the downwards directions!
        if k_down:
            first_map-=1
            new_map=True
            if first_map <= -1:
                first_map=len(maps)-1

        # Checks if the player presses enter on a map(plays it)
        if k_enter:
            play_map = True
            map_pick = False

        # Everything needed for the screen map pick things
        screen.blit(map_back,(0,0))
        screen.blit(level_button,level_button_rect)
        textbd_rect.topleft = (level_button_rect.left+14, level_button_rect.top+14)
        screen.blit(textbd,textbd_rect)
        text_rect.topleft = (level_button_rect.left+10, level_button_rect.top+10)
        screen.blit(text,text_rect)
        # Put stats on screen
        for x in range(len(stat_list)):
            screen.blit(stat_list[x][0],stat_list[x][1])
        screen.blit(map_select_back,map_select_rect)
        screen.blit(menu_layer,menu_layer_rect)
        screen.blit(menu_back,menu_back_rect)


    # THIS ISE THE PART FOR PLAYING MAPS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!      
    if play_map:
        if map_startup:
            # three sec is so the level takes 2 seconds to load up
            if three_sec >= 2000:
                map_objects = object_reading(maps,first_map,"hit_objects")
                # This makes it so the map start ontime
                start = map_objects[0][2]-1500
                if start < 0:
                    start=0
                # This reads the difficulty txt files so I know lots of cool things
                map_diff = diff_reading(maps,first_map)
                # gets the circle images to the right size (changed by circle size in the txt file)
                hc_im_part1,hc_rc_part1,hc_im_part2,hc_rc_part2,ac_im,ac_rc = image_load(map_diff[1][1])
                # This starts the music
                music_peeper(maps,first_map,start)
                # this stores the circle size stuffs! :D :-) :O :p ;) >:|
                circle = 186-((map_diff[1][1]-2)*18)

                # This is for seeing how many milliseconds the Ar is going to be (AR means approach rate(outside circle coming to the inside circle))
                if map_diff[3][1]>= 5:
                    ar = 1800-((map_diff[3][1]*150)-150)
                else:
                    ar = 1800-((map_diff[3][1]*120)-120)

                # This is for checking the OD of a map(over difficulty(how long you have to click the circles))
                od_300 = 80-(map_diff[2][1]*6)
                od_100 = 140-(map_diff[2][1]*6)
                od_50 = 200-(map_diff[2][1]*6)

                # This makes another list for if the object is currently on the screen 
                for x in range(len(map_objects)):
                    on_screen.append(False)
                    clicked.append(False)
                    blunders.append([False,0])

                map_startup=False
            else:
                three_sec+=10
    
        # start keeps track of the time of the map in milliseconds

        start+=10

        # swap the things aorunds michael!!!!!!!!!!!!!!!!! (did it)

        # OK so the way this works is as follows
        # I have 3 lists 
        # map_objects is filled with the X and Y cords aswell as the timing (in milliseconds) when the objects are suppose to appear
        # on_screen is to keep track of what objects are on screen (i use this so I know what circles are allowed to be hit and a certain time)
        # clicked is so if i click a circle early its not still being put on the screen

        # Puts the circles on the screen
        for x in range(len(map_objects)):
            x = (len(map_objects)-1)-x
            if map_objects[x][2] < start-od_50 and clicked[x] == False:
                clicked[x] = True
                on_screen[x] = False
                hit_timing.append(0)
                blunders[x] = ["0", td]
                combo_update = True
            if map_objects[x][2] <= start+ar and map_objects[x][2] >= start-od_50 and clicked[x] == False:
                on_screen[x] = True
                # get the center of the 2 blitaging imaging 
                hc_rc_part1.center = ((map_objects[x][0]*2)+448,(map_objects[x][1]*2)+156)
                hc_rc_part2.center = ((map_objects[x][0]*2)+448,(map_objects[x][1]*2)+156)
                # Blit em
                screen.blit(hc_im_part1,hc_rc_part1)
                screen.blit(hc_im_part2,hc_rc_part2)
                # i hope this works!
                # YO it did
                # This basiacaly makes a circle approach the inner one that you click as it gets closer to the time to clickage
                if map_objects[x][2] >= start:
                    # ac_im_temp = pygame.transform.scale(ac_im,(circle+0.7*(map_objects[x][2]-start),circle+0.7*(map_objects[x][2]-start)))
                    ac_im_temp = pygame.transform.scale(ac_im,(circle+500*((map_objects[x][2]-start)/ar),circle+500*((map_objects[x][2]-start)/ar)))
                    ac_rc_temp = ac_im_temp.get_rect()
                    ac_rc_temp.center = ((map_objects[x][0]*2)+448,(map_objects[x][1]*2)+156)
                # blit it
                screen.blit(ac_im_temp,ac_rc_temp)

        # 100*((map_objects[x][2]-start)/ar)

        # Make list of stuff is x and y cords and false if no click true if click for blitage
        
        if c_click:
            for x in range(len(map_objects)):
                if (pow((mousex-((map_objects[x][0]*2)+448)),2)) + (pow((mousey-((map_objects[x][1]*2)+156)),2)) <= pow((circle/2),2) and on_screen[x] == True:
                    clicked[x] = True
                    on_screen[x] = False

                    if map_objects[x][2]-od_300 <= start and map_objects[x][2]+od_300 >= start:
                        hit_timing.append(300)
                        pygame.mixer.Sound.play(click)

                    elif map_objects[x][2]-od_100 <= start and map_objects[x][2]+od_100 >= start:
                        hit_timing.append(100)
                        blunders[x] = [100, td]
                        pygame.mixer.Sound.play(click)

                    elif map_objects[x][2]-od_50 <= start and map_objects[x][2]+od_50 >= start:
                        hit_timing.append(50)
                        blunders[x] = [50, td]
                        pygame.mixer.Sound.play(click)

                    else:
                        hit_timing.append(0)
                        blunders[x] = ["0", td]

                    combo_update = True

                    break

        if z_click:
            for x in range(len(map_objects)):
                if (pow((mousex-((map_objects[x][0]*2)+448)),2)) + (pow((mousey-((map_objects[x][1]*2)+156)),2)) <= pow((circle/2),2) and on_screen[x] == True:
                    clicked[x] = True
                    on_screen[x] = False

                    if map_objects[x][2]-od_300 <= start and map_objects[x][2]+od_300 >= start:
                        hit_timing.append(300)
                        pygame.mixer.Sound.play(click)

                    elif map_objects[x][2]-od_100 <= start and map_objects[x][2]+od_100 >= start:
                        hit_timing.append(100)
                        blunders[x] = [100, td]
                        pygame.mixer.Sound.play(click)

                    elif map_objects[x][2]-od_50 <= start and map_objects[x][2]+od_50 >= start:
                        hit_timing.append(50)
                        blunders[x] = [50, td]
                        pygame.mixer.Sound.play(click)

                    else:
                        hit_timing.append(0)
                        blunders[x] = ["0", td]

                    combo_update = True

                    break

        if combo_update:
            if hit_timing[-1] == 300:
                combo+=1
                score += hit_timing[-1]*combo
            elif hit_timing[-1] == 100:
                combo+=1
                score += hit_timing[-1]*combo
            elif hit_timing[-1] == 50:
                combo+=1
                score += hit_timing[-1]*combo
            elif hit_timing[-1] == 0:
                max_combo.append(combo)
                combo=0
            combo_update=False

        # This puts the blunder images on the screen (100, 50, X)
        for x in range(len(blunders)):
            if blunders[x][0] == 100:
                blunders[x][1]-=10
                screen.blit(b100, ((map_objects[x][0]*2)+248,(map_objects[x][1]*2)+156))
                if blunders[x][1] <= 0:
                    blunders[x][0] = False

            elif blunders[x][0] == 50:
                blunders[x][1]-=10
                screen.blit(b50, ((map_objects[x][0]*2)+448,(map_objects[x][1]*2)+156))
                if blunders[x][1] <= 0:
                    blunders[x][0] = False

            elif blunders[x][0] == "0":
                blunders[x][1]-=10
                screen.blit(b0, ((map_objects[x][0]*2)+448,(map_objects[x][1]*2)))
                if blunders[x][1] <= 0:
                    blunders[x][0] = False


        if not pygame.mixer.music.get_busy() and not map_startup and work:
            # Gets the final combo if there was no break at the end
            max_combo.append(combo)
            # Write the scores to the file
            f = open(f"Maps/{maps[first_map]}/scores.txt", "a")
            f.write(f"{score},{max(max_combo)},{hit_timing.count(300)},{hit_timing.count(100)},{hit_timing.count(50)},{hit_timing.count(0)},\n")
            f.close()
            play_map = False
            map_pick = True
            # print(score)
            # print(hit_timing)
            # variables
            map_startup = True
            three_sec = 0
            map_objects = []
            start=0
            start_music = True
            on_screen = []
            clicked = []
            hit_timing = []
            combo_update = False
            score=0
            combo=0
            blunders = []
            max_combo = []
            new_map = True

    if pause:
        if pause_startup:
            pt, pt_r = new_text("Press Enter to resume and ESC to go to map select",(255,255,255))
            pt_r.center = (width/2, height/2)
            pause_startup = False
            pygame.mixer.music.pause()
        screen.blit(pt,pt_r)


    # FIX ARRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR

    # michael many hours later - I FIXXED IT
    # Lists of score
    # print(clock.get_fps())
    # ((mousex-map_objects[x][0])**2) + ((mousey-map_objects[x][1])**2) <= (circle/2)^2 and on_screen[x] == True:
    screen.blit(cursor,cursor_rect)
    # Ending Keyboard reset variable stuffs
    k_up = False
    k_down = False
    k_enter = False  
    c_click = False
    z_click = False
    work = True
    pygame.display.flip()
pygame.quit()
sys.exit()
# WYSI