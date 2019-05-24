import math

class Fraction:
	'''
	Base Fraction type, used for better processing

	Construct from:
		[no parameters] (default 0/1)
		Fraction
		numerator (float, int or Fraction)
		numerator, denominator (float, int or Fraction)
	'''
	def __init__(self, *args):
		constructed = False

		if len(args) == 0:
			self.num = 0
			self.den = 1
			constructed = True
		elif len(args) == 1:
			if type(args[0]) == int:
				self.num = args[0]
				self.den = 1
				constructed = True
			elif type(args[0]) == float:
				self.num = args[0]
				self.den = 1
				constructed = True
				self.unfloat()
			elif type(args[0]) == Fraction:
				self.num = args[0].num
				self.den = args[0].den
				constructed = True
		elif len(args) == 2:
			# Int, int
			if type(args[0]) == int and type(args[1]) == int:
				self.num = args[0]
				self.den = args[1]
				constructed = True
			# Int/float, int/float
			elif type(args[0]) in (int, float) and type(args[1]) in (int, float):
				self.num = args[0]
				self.den = args[1]
				constructed = True
				self.unfloat()
			# Fraction, Fraction
			elif type(args[0]) == Fraction and type(args[1]) == Fraction:
				self.num = args[0].num * args[1].den
				self.den = args[0].den * args[1].num
				constructed = True
			# Fraction, int/float
			elif type(args[0]) == Fraction and type(args[1]) in (int, float):
				self.num = args[0].num
				self.den = args[0].den * args[1]
				constructed = True
				self.unfloat()
			# int/float, Fraction
			elif type(args[0]) in (int, float) and type(args[1]) == Fraction:
				self.num = args[0] * args[1].den
				self.den = args[1].num
				constructed = True
				self.unfloat()
		
		if not constructed:
			raise Exception("Invalid Fraction constructor of ({})".format(", ".join([type(x) for x in args])))
		else:
			self.simplify()
		
		if self.den == 0:
			raise Exception("Invalid fraction, zero denominator!")

	def simplify(self):
		'''
		Simplify this fraction to its simplest form
		'''
		g = self.gcd(self.num, self.den)
		self.num = int(self.num/g)
		self.den = int(self.den/g)

	def gcd(self, a, b):
		'''
		Get the greatest common denominator of two numbers
		'''
		while b > 0:
			r = a % b
			a = b
			b = r
		
		return a

	def unfloat(self):
		'''
		Convert any floats on the top or bottom of the fraction to integers, while
		retaining the original value 
		'''
		floatSelf = float(self)
		decimalPlaces = str(floatSelf)[::-1].find(".")
		self.num = int(floatSelf * 10**decimalPlaces)
		self.den = int(10**decimalPlaces)
		self.simplify()		

	def __add__(self, num):
		fraction = False
		if type(num) in [int, float]:
			fraction = Fraction(num)
		elif type(num) == Fraction:
			fraction = num
		else:
			raise Exception("Invalid addition of fraction")

		n = self.num * fraction.den
		n += fraction.num * self.den
		d = self.den * fraction.den
		return Fraction(n, d)

	def __radd__(self, num):
		return self.__add__(num)
	
	def __sub__(self, num):
		return self.__add__(-num)

	def __rsub__(self, num):
		return Fraction(num).__sub__(self)

	def __mul__(self, factor):
		fraction = False
		if type(factor) in [int, float]:
			fraction = Fraction(factor)
		elif type(factor) == Fraction:
			fraction = factor
		else:
			raise Exception("Invalid multiplication of fraction")

		return Fraction(self.num * fraction.num, self.den * fraction.den)

	def __rmul__(self, factor):
		return self.__mul__(factor)

	def __truediv__(self, factor):
		fraction = False
		if type(factor) in [int, float]:
			fraction = Fraction(factor)
		elif type(factor) == Fraction:
			fraction = factor
		else:
			raise Exception("Invalid division of fraction")

		return self.__mul__(Fraction(fraction.den, fraction.num))
	
	def __rtruediv__(self, factor):
		return Fraction(factor).__truediv__(self)

	def __pow__(self, factor):
		return Fraction(self.num ** factor, self.den ** factor)

	def __rpow__(self, num):
		# hacky, TODO fix
		return Fraction(num) ** float(self)

	def genericEq(self, comp):
		fraction = False
		if comp in [int, float]:
			fraction = Fraction(comp)
		elif type(comp) == Fraction:
			fraction = comp
		else:
			raise Exception("Invalid fraction comparison")
		
		return fraction

	def __eq__(self, comp):
		fraction = genericEq(comp)

		# we can assume that they are simplified
		return (self.num == fraction.num and self.den == fraction.den)

	def __ne__(self, comp):
		fraction = genericEq(comp)
		return (self.num != fraction.num or self.den != fraction.den)
	
	def __lt__(self, comp):
		if type(comp) == Fraction:
			comp = float(comp)
		return (float(self) < comp)

	def __le__(self, comp):
		if type(comp) == Fraction:
			comp = float(comp)
		return (float(self) <= comp)

	def __gt__(self, comp):
		if type(comp) == Fraction:
			comp = float(comp)
		return (float(self) > comp)

	def __ge__(self, comp):
		if type(comp) == Fraction:
			comp = float(comp)
		return (float(self) >= comp)

	def __bool__(self):
		return self.num == 0

	def __str__(self):
		return "{}/{}".format(self.num, self.den)

	def __neg__(self):
		return Fraction(self.num * -1, self.den)
	
	def __pos__(self):
		return Fraction(self)
	
	def __abs__(self):
		return Fraction(abs(self.num), abs(self.den))

	def __int__(self):
		return int(float(self))
	
	def __float__(self):
		return float(self.num / self.den)

	def __ceil__(self):
		return Fraction(self.den * (self.num // self.den + 1), self.den)
	
	def __floor__(self):
		return Fraction(self.den * (self.num // self.den), self)

	def __round__(self):
		if self.num % self.den >= self.den * 0.5:
			return self.__ceil__()
		else:
			return self.__floor__()


class Vector:
	'''
	Can be constructed from:
		magnitude, direction
		(x, y) [real coords]
		Vector
		[no parameters]
	'''
	def __init__(self, *args):
		constructed = False
		if len(args) > 1:
			if type(args[0]) in (int, float, Fraction) and type(args[1]) in (int, float, Fraction):
				self.mag = args[0]
				self.dir = args[1]
				constructed = True
		elif len(args) > 0:
			if type(args[0]) == Vector:
				v = args[0]
				self.mag = v.mag
				self.dir = v.dir
				constructed = True
			elif type(args[0]) == tuple:
				x = args[0][0]
				y = args[0][1]
				self.mag = math.sqrt(x**2 + y**2)
				if self.mag == 0:
					self.dir = 0
				else:
					if y > 0:
						self.dir = math.acos(float(x/self.mag))	# rearrangment of x() equation
					elif x < 0:
						self.dir = math.asin(float(-y/self.mag))+math.pi
					else:
						self.dir = math.asin(float(y/self.mag))	# rearrangment of x() equation
					self.normalizeDir()
				constructed = True
		else:
			self.mag = 0
			self.dir = 0
			constructed = True

		if not constructed:
			raise Exception("Invalid Vector constructor")

	def __add__(self, vector):
		return Vector((self.x + vector.x, self.y + vector.y))

	def __sub__(self, vector):
		return Vector((self.x - vector.x, self.y - vector.y))

	def __mul__(self, mult):
		if type(mult) == Vector:
			return (self.x * mult.x) + (self.y * mult.y)
		else:
			return Vector((self.x * mult, self.y * mult))

	def __rmul__(self, mult):
		return self.__mul__(mult)

	def __floordiv__(self, div):
		if type(div) == Vector:
			raise Exception("can't divide by vector yet")
		else:
			return Vector((self.x // div, self.y // div))

	def __truediv__(self, div):
		if type(div) == Vector:
			raise Exception("can't divide by vector yet")
		else:
			return Vector((self.x / div, self.y / div))

	def __pow__(self, ind):
		toReturn = Vector(self)
		for i in range(ind-1):
			toReturn *= self
		return toReturn

	@property
	def x(self):
		return math.cos(float(self.dir)) * self.mag

	@property
	def y(self):
		return math.sin(float(self.dir)) * self.mag

	def flipY(self):
		self.dir = 2*math.pi-self.dir
		self.normalizeDir()

	def drawEndPos(self):
		return Point(self.x, -self.y)

	def endPos(self):
		return Point(self.x, self.y)

	def rotate(self, angle):
		self.dir += angle
		# for the sake of readability, keep the angle between 0 <= a < 2pi
		self.normalizeDir()

	def normalizeDir(self):
		self.dir = self.dir % (2*math.pi)

	def unit(self):
		mag = self.mag
		mult = 1/mag
		return self * mult

	def __str__(self):
		return "Vector(mag={}, dir={})".format(self.mag, self.dir)


class Point:
	'''
	Can be constructed from:
		x, y
		(x, y)
		Point
		[no parameters]
	'''
	def __init__(self, *args):
		constructed = False
		if len(args) > 1:
			if type(args[0]) in (int, float, Fraction) and type(args[1]) in (int, float, Fraction):
				self.x = args[0]
				self.y = args[1]
				constructed = True
		elif len(args) > 0:
			if type(args[0]) == Point:
				p = args[0]
				self.x = p.x
				self.y = p.y
				constructed = True
			elif type(args[0]) == tuple:
				p = args[0]
				self.x = p[0]
				self.y = p[1]
				constructed = True
		else:
			self.x = 0
			self.y = 0
			constructed = True

		if not constructed:
			raise Exception("Invalid Point constructor")

	def translated(self, x, y):
		return Point(self.x+x, self.y+y)

	def __add__(self, p):
		return Point(self.x+p.x, self.y+p.y)

	def __sub__(self, p):
		return Point(self.x-p.x, self.y-p.y)

	def __mul__(self, m):
		return Point(self.x*m, self.y*m)

	def __floordiv__(self, div):
		if type(div) == Point:
			raise Exception("can't divide by point")
		else:
			return Point((self.x // div, self.y // div))

	def __truediv__(self, div):
		if type(div) == Vector:
			raise Exception("can't divide by point")
		else:
			return Point((self.x / div, self.y / div))

	def __eq__(self, p):
		if self.x == p.x and self.y == p.y:
			return True
		return False

	def __str__(self):
		return "Point(x={}, y={})".format(self.x, self.y)

	def distance(self, p):
		return math.sqrt((self.x-p.x)**2 + (self.y-p.y)**2)

	def pos(self):
		return (self.x, self.y)

	def int(self):
		return (int(self.x), int(self.y))

	def pygameToReal(self):
		return Point(self.x, -self.y)

	def realToPygame(self):
		return Point(self.x, -self.y)


class Ball:
	def __init__(self):
		self.velocity = Vector()
		self.pos = Point()
		self.mass = 0.1
		self.radius = 0.1
		self.cor = 0.8
		self.moveable = True
		self.resultant = Vector()

	def accelerate(self, a):
		# Old: self.velocity += a
		# F = ma
		self.applyForce(a*self.mass)

	def applyForce(self, f):
		self.resultant = self.resultant + f

	def setResultant(self, f):
		self.resultant = f

	def setInEquilibrium(self):
		self.resultant = Vector()

	def move(self, dt):
		# a = f/m
		self.velocity = self.velocity + (self.resultant/self.mass)
		self.pos += self.velocity.endPos()*dt
		self.resultant = Vector()

	def translate(self, v):
		self.pos += v.endPos()

	def setPos(self, p):
		self.pos = p

	def setVelocity(self, v):
		self.velocity = v

	@property
	def bottom(self):
		return self.pos.y - self.radius

	@property
	def top(self):
		return self.pos.y + self.radius

	@property
	def left(self):
		return self.pos.x - self.radius

	@property
	def right(self):
		return self.pos.x + self.radius


class String:
	def __init__(self):
		self.forceConstant = 10	# Nm^-1
		self.length = 10
		self.connections = []
		self.active = False
		self.lastCalcDistance = -1
		self.damping = 0.5

	def setConnections(self, a, b):
		self.connections = [a, b]

	def applyTension(self, dt):
		# Legacy:
		tensionVector = Vector()
		stringVector = Vector()
		for i in range(1,2):	# only loop through once for now
			a = self.connections[i]
			b = self.connections[abs(i-1)]
			connectionDist = a.pos.distance(b.pos)
			self.lastCalcDistance = connectionDist
			if connectionDist > self.length and self.active and a.moveable:
				# String is taut
				# We can work out angle between gravity and tension vector
				# by creating a temporary vector for the string
				stringVector = Vector((a.pos-b.pos).pos())
				# tension acts on the ball towards the string pivot:
				oppositeStringAngle = stringVector.dir - math.pi
				tensionVector = Vector()

				# We can treat a taut string as a collision between balls along
				# the line of the string, i.e. ball a collides with ball b
				# So, momentum becomes involved.
				aMomentum = a.velocity * a.mass
				bMomentum = b.velocity * b.mass

				# Momentum is conserved:
				# Av*Am + Bv*Bm = Av'*Am + Bv'*Bm
				# as is KE:
				# 0.5*Am*Av^2 + 0.5*Bm*Bv^2 = 0.5*Am*Av'^2 + 0.5*Bm*Bv'^2
				# therefore
				# Av' = [(Am - Bm)·Av + 2·Bm·Bv]/(Am + Bm)
				# and 
				# Bv' = [2·Am·Av - (Am - Bm)·Bv]/(Am + Bm)
				am = a.mass
				bm = b.mass
				# A and B's velocity in the opposite string direction
				av = a.velocity.mag * math.cos(float(a.velocity.dir - stringVector.dir))
				bv = b.velocity.mag * math.cos(float(b.velocity.dir - stringVector.dir))

				# these are the new velocities in the opposite string direction
				newAv = ((am-bm)*av + 2*bm*bv)/(am+bm)
				newBv = (2*am*av - (bm-am)*bv)/(am+bm)

				# so, accelerate by the difference
				if a.moveable:
					a.accelerate((1 - self.damping) * Vector(av-newAv, oppositeStringAngle))
				if b.moveable:
					b.accelerate((1 - self.damping) * Vector(bv-newBv, oppositeStringAngle))

		return tensionVector

	def correctPositions(self):
		if self.active:
			if self.connections[1].moveable:
				b = self.connections[0]
				a = self.connections[1]
			elif self.connections[0].moveable:
				a = self.connections[0]
				b = self.connections[1]
			else:
				return False

			if self.lastCalcDistance >= self.length:
				distanceMod = self.length/self.lastCalcDistance
				distancePoint = Point(distanceMod*(a.pos.x-b.pos.x), distanceMod*(a.pos.y-b.pos.y))
				a.setPos(b.pos + distancePoint)

	def toggle(self):
		self.active = not self.active
	
class Wave:
	def __init__(self, vel, amp, wlen, pos, length, col):
		self.velocity = vel
		self.amplitude = amp
		self.wavelength = wlen
		self.pos = pos 	# position of wave front
		self.length = length
		self.colour = col

	@property
	def frequency(self):
		return self.velocity / self.wavelength

	def move(self, dt):
		self.pos += Point(self.velocity*dt, 0)
