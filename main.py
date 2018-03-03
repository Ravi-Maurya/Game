import pygame
import sys
from pygame.locals import *

class BColors:
	black = pygame.Color(0,0,0)
	white = pygame.Color(255,255,255)
	red = pygame.Color(255,0,0)
	blue = pygame.Color(0,0,255)
	green = pygame.Color(0,255,0)

class Paddle:
	def __init__(self):
		self.rect = pygame.Rect(0,480-16,160,16)

class Ball:
	def __init__(self,pos):
		self.reset(pos)

	def update(self):
		self.rect.x += self.dx
		self.rect.y += self.dy

	def reverseY(self):
		self.dy = -self.dy

	def reverseX(self):
		self.dx = -self.dx

	def reset(self,pos):
		self.rect = pygame.Rect(pos,480,16,16)
		self.dx = 5
		self.dy = -5

class Block:
	def __init__(self,rect):
		self.rect = rect

class Game:
	def __init__(self):
		self.running = False
		pygame.init()
		self.clock = pygame.time.Clock()
		self.screensize = self.screenw , self.screenh = 640 , 480
		pygame.display.set_caption("GAME BY RaV!")
		pygame.mouse.set_visible(False)
		self.screen = pygame.display.set_mode(self.screensize)
		self.font = pygame.font.Font("fonts\PressStart2P.ttf",16)
		self.paddle = Paddle()
		self.ball = Ball(320)
		self.tope = pygame.Rect(0,0,self.screenw,16)
		self.lefte = pygame.Rect(0,0,16,self.screenh)
		self.righte = pygame.Rect(self.screenw-16,0,16,self.screenh)
		self.lives = 2
		self.score = 0
		self.blocks = [pygame.Rect(32+self.screenw/6 * x,32+self.screenh/8 * y,64,16) for x in range(6) for y in range(4)]

	def run(self):
		self.running = True
		while self.running:
			for event in pygame.event.get():
				if event.type == KEYDOWN:
					if event.type == K_ESCAPE:
						pygame.event.post(pygame.event.Event(QUIT))
				if event.type == MOUSEMOTION:
					self.mousePosition = event.pos[0]
					self.paddle.rect.x = self.mousePosition
				if event.type == QUIT:
					pygame.quit()
					sys.exit()

			self.tick()
			self.render()
			pygame.display.update()
			self.clock.tick(60)

	def tick(self):
		self.ball.update()
		if self.ball.rect.left <= self.lefte.right:
			self.ball.reverseX()
		elif self.ball.rect.right >= self.righte.left:
			self.ball.reverseX()
		if self.ball.rect.top <= self.tope.bottom:
			self.ball.reverseY()

		if self.ball.rect.bottom >= self.paddle.rect.top and self.ball.rect.bottom <= self.screenh and self.ball.rect.centerx < self.paddle.rect.right and self.ball.rect.centerx > self.paddle.rect.left:
			self.ball.reverseY()

		colindex = self.ball.rect.collidelist(self.blocks)
		if colindex != -1:
			self.ball.reverseY()
			self.blocks.pop(colindex)
			self.score += 100
		if self.ball.rect.top >= self.screenh:
			self.lives -= 1
			self.ball.reset(self.mousePosition+80)
		if self.lives <= 0:
			self.gameover()
		if len(self.blocks) <= 0:
			self.win()

	def render(self):
		self.screen.fill(BColors.white)
		bg = pygame.image.load("images/log.jpeg")
		bg = pygame.transform.scale(bg,(620,460))
		self.screen.blit(bg,(0,0))

		pygame.draw.rect(self.screen,BColors.black,self.tope)
		pygame.draw.rect(self.screen,BColors.black,self.lefte)
		pygame.draw.rect(self.screen,BColors.black,self.righte)
		pygame.draw.rect(self.screen,BColors.green,self.paddle.rect)
		pygame.draw.rect(self.screen,BColors.red,self.ball.rect)

		for blocks in self.blocks:
			pygame.draw.rect(self.screen,BColors.blue,blocks)

		source = self.font.render("Lives: %i Score: %i" % (self.lives , self.score), False , BColors.red)
		self.screen.blit(source,(16,16))

	def gameover(self):
		msurf = self.font.render("GAME OVER :-P",False,BColors.green)
		
		self.screen.blit(msurf,((self.screenw - msurf.get_width())/2,240))
		pygame.display.update()
		pygame.time.wait(2000)
		self.resetgame()

	def win(self):
		msurf = self.font.render("How do you do that",False,BColors.green)
		self.screen.blit(msurf,((self.screenw - msurf.get_width())/2,240))
		pygame.display.update()
		pygame.time.wait(2000)
		self.resetgame()

	def resetgame(self):
		self.lives = 1
		self.score = 0
		self.blocks = [pygame.Rect(32+self.screenw/6 * x,32+self.screenh/8 * y,64,16) for x in range(6) for y in range(4)]

game = Game()
game.run()