import pygame, sys
from pygame.locals import *
from math import pi, cos, sin
import cmath
from time import sleep


def angleaverage(v, t):
    angle = cmath.phase(v)
    angle = (t + angle) / 2
    mag = abs(v)
    v = complex(mag * cos(angle), mag * sin(angle))
    return v


pygame.init()
pygame.font.init()

disp = pygame.display.set_mode((0, 0), FULLSCREEN)
dispwidth = disp.get_width()
dispheight = disp.get_height()
disp.fill((0, 0, 0))

fps = 45
clock = pygame.time.Clock()

pygame.display.set_caption('Pong Champions')
icon = pygame.image.load('icon.jpg')
pygame.display.set_icon(icon)

font = pygame.font.SysFont('Comic Sans MS', 30)

pongwidth = 10
pongheight = 50
pongoffset = 15

leftpong = pygame.draw.rect(disp, (255, 255, 255), (pongoffset, int((dispheight - pongheight) / 2), pongwidth, pongheight))
rightpong = pygame.draw.rect(disp, (255, 255, 255), (dispwidth - pongoffset - pongwidth, int((dispheight - pongheight) / 2), pongwidth, pongheight))


ballwidth = 10
ballheight = 10

ball = pygame.draw.rect(disp, (255, 255, 255), (int((dispwidth-ballwidth)/2), int((dispheight-ballheight)/2), ballwidth, ballheight))

leftmov = {'x': 0, 'y': 0}
rightmov = {'x': 0, 'y': 0}

ogdelta = 7
delta = ogdelta
dvconst = 1
deltadv = 1/10
theta = pi
velocity = complex(delta*dvconst*cos(theta), delta*dvconst*sin(theta))

leftscore = 0
rightscore = 0

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == pygame.K_w:
                leftmov['y'] += 1
            if event.key == pygame.K_s:
                leftmov['y'] += -1
            if event.key == pygame.K_i:
                rightmov['y'] += 1
            if event.key == pygame.K_k:
                rightmov['y'] += -1
            if event.key == pygame.K_a:
                leftmov['x'] += -1
            if event.key == pygame.K_d:
                leftmov['x'] += 1
            if event.key == pygame.K_j:
                rightmov['x'] += -1
            if event.key == pygame.K_l:
                rightmov['x'] += 1
        if event.type == KEYUP:
            if event.key == pygame.K_w:
                leftmov['y'] -= 1
            if event.key == pygame.K_s:
                leftmov['y'] += 1
            if event.key == pygame.K_i:
                rightmov['y'] -= 1
            if event.key == pygame.K_k:
                rightmov['y'] += 1
            if event.key == pygame.K_a:
                leftmov['x'] += 1
            if event.key == pygame.K_d:
                leftmov['x'] -= 1
            if event.key == pygame.K_j:
                rightmov['x'] += 1
            if event.key == pygame.K_l:
                rightmov['x'] -= 1

    leftpong.move_ip(int(delta*leftmov['x']), -int(delta*leftmov['y']))
    rightpong.move_ip(int(delta*rightmov['x']), -int(delta*rightmov['y']))

    if leftpong.left < 0:
        leftpong.left = 0
    if leftpong.right > dispwidth:
        leftpong.right = dispwidth
    if rightpong.left < 0:
        rightpong.left = 0
    if rightpong.right > dispwidth:
        rightpong.right = dispwidth

    if leftpong.top < 0:
        leftpong.top = 0
    if leftpong.bottom > dispheight:
        leftpong.bottom = dispheight
    if rightpong.top < 0:
        rightpong.top = 0
    if rightpong.bottom > dispheight:
        rightpong.bottom = dispheight

    ball.move_ip(int(velocity.real), -int(velocity.imag))

    hitleftpong = ball.left <= leftpong.right and ball.bottom >= leftpong.top and ball.top <= leftpong.bottom
    hitrightpong = ball.right >= rightpong.right and ball.bottom >= rightpong.top and ball.top <= rightpong.bottom

    if hitleftpong or hitrightpong:
        velocity = complex(-velocity.real, velocity.imag)

        if (hitleftpong and leftmov['y'] == 1) or (hitrightpong and rightmov['y']):
            velocity = angleaverage(velocity, pi/2)
        if hitleftpong and leftmov['y'] == -1:
            velocity = angleaverage(velocity, -pi/2)
        if hitrightpong and rightmov['y'] == -1:
            velocity = angleaverage(velocity, 3*pi/2)

        if hitleftpong and leftmov['x'] == 1:
            velocity = angleaverage(velocity, 0)
            velocity = (velocity / dvconst) * (dvconst + deltadv)
            dvconst += deltadv
            delta += 1

        if hitrightpong and rightmov['x'] == -1:
            velocity = angleaverage(velocity, pi)
            velocity = (velocity / dvconst) * (dvconst + deltadv)
            dvconst += deltadv
            delta += 1

        if hitleftpong:
            ball.left = leftpong.right
        if hitrightpong:
            ball.right = rightpong.left

    if ball.top <= 0 or ball.bottom >= dispheight:
        velocity = complex(velocity.real, -velocity.imag)

    displayscore = False
    if ball.left <= 0 or ball.right >= dispwidth:

        displayscore = True
        delta = ogdelta
        dvconst = 1

        velocity = complex(delta * dvconst * cos(theta), delta * dvconst * sin(theta))
        if ball.left <= 0:
            rightscore += 1
            theta = pi
        elif ball.right >= dispwidth:
            leftscore += 1
            theta = 0
        
        ball.x, ball.y = int((dispwidth - ballwidth) / 2), int((dispheight - ballheight) / 2)
        leftpong.x, leftpong.y = pongoffset, int((dispheight - pongheight) / 2)
        rightpong.x, rightpong.y = dispwidth - pongoffset - pongwidth, int((dispheight - pongheight) / 2)

        velocity = complex(delta * dvconst * cos(theta), delta * dvconst * sin(theta))

        print(leftscore, rightscore)

    disp.fill((0, 0, 0))
    pygame.draw.rect(disp, (255, 255, 255), leftpong)
    pygame.draw.rect(disp, (255, 255, 255), rightpong)
    pygame.draw.rect(disp, (255, 255, 255), ball)

    if displayscore:
        scoreboard = font.render('%d - %d' % (leftscore, rightscore), False, (255, 255, 255))
        disp.blit(scoreboard, (int(dispwidth/2), int(dispheight/2)))

    pygame.display.update()
    clock.tick(fps)

    if displayscore:
        sleep(1)
