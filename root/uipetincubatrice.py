import os
import ui
import player
import mouseModule
import net
import app
import snd
import item
import player
import chat
import grp
import uiScriptLocale
import localeInfo
import constInfo
import ime
import wndMgr


class PetSystemIncubator(ui.ScriptWindow):
	
	def __init__(self, new_pet):
		ui.ScriptWindow.__init__(self)
		self.__LoadWindow()
		self.LoadPetIncubatorImg(new_pet)

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		ui.ScriptWindow.Show(self)

	def Close(self):
		self.Hide()
	
	def __LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/PetHatchingWindow.py")
		except:
			import exception
			exception.Abort("PetHatchingWindow.LoadWindow.LoadObject")
			
		try:
			self.board = self.GetChild("board")
			self.boardtitle = self.GetChild("PetHatching_TitleBar")
			
			self.petimg = self.GetChild("HatchingItemSlot")
			self.petname = self.GetChild("pet_name")
			self.HatchingButton = self.GetChild("HatchingButton")
			
			
			#Event
			self.boardtitle.SetCloseEvent(ui.__mem_func__(self.Close))
			self.HatchingButton.SetEvent(ui.__mem_func__(self.RequestHatching,))
			
			
		except:
			import exception
			exception.Abort("PetHatchingWindow.LoadWindow.BindObject")
			
	def LoadPetIncubatorImg(self, new_pet):
		petarryname = ["Ou de maimuþã", "Ou de pãianjen", "Ou Razador", "Ou Nemere", "Ou de dragon albastru", "Ou de dragonit", "Ou Azrael", "Ou dolofan de cãlãu", "Ou Bebeluº Baashido", "Ou Nessie"]
		petarryimg = [55701, 55702, 55703, 55704, 55705, 55706, 55707, 55708, 55709, 55710]
		chat.AppendChat(chat.CHAT_TYPE_INFO, "Incubator: "+petarryname[int(new_pet)]+".")
		self.petimg.SetItemSlot(0,petarryimg[int(new_pet)], 0)
		self.petimg.SetAlwaysRenderCoverButton(0, TRUE)
		#self.petimg.SetSlotBaseImage("icon/item/"+petarryimg[new_pet], 0, 0, 0, 0)
		
		
			
			
	def RequestHatching(self):
		if self.petname.GetText() == "" or len(self.petname.GetText()) < 4:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Numele petului nu este valid.")
			return
			
		if player.GetElk() < 100000:
			#chat.AppendChat(chat.CHAT_TYPE_INFO, "[Pet-Incubator]Devi possedere "+str(localeInfo.NumberToMoneyString(100000)) +".")
			return
			
		chat.AppendChat(chat.CHAT_TYPE_INFO, "Il tuo pet e' nato!")
		import chr
		chr.RequestPetName(self.petname.GetText())
		self.Close()


			


