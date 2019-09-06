import pygame
from pygame.locals import *
from pygame import gfxdraw
import numpy as np

SCR_HEIGHT	= 800
SCR_WIDTH	= 800
FPS			= 120		# I have 144 Hz monitor bish!
COLOR		= (255,0,0)

class Point:
	def __init__(self,x=0,y=0,z=0):
		self.x = x
		self.y = y
		self.z = z
		self.rx=(self.y**2+self.z**2)**0.5
		self.ry=(self.z**2+self.x**2)**0.5
		self.rz=(self.x**2+self.y**2)**0.5
		self.alpha = np.arctan2(self.y,self.z)
		self.beta = np.arctan2(self.z,self.x)
		self.gamma = np.arctan2(self.x,self.y)

	def xyz(self):
		return self.x,self.y,self.z

	def rotateX(self,angle=1):
		theta=angle*np.pi/180
		self.alpha+=theta
		self.y=self.rz*np.cos(self.alpha)
		self.z=self.rz*np.sin(self.alpha)

	def rotateY(self,angle=1):
		theta=angle*np.pi/180
		self.beta+=theta
		self.z=self.rz*np.cos(self.beta)
		self.x=self.rz*np.sin(self.beta)

	def rotateZ(self,angle=1):
		theta=angle*np.pi/180
		self.gamma+=theta
		self.x=self.rz*np.cos(self.gamma)
		self.y=self.rz*np.sin(self.gamma)

	def project(self):
		factor = 2000/(20+self.z)
		x = self.x*factor + SCR_WIDTH/2
		y = self.y*factor + SCR_HEIGHT/2
		return x,y

class Cube:
	def __init__(self):
		self.length = 200
		self.points = [Point(-1,1,1),
						Point(1,1,1),
						Point(1,-1,1),
						Point(-1,-1,1),
						Point(-1,1,-1),
						Point(1,1,-1),
						Point(1,-1,-1),
						Point(-1,-1,-1)]
		self.ver1 = (0,2,5,7)
		self.ver2 = ((1,3,4),(1,3,6),(1,4,6),(3,4,6))

	def update(self,angle):
		for p in self.points:
			p.rotateX(angle)
			# p.rotateY(angle)
			# p.rotateZ(angle)

	def drawlines(self,screen):
		pygame.font.init()
		font = pygame.font.SysFont("Arial", 20)
		p=self.points
		for i,b in zip(self.ver1,self.ver2):
			for j in b:
				pygame.draw.aaline(screen,COLOR,p[i].project(),p[j].project())
				screen.blit(font.render(str(i),True,(0, 255, 0)),p[i].project())
				screen.blit(font.render(str(i),True,(0, 255, 0)),p[j].project())

class Render:
	def __init__(self):
		self.screen = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
		self.speed = 1
		self.cu1 = Cube()
		self.angle = 1

	def draw(self):
		self.cu1.update(self.angle)
		# self.angle=0
		self.cu1.drawlines(self.screen)

	def run(self):
		clock = pygame.time.Clock()
		n_exit_game = True
		while n_exit_game:
			clock.tick(FPS)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					n_exit_game=False
			self.screen.fill((255, 255, 255))
			self.draw()
			pygame.display.update()

if __name__ == "__main__":
	Render().run()