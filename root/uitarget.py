import app
import ui
import player
import net
import wndMgr
import uitooltip
import item
import messenger
import guild
import chr
import chrmgr
import nonplayer
import localeInfo
import constInfo
if app.ENABLE_DECORUM:
	import chat

if app.ENABLE_VIEW_ELEMENT:
	ELEMENT_IMAGE_DIC = {1: "elect", 2: "fire", 3: "ice", 4: "wind", 5: "earth", 6 : "dark"}

if app.ENABLE_SEND_TARGET_INFO:
	def HAS_FLAG(value, flag):
		return (value & flag) == flag

class TargetBoard(ui.ThinBoard):

	if app.ENABLE_SEND_TARGET_INFO:
		class InfoBoard(ui.ThinBoard):
			class ItemListBoxItem(ui.ListBoxExNew.Item):
				def __init__(self, width):
					ui.ListBoxExNew.Item.__init__(self)

					image = ui.ExpandedImageBox()
					image.SetParent(self)
					image.Show()
					self.image = image

					nameLine = ui.TextLine()
					nameLine.SetParent(self)
					nameLine.SetPosition(32 + 5, 0)
					nameLine.Show()
					self.nameLine = nameLine
					if app.ENABLE_SEND_TARGET_INFO_EXTENDED:
						rarity = ui.TextLine()
						rarity.SetParent(self)
						rarity.SetPosition(32 + 5, 11)
						rarity.Show()
						self.rarity = rarity
					self.SetSize(width, 32 + 5)

				def LoadImage(self, image, name = None):
					self.image.LoadImage(image)
					self.SetSize(self.GetWidth(), self.image.GetHeight() + 5 * (self.image.GetHeight() / 32))
					if name != None:
						self.SetText(name)

				def SetText(self, text):
					self.nameLine.SetText(text)

				if app.ENABLE_SEND_TARGET_INFO_EXTENDED:
					def SetRarity(self, rarity):
						if rarity <= 0:
							return

						real_rarity = rarity / 10000
						self.rarity.SetText(str(self.GetRarity(real_rarity)))

					def GetRarity(self, rarity):
						if rarity >= 100:
							return "|cFFFFFFFFGarantat|r"
						elif rarity < 100 and rarity >= 70:
							return "|cFFFFF432Comun|r"
						elif rarity < 70 and rarity >= 50:
							return "|cFF32CD32Normal|r"
						elif rarity < 50 and rarity >= 30:
							return "|cFF9400D3Mitic|r"
						elif rarity < 30 and rarity >= 12:
							return "|cFF1E90FFRar|r"
						elif rarity <= 11:
							return "|cFFFFD700Legendar|r"
							
						return ""

				def RefreshHeight(self):
					ui.ListBoxExNew.Item.RefreshHeight(self)
					self.image.SetRenderingRect(0.0, 0.0 - float(self.removeTop) / float(self.GetHeight()), 0.0, 0.0 - float(self.removeBottom) / float(self.GetHeight()))
					self.image.SetPosition(0, - self.removeTop)

			MAX_ITEM_COUNT = 5

			EXP_BASE_LVDELTA = [
				1,  #  -15 0
				5,  #  -14 1
				10, #  -13 2
				20, #  -12 3
				30, #  -11 4
				50, #  -10 5
				70, #  -9  6
				80, #  -8  7
				85, #  -7  8
				90, #  -6  9
				92, #  -5  10
				94, #  -4  11
				96, #  -3  12
				98, #  -2  13
				100,	#  -1  14
				100,	#  0   15
				105,	#  1   16
				110,	#  2   17
				115,	#  3   18
				120,	#  4   19
				125,	#  5   20
				130,	#  6   21
				135,	#  7   22
				140,	#  8   23
				145,	#  9   24
				150,	#  10  25
				155,	#  11  26
				160,	#  12  27
				165,	#  13  28
				170,	#  14  29
				180,	#  15  30
			]

			RACE_FLAG_TO_NAME = {
				1 << 0  : localeInfo.TARGET_INFO_RACE_ANIMAL,
				1 << 1 	: localeInfo.TARGET_INFO_RACE_UNDEAD,
				1 << 2  : localeInfo.TARGET_INFO_RACE_DEVIL,
				1 << 3  : localeInfo.TARGET_INFO_RACE_HUMAN,
				1 << 4  : localeInfo.TARGET_INFO_RACE_ORC,
				1 << 5  : localeInfo.TARGET_INFO_RACE_MILGYO,
			}

			SUB_RACE_FLAG_TO_NAME = {
				1 << 11 : localeInfo.TARGET_INFO_RACE_ELEC,
				1 << 12 : localeInfo.TARGET_INFO_RACE_FIRE,
				1 << 13 : localeInfo.TARGET_INFO_RACE_ICE,
				1 << 14 : localeInfo.TARGET_INFO_RACE_WIND,
				1 << 15 : localeInfo.TARGET_INFO_RACE_EARTH,
				1 << 16 : localeInfo.TARGET_INFO_RACE_DARK,
			}

			STONE_START_VNUM = 28030
			STONE_LAST_VNUM = 28042

			BOARD_WIDTH = 250

			def __init__(self):
				ui.ThinBoard.__init__(self)

				self.HideCorners(self.LT)
				self.HideCorners(self.RT)
				self.HideLine(self.T)

				self.race = 0
				self.hasItems = False

				self.itemTooltip = uitooltip.ItemToolTip()
				self.itemTooltip.HideToolTip()

				self.stoneImg = None
				self.stoneVnum = None
				self.lastStoneVnum = 0
				self.nextStoneIconChange = 0

				self.SetSize(self.BOARD_WIDTH, 0)

			def __del__(self):
				ui.ThinBoard.__del__(self)

			def __UpdatePosition(self, targetBoard):
				self.SetPosition(targetBoard.GetLeft() + (targetBoard.GetWidth() - self.GetWidth()) / 2, targetBoard.GetBottom() - 17)

			def Open(self, targetBoard, race):
				self.__LoadInformation(race)

				self.SetSize(self.BOARD_WIDTH, self.yPos + 10)
				self.__UpdatePosition(targetBoard)

				self.Show()

			def Refresh(self):
				self.__LoadInformation(self.race)
				self.SetSize(self.BOARD_WIDTH, self.yPos + 10)

			def Close(self):
				self.itemTooltip.HideToolTip()
				self.Hide()

			def __LoadInformation(self, race):
				self.yPos = 7
				self.children = []
				self.race = race
				self.stoneImg = None
				self.stoneVnum = None
				self.nextStoneIconChange = 0

				self.__LoadInformation_Default(race)
				self.__LoadInformation_Race(race)
				self.__LoadInformation_Drops(race)

			def __LoadInformation_Default_GetHitRate(self, race):
				attacker_dx = nonplayer.GetMonsterDX(race)
				attacker_level = nonplayer.GetMonsterLevel(race)

				self_dx = player.GetStatus(player.DX)
				self_level = player.GetStatus(player.LEVEL)

				iARSrc = min(90, (attacker_dx * 4 + attacker_level * 2) / 6)
				iERSrc = min(90, (self_dx * 4 + self_level * 2) / 6)

				fAR = (float(iARSrc) + 210.0) / 300.0
				fER = (float(iERSrc) * 2 + 5) / (float(iERSrc) + 95) * 3.0 / 10.0

				return fAR - fER

			def __LoadInformation_Default(self, race):
				self.AppendSeperator()
				self.AppendTextLine(localeInfo.TARGET_INFO_MAX_HP % str(nonplayer.GetMonsterMaxHP(race)))

				# calc att damage
				monsterLevel = nonplayer.GetMonsterLevel(race)
				fHitRate = self.__LoadInformation_Default_GetHitRate(race)
				iDamMin, iDamMax = nonplayer.GetMonsterDamage(race)
				iDamMin = int((iDamMin + nonplayer.GetMonsterST(race)) * 2 * fHitRate) + monsterLevel * 2
				iDamMax = int((iDamMax + nonplayer.GetMonsterST(race)) * 2 * fHitRate) + monsterLevel * 2
				iDef = player.GetStatus(player.DEF_GRADE) * (100 + player.GetStatus(player.DEF_BONUS)) / 100
				fDamMulti = nonplayer.GetMonsterDamageMultiply(race)
				iDamMin = int(max(0, iDamMin - iDef) * fDamMulti)
				iDamMax = int(max(0, iDamMax - iDef) * fDamMulti)
				if iDamMin < 1:
					iDamMin = 1
				if iDamMax < 5:
					iDamMax = 5
				self.AppendTextLine(localeInfo.TARGET_INFO_DAMAGE % (str(iDamMin), str(iDamMax)))

				idx = min(len(self.EXP_BASE_LVDELTA) - 1, max(0, (monsterLevel + 15) - player.GetStatus(player.LEVEL)))
				iExp = nonplayer.GetMonsterExp(race) * self.EXP_BASE_LVDELTA[idx] / 100
				self.AppendTextLine(localeInfo.TARGET_INFO_EXP % str(iExp))

			def __LoadInformation_Race(self, race):
				dwRaceFlag = nonplayer.GetMonsterRaceFlag(race)
				self.AppendSeperator()

				mainrace = ""
				subrace = ""
				for i in xrange(17):
					curFlag = 1 << i
					if HAS_FLAG(dwRaceFlag, curFlag):
						if self.RACE_FLAG_TO_NAME.has_key(curFlag):
							mainrace += self.RACE_FLAG_TO_NAME[curFlag] + ", "
						elif self.SUB_RACE_FLAG_TO_NAME.has_key(curFlag):
							if constInfo.Element_ID == 1:
								subrace += localeInfo.TARGET_INFO_RACE_ELEC + ", "
							elif constInfo.Element_ID == 2:
								subrace += localeInfo.TARGET_INFO_RACE_FIRE + ", "
							elif constInfo.Element_ID == 3:
								subrace += localeInfo.TARGET_INFO_RACE_ICE + ", "
							elif constInfo.Element_ID == 4:
								subrace += localeInfo.TARGET_INFO_RACE_WIND + ", "
							elif constInfo.Element_ID == 5:
								subrace += localeInfo.TARGET_INFO_RACE_EARTH + ", "
							elif constInfo.Element_ID == 6:
								subrace += localeInfo.TARGET_INFO_RACE_DARK + ", "
				if nonplayer.IsMonsterStone(race):
					mainrace += localeInfo.TARGET_INFO_RACE_METIN + ", "
				if mainrace == "":
					mainrace = localeInfo.TARGET_INFO_NO_RACE
				else:
					mainrace = mainrace[:-2]
				if subrace == "":
					subrace = localeInfo.TARGET_INFO_NO_RACE
				else:
					subrace = subrace[:-2]

				self.AppendTextLine(localeInfo.TARGET_INFO_MAINRACE % mainrace)
				self.AppendTextLine(localeInfo.TARGET_INFO_SUBRACE % subrace)

			def __LoadInformation_Drops(self, race):
				self.AppendSeperator()

				if race in constInfo.MONSTER_INFO_DATA:
					if len(constInfo.MONSTER_INFO_DATA[race]["items"]) == 0:
						self.AppendTextLine(localeInfo.TARGET_INFO_NO_ITEM_TEXT)
					else:
						itemListBox = ui.ListBoxExNew(32 + 5, self.MAX_ITEM_COUNT)
						itemListBox.SetSize(self.GetWidth() - 15 * 2 - ui.ScrollBar.SCROLLBAR_WIDTH, (32 + 5) * self.MAX_ITEM_COUNT)
						height = 0
						for curItem in constInfo.MONSTER_INFO_DATA[race]["items"]:
							if curItem.has_key("vnum_list"):
								height += self.AppendItem(itemListBox, curItem["vnum_list"], curItem["count"], curItem["rarity"])
							else:
								height += self.AppendItem(itemListBox, curItem["vnum"], curItem["count"], curItem["rarity"])
						if height < itemListBox.GetHeight():
							itemListBox.SetSize(itemListBox.GetWidth(), height)
						self.AppendWindow(itemListBox, 15)
						itemListBox.SetBasePos(0)

						if len(constInfo.MONSTER_INFO_DATA[race]["items"]) > itemListBox.GetViewItemCount():
							itemScrollBar = ui.ScrollBar()
							itemScrollBar.SetParent(self)
							itemScrollBar.SetPosition(itemListBox.GetRight(), itemListBox.GetTop())
							itemScrollBar.SetScrollBarSize(32 * self.MAX_ITEM_COUNT + 5 * (self.MAX_ITEM_COUNT - 1))
							itemScrollBar.SetMiddleBarSize(float(self.MAX_ITEM_COUNT) / float(height / (32 + 5)))
							itemScrollBar.Show()
							itemListBox.SetScrollBar(itemScrollBar)
				else:
					self.AppendTextLine(localeInfo.TARGET_INFO_NO_ITEM_TEXT)

			def AppendTextLine(self, text):
				textLine = ui.TextLine()
				textLine.SetParent(self)
				textLine.SetWindowHorizontalAlignCenter()
				textLine.SetHorizontalAlignCenter()
				textLine.SetText(text)
				textLine.SetPosition(0, self.yPos)
				textLine.Show()

				self.children.append(textLine)
				self.yPos += 17

			def AppendSeperator(self):
				img = ui.ImageBox()
				img.LoadImage("d:/ymir work/ui/seperator.tga")
				self.AppendWindow(img)
				img.SetPosition(img.GetLeft(), img.GetTop() - 15)
				self.yPos -= 15

			def AppendItem(self, listBox, vnums, count, rarity = 0):
				if type(vnums) == int:
					vnum = vnums
				else:
					vnum = vnums[0]

				item.SelectItem(vnum)
				itemName = item.GetItemName()
				if type(vnums) != int and len(vnums) > 1:
					vnums = sorted(vnums)
					realName = itemName[:itemName.find("+")]
					if item.GetItemType() == item.ITEM_TYPE_METIN:
						realName = localeInfo.TARGET_INFO_STONE_NAME
						itemName = realName + "+0 - +4"
					else:
						itemName = realName + "+" + str(vnums[0] % 10) + " - +" + str(vnums[len(vnums) - 1] % 10)
					vnum = vnums[len(vnums) - 1]

				myItem = self.ItemListBoxItem(listBox.GetWidth())
				myItem.LoadImage(item.GetIconImageFileName())
				if count <= 1:
					myItem.SetText(itemName)
				else:
					myItem.SetText("%dx %s" % (count, itemName))
				if app.ENABLE_SEND_TARGET_INFO_EXTENDED:
					myItem.SetRarity(rarity)
				myItem.SAFE_SetOverInEvent(self.OnShowItemTooltip, vnum)
				myItem.SAFE_SetOverOutEvent(self.OnHideItemTooltip)
				listBox.AppendItem(myItem)

				if item.GetItemType() == item.ITEM_TYPE_METIN:
					self.stoneImg = myItem
					self.stoneVnum = vnums
					self.lastStoneVnum = self.STONE_LAST_VNUM + vnums[len(vnums) - 1] % 1000 / 100 * 100

				return myItem.GetHeight()

			def OnShowItemTooltip(self, vnum):
				item.SelectItem(vnum)
				if item.GetItemType() == item.ITEM_TYPE_METIN:
					self.itemTooltip.isStone = True
					self.itemTooltip.isBook = False
					self.itemTooltip.isBook2 = False
					self.itemTooltip.SetItemToolTip(self.lastStoneVnum)
				else:
					self.itemTooltip.isStone = False
					self.itemTooltip.isBook = True
					self.itemTooltip.isBook2 = True
					self.itemTooltip.SetItemToolTip(vnum)

			def OnHideItemTooltip(self):
				self.itemTooltip.HideToolTip()

			def AppendWindow(self, wnd, x = 0, width = 0, height = 0):
				if width == 0:
					width = wnd.GetWidth()
				if height == 0:
					height = wnd.GetHeight()

				wnd.SetParent(self)
				if x == 0:
					wnd.SetPosition((self.GetWidth() - width) / 2, self.yPos)
				else:
					wnd.SetPosition(x, self.yPos)
				wnd.Show()

				self.children.append(wnd)
				self.yPos += height + 5

			def OnUpdate(self):
				if self.stoneImg != None and self.stoneVnum != None and app.GetTime() >= self.nextStoneIconChange:
					nextImg = self.lastStoneVnum + 1
					if nextImg % 100 > self.STONE_LAST_VNUM % 100:
						nextImg -= (self.STONE_LAST_VNUM - self.STONE_START_VNUM) + 1
					self.lastStoneVnum = nextImg
					self.nextStoneIconChange = app.GetTime() + 2.5

					item.SelectItem(nextImg)
					itemName = item.GetItemName()
					realName = itemName[:itemName.find("+")]
					realName = realName + "+0 - +4"
					self.stoneImg.LoadImage(item.GetIconImageFileName(), realName)

					if self.itemTooltip.IsShow() and self.itemTooltip.isStone:
						self.itemTooltip.SetItemToolTip(nextImg)
						
	if app.ENABLE_DECORUM:
		BUTTON_NAME_LIST = (
			localeInfo.TARGET_BUTTON_WHISPER,
			localeInfo.TARGET_BUTTON_EXCHANGE,
			localeInfo.TARGET_BUTTON_FIGHT,
			localeInfo.TARGET_BUTTON_ACCEPT_FIGHT,
			localeInfo.TARGET_BUTTON_AVENGE,
			localeInfo.TARGET_BUTTON_FRIEND,
			localeInfo.TARGET_BUTTON_INVITE_PARTY,
			localeInfo.TARGET_BUTTON_LEAVE_PARTY,
			localeInfo.TARGET_BUTTON_EXCLUDE,
			localeInfo.TARGET_BUTTON_INVITE_GUILD,
			localeInfo.TARGET_BUTTON_DISMOUNT,
			localeInfo.TARGET_BUTTON_EXIT_OBSERVER,
			localeInfo.TARGET_BUTTON_VIEW_EQUIPMENT,
			localeInfo.TARGET_BUTTON_REQUEST_ENTER_PARTY,
			localeInfo.TARGET_BUTTON_BUILDING_DESTROY,
			localeInfo.TARGET_BUTTON_EMOTION_ALLOW,
			localeInfo.TARGET_BUTTON_DECORUM_STAT,
			localeInfo.TARGET_BUTTON_DECORUM_DUEL,			
			localeInfo.TARGET_BUTTON_BLOCK,
			localeInfo.TARGET_BUTTON_UNBLOCK,
			
			"VOTE_BLOCK_CHAT",
		)
	else:		
		BUTTON_NAME_LIST = (
			localeInfo.TARGET_BUTTON_WHISPER,
			localeInfo.TARGET_BUTTON_EXCHANGE,
			localeInfo.TARGET_BUTTON_FIGHT,
			localeInfo.TARGET_BUTTON_ACCEPT_FIGHT,
			localeInfo.TARGET_BUTTON_AVENGE,
			localeInfo.TARGET_BUTTON_FRIEND,
			localeInfo.TARGET_BUTTON_INVITE_PARTY,
			localeInfo.TARGET_BUTTON_LEAVE_PARTY,
			localeInfo.TARGET_BUTTON_EXCLUDE,
			localeInfo.TARGET_BUTTON_INVITE_GUILD,
			localeInfo.TARGET_BUTTON_DISMOUNT,
			localeInfo.TARGET_BUTTON_EXIT_OBSERVER,
			localeInfo.TARGET_BUTTON_VIEW_EQUIPMENT,
			localeInfo.TARGET_BUTTON_REQUEST_ENTER_PARTY,
			localeInfo.TARGET_BUTTON_BUILDING_DESTROY,
			localeInfo.TARGET_BUTTON_EMOTION_ALLOW,
			localeInfo.TARGET_BUTTON_BLOCK,
			localeInfo.TARGET_BUTTON_UNBLOCK,
			
			"VOTE_BLOCK_CHAT",
		)

	GRADE_NAME =	{
						nonplayer.PAWN : localeInfo.TARGET_LEVEL_PAWN,
						nonplayer.S_PAWN : localeInfo.TARGET_LEVEL_S_PAWN,
						nonplayer.KNIGHT : localeInfo.TARGET_LEVEL_KNIGHT,
						nonplayer.S_KNIGHT : localeInfo.TARGET_LEVEL_S_KNIGHT,
						nonplayer.BOSS : localeInfo.TARGET_LEVEL_BOSS,
						nonplayer.KING : localeInfo.TARGET_LEVEL_KING,
					}
	EXCHANGE_LIMIT_RANGE = 3000

	def __init__(self):
		ui.ThinBoard.__init__(self)

		name = ui.TextLine()
		name.SetParent(self)
		name.SetDefaultFontName()
		name.SetOutline()
		name.Show()

		hpGauge = ui.DynamicGauge()
		hpGauge.SetParent(self)
		hpGauge.MakeGauge(130, "red", "blue")
		hpGauge.Hide()
		
		if app.ENABLE_POISON_GAUGE_EFFECT:
			hpPoisonGauge = ui.Gauge()
			hpPoisonGauge.SetParent(self)
			hpPoisonGauge.MakeGauge(130, "lime")
			hpPoisonGauge.SetPosition(175, 17)
			hpPoisonGauge.SetWindowHorizontalAlignRight()
			hpPoisonGauge.Hide()
		
		hpPercenttxt = ui.TextLine()
		hpPercenttxt.SetParent(self)
		hpPercenttxt.SetPosition(160, 13)
		hpPercenttxt.SetText("")
		hpPercenttxt.Hide()
		
		if app.ENABLE_NEW_TARGET_HP:
			hpTarget = ui.NewTargetInfo()
			hpTarget.SetParent(self)
			hpTarget.SetPosition(-hpTarget.GetWidth(),0)
			hpTarget.Show()
			self.hpTarget = hpTarget

		closeButton = ui.Button()
		closeButton.SetParent(self)
		closeButton.SetUpVisual("d:/ymir work/ui/public/close_button_01.sub")
		closeButton.SetOverVisual("d:/ymir work/ui/public/close_button_02.sub")
		closeButton.SetDownVisual("d:/ymir work/ui/public/close_button_03.sub")
		closeButton.SetPosition(30, 13)

		if localeInfo.IsARABIC():
			hpGauge.SetPosition(55, 17)
			hpGauge.SetWindowHorizontalAlignLeft()
			closeButton.SetWindowHorizontalAlignLeft()
		else:
			hpGauge.SetPosition(175, 17)
			hpGauge.SetWindowHorizontalAlignRight()
			closeButton.SetWindowHorizontalAlignRight()
		if app.ENABLE_SEND_TARGET_INFO:
			infoButton = ui.Button()
			infoButton.SetParent(self)
			infoButton.SetUpVisual("d:/ymir work/ui/game/targetinfo/pattern/q_mark_01.tga")
			infoButton.SetOverVisual("d:/ymir work/ui/game/targetinfo/pattern/q_mark_02.tga")
			infoButton.SetDownVisual("d:/ymir work/ui/game/targetinfo/pattern/q_mark_01.tga")
			infoButton.SetEvent(ui.__mem_func__(self.OnPressedInfoButton))
			infoButton.Hide()

			infoBoard = self.InfoBoard()
			infoBoard.Hide()
			infoButton.showWnd = infoBoard

		closeButton.SetEvent(ui.__mem_func__(self.OnPressedCloseButton))
		closeButton.Show()
		
		self.firstMountBtn = None
		self.SecondMountBtn = None

		self.buttonDict = {}
		self.showingButtonList = []
		for buttonName in self.BUTTON_NAME_LIST:
			button = ui.Button()
			button.SetParent(self)

			button.SetUpVisual("ibowork/buttons/button_normal.tga")
			button.SetOverVisual("ibowork/buttons/button_hover.tga")
			button.SetDownVisual("ibowork/buttons/button_down.tga")

			button.SetWindowHorizontalAlignCenter()
			button.SetText(buttonName)
			button.Hide()
			self.buttonDict[buttonName] = button
			self.showingButtonList.append(button)

		self.buttonDict[localeInfo.TARGET_BUTTON_WHISPER].SetEvent(ui.__mem_func__(self.OnWhisper))
		if app.ENABLE_MESSENGER_BLOCK:
			self.buttonDict[localeInfo.TARGET_BUTTON_BLOCK].SetEvent(ui.__mem_func__(self.OnAppendToBlockMessenger))
			self.buttonDict[localeInfo.TARGET_BUTTON_UNBLOCK].SetEvent(ui.__mem_func__(self.OnRemoveToBlockMessenger))

		self.buttonDict[localeInfo.TARGET_BUTTON_EXCHANGE].SetEvent(ui.__mem_func__(self.OnExchange))
		self.buttonDict[localeInfo.TARGET_BUTTON_FIGHT].SetEvent(ui.__mem_func__(self.OnPVP))
		self.buttonDict[localeInfo.TARGET_BUTTON_ACCEPT_FIGHT].SetEvent(ui.__mem_func__(self.OnPVP))
		self.buttonDict[localeInfo.TARGET_BUTTON_AVENGE].SetEvent(ui.__mem_func__(self.OnPVP))
		self.buttonDict[localeInfo.TARGET_BUTTON_FRIEND].SetEvent(ui.__mem_func__(self.OnAppendToMessenger))
		self.buttonDict[localeInfo.TARGET_BUTTON_FRIEND].SetEvent(ui.__mem_func__(self.OnAppendToMessenger))
		self.buttonDict[localeInfo.TARGET_BUTTON_INVITE_PARTY].SetEvent(ui.__mem_func__(self.OnPartyInvite))
		self.buttonDict[localeInfo.TARGET_BUTTON_LEAVE_PARTY].SetEvent(ui.__mem_func__(self.OnPartyExit))
		self.buttonDict[localeInfo.TARGET_BUTTON_EXCLUDE].SetEvent(ui.__mem_func__(self.OnPartyRemove))

		self.buttonDict[localeInfo.TARGET_BUTTON_INVITE_GUILD].SAFE_SetEvent(self.__OnGuildAddMember)
		self.buttonDict[localeInfo.TARGET_BUTTON_DISMOUNT].SAFE_SetEvent(self.__OnDismount)
		self.buttonDict[localeInfo.TARGET_BUTTON_EXIT_OBSERVER].SAFE_SetEvent(self.__OnExitObserver)
		self.buttonDict[localeInfo.TARGET_BUTTON_VIEW_EQUIPMENT].SAFE_SetEvent(self.__OnViewEquipment)
		self.buttonDict[localeInfo.TARGET_BUTTON_REQUEST_ENTER_PARTY].SAFE_SetEvent(self.__OnRequestParty)
		self.buttonDict[localeInfo.TARGET_BUTTON_BUILDING_DESTROY].SAFE_SetEvent(self.__OnDestroyBuilding)
		self.buttonDict[localeInfo.TARGET_BUTTON_EMOTION_ALLOW].SAFE_SetEvent(self.__OnEmotionAllow)

		if app.ENABLE_DECORUM:
			self.buttonDict[localeInfo.TARGET_BUTTON_DECORUM_STAT].SetEvent(ui.__mem_func__(self.__OnDecoredStat))
			self.buttonDict[localeInfo.TARGET_BUTTON_DECORUM_DUEL].SetEvent(ui.__mem_func__(self.__OnDecoredDuel))

		self.buttonDict["VOTE_BLOCK_CHAT"].SetEvent(ui.__mem_func__(self.__OnVoteBlockChat))

		self.name = name
		self.hpGauge = hpGauge
		self.hpPoisonGauge = hpPoisonGauge
		self.hpPercenttxt = hpPercenttxt
		if app.ENABLE_SEND_TARGET_INFO:
			self.infoButton = infoButton
		if app.ENABLE_SEND_TARGET_INFO:
			self.vnum = 0
		self.closeButton = closeButton
		self.nameString = 0
		self.nameLength = 0
		self.vid = 0
		self.eventWhisper = None
		self.isShowButton = False
		if app.ENABLE_VIEW_ELEMENT:
			self.elementImage = None

		self.__Initialize()
		self.ResetTargetBoard()

	def __del__(self):
		ui.ThinBoard.__del__(self)

		print "===================================================== DESTROYED TARGET BOARD"

	def __Initialize(self):
		self.nameString = ""
		self.nameLength = 0
		self.vid = 0
		if app.ENABLE_SEND_TARGET_INFO:
			self.vnum = 0
		self.isShowButton = False

	def Destroy(self):
		self.hpPercenttxt = None
		self.eventWhisper = None
		if app.ENABLE_SEND_TARGET_INFO:
			self.infoButton = None
		self.closeButton = None
		self.showingButtonList = None
		self.buttonDict = None
		self.name = None
		if app.ENABLE_NEW_TARGET_HP:
			if self.hpTarget:
				self.hpTarget.Hide()
				self.hpTarget.Destroy()
				self.hpTarget=None
		self.hpGauge = None
		if app.ENABLE_POISON_GAUGE_EFFECT:
			self.hpPoisonGauge = None
		self.__Initialize()
		if app.ENABLE_VIEW_ELEMENT:
			self.elementImage = None

	if app.ENABLE_SEND_TARGET_INFO:
		def RefreshMonsterInfoBoard(self):
			if not self.infoButton.showWnd.IsShow():
				return

			self.infoButton.showWnd.Refresh()

		def OnPressedInfoButton(self):
			net.SendTargetInfoLoad(player.GetTargetVID())
			if self.infoButton.showWnd.IsShow():
				self.infoButton.showWnd.Close()
			elif self.vnum != 0:
				self.infoButton.showWnd.Open(self, self.vnum)

	def OnPressedCloseButton(self):
		player.ClearTarget()
		self.Close()

	def Close(self):
		self.__Initialize()
		if app.ENABLE_SEND_TARGET_INFO:
			self.infoButton.showWnd.Close()
		self.Hide()

	def Open(self, vid, name):
		if vid:
			if not constInfo.GET_VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD():
				if not player.IsSameEmpire(vid):
					self.Hide()
					return

			if vid != self.GetTargetVID():
				self.ResetTargetBoard()
				self.SetTargetVID(vid)
				self.SetTargetName(name)

				self.FaceTargetImage = ui.ExpandedImageBox()	
				self.FaceTargetImage.SetParent(self)
				self.FaceTargetImage.LoadImage("ibowork/target/circle_bg.png")
				self.FaceTargetImage.SetPosition(-60, -15)

				self.FaceTargetIcon = ui.ExpandedImageBox()	
				self.FaceTargetIcon.SetParent(self.FaceTargetImage)
				self.FaceTargetIcon.SetPosition(13, 12)

			if player.IsMainCharacterIndex(vid):
				self.__ShowMainCharacterMenu()
			elif chr.INSTANCE_TYPE_BUILDING == chr.GetInstanceType(self.vid):
				self.Hide()
			else:
				self.RefreshButton()
				self.Show()
		else:
			self.HideAllButton()
			self.__ShowButton(localeInfo.TARGET_BUTTON_WHISPER)
			self.__ShowButton("VOTE_BLOCK_CHAT")
			self.__ArrangeButtonPosition()
			self.SetTargetName(name)
			self.Show()

	def Refresh(self):
		if self.IsShow():
			if self.IsShowButton():
				self.RefreshButton()

	def RefreshByVID(self, vid):
		if vid == self.GetTargetVID():
			self.Refresh()

	def RefreshByName(self, name):
		if name == self.GetTargetName():
			self.Refresh()

	def __ShowMainCharacterMenu(self):
		canShow=0

		self.HideAllButton()

		if player.IsMountingHorse():
			self.__ShowButton(localeInfo.TARGET_BUTTON_DISMOUNT)
			canShow=1

		if player.IsObserverMode():
			self.__ShowButton(localeInfo.TARGET_BUTTON_EXIT_OBSERVER)
			canShow=1

		if canShow:
			self.__ArrangeButtonPosition()
			self.Show()
		else:
			self.Hide()

	def __ShowNameOnlyMenu(self):
		self.HideAllButton()

	def SetWhisperEvent(self, event):
		self.eventWhisper = event

	def UpdatePosition(self):
		self.SetPosition(wndMgr.GetScreenWidth()/2 - self.GetWidth()/2, 10)	

	def ResetTargetBoard(self):

		for btn in self.buttonDict.values():
			btn.Hide()

		self.__Initialize()

		self.name.SetPosition(0, 13)
		self.name.SetHorizontalAlignCenter()
		self.name.SetWindowHorizontalAlignCenter()
		self.hpGauge.Hide()
		if app.ENABLE_POISON_GAUGE_EFFECT:
			self.hpPoisonGauge.Hide()
		self.hpPercenttxt.Hide()
		if app.ENABLE_VIEW_ELEMENT and self.elementImage:
			self.elementImage = None
		if app.ENABLE_SEND_TARGET_INFO:
			self.infoButton.Hide()
			self.infoButton.showWnd.Close()
		self.SetSize(250, 40)

	def SetTargetVID(self, vid):
		self.vid = vid
		if app.ENABLE_SEND_TARGET_INFO:
			self.vnum = 0

	def SetEnemyVID(self, vid):
		self.SetTargetVID(vid)

		name = chr.GetNameByVID(vid)
		if app.ENABLE_SEND_TARGET_INFO:
			vnum = nonplayer.GetRaceNumByVID(vid)
		level = nonplayer.GetLevelByVID(vid)
		grade = nonplayer.GetGradeByVID(vid)

		nameFront = ""
		if -1 != level:
			nameFront += "Lv." + str(level) + " "
		if self.GRADE_NAME.has_key(grade):
			nameFront += "(" + self.GRADE_NAME[grade] + ") "

		self.SetTargetName(nameFront + name)
		if app.ENABLE_SEND_TARGET_INFO:
			(textWidth, textHeight) = self.name.GetTextSize()

			self.infoButton.SetPosition(textWidth + 25, 12)
			self.infoButton.SetWindowHorizontalAlignLeft()

			self.vnum = vnum
			self.infoButton.Show()

	def GetTargetVID(self):
		return self.vid

	def GetTargetName(self):
		return self.nameString

	def SetTargetName(self, name):
		self.nameString = name
		self.nameLength = len(name)
		self.name.SetText(name)

	if app.ENABLE_NEW_TARGET_HP:
		def SetNewHP(self, hpPercentage):
			chr.SelectInstance(self.vid)
			self.hpTarget.SetHP(chr.GetRace(),hpPercentage)

	def SetMount(self, vid):
		self.ResetTargetBoard()
		self.SetTargetVID(vid)
		self.SetTargetName(chr.GetNameByVID(vid))
		#self.SetSize(200 + 7*self.nameLength, self.GetHeight()+20)

		self.HideAllButton()

		button = ui.Button()
		button.SetParent(self)
		if localeInfo.IsARABIC():
			button.SetUpVisual("d:/ymir work/ui/public/Small_Button_01.sub")
			button.SetOverVisual("d:/ymir work/ui/public/Small_Button_02.sub")
			button.SetDownVisual("d:/ymir work/ui/public/Small_Button_03.sub")
		else:
			button.SetUpVisual("d:/ymir work/ui/public/small_thin_button_01.sub")
			button.SetOverVisual("d:/ymir work/ui/public/small_thin_button_02.sub")
			button.SetDownVisual("d:/ymir work/ui/public/small_thin_button_03.sub")
		button.SetWindowHorizontalAlignCenter()
		button.SetText("Cavalca")#set here
		button.SetEvent(self.FirstMountButton)
		button.Show()
		self.showingButtonList.append(button)
		
		button = ui.Button()
		button.SetParent(self)
		if localeInfo.IsARABIC():
			button.SetUpVisual("d:/ymir work/ui/public/Small_Button_01.sub")
			button.SetOverVisual("d:/ymir work/ui/public/Small_Button_02.sub")
			button.SetDownVisual("d:/ymir work/ui/public/Small_Button_03.sub")
		else:
			button.SetUpVisual("d:/ymir work/ui/public/small_thin_button_01.sub")
			button.SetOverVisual("d:/ymir work/ui/public/small_thin_button_02.sub")
			button.SetDownVisual("d:/ymir work/ui/public/small_thin_button_03.sub")
		button.SetWindowHorizontalAlignCenter()
		button.SetText("Manda Via")#set here
		button.SetEvent(self.SecondMountButton)
		button.Show()
		self.showingButtonList.append(button)
		
		self.__ArrangeButtonPosition()
		
		self.name.SetPosition(0, 13)
		self.name.SetHorizontalAlignCenter()
		self.SetNewHP(100)
		self.UpdatePosition()
		self.Show()

	def FirstMountButton(self):
		net.SendChatPacket("/mount_target 0")

	def SecondMountButton(self):
		net.SendChatPacket("/mount_target 1")

	def SetHP(self, hpPercentage):
		#if self.vid != 0:
			#self.FaceTargetImage = ui.ExpandedImageBox()	
			#self.FaceTargetImage.SetParent(self)
			#self.FaceTargetImage.LoadImage("ibowork/target/circle_bg.png")
			#self.FaceTargetImage.SetPosition(-60, -15)

			#self.FaceTargetIcon = ui.ExpandedImageBox()	
			#self.FaceTargetIcon.SetParent(self.FaceTargetImage)
			#self.FaceTargetIcon.SetPosition(13, 12)

			#pcRace = nonplayer.GetRaceNumByVID(self.vid)
			#if pcRace == 8010 or pcRace == 8015 or pcRace == 8025:
			#	self.FaceTargetIcon.LoadImage("ibowork/target/8004.png")
			#elif pcRace == 2036:
			#	self.FaceTargetIcon.LoadImage("ibowork/target/2035.png")
			#elif pcRace >= 131 and pcRace <= 144:
				#self.FaceTargetIcon.LoadImage("ibowork/target/%d.png" % (pcRace-29))
		#	elif pcRace == 8016 or pcRace == 8020 or pcRace == 8026:
			#	self.FaceTargetIcon.LoadImage("ibowork/target/8005.png")
			#elif pcRace == 8017 or pcRace == 8033:
			#	self.FaceTargetIcon.LoadImage("ibowork/target/8006.png")
			#elif pcRace == 8018 or pcRace == 8021  or pcRace == 8027:
			#	self.FaceTargetIcon.LoadImage("ibowork/target/8007.png")
			#elif pcRace == 8019 or pcRace == 8022:
				#self.FaceTargetIcon.LoadImage("ibowork/target/8008.png")
			#elif pcRace == 8023 or pcRace == 8031:
			#	self.FaceTargetIcon.LoadImage("ibowork/target/8009.png")
			#elif pcRace == 8024:
			#	self.FaceTargetIcon.LoadImage("ibowork/target/8003.png")
			#elif pcRace == 8032:
			#	self.FaceTargetIcon.LoadImage("ibowork/target/8001.png")
			#elif pcRace == 8034:
			#	self.FaceTargetIcon.LoadImage("ibowork/target/8002.png")
			#elif pcRace >= 8035 and pcRace <= 8040:
			#	self.FaceTargetIcon.LoadImage("ibowork/target/%d.png" % (pcRace+16))
			#elif pcRace >= 8041 and pcRace <= 8050:
			#	self.FaceTargetIcon.LoadImage("ibowork/target/8832.png")
			#elif pcRace == 8057:
			#	self.FaceTargetIcon.LoadImage("ibowork/target/8053.png")
		#	elif pcRace == 8073:
			#	self.FaceTargetIcon.LoadImage("ibowork/target/8874.png")
			#elif pcRace == 8116:
		#		self.FaceTargetIcon.LoadImage("ibowork/target/8804.png")
			#elif pcRace >= 8101 and pcRace <= 8108:
				#self.FaceTargetIcon.LoadImage("ibowork/target/%d.png" % (pcRace-100))
			#elif pcRace == 8109 :
			#	self.FaceTargetIcon.LoadImage("ibowork/target/8800.png")
			#elif pcRace >= 8110 and pcRace <= 8112:
			#	self.FaceTargetIcon.LoadImage("ibowork/target/8009.png")
			#elif pcRace > 8904 :
			#	self.FaceTargetIcon.LoadImage("ibowork/target/default.png")
			#Yapilacak Bosslar
			#elif pcRace == 6418 or pcRace == 2862 or pcRace == 236 or pcRace == 241 or pcRace == 950 or pcRace == 4103 or pcRace == 4104 or pcRace == 4105 or pcRace == 1765 or pcRace == 1754 or pcRace == 1751 or pcRace == 1750 or pcRace == 1752 or pcRace == 1753 or pcRace == 1759 or pcRace == 1758:
			#	self.FaceTargetIcon.LoadImage("ibowork/target/default.png")
			#Yapilacak Metinler
			#elif pcRace >= 8439 and pcRace <= 8444 or pcRace >= 8452 and pcRace <= 8453:
			#	self.FaceTargetIcon.LoadImage("ibowork/target/default.png")
			#else:
				#self.FaceTargetIcon.LoadImage("ibowork/target/%d.png" % pcRace)
			#self.FaceTargetIcon.Show()
			#self.FaceTargetImage.Show()
		self.HideAllButton()
		if not self.hpGauge.IsShow():
			self.SetSize(200 + 7*self.nameLength, self.GetHeight())
			if localeInfo.IsARABIC():
				self.name.SetPosition( self.GetWidth()-23, 13)
			else:
				self.name.SetPosition(23, 13)
			self.name.SetWindowHorizontalAlignLeft()
			self.name.SetHorizontalAlignLeft()
			self.hpGauge.Show()
			self.UpdatePosition()
			self.hpPercenttxt.SetPosition(200 + 7*self.nameLength-120, 3)
			self.hpPercenttxt.Show()
		self.hpGauge.SetPercentage(hpPercentage, 100)
		if app.ENABLE_POISON_GAUGE_EFFECT:
			self.hpPoisonGauge.SetPercentage(hpPercentage, 100)
		self.hpPercenttxt.SetText("%d%%" % (hpPercentage))
		if app.ENABLE_NEW_TARGET_HP:
			self.hpTarget.Hide()

	if app.ENABLE_VIEW_ELEMENT:
		def SetElementImage(self,elementId):
			try:
				if elementId > 0 and elementId in ELEMENT_IMAGE_DIC.keys():
					self.elementImage = ui.ImageBox()
					self.elementImage.SetParent(self.name)
					self.elementImage.SetPosition(-70,-12)
					#self.elementImage.SetPosition(-15,27)
					self.elementImage.LoadImage("d:/ymir work/ui/game/12zi/element/%s.sub" % (ELEMENT_IMAGE_DIC[elementId]))
					constInfo.Element_ID = elementId
					self.elementImage.Show()
			except:
				pass

	def ShowDefaultButton(self):

		self.isShowButton = True
		self.showingButtonList.append(self.buttonDict[localeInfo.TARGET_BUTTON_WHISPER])
		self.showingButtonList.append(self.buttonDict[localeInfo.TARGET_BUTTON_EXCHANGE])
		self.showingButtonList.append(self.buttonDict[localeInfo.TARGET_BUTTON_FIGHT])
		self.showingButtonList.append(self.buttonDict[localeInfo.TARGET_BUTTON_EMOTION_ALLOW])
		for button in self.showingButtonList:
			button.Show()

	def HideAllButton(self):
		self.isShowButton = False
		for button in self.showingButtonList:
			button.Hide()
		self.showingButtonList = []

	def __ShowButton(self, name):

		if not self.buttonDict.has_key(name):
			return

		self.buttonDict[name].Show()
		self.showingButtonList.append(self.buttonDict[name])

	def __HideButton(self, name):

		if not self.buttonDict.has_key(name):
			return

		button = self.buttonDict[name]
		button.Hide()

		for btnInList in self.showingButtonList:
			if btnInList == button:
				self.showingButtonList.remove(button)
				break

	def OnWhisper(self):
		if None != self.eventWhisper:
			self.eventWhisper(self.nameString)

	def OnExchange(self):
		net.SendExchangeStartPacket(self.vid)

	def OnPVP(self):
		if app.ENABLE_RENEWAL_PVP:
			interface = constInfo.GetInterfaceInstance()
			if interface != None:
				interface.OpenPvPFirst(self.nameString,self.vid)
		else:
			net.SendChatPacket("/pvp %d" % (self.vid))

	def OnAppendToMessenger(self):
		net.SendMessengerAddByVIDPacket(self.vid)

	if app.ENABLE_MESSENGER_BLOCK:
		def OnAppendToBlockMessenger(self):
			net.SendMessengerAddBlockByVIDPacket(self.vid)
		def OnRemoveToBlockMessenger(self):
			messenger.RemoveBlock(constInfo.ME_KEY)
			net.SendMessengerRemoveBlockPacket(constInfo.ME_KEY, chr.GetNameByVID(self.vid))
			

	def OnPartyInvite(self):
		net.SendPartyInvitePacket(self.vid)

	def OnPartyExit(self):
		net.SendPartyExitPacket()

	def OnPartyRemove(self):
		net.SendPartyRemovePacketVID(self.vid)

	def __OnGuildAddMember(self):
		net.SendGuildAddMemberPacket(self.vid)

	def __OnDismount(self):
		net.SendChatPacket("/unmount")

	def __OnExitObserver(self):
		net.SendChatPacket("/observer_exit")

	def __OnViewEquipment(self):
		net.SendChatPacket("/view_equip " + str(self.vid))

	def __OnRequestParty(self):
		net.SendChatPacket("/party_request " + str(self.vid))

	def __OnDestroyBuilding(self):
		net.SendChatPacket("/build d %d" % (self.vid))

	def __OnEmotionAllow(self):
		net.SendChatPacket("/emotion_allow %d" % (self.vid))

	def __OnVoteBlockChat(self):
		cmd = "/vote_block_chat %s" % (self.nameString)
		net.SendChatPacket(cmd)

	if app.ENABLE_DECORUM:
		def __OnDecoredStat(self):
			net.SendChatPacket("/decorum_stat %d" % (self.vid))
			
		def __OnDecoredDuel(self):
			if app.ENABLE_RENEWAL_PVP:
				net.SendChatPacket("/pvp decorum %d" % (self.vid))
			else:
				net.SendChatPacket("/pvp %d 1" % (self.vid))
			if constInfo.PVPMODE_ENABLE:
				net.SendChatPacket("/pkmode 0", chat.CHAT_TYPE_TALKING)

	def OnPressEscapeKey(self):
		self.OnPressedCloseButton()
		return True

	def IsShowButton(self):
		return self.isShowButton

	def RefreshButton(self):

		self.HideAllButton()

		if chr.INSTANCE_TYPE_BUILDING == chr.GetInstanceType(self.vid):
			#self.__ShowButton(localeInfo.TARGET_BUTTON_BUILDING_DESTROY)
			#self.__ArrangeButtonPosition()
			return

		if player.IsPVPInstance(self.vid) or player.IsObserverMode():
			# PVP_INFO_SIZE_BUG_FIX
			self.SetSize(200 + 7*self.nameLength, 40)
			self.UpdatePosition()
			# END_OF_PVP_INFO_SIZE_BUG_FIX
			return

		self.ShowDefaultButton()

		if guild.MainPlayerHasAuthority(guild.AUTH_ADD_MEMBER):
			if not guild.IsMemberByName(self.nameString):
				if 0 == chr.GetGuildID(self.vid):
					self.__ShowButton(localeInfo.TARGET_BUTTON_INVITE_GUILD)

		if not messenger.IsFriendByName(self.nameString):
			self.__ShowButton(localeInfo.TARGET_BUTTON_FRIEND)
		if app.ENABLE_MESSENGER_BLOCK and not str(self.nameString)[0] == "[":
			if not messenger.IsBlockByName(self.nameString):
				self.__ShowButton(localeInfo.TARGET_BUTTON_BLOCK)
				self.__HideButton(localeInfo.TARGET_BUTTON_UNBLOCK)
			else:
				self.__ShowButton(localeInfo.TARGET_BUTTON_UNBLOCK)
				self.__HideButton(localeInfo.TARGET_BUTTON_BLOCK)
		if player.IsPartyMember(self.vid):

			self.__HideButton(localeInfo.TARGET_BUTTON_FIGHT)

			if player.IsPartyLeader(self.vid):
				self.__ShowButton(localeInfo.TARGET_BUTTON_LEAVE_PARTY)
			elif player.IsPartyLeader(player.GetMainCharacterIndex()):
				self.__ShowButton(localeInfo.TARGET_BUTTON_EXCLUDE)

		else:
			if player.IsPartyMember(player.GetMainCharacterIndex()):
				if player.IsPartyLeader(player.GetMainCharacterIndex()):
					self.__ShowButton(localeInfo.TARGET_BUTTON_INVITE_PARTY)
			else:
				if chr.IsPartyMember(self.vid):
					self.__ShowButton(localeInfo.TARGET_BUTTON_REQUEST_ENTER_PARTY)
				else:
					self.__ShowButton(localeInfo.TARGET_BUTTON_INVITE_PARTY)

			if app.ENABLE_DECORUM:
				self.__HideButton(localeInfo.TARGET_BUTTON_DECORUM_STAT)
				if player.IsDecored(self.vid):
					self.__ShowButton(localeInfo.TARGET_BUTTON_DECORUM_STAT)
					if 0 != player.GetDecorum():
						self.__ShowButton(localeInfo.TARGET_BUTTON_DECORUM_DUEL)

			if player.IsRevengeInstance(self.vid):
				self.__HideButton(localeInfo.TARGET_BUTTON_FIGHT)
				self.__ShowButton(localeInfo.TARGET_BUTTON_AVENGE)
			elif player.IsChallengeInstance(self.vid):
				self.__HideButton(localeInfo.TARGET_BUTTON_FIGHT)
				if app.ENABLE_DECORUM:
					self.__HideButton(localeInfo.TARGET_BUTTON_DECORUM_DUEL)
				self.__ShowButton(localeInfo.TARGET_BUTTON_ACCEPT_FIGHT)
			elif player.IsCantFightInstance(self.vid):
				self.__HideButton(localeInfo.TARGET_BUTTON_FIGHT)
				if app.ENABLE_DECORUM:
					self.__HideButton(localeInfo.TARGET_BUTTON_DECORUM_DUEL)
					
			if not player.IsSameEmpire(self.vid):
				self.__HideButton(localeInfo.TARGET_BUTTON_INVITE_PARTY)
				self.__HideButton(localeInfo.TARGET_BUTTON_FRIEND)
				self.__HideButton(localeInfo.TARGET_BUTTON_FIGHT)

		distance = player.GetCharacterDistance(self.vid)
		if distance > self.EXCHANGE_LIMIT_RANGE:
			self.__HideButton(localeInfo.TARGET_BUTTON_EXCHANGE)
			self.__ArrangeButtonPosition()

		self.__ArrangeButtonPosition()

	def __ArrangeButtonPosition(self):
		showingButtonCount = len(self.showingButtonList)

		pos = -(showingButtonCount / 2) * 68
		if 0 == showingButtonCount % 2:
			pos += 34

		for button in self.showingButtonList:
			button.SetPosition(pos, 33)
			pos += 68

		self.SetSize(max(150, showingButtonCount * 75), 65)
		self.UpdatePosition()

	def OnUpdate(self):
		if self.isShowButton:

			exchangeButton = self.buttonDict[localeInfo.TARGET_BUTTON_EXCHANGE]
			distance = player.GetCharacterDistance(self.vid)

			if distance < 0:
				return

			if exchangeButton.IsShow():
				if distance > self.EXCHANGE_LIMIT_RANGE:
					self.RefreshButton()

			else:
				if distance < self.EXCHANGE_LIMIT_RANGE:
					self.RefreshButton()

		if app.ENABLE_POISON_GAUGE_EFFECT:
			if self.hpGauge and self.hpGauge.IsShow():
				if chrmgr.HasAffectByVID(self.GetTargetVID(), chr.AFFECT_POISON):
					self.hpPoisonGauge.Show()
				else:
					self.hpPoisonGauge.Hide()
					
if app.ENABLE_SHIP_DEFENSE:
	class AllianceTargetBoard(ui.ThinBoard):
		class TextToolTip(ui.Window):
			def __init__(self):
				ui.Window.__init__(self, "TOP_MOST")

				textLine = ui.TextLine()
				textLine.SetParent(self)
				textLine.SetHorizontalAlignCenter()
				textLine.SetOutline()
				textLine.Show()
				self.textLine = textLine

			def __del__(self):
				ui.Window.__del__(self)

			def SetText(self, text):
				self.textLine.SetText(text)

			def OnRender(self):
				(mouseX, mouseY) = wndMgr.GetMousePosition()
				self.textLine.SetPosition(mouseX, mouseY + 30)

		def __init__(self):
			ui.ThinBoard.__init__(self)

			name = ui.TextLine()
			name.SetParent(self)
			name.SetDefaultFontName()
			name.SetOutline()
			name.Show()

			hpGauge = ui.Gauge()
			hpGauge.SetParent(self)
			hpGauge.MakeGauge(80, "red")
			hpGauge.SetPosition(10, 25)
			hpGauge.SetOverEvent(ui.__mem_func__(self.IsIn))
			hpGauge.SetOverOutEvent(ui.__mem_func__(self.IsOut))
			hpGauge.Hide()

			self.name = name
			self.hpGauge = hpGauge

			self.toolTipHP = self.TextToolTip()
			self.toolTipHP.Hide()

			self.Initialize()
			self.ResetTargetBoard()

		def __del__(self):
			ui.ThinBoard.__del__(self)

		def Initialize(self):
			self.nameLength = 0
			self.vid = 0

		def Destroy(self):
			self.name = None
			self.hpGauge = None
			self.tooltipHP = None

			self.Initialize()

		def Close(self):
			self.Initialize()
			self.tooltipHP.Hide()
			self.Hide()

		def ResetTargetBoard(self):
			self.Initialize()

			self.name.SetPosition(0, 13)
			self.name.SetHorizontalAlignCenter()
			self.name.SetWindowHorizontalAlignCenter()

			self.hpGauge.Hide()
			self.SetSize(100, 40)

		def SetTargetVID(self, vid):
			self.vid = vid

		def SetTarget(self, vid):
			self.SetTargetVID(vid)

			name = chr.GetNameByVID(vid)
			self.SetTargetName(name)

		def GetTargetVID(self):
			return self.vid

		def SetTargetName(self, name):
			self.nameLength = len(name)
			self.name.SetText(name)

		def SetHP(self, hp, hpMax):
			hp = min(hp, hpMax)
			if hp > 0:
				self.SetSize(100, self.GetHeight())

				if localeInfo.IsARABIC():
					self.name.SetPosition(self.GetWidth() - 10, 10)
				else:
					self.name.SetPosition(10, 10)

				self.name.SetWindowHorizontalAlignLeft()
				self.name.SetHorizontalAlignLeft()
				self.hpGauge.Show()
				self.UpdatePosition()

			self.hpGauge.SetPercentage(hp, hpMax)
			self.toolTipHP.SetText("%s : %d / %d" % (localeInfo.TASKBAR_HP, hp, hpMax))

		def UpdatePosition(self):
			# NOTE : y = miniMap + serverInfo Height
			self.SetPosition(wndMgr.GetScreenWidth() - self.GetWidth() - 18, 250)

		def IsOut(self):
			if self.toolTipHP:
				self.toolTipHP.Hide()

		def IsIn(self):
			if self.toolTipHP:
				self.toolTipHP.Show()

		# NOTE : Unused.
		def SetMouseEvent(self):
			pass
