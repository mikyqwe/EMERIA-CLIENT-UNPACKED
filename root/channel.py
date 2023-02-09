import net, constInfo, ui, background, time, chat
	###################################################################################################################
	# Skype: sacadatt.amazon 
	###################################################################################################################
class Titan2_Channel_Changer(ui.BoardWithTitleBar):
	def __init__(self):
		ui.BoardWithTitleBar.__init__(self)
		
		self.Destroy()
		self.__LoadWindow()

	def __del__(self):
		self.Destroy()
		ui.BoardWithTitleBar.__del__(self)

	def Destroy(self):
		self.isLoaded = 0
		self.opened = 0
		self.vegas_change = None

	def OnPressEscapeKey(self):
		self.Close()
		return True
		
	def __LoadWindow(self):
		if self.isLoaded == 1:
			return
		
		self.isLoaded = 1
		
		self.AddFlag("movable")
		self.AddFlag("float")
		self.SetTitleName("Cambia Canale") # Title name
		self.SetCloseEvent(self.Close)
		
		x = 0
		
		self.channel_list = []
		
		for ch in xrange(4): # Sets the number of ch's, and we will automatically add buttons.
			channel_button = ui.Button()
			channel_button.SetParent(self)
			channel_button.SetSize(80, 80)
			channel_button.SetPosition(30, 48 + (40 * x + x))
			
			channel_button.SetUpVisual("d:/ymir work/ui/game/myshop_deco/public_store_001.dds")
			channel_button.SetOverVisual("d:/ymir work/ui/game/myshop_deco/public_store_002.dds")
			channel_button.SetDownVisual("d:/ymir work/ui/game/myshop_deco/public_store_003.dds")
			channel_button.SetEvent(ui.__mem_func__(self.change_channel), ch) # Apply function + ch , function ch1 / ch2 etc.
			
			channel_button.SetText("Channel " + str(ch+1))
			channel_button.Show()
			
			self.channel_list.append(channel_button)
			x = x + 1
		
		self.SetSize(209, 50 + (40 * x + x)) 
		self.SetCenterPosition()
		
	def Open(self):
		if self.opened == 1:
			return
			
		self.__LoadWindow()
		self.Show()
		self.opened = 1
		
	def protect_maps(self):
		protect_list = [
			"season99/new_map_ox",
			"maps_dungeon/devils_zone",
			"maps_dungeon/dt_zone",
			"maps_vegas/wedding_zone",
			"maps_dungeon/spider_3",  
			"maps_vegas/duel_zone",
		]
		if str(background.GetCurrentMapName()) in protect_list:
			return TRUE
		return FALSE    		
		
	def change_channel(self, ch):
		if self.protect_maps():  #Block change in some maps who are in <protect_list>.
			chat.AppendChat(1, "Non puoi cambiare channel in questa mappa.")
			return	
		elif time.clock() >= constInfo.change_time:			
			self.Close()
			net.SetServerInfo("Emeria - Channel %d" % int(ch+1)) # Set ch name under the minimap and you're on.
			#chat.AppendChat(chat.CHAT_TYPE_INFO, "[Change Channel] You have successfully changed the channel!")
			net.SendChatPacket("/ch %d" % int(ch+1)) # Application change control ch + 1 which are added in <xrange(4)>.
			constInfo.change_time = time.clock() + 4 # After pressing the button, the system adds 10 seconds to hold.
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Devi aspettare un attimo per cambiare channel.")		
		
	def	Close(self):
		self.Hide()
		self.opened = 0
	