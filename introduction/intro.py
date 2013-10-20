#This is a simple exercise for those who want to get familiar with our piece of code. It was taken from the website pygame.org, and it is subject to pygame licence. We do not hold any copyright whatsoever. Ball.gif is alike owned by pygame.org

#1 task. Make the ball bounce slower
#2 task. Replace the ball with a circle
#3 task. Introduce one more circle
#4 task. Try to collide both circles, using linear algebra/ vector operations. Look to my code to see how I've solved.
#5 task. Perform a posteriori collisions of these two circles in an infinite (game) loop.

import sys, pygame
pygame.init()
 
size = width, height = 320, 240
speed = [2, 2]
black = 0, 0, 0
 
screen = pygame.display.set_mode(size)

ball = pygame.image.load("ball.gif")
ballrect = ball.get_rect()
while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
	ballrect = ballrect.move(speed)
	if ballrect.left < 0 or ballrect.right > width:
		speed[0] = -speed[0]
	if ballrect.top < 0 or ballrect.bottom > height:
		speed[1] = -speed[1]
	screen.fill(black)
	screen.blit(ball, ballrect)
	pygame.display.flip()
