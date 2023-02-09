import ui
import player
import mouseModule
import net
import app
import chat
import snd
import item
import player
import chat
import grp
import uiScriptLocale
import uiRefine
import uiAttachMetin
import uiCommon
import localeInfo
import constInfo
import ime
import grpText
import uiToolTip

	
class Switcher(ui.ScriptWindow):

	POSITIVE_COLOR = grp.GenerateColor(0.5411, 0.7254, 0.5568, 1.0)
	NEGATIVE_COLOR = grp.GenerateColor(0.9, 0.4745, 0.4627, 1.0)

	def __init__(self):
		import exception
		ui.ScriptWindow.__init__(self)

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		constInfo.BONUS_SWITCHER = 1
		self.__LoadWindow()
		ui.ScriptWindow.Show(self)

	def Close(self):
		constInfo.BONUS_SWITCHER = 0
		self.Hide()
		
	def OnPressEscapeKey(self):
		self.Close()
		return TRUE

	def __LoadWindow(self):
		try:			
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/manualswitchbot.py")
		except:
			import exception
			exception.Abort("SwitcherWindow.LoadWindow.LoadObject")
		self.TitleBar = self.GetChild("TitleBar")
		self.switchslot = self.GetChild("switchslot")		
		self.bonusslot = [self.GetChild2("bonus1"), self.GetChild2("bonus2"), self.GetChild2("bonus3"), ]
		self.buttongira = self.GetChild("gira_bonus")
		self.buttongira.SetEvent(ui.__mem_func__(self.switchbonus))
		self.TitleBar.SetCloseEvent(ui.__mem_func__(self.Close))
		self.switchslot.SetSelectEmptySlotEvent(ui.__mem_func__(self.__OnSelectEmptySlot))
		self.switchslot.SetSelectItemSlotEvent(ui.__mem_func__(self.__OnSelectItemSlot))
		self.toolTipCostume = uiToolTip.ToolTip(190)
		self.toolTipCostume.SetTitle(item.GetItemName())
		
		self.slotitem = None
		self.slotgira = None
		self.realSwitch = None
		
	def __OnSelectItemSlot(self, selectedSlotPos):
		isAttached = mouseModule.mouseController.isAttached()
		if isAttached:
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			mouseModule.mouseController.DeattachObject()
			itemIndex = player.GetItemIndex(attachedSlotPos)
			itemCount = player.GetItemCount(attachedSlotPos)
			item.SelectItem(itemIndex)
			itemType = item.GetItemType()
			if selectedSlotPos == 0:
				self.slotitem = attachedSlotPos
				if item.ITEM_TYPE_COSTUME == itemType:
					self.switchslot.SetItemSlot(selectedSlotPos, itemIndex, 0)						
					attrSlot = [player.GetItemAttribute(attachedSlotPos, i) for i in xrange(3)]	
					for i in xrange(3):
						type = attrSlot[i][0]
						value = attrSlot[i][1]
						affectString = self.__GetAffectString(type, value)
						self.bonusslot[i].SetText(affectString)
		else:			
			if selectedSlotPos == 0:
				self.switchslot.SetItemSlot(0, 0, 0)
				self.slotitem = None
			
	def __OnSelectEmptySlot(self, selectedSlotPos):
		isAttached = mouseModule.mouseController.isAttached()
		if isAttached:
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			mouseModule.mouseController.DeattachObject()
			itemIndex = player.GetItemIndex(attachedSlotPos)
			itemCount = player.GetItemCount(attachedSlotPos)
			item.SelectItem(itemIndex)
			itemType = item.GetItemType()
			if selectedSlotPos == 0:
				self.slotitem = attachedSlotPos
				if item.ITEM_TYPE_COSTUME == itemType:
					self.switchslot.SetItemSlot(selectedSlotPos, itemIndex, 0)						
					attrSlot = [player.GetItemAttribute(attachedSlotPos, i) for i in xrange(3)]	
					for i in xrange(3):
						type = attrSlot[i][0]
						value = attrSlot[i][1]
						affectString = self.__GetAffectString(type, value)
						self.bonusslot[i].SetText(affectString)
			if selectedSlotPos == 1 and constInfo.IS_SWITCHER(itemIndex):
					self.slotgira = attachedSlotPos
					self.realSwitch = attachedSlotPos
					self.switchslot.SetItemSlot(selectedSlotPos, itemIndex, itemCount)
			
	def __GetAffectString(self, affectType, affectValue):
		if 0 == affectType:
			return None
		if 0 == affectValue:
			return None
			
		try:
			return self.AFFECT_DICT[affectType](affectValue)
		except TypeError:
			return "UNKNOWN_VALUE[%s] %s" % (affectType, affectValue)
		except KeyError:
			return "UNKNOWN_TYPE[%s] %s" % (affectType, affectValue)
			
	def switchbonus(self):
		attrSlot = [player.GetItemAttribute(self.slotitem, i) for i in xrange(3)]	
		question = 0
		for i in xrange(3):
			type = attrSlot[i][0]
			value = attrSlot[i][1]
			affectString = self.__GetAffectString(type, value)
			
			if type == item.APPLY_SKILL_DAMAGE_BONUS and value >= constInfo.SK_DMG_WARNING:
				question = 1
				
			if type == item.APPLY_NORMAL_HIT_DAMAGE_BONUS and value >= constInfo.AVG_DMG_WARNING:
				question = 1
			
		if question == 1:
			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText(localeInfo.SWITCHER_HIGH_BONUS)
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.__gira_bonus))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
			self.questionDialog.Open()
		else:
			self.__Switch(self.slotitem,self.slotgira)
		
		
	def OnCloseQuestionDialog(self):
		if not self.questionDialog:
			return

		self.questionDialog.Close()
		self.questionDialog = None
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	def __gira_bonus(self):
		self.__Switch(self.slotitem,self.slotgira)
		self.OnCloseQuestionDialog()
		
	def __Switch(self,dstSlotPos,srcSlotPos):
		net.SendItemUseToItemPacket(srcSlotPos,dstSlotPos)
		
	def refresh(self,dstSlotPos,srcSlotPos):
		attrSlot = [player.GetItemAttribute(dstSlotPos, i) for i in xrange(3)]	
		for i in xrange(3):		
			self.bonusslot[i].SetText("")
			
		for i in xrange(3):
			type = attrSlot[i][0]
			value = attrSlot[i][1]
			affectString = self.__GetAffectString(type, value)
			if int(value) < 0:				
				self.bonusslot[i].SetPackedFontColor(self.NEGATIVE_COLOR)
			else:
				self.bonusslot[i].SetPackedFontColor(self.POSITIVE_COLOR)
			self.bonusslot[i].SetText(affectString)
		
		itemIndex = player.GetItemIndex(srcSlotPos)
		itemCount = player.GetItemCount(srcSlotPos)
		self.switchslot.ClearSlot(1)
		self.switchslot.SetItemSlot(1, itemIndex, itemCount)
		
		if itemCount >= 1:
			for i in xrange(player.INVENTORY_SLOT_COUNT):
				vnum = player.GetItemIndex(i)
				count= player.GetItemCount(i)
				if constInfo.IS_SWITCHER(vnum) and vnum == self.realSwitch:
					self.switchslot.ClearSlot(1)
					self.switchslot.SetItemSlot(1, vnum, count)	
					self.slotgira = i
					
			
	def OnUpdate(self):
		if self.slotitem >= 0:
			self.refresh(self.slotitem,self.slotgira)
		else:
			for i in xrange(3):		
				self.bonusslot[i].SetText("")			

	AFFECT_DICT = {
		item.APPLY_MAX_HP : localeInfo.TOOLTIP_MAX_HP,
		item.APPLY_MAX_SP : localeInfo.TOOLTIP_MAX_SP,
		item.APPLY_CON : localeInfo.TOOLTIP_CON,
		item.APPLY_INT : localeInfo.TOOLTIP_INT,
		item.APPLY_STR : localeInfo.TOOLTIP_STR,
		item.APPLY_DEX : localeInfo.TOOLTIP_DEX,
		item.APPLY_ATT_SPEED : localeInfo.TOOLTIP_ATT_SPEED,
		item.APPLY_MOV_SPEED : localeInfo.TOOLTIP_MOV_SPEED,
		item.APPLY_CAST_SPEED : localeInfo.TOOLTIP_CAST_SPEED,
		item.APPLY_HP_REGEN : localeInfo.TOOLTIP_HP_REGEN,
		item.APPLY_SP_REGEN : localeInfo.TOOLTIP_SP_REGEN,
		item.APPLY_POISON_PCT : localeInfo.TOOLTIP_APPLY_POISON_PCT,
		item.APPLY_STUN_PCT : localeInfo.TOOLTIP_APPLY_STUN_PCT,
		item.APPLY_SLOW_PCT : localeInfo.TOOLTIP_APPLY_SLOW_PCT,
		item.APPLY_CRITICAL_PCT : localeInfo.TOOLTIP_APPLY_CRITICAL_PCT,
		item.APPLY_PENETRATE_PCT : localeInfo.TOOLTIP_APPLY_PENETRATE_PCT,

		item.APPLY_ATTBONUS_WARRIOR : localeInfo.TOOLTIP_APPLY_ATTBONUS_WARRIOR,
		item.APPLY_ATTBONUS_ASSASSIN : localeInfo.TOOLTIP_APPLY_ATTBONUS_ASSASSIN,
		item.APPLY_ATTBONUS_SURA : localeInfo.TOOLTIP_APPLY_ATTBONUS_SURA,
		item.APPLY_ATTBONUS_SHAMAN : localeInfo.TOOLTIP_APPLY_ATTBONUS_SHAMAN,
		item.APPLY_ATTBONUS_MONSTER : localeInfo.TOOLTIP_APPLY_ATTBONUS_MONSTER,

		item.APPLY_ATTBONUS_HUMAN : localeInfo.TOOLTIP_APPLY_ATTBONUS_HUMAN,
		item.APPLY_ATTBONUS_ANIMAL : localeInfo.TOOLTIP_APPLY_ATTBONUS_ANIMAL,
		item.APPLY_ATTBONUS_ORC : localeInfo.TOOLTIP_APPLY_ATTBONUS_ORC,
		item.APPLY_ATTBONUS_MILGYO : localeInfo.TOOLTIP_APPLY_ATTBONUS_MILGYO,
		item.APPLY_ATTBONUS_UNDEAD : localeInfo.TOOLTIP_APPLY_ATTBONUS_UNDEAD,
		item.APPLY_ATTBONUS_DEVIL : localeInfo.TOOLTIP_APPLY_ATTBONUS_DEVIL,
		item.APPLY_STEAL_HP : localeInfo.TOOLTIP_APPLY_STEAL_HP,
		item.APPLY_STEAL_SP : localeInfo.TOOLTIP_APPLY_STEAL_SP,
		item.APPLY_MANA_BURN_PCT : localeInfo.TOOLTIP_APPLY_MANA_BURN_PCT,
		item.APPLY_DAMAGE_SP_RECOVER : localeInfo.TOOLTIP_APPLY_DAMAGE_SP_RECOVER,
		item.APPLY_BLOCK : localeInfo.TOOLTIP_APPLY_BLOCK,
		item.APPLY_DODGE : localeInfo.TOOLTIP_APPLY_DODGE,
		item.APPLY_RESIST_SWORD : localeInfo.TOOLTIP_APPLY_RESIST_SWORD,
		item.APPLY_RESIST_TWOHAND : localeInfo.TOOLTIP_APPLY_RESIST_TWOHAND,
		item.APPLY_RESIST_DAGGER : localeInfo.TOOLTIP_APPLY_RESIST_DAGGER,
		item.APPLY_RESIST_BELL : localeInfo.TOOLTIP_APPLY_RESIST_BELL,
		item.APPLY_RESIST_FAN : localeInfo.TOOLTIP_APPLY_RESIST_FAN,
		item.APPLY_RESIST_BOW : localeInfo.TOOLTIP_RESIST_BOW,
		item.APPLY_RESIST_FIRE : localeInfo.TOOLTIP_RESIST_FIRE,
		item.APPLY_RESIST_ELEC : localeInfo.TOOLTIP_RESIST_ELEC,
		item.APPLY_RESIST_MAGIC : localeInfo.TOOLTIP_RESIST_MAGIC,
		item.APPLY_RESIST_WIND : localeInfo.TOOLTIP_APPLY_RESIST_WIND,
		item.APPLY_REFLECT_MELEE : localeInfo.TOOLTIP_APPLY_REFLECT_MELEE,
		item.APPLY_REFLECT_CURSE : localeInfo.TOOLTIP_APPLY_REFLECT_CURSE,
		item.APPLY_POISON_REDUCE : localeInfo.TOOLTIP_APPLY_POISON_REDUCE,
		item.APPLY_KILL_SP_RECOVER : localeInfo.TOOLTIP_APPLY_KILL_SP_RECOVER,
		item.APPLY_EXP_DOUBLE_BONUS : localeInfo.TOOLTIP_APPLY_EXP_DOUBLE_BONUS,
		item.APPLY_GOLD_DOUBLE_BONUS : localeInfo.TOOLTIP_APPLY_GOLD_DOUBLE_BONUS,
		item.APPLY_ITEM_DROP_BONUS : localeInfo.TOOLTIP_APPLY_ITEM_DROP_BONUS,
		item.APPLY_POTION_BONUS : localeInfo.TOOLTIP_APPLY_POTION_BONUS,
		item.APPLY_KILL_HP_RECOVER : localeInfo.TOOLTIP_APPLY_KILL_HP_RECOVER,
		item.APPLY_IMMUNE_STUN : localeInfo.TOOLTIP_APPLY_IMMUNE_STUN,
		item.APPLY_IMMUNE_SLOW : localeInfo.TOOLTIP_APPLY_IMMUNE_SLOW,
		item.APPLY_IMMUNE_FALL : localeInfo.TOOLTIP_APPLY_IMMUNE_FALL,
		item.APPLY_BOW_DISTANCE : localeInfo.TOOLTIP_BOW_DISTANCE,
		item.APPLY_DEF_GRADE_BONUS : localeInfo.TOOLTIP_DEF_GRADE,
		item.APPLY_ATT_GRADE_BONUS : localeInfo.TOOLTIP_ATT_GRADE,
		item.APPLY_MAGIC_ATT_GRADE : localeInfo.TOOLTIP_MAGIC_ATT_GRADE,
		item.APPLY_MAGIC_DEF_GRADE : localeInfo.TOOLTIP_MAGIC_DEF_GRADE,
		item.APPLY_MAX_STAMINA : localeInfo.TOOLTIP_MAX_STAMINA,
		item.APPLY_MALL_ATTBONUS : localeInfo.TOOLTIP_MALL_ATTBONUS,
		item.APPLY_MALL_DEFBONUS : localeInfo.TOOLTIP_MALL_DEFBONUS,
		item.APPLY_MALL_EXPBONUS : localeInfo.TOOLTIP_MALL_EXPBONUS,
		item.APPLY_MALL_ITEMBONUS : localeInfo.TOOLTIP_MALL_ITEMBONUS,
		item.APPLY_MALL_GOLDBONUS : localeInfo.TOOLTIP_MALL_GOLDBONUS,
		item.APPLY_SKILL_DAMAGE_BONUS : localeInfo.TOOLTIP_SKILL_DAMAGE_BONUS,
		item.APPLY_NORMAL_HIT_DAMAGE_BONUS : localeInfo.TOOLTIP_NORMAL_HIT_DAMAGE_BONUS,
		item.APPLY_SKILL_DEFEND_BONUS : localeInfo.TOOLTIP_SKILL_DEFEND_BONUS,
		item.APPLY_NORMAL_HIT_DEFEND_BONUS : localeInfo.TOOLTIP_NORMAL_HIT_DEFEND_BONUS,
		item.APPLY_PC_BANG_EXP_BONUS : localeInfo.TOOLTIP_MALL_EXPBONUS_P_STATIC,
		item.APPLY_PC_BANG_DROP_BONUS : localeInfo.TOOLTIP_MALL_ITEMBONUS_P_STATIC,
		item.APPLY_RESIST_WARRIOR : localeInfo.TOOLTIP_APPLY_RESIST_WARRIOR,
		item.APPLY_RESIST_ASSASSIN : localeInfo.TOOLTIP_APPLY_RESIST_ASSASSIN,
		item.APPLY_RESIST_SURA : localeInfo.TOOLTIP_APPLY_RESIST_SURA,
		item.APPLY_RESIST_SHAMAN : localeInfo.TOOLTIP_APPLY_RESIST_SHAMAN,
		item.APPLY_MAX_HP_PCT : localeInfo.TOOLTIP_APPLY_MAX_HP_PCT,
		item.APPLY_MAX_SP_PCT : localeInfo.TOOLTIP_APPLY_MAX_SP_PCT,
		item.APPLY_ENERGY : localeInfo.TOOLTIP_ENERGY,
		item.APPLY_COSTUME_ATTR_BONUS : localeInfo.TOOLTIP_COSTUME_ATTR_BONUS,
		
		item.APPLY_MAGIC_ATTBONUS_PER : localeInfo.TOOLTIP_MAGIC_ATTBONUS_PER,
		item.APPLY_MELEE_MAGIC_ATTBONUS_PER : localeInfo.TOOLTIP_MELEE_MAGIC_ATTBONUS_PER,
		item.APPLY_RESIST_ICE : localeInfo.TOOLTIP_RESIST_ICE,
		item.APPLY_RESIST_EARTH : localeInfo.TOOLTIP_RESIST_EARTH,
		item.APPLY_RESIST_DARK : localeInfo.TOOLTIP_RESIST_DARK,
		item.APPLY_ANTI_CRITICAL_PCT : localeInfo.TOOLTIP_ANTI_CRITICAL_PCT,
		item.APPLY_ANTI_PENETRATE_PCT : localeInfo.TOOLTIP_ANTI_PENETRATE_PCT,

	}
