import pygame
from pygame.locals import *
import numpy as np

SCR_HEIGHT	= 600
SCR_WIDTH	= 600
FPS			= 120		# I have 144 Hz monitor bish!
COLOR		= (255,0,0)

class Point:
	def __init__(self,x=0,y=0,z=0):
		self.x = x
		self.y = y
		self.z = z

	def xyz(self):
		return self.x,self.y,self.z

	def rotateX(self,angle=1):		#(rcos(a),rsin(a)) --> (rcos(a+tht), rsin(a+tht))
		theta=angle*np.pi/180
		sintht = np.sin(theta)
		costht = np.cos(theta)
		self.y=self.y*costht - self.z*sintht
		self.z=self.y*sintht + self.z*costht

	def rotateY(self,angle=1):
		theta=angle*np.pi/180
		sintht = np.sin(theta)
		costht = np.cos(theta)
		self.z=self.z*costht - self.x*sintht
		self.x=self.z*sintht + self.x*costht

	def rotateZ(self,angle=1):
		theta=angle*np.pi/180
		sintht = np.sin(theta)
		costht = np.cos(theta)
		self.x=self.x*costht - self.y*sintht
		self.y=self.x*sintht + self.y*costht

	def project(self):
		factor = 2000/(15+self.z)
		x = self.x*factor + SCR_WIDTH/2
		y = self.y*factor + SCR_HEIGHT/2
		return x,y

class Cube:
	def __init__(self):
		self.length = 200
		self.points = [	Point(-1,1,1),
						Point(1,1,1),
						Point(1,-1,1),
						Point(-1,-1,1),
						Point(-1,1,-1),
						Point(1,1,-1),
						Point(1,-1,-1),
						Point(-1,-1,-1)]
		self.ver1 = (0,2,5,7)
		self.ver2 = ((1,3,4),(1,3,6),(1,4,6),(3,4,6))

	def update(self,x,y,z):
		for p in self.points:
			if x:
				p.rotateX(x)
			if y:
				p.rotateY(y)
			if z:
				p.rotateZ(z)

	def drawlines(self,screen):
		pygame.font.init()
		font = pygame.font.SysFont("Arial", 20)
		p=self.points
		for i,b in zip(self.ver1,self.ver2):
			for j in b:
				pygame.draw.aaline(screen,COLOR,p[i].project(),p[j].project())

class Render:
	def __init__(self):
		self.screen = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
		self.speed = 1
		self.cu1 = Cube()
		self.angle = 1

	def draw(self,x,y,z):
		self.cu1.update(x,y,z)
		self.cu1.drawlines(self.screen)

	def run(self):
		clock = pygame.time.Clock()
		n_exit_game = True
		while n_exit_game:
			clock.tick(FPS)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					n_exit_game=False
			keys=pygame.key.get_pressed()
			x=y=z=0
			if keys[K_s]:
				x=1
			if keys[K_w]:
				x=-1
			if keys[K_a]:
				y=1
			if keys[K_d]:
				y=-1
			if keys[K_x]:
				z=1
			if keys[K_z]:
				z=-1
			self.screen.fill((0, 0, 0))
			self.draw(x,y,z)
			pygame.display.update()

if __name__ == "__main__":
	Render().run()