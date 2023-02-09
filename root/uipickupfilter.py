import ui, systemSetting, app

class PickupFilter(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.modeList = []
		self.modeAutoList = []
		self.filterList = []
		self.LoadDialog()
		self.__ClickFilterMode(systemSetting.GetPickupMode())
		self.__ClickFilterAutoMode(systemSetting.GetPickupAutoMode())
		self.RefreshPickupFilter()


	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadDialog(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/pickupfilter.py")
		except:
			import exception
			exception.Abort("PickupFilter.LoadDialog.BindObject")
		self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))

		self.modeList.append(self.GetChild("mode_old"))
		self.modeList.append(self.GetChild("mode_fast"))
		
		self.modeAutoList.append(self.GetChild("mode_auto_deactive"))
		self.modeAutoList.append(self.GetChild("mode_auto_active"))

		self.filterList.append(self.GetChild("filter_weapon"))#0
		self.filterList.append(self.GetChild("filter_armor"))#1
		self.filterList.append(self.GetChild("filter_ear"))#2
		self.filterList.append(self.GetChild("filter_neck"))#3
		self.filterList.append(self.GetChild("filter_foots"))#4
		self.filterList.append(self.GetChild("filter_shield"))#5
		self.filterList.append(self.GetChild("filter_head"))#6
		self.filterList.append(self.GetChild("filter_wrist"))#7
		self.filterList.append(self.GetChild("filter_book"))#8
		self.filterList.append(self.GetChild("filter_stone"))#9
		#self.filterList.append(self.GetChild("filter_etc"))#10
		self.GetChild("filter_etc").Hide()#empty

		self.modeList[0].SetToggleDownEvent(lambda arg=0: self.__ClickFilterMode(arg))
		self.modeList[1].SetToggleDownEvent(lambda arg=1: self.__ClickFilterMode(arg))
		
		self.modeAutoList[0].SetToggleDownEvent(lambda arg=0: self.__ClickFilterAutoMode(arg))
		self.modeAutoList[1].SetToggleDownEvent(lambda arg=1: self.__ClickFilterAutoMode(arg))

		for j in xrange(len(self.filterList)):
			self.filterList[j].SetToggleDownEvent(lambda arg=0,arg2=j: self.__SetFilterMode(arg,arg2))
			self.filterList[j].SetToggleUpEvent(lambda arg=1,arg2=j: self.__SetFilterMode(arg,arg2))

	def __SetFilterMode(self, arg, type):
		flag_list = [systemSetting.PICKUP_FILTER_WEAPON,systemSetting.PICKUP_FILTER_ARMOR,systemSetting.PICKUP_FILTER_EAR,systemSetting.PICKUP_FILTER_NECK,systemSetting.PICKUP_FILTER_FOOTS,systemSetting.PICKUP_FILTER_SHIELD,systemSetting.PICKUP_FILTER_HEAD,systemSetting.PICKUP_FILTER_WRIST,systemSetting.PICKUP_FILTER_BOOK,systemSetting.PICKUP_FILTER_STONE,systemSetting.PICKUP_FILTER_ETC]
		if arg == 0:
			flag = systemSetting.SetBit(systemSetting.GetPickupFilter(),flag_list[type])
			systemSetting.SetPickupFilter(flag)
		elif arg == 1:
			flag = systemSetting.RemoveBit(systemSetting.GetPickupFilter(),flag_list[type])
			systemSetting.SetPickupFilter(flag)
		self.RefreshPickupFilter()

	def RefreshPickupFilter(self):
		flag_list = [systemSetting.PICKUP_FILTER_WEAPON,systemSetting.PICKUP_FILTER_ARMOR,systemSetting.PICKUP_FILTER_EAR,systemSetting.PICKUP_FILTER_NECK,systemSetting.PICKUP_FILTER_FOOTS,systemSetting.PICKUP_FILTER_SHIELD,systemSetting.PICKUP_FILTER_HEAD,systemSetting.PICKUP_FILTER_WRIST,systemSetting.PICKUP_FILTER_BOOK,systemSetting.PICKUP_FILTER_STONE,systemSetting.PICKUP_FILTER_ETC]
		for j in xrange(len(self.filterList)):
			if systemSetting.IsSet(systemSetting.GetPickupFilter(),flag_list[j]):
				self.filterList[j].Down()
			else:
				self.filterList[j].SetUp()

	def __ClickFilterMode(self, index):
		self.__ClickRadioButton(self.modeList, index)
		systemSetting.SetPickupMode(index)

	def __ClickFilterAutoMode(self, index):
		self.__ClickRadioButton(self.modeAutoList, index)
		systemSetting.SetPickupAutoMode(index)

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def __ClickRadioButton(self, buttonList, buttonIndex):
		try:
			selButton=buttonList[buttonIndex]
		except IndexError:
			return
		for eachButton in buttonList:
			eachButton.SetUp()
		selButton.Down()

	def Close(self):
		self.Hide()
