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
import uicommon
class teleportwindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadWindow()
	
	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		ui.ScriptWindow.Show(self)

	def Close(self):
		self.Hide()
		constInfo.TELEPORT_SYSTEM_GUI = 0
		
	def OnPressEscapeKey(self):
		self.Close()
		return TRUE	

	def __LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/teleportwindow.py")
		except:
			import exception
			exception.Abort("TeleportWindow.LoadWindow.LoadObject")
			
		try:
		
			#Button
			self.board = self.GetChild("board")
			self.boardclose = self.GetChild("CloseButton")
			self.capitalebutton = self.GetChild("CapitaleButton")
			self.vallebutton = self.GetChild("ValleButton")
			self.covobutton = self.GetChild("CovoButton")
			self.montebutton = self.GetChild("MonteButton")
			self.grottabutton = self.GetChild("GrottaButton")
			self.desertobutton = self.GetChild("DesertoButton")
			self.capobutton = self.GetChild("CapoButton")
			self.boscobutton = self.GetChild("BoscoButton")
			self.fantasmabutton = self.GetChild("FantasmaButton")
			self.fuocobutton = self.GetChild("FuocoButton")
			#self.tonantibutton = self.GetChild("TonantiButton")
			self.torrebutton = self.GetChild("TorreButton")
			self.eruzionebutton = self.GetChild("EruzioneButton")
	
			#Event
			self.boardclose.SetEvent(ui.__mem_func__(self.Close))
			self.capitalebutton.SetEvent(ui.__mem_func__(self.CapitaleTeleport))
			self.vallebutton.SetEvent(ui.__mem_func__(self.ValleTeleport))
			self.covobutton.SetEvent(ui.__mem_func__(self.CovoTeleport))
			self.montebutton.SetEvent(ui.__mem_func__(self.MonteTeleport))
			self.grottabutton.SetEvent(ui.__mem_func__(self.GrottaTeleport))
			self.desertobutton.SetEvent(ui.__mem_func__(self.DesertoTeleport))
			self.capobutton.SetEvent(ui.__mem_func__(self.CapoTeleport))
			self.boscobutton.SetEvent(ui.__mem_func__(self.BoscoTeleport))
			self.fantasmabutton.SetEvent(ui.__mem_func__(self.FantasmaTeleport))
			self.fuocobutton.SetEvent(ui.__mem_func__(self.FuocoTeleport))
			#self.tonantibutton.SetEvent(ui.__mem_func__(self.TonantiTeleport))
			self.torrebutton.SetEvent(ui.__mem_func__(self.TorreTeleport))
			self.eruzionebutton.SetEvent(ui.__mem_func__(self.EruzioneTeleport))
			
		except:
			import exception
			exception.Abort("PetInformationWindow.LoadWindow.BindObject")

			
	def CapitaleTeleport(self):
		self.Capitale = uicommon.QuestionDialog()
		self.Capitale.SetText("Vrei s� c�l�tore�ti �n Capital�?")
		self.Capitale.SetAcceptEvent(ui.__mem_func__(self.AccettaCapitale))
		self.Capitale.SetCancelEvent(ui.__mem_func__(self.Capitale.Close))
		self.Capitale.Open()
		
	def ValleTeleport(self):
		self.Valle = uicommon.QuestionDialog()
		self.Valle.SetText("Vrei s� c�l�tore�ti �n Vale?")
		self.Valle.SetAcceptEvent(ui.__mem_func__(self.AccettaValle))
		self.Valle.SetCancelEvent(ui.__mem_func__(self.Valle.Close))
		self.Valle.Open()
		
	def CovoTeleport(self):
		self.Covo = uicommon.QuestionDialog()
		self.Covo.SetText("Vrei s� c�l�tore�ti �n Temni�a P�ianjenilor")
		self.Covo.SetAcceptEvent(ui.__mem_func__(self.AccettaCovo))
		self.Covo.SetCancelEvent(ui.__mem_func__(self.Covo.Close))
		self.Covo.Open()

	def MonteTeleport(self):
		self.Monte = uicommon.QuestionDialog()
		self.Monte.SetText("Vrei s� c�l�tore�ti la Muntele Sohan?")
		self.Monte.SetAcceptEvent(ui.__mem_func__(self.AccettaMonte))
		self.Monte.SetCancelEvent(ui.__mem_func__(self.Monte.Close))
		self.Monte.Open()

	def GrottaTeleport(self):
		self.Grotta = uicommon.QuestionDialog()
		self.Grotta.SetText("Vrei s� c�l�tore�ti �n Grota Exilului?")
		self.Grotta.SetAcceptEvent(ui.__mem_func__(self.AccettaGrotta))
		self.Grotta.SetCancelEvent(ui.__mem_func__(self.Grotta.Close))
		self.Grotta.Open()
		
	def DesertoTeleport(self):
		self.Deserto = uicommon.QuestionDialog()
		self.Deserto.SetText("Vrei s� c�l�tore�ti �n de�ertul Yongbi?")
		self.Deserto.SetAcceptEvent(ui.__mem_func__(self.AccettaDeserto))
		self.Deserto.SetCancelEvent(ui.__mem_func__(self.Deserto.Close))
		self.Deserto.Open()
		
	def CapoTeleport(self):
		self.Capo = uicommon.QuestionDialog()
		self.Capo.SetText("Vrei s� c�l�tore�ti �n De�ertul Arid?")
		self.Capo.SetAcceptEvent(ui.__mem_func__(self.AccettaCapo))
		self.Capo.SetCancelEvent(ui.__mem_func__(self.Capo.Close))
		self.Capo.Open()
		
	def BoscoTeleport(self):
		self.Bosco = uicommon.QuestionDialog()
		self.Bosco.SetText("Vrei s� c�l�tore�ti �n P�durea Ro�ie?")
		self.Bosco.SetAcceptEvent(ui.__mem_func__(self.AccettaBosco))
		self.Bosco.SetCancelEvent(ui.__mem_func__(self.Bosco.Close))
		self.Bosco.Open()
		
	def FantasmaTeleport(self):
		self.Fantasma = uicommon.QuestionDialog()
		self.Fantasma.SetText("Vrei s� c�l�tore�ti �n Lungsam?")
		self.Fantasma.SetAcceptEvent(ui.__mem_func__(self.AccettaFantasma))
		self.Fantasma.SetCancelEvent(ui.__mem_func__(self.Fantasma.Close))
		self.Fantasma.Open()
		
	def FuocoTeleport(self):
		self.Fuoco = uicommon.QuestionDialog()
		self.Fuoco.SetText("Vrei s� c�l�tore�ti �n �ara de Foc?")
		self.Fuoco.SetAcceptEvent(ui.__mem_func__(self.AccettaFuoco))
		self.Fuoco.SetCancelEvent(ui.__mem_func__(self.Fuoco.Close))
		self.Fuoco.Open()
		
	#def TonantiTeleport(self):
		#self.Tonanti = uicommon.QuestionDialog()
		#self.Tonanti.SetText("Vuoi viaggiare verso la Valle dell'Oblio?")
		#self.Tonanti.SetAcceptEvent(ui.__mem_func__(self.AccettaTonanti))
		#self.Tonanti.SetCancelEvent(ui.__mem_func__(self.Tonanti.Close))
		#self.Tonanti.Open()
		
	def TorreTeleport(self):
		self.Torre = uicommon.QuestionDialog()
		self.Torre.SetText("Vrei s� c�l�tore�ti �n Turnul Demonilor?")
		self.Torre.SetAcceptEvent(ui.__mem_func__(self.AccettaTorre))
		self.Torre.SetCancelEvent(ui.__mem_func__(self.Torre.Close))
		self.Torre.Open()
		
	def EruzioneTeleport(self):
		self.Eruzione = uicommon.QuestionDialog()
		self.Eruzione.SetText("Vuoi viaggiare verso Eruzione?")
		self.Eruzione.SetAcceptEvent(ui.__mem_func__(self.AccettaEruzione))
		self.Eruzione.SetCancelEvent(ui.__mem_func__(self.Eruzione.Close))
		self.Eruzione.Open()

	def AccettaCapitale(self):
		net.SendChatPacket("/capitale_teleport")
		self.Capitale.Close()
		
	def AccettaValle(self):
		net.SendChatPacket("/valle_teleport")
		self.Valle.Close()

	def AccettaCovo(self):
		net.SendChatPacket("/covo_teleport")
		self.Covo.Close()
		
	def AccettaMonte(self):
		net.SendChatPacket("/monte_teleport")
		self.Monte.Close()
		
	def AccettaGrotta(self):
		net.SendChatPacket("/grotta_teleport")
		self.Grotta.Close()
		
	def AccettaDeserto(self):
		net.SendChatPacket("/deserto_teleport")
		self.Deserto.Close()
		
	def AccettaCapo(self):
		net.SendChatPacket("/capo_teleport")
		self.Capo.Close()
		
	def AccettaBosco(self):
		net.SendChatPacket("/bosco_teleport")
		self.Bosco.Close()
		
	def AccettaFantasma(self):
		net.SendChatPacket("/fantasma_teleport")
		self.Fantasma.Close()
		
	def AccettaFuoco(self):
		net.SendChatPacket("/fuoco_teleport")
		self.Fuoco.Close()
		
	#def AccettaTonanti(self):
	#	net.SendChatPacket("/tonanti_teleport")
		#self.Tonanti.Close()
		
	def AccettaTorre(self):
		net.SendChatPacket("/torre_teleport")
		self.Torre.Close()
		
	def AccettaEruzione(self):
		net.SendChatPacket("/eruzione_teleport")
		self.Eruzione.Close()