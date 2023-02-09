import app
import grp
import ui

class SpecialChat(ui.Window):
	def __init__(self, parent, x = 0, y = 0):
		ui.Window.__init__(self)
		self.texts = {}
		self.parent = parent
		self.SpaceBet = 14
		self.maxY = 0
		self.x = x
		self.y = y
		self.ColorValue = 0xFFff80b3
				
		self.lastlinetime = 0
		self.SetTop()
		
		self.showSpecialChat()
		

	def showSpecialChat(self):
		for i in xrange(len(self.texts)):
			self.texts[i].Show()
		self.Show()

	def OnRender(self):
		if len(self.texts) > 0:
			x, y = self.texts[0].GetGlobalPosition()
			w, h = self.texts[0].GetTextSize()
			grp.SetColor(grp.GenerateColor(0.0, 0.0, 0.0, 0.3))
			grp.RenderBar(x-2, y+h-12, 200, (h+2)*len(self.texts)+4)
			
	def AddSpecialChatLine(self, text):
		for i in xrange(len(self.texts)):
			if len(self.texts) == 6 and i == 0:
				self.texts[i].Hide()
			x, y = self.texts[i].GetLocalPosition()
			self.texts[i].SetPosition(x, y-self.SpaceBet)

		i = 0
		if len(self.texts) == 6:
			for i in xrange(len(self.texts)-1):
				self.texts[i] = self.texts[i+1]
			i = 5
		else:
			i = len(self.texts)
				
		self.texts[i] = ui.TextLine()
		self.texts[i].SetParent(self.parent)
		self.texts[i].SetPosition(self.x, self.y)
		self.texts[i].SetPackedFontColor(self.ColorValue)
		self.texts[i].SetHorizontalAlignLeft()
		self.texts[i].SetOutline(TRUE)
		self.texts[i].SetText(text)
		self.texts[i].Show()
		self.lastlinetime = app.GetTime()

	def ClearAll(self):
		self.Hide()
		self.texts = {}
					
	def OnUpdate(self):
		if len(self.texts) > 0:
			if app.GetTime() > self.lastlinetime + 6:
				self.texts = {}
				
