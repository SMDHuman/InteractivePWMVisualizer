import pygame


def rotate(p, angle):
	angle = math.radians(angle)
	xr = p[0]*math.cos(angle) - p[1]*math.sin(angle)
	yr = p[0]*math.sin(angle) + p[1]*math.cos(angle)
	return ((xr,yr))

def interpolation(d, t):
	return (d[1] - d[0])*t + d[0] 

def bezierCurvePoint(p0, p1, p2, t):
	p01 = [interpolation([p0[0], p1[0]], t), interpolation([p0[1], p1[1]], t)]
	p12 = [interpolation([p1[0], p2[0]], t), interpolation([p1[1], p2[1]], t)]
	x, y= interpolation([p01[0], p12[0]], t), interpolation([p01[1], p12[1]], t)
	return [x, y]

class App():
	def __init__(self):
		pygame.init()
		pygame.font.init()
		self.winX, self.winY = 800, 600
		self.win = pygame.display.set_mode((self.winX, self.winY), pygame.RESIZABLE)
		self.keep = 1

		self.mousePos = (0, 0)
		self.mouseDown = []
		self.mouseScroll = 0
		self.keyDown = []


		self.xGap = 40
		self.yGap = 60

		self.sliderARect = pygame.Rect(0, 0, self.xGap-10, self.yGap-20)
		self.sliderBRect = pygame.Rect(0, 0, self.xGap-10, self.yGap-20)

		self.sliderAValue = 0.5
		self.sliderBValue = 0.5
		self.sliderARealValue = 0.5
		self.sliderBRealValue = 0.5

		self.sliderAMoveEnable = 0
		self.sliderBMoveEnable = 0

		self.sliderAStep = 200
		self.sliderBStep = 100

		self.textFont = pygame.font.SysFont("arial", 32)

	def checkEvents(self, events):
		self.mouseRel = (0, 0)
		self.mouseScroll = 0
		self.mousePressed = 0
		self.mouseReleased = 0
		self.keyPressed = 0
		self.keyReleased = 0
		for event in events:
			match event.type:
				case pygame.QUIT:
					self.keep = 0

				case pygame.VIDEORESIZE:
					self.winX, self.winY = event.w, event.h

				case pygame.MOUSEMOTION:
					self.mousePos = event.pos
					self.mouseRel = event.rel
	
				case pygame.MOUSEBUTTONDOWN:
					self.mousePressed = 1
					self.mouseDown.append(event.button)
					match event.button:
						case 4:
							self.mouseScroll = 1 
						case 5:
							self.mouseScroll = -1

				case pygame.MOUSEBUTTONUP:
					self.mouseReleased = 1
					self.mouseDown.remove(event.button)

				case pygame.KEYDOWN:
					self.keyPressed = 1
					self.keyDown.append(event.key)

				case pygame.KEYUP:
					self.keyPressed = -1
					self.keyDown.remove(event.key)

	def renderDemo(self):
		events = pygame.event.get()
		self.checkEvents(events)

		self.win.fill((40, 40, 40))

		self.drawSliders()

		self.drawPWMSignal()

		surf = self.textFont.render(f"< - - - - - - - Frequency : {self.freq} - - - - - - - >", 1, "White")
		self.win.blit(surf, pygame.Rect(self.pwmPos[0] + self.pwmWidth/2 - surf.get_width()/2, self.pwmPos[1] + self.pwmHeight + 20, 0, 0))
		
		surf = self.textFont.render("PWM Signal", 1, "red")
		self.win.blit(surf, pygame.Rect(self.pwmPos[0] + self.pwmWidth/2 - surf.get_width()/2, self.pwmPos[1] - 100, 0, 0))
		
		surf = self.textFont.render(f"Duty : {round((1 - self.sliderBValue) * 65535)}", 1, "White")
		self.win.blit(surf, pygame.Rect(self.pwmPos[0] + self.pwmWidth/2 - surf.get_width()/2, self.pwmPos[1] + self.pwmHeight + 70, 0, 0))

		pygame.display.update()

	def drawPWMSignal(self):
		self.pwmWidth = self.winX - 170
		self.pwmHeight = 150
		self.pwmPos = (10, (self.winY - self.pwmHeight)/2)

		pwmValue = 1 
		minFreq = 1
		for x in range(self.sliderAStep * minFreq):
			a = round((self.sliderAValue*self.sliderAStep+1))
			self.freq = round(self.sliderAStep * minFreq / a)
			if(x % a >= a * self.sliderBValue):
				pwmValue = 1
			else:
				pwmValue = 0

			currentPos = (self.pwmPos[0] + round(x * self.pwmWidth / (self.sliderAStep * minFreq)), self.pwmPos[1] + self.pwmHeight*(1-pwmValue))

			if(x == 0):
				oldPos = currentPos
				continue
			pygame.draw.line(self.win, "red", oldPos, currentPos, 2)
			oldPos = currentPos

			if(0):
				time.sleep(0.01)
				pygame.display.update()



	def drawSliders(self):
		pygame.draw.line(self.win, "white",(self.winX-self.xGap, self.yGap), (self.winX-self.xGap, self.winY -self.yGap))
		pygame.draw.line(self.win, "white",(self.winX-self.xGap*3, self.yGap), (self.winX-self.xGap*3, self.winY -self.yGap))

		self.sliderLength = self.winY - self.yGap*2

		self.sliderARect.center = (self.winX-self.xGap, self.yGap + self.sliderLength*self.sliderAValue)
		pygame.draw.rect(self.win, "Orange", self.sliderARect)

		self.sliderBRect.center = (self.winX-self.xGap*3, self.yGap + self.sliderLength*self.sliderBValue)
		pygame.draw.rect(self.win, "Orange", self.sliderBRect)


		if(1 in self.mouseDown and self.mousePressed):
			if(self.sliderARect.collidepoint(self.mousePos)):
				self.sliderAMoveEnable = 1
			if(self.sliderBRect.collidepoint(self.mousePos)):
				self.sliderBMoveEnable = 1

		if(self.mouseReleased):
			self.sliderAMoveEnable = 0
			self.sliderBMoveEnable = 0

		if(self.sliderAMoveEnable):
			self.sliderARealValue += self.mouseRel[1] / self.sliderLength
			self.sliderARealValue = max(min(self.sliderARealValue, 1), 0)
			self.sliderAValue = round(self.sliderAStep * self.sliderARealValue) / self.sliderAStep
		if(self.sliderBMoveEnable):
			self.sliderBRealValue += self.mouseRel[1] / self.sliderLength
			self.sliderBRealValue = max(min(self.sliderBRealValue, 1), 0)
			self.sliderBValue = round(self.sliderBStep * self.sliderBRealValue) / self.sliderBStep

	def run(self):
		while(self.keep):
			self.renderDemo()

		# Closing program
		pygame.quit()
		exit()


if(__name__ == "__main__"):
	App().run()
	