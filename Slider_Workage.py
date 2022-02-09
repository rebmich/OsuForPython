
import pygame
import sys
import math

from pygame.constants import K_ESCAPE

pygame.init()
clock = pygame.time.Clock()
width=1920/2
height=1080/2
pygame.display.set_caption("No internet")
screen= pygame.display.set_mode((width,height))

circles = []

final_points = []

points = []
# (Slider_Testage)
st = 0

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


main = True
while main:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            main=False
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                main=False

    clock.tick(240)

    # screen.fill(0)

    # gets the mouse area
    mousex, mousey = pygame.mouse.get_pos()

    screen.fill(0)

    # THIS IS COMPLEX SO THE BUTTON ONLY GETS PRESSED ONCE IF YOU HOLD IT
    # Saves the last mouse state
    mouse_prev = mouse_flag.copy()
    # Sets a flag if you clicked the button
    mouse_flag = list(pygame.mouse.get_pressed())
    # Puts in the magic function
    left, middle, right = mouse_inputs(mouse_prev,mouse_flag)

    if left:
        points.append([mousex,mousey])

    if len(points) == 3:
            degs = []
        # try:
            # y = mx+b
            # mx+b = mx+b
            # Get the 2 mid points
            mid1 = [(points[st][0]+points[st+1][0])/2,(points[st][1]+points[st+1][1])/2]
            mid2 = [(points[st+1][0]+points[st+2][0])/2,(points[st+1][1]+points[st+2][1])/2]
            # Get the slope of each
            m1 = -1/((points[st][1]-points[st+1][1])/(points[st][0]-points[st+1][0]))
            m2 = -1/((points[st+1][1]-points[st+2][1])/(points[st+1][0]-points[st+2][0]))
            # Get the B numba
            b1 = mid1[1]-(m1*mid1[0])
            b2 = mid2[1]-(m2*mid2[0])
            # Get X and Y cords
            main_x = (b2-b1)/(m1-m2)
            main_y = (m1*main_x)+b1
            # Get radius
            r = math.sqrt(abs((points[st][0]-main_x)**2)+abs((points[st][1]-main_y)**2))

            circles.append([main_x,main_y,r])

            # Get the degreas of the 3 arms
            for x in range(3):
                if points[st+x][1] < main_y:
                    degs.append(360-(math.degrees(math.acos((points[st+x][0]-main_x)/r))))
                else:
                    degs.append(math.degrees(math.acos((points[st+x][0]-main_x)/r)))
            # Get a sub degree to act as refernce
            dubdeg = round(degs[0])

            if degs[0] < degs[1]:
                if degs[2] < degs[0]:
                    degs[2] = degs[2]+360
                while dubdeg < degs[2]:
                    temp_x = math.cos(math.radians(dubdeg))*r
                    temp_y = math.sin(math.radians(dubdeg))*r

                    final_x = main_x+temp_x
                    final_y = main_y+temp_y

                    dubdeg+=4
                    final_points.append([final_x,final_y])
            else:
                if degs[2] > degs[0]:
                    degs[2] = degs[2]-360
                while dubdeg > degs[2]:
                    temp_x = math.cos(math.radians(dubdeg))*r
                    temp_y = math.sin(math.radians(dubdeg))*r

                    final_x = main_x+temp_x
                    final_y = main_y+temp_y

                    # Fix deeg thing (devide radius)

                    dubdeg-=4
                    final_points.append([final_x,final_y])

            # print(points)
            # print(mid1)
            # print(mid2)
            # print(m1)
            # print(m2)
            # print(b1)
            # print(b2)
            # print(main_x)
            # print(main_y)
            # print(r)

            # print(degs)

            # print(f"({points[st][0]},{points[st][1]}),({points[st+1][0]},{points[st+1][1]}),({points[st+2][0]},{points[st+2][1]})")
            # print(f"({mid1[0]},{mid1[1]}),({mid2[0]},{mid2[1]})")
            # print(f"y = {m1}x + {b1}")
            # print(f"y = {m2}x + {b2}")
            # print(f"({main_x},{main_y})")
            # print(f"(x-{main_x})^2+(y-{main_y})^2={r}^2")
            # print(final_points)
            points=[]



        # except:
        #     pass
        # points=[]

    for x in range(len(final_points)):
        pygame.draw.circle(screen, (255,255,255), (final_points[x][0],final_points[x][1]),55,0)

    for x in range(len(final_points)):
        pygame.draw.circle(screen, (0,0,0), (final_points[x][0],final_points[x][1]),50,0)

    pygame.display.flip()

pygame.quit()
sys.exit()

