#!/usr/bin/env python3

import pygame, math, sys, os
from colours import *
from objects import Vector, Ball, Point, String
from gameObjects import Player, Goal


def main():
	pygame.init()
	SCREEN_WIDTH = 800
	SCREEN_HEIGHT = 600
	SCALE = 80	# pixels per meter
	WIDTH = SCREEN_WIDTH/SCALE
	HEIGHT = SCREEN_HEIGHT/SCALE

	SCREEN_CENTRE = Point(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
	CENTRE = SCREEN_CENTRE/SCALE

	DISPLAY = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	CLOCK = pygame.time.Clock()
	totalTime = 0

	GRAVITY = 9.81

	FONT_MONO_SMALL = pygame.font.SysFont("monospace", 14)
	FONT_MONO_LARGE = pygame.font.SysFont("monospace", 24)

	def drawPos(pos):
		return (int(pos.x*SCALE), int((HEIGHT-pos.y)*SCALE))

	def worldPos(pos):
		return (pos.x/SCALE, HEIGHT - pos.y/SCALE)

	def drawVector(v, start, scale=1, showBall=True, colour=PURPLE, width=2):
		'''
		Draws a vector, from
			Vector v
			Point start
			float scale
			bool showBall
		'''
		if v.mag > 0:
			pygame.draw.line(DISPLAY, colour, drawPos(start), drawPos(start + (v/scale).endPos()), width)
			if showBall:
				pygame.draw.circle(DISPLAY, colour, drawPos(start+(v/scale).endPos()), 3, 3)

	def checkCollisions(r1, r2):
		'''
		r1, r2 as tuples/lists of real points, from top-left clockwise
		'''
		for i in range(4):
			if (r1[i].x >= r2[0].x and r1[i].x <= r2[2].x
				and r1[i].y >= r2[2].y and r1[i].y <= r2[0].y):
				return True
		return False


	playerOne = Player()
	playerTwo = Player()
	playerOne.setPos(Point(WIDTH/4, HEIGHT/2))
	playerTwo.setPos(Point(3*WIDTH/4, HEIGHT/2))
	players = [playerOne, playerTwo]

	ball = Ball()
	ball.setPos(CENTRE)

	p1String = String()
	p2String = String()
	strings = [p1String, p2String]

	playerOneGoal = Goal()
	playerOneGoal.pos = Point(0.5, 3)
	playerTwoGoal = Goal()
	playerTwoGoal.pos = Point(WIDTH-0.5-playerTwoGoal.width, 3)
	goals = [playerOneGoal, playerTwoGoal]

	scores = [0, 0]

	stringAmounts = [1, 1]
	STRING_MAX = 1
	STRING_MIN_ACTIVATE = 0.2
	STRING_DISCHARGE = 0.6
	STRING_RECHARGE = 0.45
	STRING_KEYS = [pygame.K_SPACE, pygame.K_m]

	PLAYER_KEYS = ([pygame.K_w, pygame.K_d, pygame.K_s, pygame.K_a],
			[pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT])

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

				if e.key == STRING_KEYS[0]:
					dist = playerOne.pos.distance(ball.pos)
					if dist > 0 and stringAmounts[0] >= STRING_MIN_ACTIVATE:
						playerOne.string = True
						strings[0].length = dist
				elif e.key == STRING_KEYS[1]:
					dist = playerTwo.pos.distance(ball.pos)
					if dist > 0 and stringAmounts[1] >= STRING_MIN_ACTIVATE:
						playerTwo.string = True
						strings[1].length = dist

			elif e.type == pygame.MOUSEBUTTONDOWN:
				if e.button == 1:
					None

			elif e.type == pygame.MOUSEBUTTONUP:
				if e.button == 1:
					None

		for i in range(len(players)):
			p = players[i]
			if heldKeys[STRING_KEYS[i]] and p.string:
				stringAmounts[i] -= STRING_DISCHARGE * deltaT
				if stringAmounts[i] <= 0:
					stringAmounts[i] = 0
					p.string = False
			else:
				p.string = False
				stringAmounts[i] += STRING_RECHARGE * deltaT
				if stringAmounts[i] > STRING_MAX:
					stringAmounts[i] = STRING_MAX

		# player controls
		# Clockwise from up
		keyDirections = [math.pi/2, 0, 3*(math.pi/2), math.pi]

		for i in range(len(players)):
			p = players[i]
			accelVector = Vector()
			if sum([(1 if heldKeys[x] else 0) for x in PLAYER_KEYS[i]]) == 0:
				# No key held
				accelVector = Vector(p.dampingBase*deltaT, p.velocity.dir-math.pi)
				if p.velocity.mag < (p.velocity + accelVector).mag:
					p.velocity = Vector()
					accelVector = Vector()
			else:
				directionVector = Vector()
				for j in range(len(PLAYER_KEYS[i])):
					if heldKeys[PLAYER_KEYS[i][j]]:
						directionVector += Vector(1, keyDirections[j])
				
				# accelerate less as we approach max v
				# f(x)  = -e^-x
				# f'(x) = ln(e) * e^-x = e^-x
				# from x = 0-6
				# so x = 6/maxV * velMag
				#x = 6/playerOne.maxVelocity * playerOne.velocity.mag - 1	# -1 for reasons
				#multiplier = min(1, math.e**-x)
				# for now, leave as this
				multiplier = 1
				accelVector = Vector(p.acceleration*multiplier*deltaT, directionVector.dir)

			p.accelerate(accelVector)
			if p.velocity.mag > p.maxVelocity:
				p.velocity = Vector(p.maxVelocity, p.velocity.dir)

		if ball.bottom <= 0:
			#if abs(ball.velocity.y) < 0.5:
				#ball.setVelocity(Vector((ball.velocity.x, 0)))
				#ball.setPos(Point(ball.pos.x, ball.radius))
			if ball.velocity.y < 0:
				ball.accelerate(Vector((0, -ball.velocity.y-ball.velocity.y*ball.cor)))
		else:
			ball.accelerate(Vector((0, -GRAVITY))*deltaT)

			# for debug
			tensionVector = Vector()
			stringVector = Vector()
			mouseAccelTension = Vector()
			antiVelocityVector = Vector()
			for i in range(len(players)):
				string = strings[i]
				p = players[i]
				pBallDistance = p.pos.distance(ball.pos)
				if pBallDistance >= string.length and p.string:
					# String is taut
					# Create a temporary vector for the string
					stringVector = Vector((ball.pos-p.pos).pos())
					# tension acts on the ball towards the string pivot:
					oppositeStringAngle = stringVector.dir - math.pi

					# do tension created by movement
					pAccelTensionMag = p.velocity.mag * math.cos(oppositeStringAngle - p.velocity.dir)
					# this tension acts upon the ball along the oppositeStringAngle angle
					pAccelTension = Vector(pAccelTensionMag, oppositeStringAngle)
					#tensionVector = tensionVector + pAccelTension
					ball.accelerate(pAccelTension)

					# calculate tension created by taut string against velocity
					# away from string pivot
					ballVelMag = ball.velocity.mag
					ballVelAngle = ball.velocity.dir
					theta = ballVelAngle - stringVector.dir 
					antiVelocityMag = ballVelMag * math.cos(theta)
					if antiVelocityMag > 0:
						antiVelocityVector = Vector(antiVelocityMag, oppositeStringAngle)
						tensionVector = tensionVector + antiVelocityVector

					tensionVector.normalizeDir()
					ball.accelerate(tensionVector)

					# acceleration on player = F/m
					# F = m of ball * a of ball
					ballF = ball.mass * tensionVector.mag
					playerAccel = ballF / p.mass
					p.accelerate(Vector(playerAccel, stringVector.dir))

		if ball.left <= 0:
			if ball.velocity.x < 0:
				ball.accelerate(Vector((-ball.velocity.x-ball.velocity.x*ball.cor, 0)))

		if ball.right >= WIDTH:
			if ball.velocity.x > 0:
				ball.accelerate(Vector((-ball.velocity.x-ball.velocity.x*ball.cor, 0)))

		for p in players:
			if p.pos.x <= 0:
				if p.velocity.x < 0:
					p.accelerate(Vector((2*-p.velocity.x, 0)))

			if p.pos.x >= WIDTH:
				if p.velocity.x > 0:
					p.accelerate(Vector((2*-p.velocity.x, 0)))

			if p.pos.y <= 0:
				if p.velocity.y < 0:
					p.accelerate(Vector((0, 2*-p.velocity.y)))

			if p.pos.y >= HEIGHT:
				if p.velocity.y > 0:
					p.accelerate(Vector((0, 2*-p.velocity.y)))

		ball.move(deltaT)

		for i in range(len(players)):
			p = players[i]
			string = strings[i]
			p.move(deltaT)

			ballDist = p.pos.distance(ball.pos)
			if p.string and ballDist > string.length:
				# test scale ball distance
				distanceMod = string.length/ballDist
				distancePoint = Point(distanceMod*(ball.pos.x-p.pos.x), distanceMod*(ball.pos.y-p.pos.y))
				ball.setPos(p.pos + distancePoint)

		# Check if ball has collided with goal
		topLeft = ball.pos+Point(-ball.radius, -ball.radius)
		ballRect = (topLeft, topLeft+Point(ball.radius, 0), topLeft+Point(ball.radius, ball.radius), topLeft+Point(0, ball.radius))
		reset = False
		if checkCollisions(ballRect, playerOneGoal.drawPoints()) and ball.velocity.y < 0:
			scores[1] += 1
			reset = True
		elif checkCollisions(ballRect, playerTwoGoal.drawPoints()) and ball.velocity.y < 0:
			scores[0] += 1
			reset = True

		if reset:
			ball.setPos(CENTRE)
			ball.setVelocity(Vector())
			playerOne.string = False
			playerTwo.string = False

		# === DRAW

		# draw goal
		p1GoalDrawPoints = [drawPos(x) for x in playerOneGoal.drawPoints()]
		pygame.draw.polygon(DISPLAY, BLUE, p1GoalDrawPoints, 0)
		p2GoalDrawPoints = [drawPos(x) for x in playerTwoGoal.drawPoints()]
		pygame.draw.polygon(DISPLAY, GREEN, p2GoalDrawPoints, 0)

		# velocity vector is scaled so it can be more easily comprehended
		drawVector(ball.velocity, ball.pos, 10, False, GREEN, 1)

		# draw ball
		pygame.draw.circle(DISPLAY, RED, drawPos(ball.pos), int(ball.radius*SCALE), 1)

		# draw tension vector
		# drawVector(tensionVector, ball.pos, 10)

		for p in players:
			if p.string:
				pygame.draw.line(DISPLAY, GREEN, drawPos(ball.pos), drawPos(p.pos), 1)
		
		pygame.draw.circle(DISPLAY, BLUE, drawPos(playerOne.pos), 9, 0)
		pygame.draw.circle(DISPLAY, GREEN, drawPos(playerTwo.pos), 9, 0)

		
		# render text
		fps = FONT_MONO_SMALL.render("{}fps".format(int(CLOCK.get_fps())), 1, BLACK)
		DISPLAY.blit(fps, (10, 10))

		# Point sizes in pixels here
		h = 20
		maxW = 100

		topLeft = Point(10, 50)
		w = maxW*stringAmounts[0]
		p1StringPolyPoints = (topLeft, topLeft + Point(w, 0), topLeft+Point(w, h), topLeft+Point(0, h))
		pygame.draw.polygon(DISPLAY, (BLUE if stringAmounts[0] > STRING_MIN_ACTIVATE else RED), [x.pos() for x in p1StringPolyPoints], 0)

		topRight = Point(SCREEN_WIDTH-10, 50)
		w = maxW*stringAmounts[1]
		p2StringPolyPoints = (topRight, topRight+Point(-w, 0), topRight+Point(-w, h), topRight+Point(0, h))
		pygame.draw.polygon(DISPLAY, (GREEN if stringAmounts[1] > STRING_MIN_ACTIVATE else RED), [x.pos() for x in p2StringPolyPoints], 0)

		score1Label = FONT_MONO_LARGE.render("{}".format(scores[0]), 1, BLUE)
		DISPLAY.blit(score1Label, (SCREEN_WIDTH/2-50-score1Label.get_rect().width, 30))
		score2Label = FONT_MONO_LARGE.render("{}".format(scores[1]), 1, GREEN)
		DISPLAY.blit(score2Label, (SCREEN_WIDTH/2+50, 30))

		pygame.display.update()
		CLOCK.tick(120)

if __name__ == "__main__":
	main()