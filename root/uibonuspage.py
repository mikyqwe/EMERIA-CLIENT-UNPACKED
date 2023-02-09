#!/usr/bin/python
# -*- coding: latin-1 -*-
import ui
import chat
import app
import player
import snd
import item
import net

class BonusBoardDialog(ui.BoardWithTitleBar):
	MaxBoni = { "1": 16000, "2": 320, "3": 32, "4": 32, "5": 32, "6": 32, "7": 10, "9": 40, "10": 60, "11": 60, "12": 16, "13": 24, "14": 16, "15": 30, "16": 30, "17": 50, "18": 100, "19": 100, "20": 100, "21": 100, "22": 100, "23": 20, "24": 40, "27": 15, "28": 30, "29": 72, "30": 72, "31": 72, "32": 72, "33": 72, "34": 72, "35": 60, "36": 60, "37": 40, "38": 60, "39": 20, "41": 10, "43": 60, "44": 60, "45": 40, "48": 1, "53": 50 }
	BonusDict = ["PvP Bonus", "PvM Bonus", "Resistenze"]
	BonusIDListe = [["", 0, 0],["Max. HP", 1, 16000],["Max. MP", 2, 320],["Vitalità", 3, 32],["Intelligenza", 4, 32],["Forza", 5, 32],["Destrezza", 6, 32],["Resistenza", 7, 10],["Bewegungsgeschwindigkeit", 8, 0],["Velocità della magia", 9, 40],["Rigenerazione HP", 10, 32],["Rigenerazione MP", 11, 33],["Possibilità di avvelenamento", 12, 37],["Possibilità di svenimento", 13, 38],["Verlangsamungschance", 14, 39],["Colpi Critici", 15, 40],["Colpi Trafiggenti", 16, 41],["Forte contro Mezzuomini", 17, 43],["Forte contro animali", 18, 44],["Forte contro orchi", 19, 45],["Forte contro esoterici", 20, 46],["Forte contro zombie", 21, 47],["Forte contro diavolo", 22, 48],["Possibilità di Ass.HP", 23, 63],["Possibilità di Ass.MP", 24, 64],["Chance auf Manaraub", 25, 65],["Chance Rigenerazione MP", 26, 66],["Possibilità di blocco corporale", 27, 67],["Possibilità di schivare frecce", 28, 68],["Difesa Spada", 29, 69],["Difesa Spadone", 30, 70],["Difesa Pugnale", 31, 71],["Difesa Campana", 32, 72],["Difesa Ventaglio", 33, 73],["Resistenza freccia", 34, 74],["Feuerwiderstand", 35, 75],["Blitzwiderstand", 36, 76],["Resistenza Magia", 37, 77],["Windverteidigung", 38, 78],["Nahkampftreffer reflektieren", 39, 79],["Fluch reflektieren", 40, 80],["Giftverteidigung", 41, 81],["Chance MP wiederherzustellen", 42, 82],["Exp-Bonus", 43, 83],["Yang-Drop", 44, 84],["Item-Drop", 45, 85],["steigernde Trankwirkung", 46, 86],["Chance TP wiederherzustellen", 47, 87],["Difesa svenimento", 48, 88],["Immun gegen Verlangsamung", 49, 89],["Immun gegen Stürzen", 50, 90],["APPLY_SKILL", 51, 0],["Pfeilreichweite", 52, 95],["Valore d'attacco", 53, 0],["Verteidigungswert", 54, 96],["Magischer Valore d'attacco", 55, 97],["Magischer Verteidigungswert", 56, 98],["", 57, 0],["Max. Ausdauer", 58, 0],["Forte contro guerrieri", 59, 54],["Forte contro ninja", 60, 55],["Forte contro sura", 61, 56],["Forte contro shamano", 62, 57],["Forte contro mostri", 63, 53],["Itemshop Valore d'attacco", 64, 114],["Itemshop Verteidigungswert", 65, 115],["Itemshop Exp-Bonus", 66, 116],["Itemshop Item-Bonus", 67, 117],["Itemshop Yang-Bonus", 68, 118],["APPLY_MAX_HP_PCT", 69, 119],["APPLY_MAX_SP_PCT", 70, 120],["Danni abilità", 71, 121],["Danni medi", 72, 122],["Danni abilità Widerstand", 73, 123],["Danni mediswiderstand", 74, 124],["", 75, 0],["iCafe EXP-Bonus", 76, 125],["iCafe Item-Bonus", 77, 126],["Difesa contro guerrieri", 78, 59],["Difesa contro ninja", 79, 60],["Difesa contro sura", 80, 61],["Difesa contro shamani", 81, 62]]
	SpecialBoni = { 1: "Norm.State", 2: "Norm.State", 3: "Norm.State", 4: "Norm.State", 5: "Norm.State", 6: "Norm.State", 55: "Norm.State", 56: "Norm.State", 58: "Norm.State" }
	PvPOffenseBoni = ["Forte contro Mezzuomini", "Colpi Critici", "Colpi Trafiggenti", "Danni medi", "Danni abilità", "Vitalità", "Intelligenza", "Forza", "Destrezza", "Velocità della magia"]
	PvPDefenseBoni = ["Difesa Spada", "Difesa Spadone", "Difesa Pugnale", "Difesa Campana", "Difesa Ventaglio", "Resistenza freccia", "Possibilità di schivare frecce", "Resistenza Magia", "Possibilità di blocco corporale", "Difesa svenimento"]
	PvMOffenseBoni = ["Forte contro mostri", "Forte contro diavolo", "Forte contro zombie", "Forte contro animali", "Forte contro orchi", "Forte contro esoterici", "Possibilità di svenimento", "Possibilità di avvelenamento", "Resistenza", "Valore d'attacco"]
	PvMDefenseBoni = ["Max. HP", "Max. MP", "Possibilità di blocco corporale", "Rigenerazione HP", "Rigenerazione MP", "Possibilità di Ass.HP", "Possibilità di Ass.MP", "Exp-Bonus", "Yang-Drop", "Item-Drop"]
	LeftoversOffenseBoni = ["Forte contro guerrieri", "Forte contro ninja", "Forte contro sura", "Forte contro shamano"]
	LeftoversDefenseBoni = ["Difesa contro guerrieri", "Difesa contro ninja", "Difesa contro sura", "Difesa contro shamani", ]

	BonusList = []
	UI = []
	
	TestSystem = 0
	ProcessTimeStamp = 0
	
	def __init__(self):
		ui.BoardWithTitleBar.__init__(self)
		self.LoadUI()
		self.Show()
	
	def __del__(self):
		self.Hide()
		ui.BoardWithTitleBar.__del__(self)

	def LoadUI(self):
		self.AddFlag("movable")
		self.AddFlag("float")
		self.SetSize(313, 420)
		self.SetCenterPosition()
		self.SetTitleName("Emeria - Pagina Bonus")
		self.SetCloseEvent(self.Hide)
		self.Show()
		
		Vertical = ui.Line()
		Vertical.SetParent(self)
		Vertical.SetPosition(8, 60)
		Vertical.SetSize(297, 0)
		Vertical.SetColor(0xff777777)
		Vertical.Show()
		self.UI.append(Vertical)
		
		x = 25
		for i in xrange(3):
			ChangeBonusDict = ui.Button()
			ChangeBonusDict.SetParent(self)
			ChangeBonusDict.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
			ChangeBonusDict.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
			ChangeBonusDict.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
			ChangeBonusDict.SetText(self.BonusDict[i])
			ChangeBonusDict.SetPosition(x, 380)
			ChangeBonusDict.SetEvent(lambda arg = ChangeBonusDict.GetText(): self.ChangeBonusDict(arg))
			ChangeBonusDict.Show()
			x += 88
			self.UI.append(ChangeBonusDict)
		
		x = 55
		Type = ["Offensivo", "Difensivo"]
		for i in xrange(2):
			BonusDescription = ui.TextLine()
			BonusDescription.SetParent(self)
			BonusDescription.SetPosition(x, 35)
			BonusDescription.SetText(str(Type[i]))
			BonusDescription.SetFontColor(1.0, 0.63, 0)
			BonusDescription.Show()			
			x += 150
			self.UI.append(BonusDescription)

		self.SetBoni(self.BonusDict[0])
		self.dict = self.BonusDict[0]
		
	def SetBoni(self, type):
		Offense = [[25, 70], [25, 100], [25, 130], [25, 160], [25, 190], [25, 220], [25, 250], [25, 280], [25, 310], [25, 340]]
		Defense = [[170, 70], [170, 100], [170, 130], [170, 160], [170, 190], [170, 220], [170, 250], [170, 280], [170, 310], [170, 340]]
		for bonus in self.BonusIDListe:
			if type == self.BonusDict[0]:
				self.CheckBonus(bonus, self.PvPOffenseBoni, Offense)
				self.CheckBonus(bonus, self.PvPDefenseBoni, Defense)
			elif type == self.BonusDict[1]:
				self.CheckBonus(bonus, self.PvMOffenseBoni, Offense)
				self.CheckBonus(bonus, self.PvMDefenseBoni, Defense)
			elif type == self.BonusDict[2]:
				self.CheckBonus(bonus, self.LeftoversOffenseBoni, Offense)
				self.CheckBonus(bonus, self.LeftoversDefenseBoni, Defense)
			else:
				return
				
	def CheckBonus(self, bonus, bonuslist, offset):
		for boni in bonuslist:
			if bonus[0] == boni:
				try:
					Index = bonuslist.index(boni)
					BonusDescription = ui.TextLine()
					BonusDescription.SetParent(self)
					BonusDescription.SetPosition(offset[Index][0], offset[Index][1])
					BonusDescription.SetText(str(bonus[0]))
					BonusDescription.Show()
					
					BonusSlotBar = ui.SlotBar()
					BonusSlotBar.SetParent(self)
					BonusSlotBar.SetSize(115, 15)
					BonusSlotBar.SetPosition(offset[Index][0], offset[Index][1] + 15)
					BonusSlotBar.Show()
					
					BonusAttrLine = ui.TextLine()
					BonusAttrLine.SetParent(self)
					BonusAttrLine.SetPosition(offset[Index][0] + 5, offset[Index][1] + 15)
					
					try:
						Type = self.SpecialBoni[bonus[1]]
						Attribute = self.EquipAttribute(bonus)
					except:
						Attribute = player.GetStatus(int(bonus[2]))
					if self.TestSystem != 1:
						BonusAttrLine.SetText(str(Attribute))
						try:
							if int(Attribute) >= int(self.MaxBoni[str(bonus[1])]):
								BonusAttrLine.SetFontColor(1.0, 0.63, 0)
							else:
								BonusAttrLine.SetFontColor(1, 1, 1)
						except:
							BonusAttrLine.SetFontColor(1, 1, 1)
					else:
						BonusAttrLine.SetText("Test system is active")
						BonusAttrLine.SetFontColor(0.1, 0.7, 1.0)
					
					BonusAttrLine.Show()
					self.BonusList.append([BonusDescription, BonusAttrLine, BonusSlotBar])
				except:
					pass		
				
	def EquipAttribute(self, bonus):
		value = 0
		for slot in xrange(90, 101):
			for attr in xrange(0, 7):
				attr, val = player.GetItemAttribute(slot, attr)
				if int(attr) == bonus[1]:
					value += int(val)
		return int(value)

	def ChangeBonusDict(self, dict):
		self.dict = dict
		for bonus in self.BonusList:
			try:
				for array in bonus:
					array.Hide()
			except:
				pass			
		self.SetBoni(dict)
		
	def OnUpdate(self):
		import item
		if int(app.GetTime()) > int(self.ProcessTimeStamp) + 6:
			self.SetBoni(self.dict)
			self.ProcessTimeStamp = app.GetTime()
			
			