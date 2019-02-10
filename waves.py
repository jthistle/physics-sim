#!/usr/bin/env python3

import pygame, math, sys, os, random
from colours import *
from objects import Point, Wave
from helper import Helper
from decimal import *

def main():
	pygame.init()
	SCREEN_WIDTH = 800
	SCREEN_HEIGHT = 600
	SCALE = 80	# pixels per meter
	WIDTH = SCREEN_WIDTH/SCALE
	HEIGHT = SCREEN_HEIGHT/SCALE

	SCREEN_CENTRE = Point(WIDTH/2, HEIGHT/2)
	CENTRE = SCREEN_CENTRE/SCALE

	DISPLAY = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	CLOCK = pygame.time.Clock()
	totalTime = 0

	#waves = [
	#Wave(0.5, 1, 0.5, Point(SCREEN_CENTRE), 10, RED), 
	#Wave(-1, 1, 1, Point(SCREEN_CENTRE), 10, BLUE),
	#Wave(0.25, 0.75, 0.25, Point(SCREEN_CENTRE), 10, GREEN)]

	waves = [
	Wave(1, 1, 1, Point(SCREEN_CENTRE), 20, RED), 
	Wave(-1, 1, 1, Point(SCREEN_CENTRE), 20, BLUE)]

	hp = Helper(DISPLAY, SCALE, WIDTH, HEIGHT)

	while True:
		DISPLAY.fill(WHITE)
		deltaT = CLOCK.get_time()/1000
		totalTime += deltaT

		heldKeys = pygame.key.get_pressed()
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				pygame.quit()

			elif e.type == pygame.KEYDOWN:
				heldKeys = pygame.key.get_pressed()
				if (heldKeys[pygame.K_RCTRL] or heldKeys[pygame.K_LCTRL]) and\
					(heldKeys[pygame.K_w] or heldKeys[pygame.K_q]):
					pygame.quit()

		# === DRAW

		yVals = {}

		for w in waves:
			step = 0.02
			xTrans = math.pi / w.wavelength
			amp = w.amplitude
			myXVals = []
			for i in [x*step for x in (range(0, -int(w.length/step)-1, -1) if w.velocity > 0 else range(0, int(w.length/step)+1))]:
				yVal = amp*math.sin(i*xTrans)
				xVal = float(Decimal(w.pos.x + i).quantize(Decimal('.1'), rounding=ROUND_DOWN))
				if xVal not in myXVals:
					if xVal in yVals.keys():
						yVals[xVal].append(yVal)
					else:
						yVals[xVal] = [yVal]
					myXVals.append(xVal)
					
				pygame.draw.line(DISPLAY, w.colour, 
					hp.drawPos(w.pos + Point(i, yVal+HEIGHT/4)), 
					hp.drawPos(w.pos + Point(i + step, amp*math.sin((i + step)*xTrans)+HEIGHT/4))
					)

		last = ["NaN", 0]
		for i in sorted(yVals.keys()):
			vs = yVals[i]
			if len(vs) < 2:
				continue

			tot = sum(vs)
			if last[0] != "NaN":
				pygame.draw.line(DISPLAY, PURPLE,
				hp.drawPos(Point(last[1], HEIGHT/4 + last[0])), 
				hp.drawPos(Point(i, HEIGHT/4 + tot))
				)

			last = [tot, i]

		for w in waves:
			w.move(deltaT)

		pygame.display.update()
		CLOCK.tick(120)

if __name__ == "__main__":
	main()