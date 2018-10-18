import math
from objects import Vector, Point

class Player:
	def __init__(self):
		self.velocity = Vector()
		self.pos = Point()
		self.mass = 1
		self.dampingBase = 8	# base deaccleration
		self.maxVelocity = 5
		self.acceleration = 15
		self.string = False

	def accelerate(self, a):
		self.velocity += a

	def move(self, dt):
		self.pos += self.velocity.endPos()*dt

	def toggleString(self):
		self.string = not self.string

	def setPos(self, p):
		self.pos = p

class Goal:
	def __init__(self):
		self.pos = Point()
		self.width = 0.7
		self.thickness = 0.1

	def drawPoints(self):
		return (self.pos, self.pos+Point(self.width, 0), self.pos+Point(self.width, -self.thickness), self.pos+Point(0, -self.thickness))