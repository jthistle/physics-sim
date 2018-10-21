# Some helper functions for drawing

import math, pygame
from objects import *
from colours import *

class Helper:
	def __init__(self, displaySurf, scale, width, height):
		self.display = displaySurf
		self.scale = scale
		self.width = width
		self.height = height

	def drawPos(self, pos):
		return (int(pos.x*self.scale), int((self.height-pos.y)*self.scale))

	def worldPos(self, pos):
		return (pos.x/self.scale, self.height - pos.y/self.scale)

	def drawVector(self, v, start, scale=1, showBall=True, colour=PURPLE, width=2):
		'''
		Draws a vector, from
			Vector v
			Point start
			float scale
			bool showBall
		'''
		if v.mag > 0:
			pygame.draw.line(self.display, colour, self.drawPos(start), self.drawPos(start + (v/scale).endPos()), width)
			if showBall:
				pygame.draw.circle(self.display, colour, self.drawPos(start+(v/scale).endPos()), 3, 3)