import ui
import dbg
import app
import wndMgr
import localeInfo
import game
import grp
import component

TITLE_COLOR = grp.GenerateColor(0.9490, 0.9058, 0.7568, 1.0)
SPECIAL_TITLE_COLOR = grp.GenerateColor(1.0, 0.7843, 0.0, 1.0)
NORMAL_COLOR = grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0)

class PopupMsg(ui.Window):
	def __init__(self):
		ui.Window.__init__(self)
		self.BuildWindow()

	def __del__(self):
		ui.Window.__del__(self)

	def BuildWindow(self):
		self.Board = ui.ThinBoard()
		self.Board.SetSize(300, 50)
		self.Board.SetPosition(wndMgr.GetScreenWidth()-310, wndMgr.GetScreenHeight() - 90)
		self.Board.Show()
		self.comp = component.Component()
		
		self.text_title = self.comp.LargeTextLine(self.Board, "Un amico e' ONLINE!", 45, 8, SPECIAL_TITLE_COLOR)
		self.textline = self.comp.TextLine(self.Board, "Prietenul tau xBooK este acum ONLINE !", 45, 25, self.comp.RGB(255, 255, 255))
		
		#self.textline = ui.TextLine()
		#self.textline.SetParent(self.Board)
		#self.textline.SetPosition(15, 15)
		#self.textline.SetFontName(locale.UI_DEF_FONT_LARGE)
		#self.textline.SetText("")
		#self.textline.Show()
		
		self.WarteSchleife = game.WaitingDialog()
		self.WarteSchleife.Open(3.0)
		self.WarteSchleife.SAFE_SetTimeOverEvent(self.Close)
	
	def OpenWindow(self):
		if self.Board.IsShow():
			self.Board.Hide()
		else:
			self.Board.Show()
	
	def Close(self):
		self.Board.Hide()
		
	def SetMsg(self, arg):
		self.textline.SetText(arg.replace("_"," "))
		
	def SetType(self, type, add = ""):
		if type == 1:
			self.text_title.SetText("Un amico e' ONLINE!")
		elif type == 2:
			self.text_title.SetText("Cercetarea biologilor")
			self.img = self.comp.ExpandedImage(self.Board, 8, 8, 'icon\\item\\%s.tga'%str(add))
		elif type == 3:
			self.text_title.SetText("Un amico e' ONLINE!")
			self.img = self.comp.ExpandedImage(self.Board, 8, 8, 'pet_button.tga')
		elif type == 4:
			self.text_title.SetText("Fabricarea articolului")
			self.img = self.comp.ExpandedImage(self.Board, 8, 8, 'icon\\item\\%s.tga'%str(add))
