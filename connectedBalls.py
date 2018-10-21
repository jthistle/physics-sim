#!/usr/bin/env python3

import pygame, math, sys, os
from colours import *
from objects import Vector, Ball, Point, String
from helper import Helper


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

	GRAVITY = 9.81

	helper = Helper(DISPLAY, SCALE, WIDTH, HEIGHT)
	drawPos = helper.drawPos
	worldPos = helper.worldPos
	drawVector = helper.drawVector


	personImage = pygame.image.load("person.jpg")
	personRect = personImage.get_rect()
	personImage = pygame.transform.scale(personImage, (int(personRect.width*(int(1.8*SCALE)/personRect.height)), int(1.8*SCALE)))

	moveData = {
		"lastPos": Point(),
		"currentPos": Point(CENTRE.x, 0),
		"lastScreenMousePos": Point(),
		"mouseHeld": False,
		"lastVelocity": Vector()
	}
	mouseVelocity = Vector()

	tickerPoints = []
	MAX_TICKER_POINTS = 100
	TICKER_PERIOD = 0.02
	timeSinceLastTicker = 0

	mouseBall = Ball()
	mouseBall.moveable = False

	ball = Ball()
	ball.setPos(Point(WIDTH/2, HEIGHT/2))
	balls = [ball]

	ballMouseString = String()
	ballMouseString.setConnections(mouseBall, ball)
	strings = [ballMouseString]
	for i in range(5):
		a = Ball()
		a.setPos(Point(WIDTH/2, HEIGHT/4))
		balls.append(a)
		st = String()
		st.setConnections(balls[i], balls[i+1])
		st.length = 0.75
		st.active = True
		strings.append(st)

	print(len(balls))
	print(len(strings))

	'''ball2 = Ball()
	ball2.setPos(Point(WIDTH/2, HEIGHT/4))
	#ball2.mass = 0.5
	balls.append(ball2)
	ball3 = Ball()
	ball3.setPos(Point(WIDTH/2, HEIGHT/4))
	#ball3.mass = 1
	balls.append(ball3)'''
	

	
	'''ballString1 = String()
	ballString1.setConnections(ball, ball2)
	ballString1.length = 1
	ballString1.active = True
	ballString2 = String()
	ballString2.setConnections(ball2, ball3)
	ballString2.length = 1
	ballString2.active = True
	strings = [ballMouseString, ballString1, ballString2]'''

	while True:
		DISPLAY.fill(WHITE)
		deltaT = CLOCK.get_time()/1000
		totalTime += deltaT

		moveData["lastPos"] = Point(moveData["currentPos"])
		if not moveData["lastScreenMousePos"] == Point(pygame.mouse.get_pos()):
			moveData["currentPos"] = Point(worldPos(Point(pygame.mouse.get_pos())))

		moveData["lastScreenMousePos"] = Point(pygame.mouse.get_pos())

		heldKeys = pygame.key.get_pressed()
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				pygame.quit()

			elif e.type == pygame.KEYDOWN:
				heldKeys = pygame.key.get_pressed()
				if (heldKeys[pygame.K_RCTRL] or heldKeys[pygame.K_LCTRL]) and\
					(heldKeys[pygame.K_w] or heldKeys[pygame.K_q]):
					pygame.quit()
				if (heldKeys[pygame.K_SPACE]):
					mouseBallDist = moveData["currentPos"].distance(balls[0].pos)
					if mouseBallDist > 0:
						strings[0].length = mouseBallDist
						strings[0].toggle()

			elif e.type == pygame.MOUSEBUTTONDOWN:
				if e.button == 1:
					moveData["mouseHeld"] = True

			elif e.type == pygame.MOUSEBUTTONUP:
				if e.button == 1:
					moveData["mouseHeld"] = False

		keyboardMoveSpeed = 1
		if heldKeys[pygame.K_a]:
			moveData["currentPos"] = moveData["currentPos"] - Point(keyboardMoveSpeed*deltaT, 0)
		elif heldKeys[pygame.K_d]:
			moveData["currentPos"] = moveData["currentPos"] + Point(keyboardMoveSpeed*deltaT, 0)
		if heldKeys[pygame.K_w]:
			moveData["currentPos"] = moveData["currentPos"] + Point(0, keyboardMoveSpeed*deltaT)
		elif heldKeys[pygame.K_s]:
			moveData["currentPos"] = moveData["currentPos"] - Point(0, keyboardMoveSpeed*deltaT)

		if deltaT > 0:
			moveData["lastVelocity"] = Vector(mouseVelocity)
			mouseVelocity = Vector(((moveData["currentPos"]-moveData["lastPos"])/deltaT).pos())
			mouseAcceleration = (mouseVelocity - moveData["lastVelocity"])/deltaT
		else:
			mouseVelocity = Vector()
			mouseAcceleration = Vector()
		mouseBall.setVelocity(mouseVelocity)
		mouseBall.setPos(moveData["currentPos"])

		for i in range(len(balls)):
			b = balls[i]
			if b.bottom <= 0:
				if b.velocity.y < 0:
					b.accelerate(Vector((0, -b.velocity.y-b.velocity.y*b.cor)))
			else:
				b.accelerate(Vector((0, -GRAVITY))*deltaT)

			if b.left <= 0:
				if b.velocity.x < 0:
					ball.accelerate(Vector((-b.velocity.x-b.velocity.x*b.cor, 0)))

			if b.right >= WIDTH:
				if b.velocity.x > 0:
					ball.accelerate(Vector((-b.velocity.x-b.velocity.x*b.cor, 0)))

		for s in strings:
			s.applyTension()
			#drawVector(s.applyTension(), s.connections[1].pos, 1)
		
		if moveData["mouseHeld"]:
			balls[0].setPos(mouseBall.pos)
			balls[0].setVelocity(mouseBall.velocity)
			balls[0].moveable = False
		else:
			balls[0].moveable = True

		for i in range(len(balls)):
			if i == 0 and moveData["mouseHeld"]:
				continue

			b = balls[i]
			b.move(deltaT)

		for s in strings:
			s.correctPositions()

		# === DRAW

		# draw person
		DISPLAY.blit(personImage, (-(1/3)*personImage.get_rect().width, SCREEN_HEIGHT-personImage.get_rect().height))

		# draw ticker tape
		if not moveData["mouseHeld"] and False:
			timeSinceLastTicker += deltaT
			if timeSinceLastTicker >= TICKER_PERIOD:
				tickerPoints.append(Point(ball.pos))
				if len(tickerPoints) > MAX_TICKER_POINTS:
					del tickerPoints[0]
				timeSinceLastTicker = 0
		else:
			tickerPoints = []

		for p in tickerPoints:
			pygame.draw.circle(DISPLAY, BLUE, drawPos(p), 2, 2)

		# draw mouse velocity vector
		drawVector(mouseBall.velocity, mouseBall.pos, 20, False, BLUE)

		# velocity vector is scaled so it can be more easily comprehended
		for b in balls:
			drawVector(b.velocity, b.pos, 10, False, GREEN, 1)

		# draw ball
		for b in balls:
			pygame.draw.circle(DISPLAY, RED, drawPos(b.pos), int(ball.radius*SCALE), 1)

		for s in strings:
			if s.active:
				pygame.draw.line(DISPLAY, GREEN, drawPos(s.connections[0].pos), drawPos(s.connections[1].pos), 1)

		font = pygame.font.SysFont("monospace", 15)
		# render text
		fps = font.render("{}fps".format(int(CLOCK.get_fps())), 1, BLACK)
		DISPLAY.blit(fps, (10, 10))
		ballVelLabel = font.render("Ball velocity: {:.2f}ms-1".format(ball.velocity.mag), 1, BLACK)
		DISPLAY.blit(ballVelLabel, (10, 30))
		mouseVelLabel = font.render("Mouse velocity: {:.2f}ms-1".format(mouseVelocity.mag), 1, BLACK)
		DISPLAY.blit(mouseVelLabel, (10, 50))

		pygame.display.update()
		CLOCK.tick(120)

if __name__ == "__main__":
	main()