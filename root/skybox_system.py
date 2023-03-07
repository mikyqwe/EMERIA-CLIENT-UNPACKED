import ui
import dbg
import app
import background
import constInfo

class MentaLGui(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.BuildWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def BuildWindow(self):
		self.Board = ui.BoardWithTitleBar()
		self.Board.SetSize(170, 302)
		self.Board.SetCenterPosition()
		self.Board.AddFlag('movable')
		self.Board.AddFlag('float')
		self.Board.SetTitleName('Skybox')
		self.Board.SetCloseEvent(self.Close)
		self.Board.Hide()
		self.comp = Component()

		self.cielo_ab = self.comp.Button(self.Board, 'Sereno', '', 38, 57, self.cielo_a, 'd:/ymir work/ui/public/large_button_01.sub', 'd:/ymir work/ui/public/large_button_02.sub', 'd:/ymir work/ui/public/large_button_03.sub')
		self.cielo_bc = self.comp.Button(self.Board, 'Rosso di Sera', '', 38, 89, self.cielo_b, 'd:/ymir work/ui/public/large_button_01.sub', 'd:/ymir work/ui/public/large_button_02.sub', 'd:/ymir work/ui/public/large_button_03.sub')
		self.cielo_cd = self.comp.Button(self.Board, 'Penombra', '', 38, 122, self.cielo_c, 'd:/ymir work/ui/public/large_button_01.sub', 'd:/ymir work/ui/public/large_button_02.sub', 'd:/ymir work/ui/public/large_button_03.sub')
		self.cielo_ef = self.comp.Button(self.Board, 'Grotta', '', 38, 152, self.cielo_d, 'd:/ymir work/ui/public/large_button_01.sub', 'd:/ymir work/ui/public/large_button_02.sub', 'd:/ymir work/ui/public/large_button_03.sub')
		self.cielo_il = self.comp.Button(self.Board, 'Mistico', '', 38, 182, self.cielo_f, 'd:/ymir work/ui/public/large_button_01.sub', 'd:/ymir work/ui/public/large_button_02.sub', 'd:/ymir work/ui/public/large_button_03.sub')
		self.cielo_mn = self.comp.Button(self.Board, 'Nuvoloso', '', 38, 212, self.cielo_g, 'd:/ymir work/ui/public/large_button_01.sub', 'd:/ymir work/ui/public/large_button_02.sub', 'd:/ymir work/ui/public/large_button_03.sub')
		self.cielo_op = self.comp.Button(self.Board, 'Sunshine', '', 38, 242, self.cielo_h, 'd:/ymir work/ui/public/large_button_01.sub', 'd:/ymir work/ui/public/large_button_02.sub', 'd:/ymir work/ui/public/large_button_03.sub')
		self.cielo_qh = self.comp.Button(self.Board, 'Default', '', 38, 272, self.cielo_q, 'd:/ymir work/ui/public/large_button_01.sub', 'd:/ymir work/ui/public/large_button_02.sub', 'd:/ymir work/ui/public/large_button_03.sub')
		self.testo = self.comp.TextLine(self.Board, 'Selecta�i Skybox:', 38, 35, self.comp.RGB(255, 255, 255))
	
	def cielo_a(self):
		background.RegisterEnvironmentData(0, "d:/ymir work/environment/ridacksky5.msenv")
		background.SetEnvironmentData(0)
	
	def cielo_b(self):
		background.RegisterEnvironmentData(1, "d:/ymir work/environment/map_n_flame_01.msenv")
		background.SetEnvironmentData(1)
	
	def cielo_c(self):
		background.RegisterEnvironmentData(2, "d:/ymir work/environment/snowm02.msenv")
		background.SetEnvironmentData(2)
		
	def cielo_d(self):
		background.RegisterEnvironmentData(3, "d:/ymir work/environment/nephrite_cave.msenv")
		background.SetEnvironmentData(3)
		
	def cielo_f(self):
		background.RegisterEnvironmentData(4, "d:/ymir work/environment/moon_cave.msenv")
		background.SetEnvironmentData(4)
		
	def cielo_g(self):
		background.RegisterEnvironmentData(5, "d:/ymir work/environment/storm.msenv")
		background.SetEnvironmentData(5)
		
	def cielo_h(self):
		background.RegisterEnvironmentData(6, "d:/ymir work/environment/ridacksky18.msenv")
		background.SetEnvironmentData(6)
		
	def cielo_q(self):
		background.RegisterEnvironmentData(6, "d:/ymir work/environment/battle_guild01.msenv")
		background.SetEnvironmentData(6)
		
	def Close(self):
		self.Board.Hide()
		constInfo.SKYBOX_GUI = 0
		
	def OpenWindow(self):
		if not self.Board.IsShow():
			self.Board.Show()
			
	def OnPressEscapeKey(self):
		self.Board.Close()
		
class Component:
	def Button(self, parent, buttonName, tooltipText, x, y, func, UpVisual, OverVisual, DownVisual):
		button = ui.Button()
		if parent != None:
			button.SetParent(parent)
		button.SetPosition(x, y)
		button.SetUpVisual(UpVisual)
		button.SetOverVisual(OverVisual)
		button.SetDownVisual(DownVisual)
		button.SetText(buttonName)
		button.SetToolTipText(tooltipText)
		button.Show()
		button.SetEvent(func)
		return button

	def ToggleButton(self, parent, buttonName, tooltipText, x, y, funcUp, funcDown, UpVisual, OverVisual, DownVisual):
		button = ui.ToggleButton()
		if parent != None:
			button.SetParent(parent)
		button.SetPosition(x, y)
		button.SetUpVisual(UpVisual)
		button.SetOverVisual(OverVisual)
		button.SetDownVisual(DownVisual)
		button.SetText(buttonName)
		button.SetToolTipText(tooltipText)
		button.Show()
		button.SetToggleUpEvent(funcUp)
		button.SetToggleDownEvent(funcDown)
		return button

	def EditLine(self, parent, editlineText, x, y, width, heigh, max):
		SlotBar = ui.SlotBar()
		if parent != None:
			SlotBar.SetParent(parent)
		SlotBar.SetSize(width, heigh)
		SlotBar.SetPosition(x, y)
		SlotBar.Show()
		Value = ui.EditLine()
		Value.SetParent(SlotBar)
		Value.SetSize(width, heigh)
		Value.SetPosition(1, 1)
		Value.SetMax(max)
		Value.SetLimitWidth(width)
		Value.SetMultiLine()
		Value.SetText(editlineText)
		Value.Show()
		return SlotBar, Value

	def TextLine(self, parent, textlineText, x, y, color):
		textline = ui.TextLine()
		if parent != None:
			textline.SetParent(parent)
		textline.SetPosition(x, y)
		if color != None:
			textline.SetFontColor(color[0], color[1], color[2])
		textline.SetText(textlineText)
		textline.Show()
		return textline

	def RGB(self, r, g, b):
		return (r*255, g*255, b*255)

	def SliderBar(self, parent, sliderPos, func, x, y):
		Slider = ui.SliderBar()
		if parent != None:
			Slider.SetParent(parent)
		Slider.SetPosition(x, y)
		Slider.SetSliderPos(sliderPos / 100)
		Slider.Show()
		Slider.SetEvent(func)
		return Slider

	def ExpandedImage(self, parent, x, y, img):
		image = ui.ExpandedImageBox()
		if parent != None:
			image.SetParent(parent)
		image.SetPosition(x, y)
		image.LoadImage(img)
		image.Show()
		return image

	def ComboBox(self, parent, text, x, y, width):
		combo = ui.ComboBox()
		if parent != None:
			combo.SetParent(parent)
		combo.SetPosition(x, y)
		combo.SetSize(width, 15)
		combo.SetCurrentItem(text)
		combo.Show()
		return combo

	def ThinBoard(self, parent, moveable, x, y, width, heigh, center):
		thin = ui.ThinBoard()
		if parent != None:
			thin.SetParent(parent)
		if moveable == TRUE:
			thin.AddFlag('movable')
			thin.AddFlag('float')
		thin.SetSize(width, heigh)
		thin.SetPosition(x, y)
		if center == TRUE:
			thin.SetCenterPosition()
		thin.Show()
		return thin

	def Gauge(self, parent, width, color, x, y):
		gauge = ui.Gauge()
		if parent != None:
			gauge.SetParent(parent)
		gauge.SetPosition(x, y)
		gauge.MakeGauge(width, color)
		gauge.Show()
		return gauge

	def ListBoxEx(self, parent, x, y, width, heigh):
		bar = ui.Bar()
		if parent != None:
			bar.SetParent(parent)
		bar.SetPosition(x, y)
		bar.SetSize(width, heigh)
		bar.SetColor(0x77000000)
		bar.Show()
		ListBox=ui.ListBoxEx()
		ListBox.SetParent(bar)
		ListBox.SetPosition(0, 0)
		ListBox.SetSize(width, heigh)
		ListBox.Show()
		scroll = ui.ScrollBar()
		scroll.SetParent(ListBox)
		scroll.SetPosition(width-15, 0)
		scroll.SetScrollBarSize(heigh)
		scroll.Show()
		ListBox.SetScrollBar(scroll)
		return bar, ListBox
