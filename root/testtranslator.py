#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import ui
import wndMgr
import grp
from googletrans import Translator
## Ente ente ente ente

''' 
## Available languages
{
	'gu': 'gujarati', 'gd': 'scots gaelic', 'ga': 'irish', 'gl': 'galician', 'lb': 'luxembourgish', 'la': 'latin',
	'lo': 'lao', 'tr': 'turkish', 'lv': 'latvian', 'lt': 'lithuanian', 'th': 'thai', 'tg': 'tajik', 'te': 'telugu', 
	'fil': 'Filipino', 'haw': 'hawaiian', 'yi': 'yiddish', 'ceb': 'cebuano', 'yo': 'yoruba', 'de': 'german', 'da': 'danish', 
	'el': 'greek', 'eo': 'esperanto', 'en': 'english', 'eu': 'basque', 'et': 'estonian', 'es': 'spanish', 'ru': 'russian', 
	'zh-cn': 'chinese (simplified)', 'ro': 'romanian', 'be': 'belarusian', 'bg': 'bulgarian', 'uk': 'ukrainian', 'bn': 'bengali', 
	'jw': 'javanese', 'bs': 'bosnian', 'ja': 'japanese', 'xh': 'xhosa', 'co': 'corsican', 'ca': 'catalan', 'cy': 'welsh',
	'cs': 'czech', 'ps': 'pashto', 'pt': 'portuguese', 'zh-tw': 'chinese (traditional)', 'tl': 'filipino', 'pa': 'punjabi', 
	'vi': 'vietnamese', 'pl': 'polish', 'hy': 'armenian', 'hr': 'croatian', 'ht': 'haitian creole', 'hu': 'hungarian', 'hmn': 'hmong', 
	'hi': 'hindi', 'ha': 'hausa', 'he': 'Hebrew', 'mg': 'malagasy', 'uz': 'uzbek', 'ml': 'malayalam', 'mn': 'mongolian', 'mi': 'maori', 
	'mk': 'macedonian', 'ur': 'urdu', 'mt': 'maltese', 'ms': 'malay', 'mr': 'marathi', 'ta': 'tamil', 'my': 'myanmar (burmese)', 'af': 'afrikaans', 
	'sw': 'swahili', 'is': 'icelandic', 'am': 'amharic', 'it': 'italian', 'iw': 'hebrew', 'sv': 'swedish', 'ar': 'arabic', 'su': 'sundanese', 
	'zu': 'zulu', 'az': 'azerbaijani', 'id': 'indonesian', 'ig': 'igbo', 'nl': 'dutch', 'no': 'norwegian', 'ne': 'nepali', 'ny': 'chichewa', 
	'fr': 'french', 'ku': 'kurdish (kurmanji)', 'fy': 'frisian', 'fa': 'persian', 'fi': 'finnish', 'ka': 'georgian', 'kk': 'kazakh', 
	'sr': 'serbian', 'sq': 'albanian', 'ko': 'korean', 'kn': 'kannada', 'km': 'khmer', 'st': 'sesotho', 'sk': 'slovak', 'si': 'sinhala', 
	'so': 'somali', 'sn': 'shona', 'sm': 'samoan', 'sl': 'slovenian', 'ky': 'kyrgyz', 'sd': 'sindhi'
}
'''
AVAILABLE_LANGUAGES = {
	'tr': {
			'name':'turkish', 
			'encoding':'Windows-1254'
		},
	'de': {
			'name':'german', 
			'encoding':'Windows-1252'
		},
	'ro': {
			'name':'romanian', 
			'encoding':'ISO 8859-16'
		},
	'pl': {
			'name':'polish', 
			'encoding':'Windows-1250'
		},
	'es': {
			'name':'spanish', 
			'encoding':'iso-8859-1'
		},
	'en': {
			'name':'english', 
			'encoding':'Windows-1252'
		},
	'pt': {
			'name':'portuguese', 
			'encoding':'Windows-1252'
		}
}

TEXTLINE_MSG1 = '[STRG] - select text'
TEXTLINE_MSG2 = '[STRG+Shift] - multiselect text'
TEXTLINE_MSG3 = '[STRG+ALT] - translate directly'

class TextTranslator(ui.BoardWithTitleBar):
	def __init__(self):
		ui.BoardWithTitleBar.__init__(self)
		self.isLoaded = FALSE
		if FALSE == self.isLoaded:
			self.__LoadMe()

	def __del__(self):
		ui.BoardWithTitleBar.__del__(self)
		
	def __LoadMe(self):
		self.SetSize(200+30, 200+15+15+15)
		self.SetCenterPosition()
		self.AddFlag('movable')
		self.SetTitleName("Translator by Ente")
		self.SetCloseEvent(self.Close)

		textLine1 = ui.TextLine()
		textLine1.SetParent(self)
		textLine1.SetPosition(15, 35)
		textLine1.SetSize(200 -15 -15, 15)
		textLine1.SetText(TEXTLINE_MSG1)
		textLine1.Show()
		self.textLine1 = textLine1

		textLine2 = ui.TextLine()
		textLine2.SetParent(self)
		textLine2.SetPosition(15, 35+15)
		textLine2.SetSize(200 -15 -15, 15)
		textLine2.SetText(TEXTLINE_MSG2)
		textLine2.Show()
		self.textLine2 = textLine2

		textLine3 = ui.TextLine()
		textLine3.SetParent(self)
		textLine3.SetPosition(15, 35+15+15)
		textLine3.SetSize(200 -15 -15, 15)
		textLine3.SetText(TEXTLINE_MSG3)
		textLine3.Show()
		self.textLine3 = textLine3

		self.slotbarTranslateFrom, self.editlineTranslateFrom = self.CreateEditLine(self, "", 15, 35+15+15+15+(65*0), 200, 60, 120)
		self.slotbarTranslateTo, self.editlineTranslateTo = self.CreateEditLine(self, "", 15, 35+15+15+15+(65*1), 200, 60, 120)

		comboBoxLanguageFrom = ui.ComboBox()
		comboBoxLanguageFrom.SetParent(self)
		comboBoxLanguageFrom.SetPosition(15,35+15+15+15+(65*2))
		comboBoxLanguageFrom.SetSize(50, 20)
		comboBoxLanguageFrom.ClearItem()

		comboBoxLanguageTo = ui.ComboBox()
		comboBoxLanguageTo.SetParent(self)
		comboBoxLanguageTo.SetPosition(15+60,35+15+15+15+(65*2))
		comboBoxLanguageTo.SetSize(50, 20)
		comboBoxLanguageTo.ClearItem()

		comboBoxLanguageFrom.InsertItem('auto', 'auto')
		for langKey, lang in AVAILABLE_LANGUAGES.iteritems():
			comboBoxLanguageFrom.InsertItem(langKey, lang['name'])
			comboBoxLanguageTo.InsertItem(langKey, lang['name'])

		self.languageFrom = 'auto'
		comboBoxLanguageFrom.SetCurrentItem(self.languageFrom)

		self.languageTo = '-- to --'
		comboBoxLanguageTo.SetCurrentItem(self.languageTo)
		
		self.comboBoxLanguageFrom = comboBoxLanguageFrom
		self.comboBoxLanguageFrom.SetEvent(self._OnSelectItemComboBoxLanguageFrom)

		self.comboBoxLanguageTo = comboBoxLanguageTo
		self.comboBoxLanguageTo.SetEvent(self._OnSelectItemComboBoxLanguageTo)

		self.comboBoxLanguageFrom.Show()
		self.comboBoxLanguageTo.Show()
		
		buttonTranslate = ui.Button()
		buttonTranslate.SetParent(self)
		buttonTranslate.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
		buttonTranslate.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
		buttonTranslate.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
		buttonTranslate.SetText("Translate")
		buttonTranslate.SetPosition(230-100,35+15+15+15+(65*2))
		buttonTranslate.SetEvent(self._OnClickButtonTranslate)
		buttonTranslate.Show()
		self.buttonTranslate = buttonTranslate

		self.lastTranslatedFromText = ''
		self.lastTranslatedLanguageTo = ''
		
		self.translator = Translator()

		self.isLoaded = True
		
	def SetTranslateFromText(self, text):
		if text and self.editlineTranslateFrom.GetText() != text:
			print("set new text")
			self.editlineTranslateFrom.SetText(text)

	def AppendTranslateFromText(self, text):
		if text and not text in self.editlineTranslateFrom.GetText():
			print("append new text")
			self.editlineTranslateFrom.SetText(self.editlineTranslateFrom.GetText()+' '+text)
		
	def _OnClickButtonTranslate(self):
		self.Translate()

	def Translate(self):
		print("try to translate...")
		textToTranslate = self.editlineTranslateFrom.GetText()
		if self.languageTo != 'To' and textToTranslate != '' and not (textToTranslate == self.lastTranslatedFromText and self.languageTo == self.lastTranslatedLanguageTo):
			print("translating...")
			if self.languageFrom == 'auto':
				detectedLang = self.translator.detect(unicode(textToTranslate, errors='replace'))
				# print("Language: %s" %detectedLang['lang'])
				translated = self.translator.translate(unicode(textToTranslate, errors='replace'), dest=self.languageTo)
			else:
				translated = self.translator.translate(unicode(textToTranslate, errors='replace'), src=self.languageFrom, dest=self.languageTo)
			self.editlineTranslateTo.SetText(translated.text.encode(AVAILABLE_LANGUAGES[self.languageTo]['encoding']))

			self.lastTranslatedFromText = textToTranslate
			self.lastTranslatedLanguageTo = self.languageTo

	def _OnSelectItemComboBoxLanguageFrom(self, id):
		if id == 'auto':
			self.comboBoxLanguageFrom.SetCurrentItem("Auto")
			
		else:
			self.comboBoxLanguageFrom.SetCurrentItem(AVAILABLE_LANGUAGES[id]['name'])
		self.languageFrom = id

	def _OnSelectItemComboBoxLanguageTo(self, id):
		self.comboBoxLanguageTo.SetCurrentItem(AVAILABLE_LANGUAGES[id]['name'])
		self.languageTo = id

	def CreateEditLine(self, parent, editlineText, x, y, width, height, max):
		slotBar = ui.SlotBar()
		if parent != None:
			slotBar.SetParent(parent)
		slotBar.SetSize(width, height)
		slotBar.SetPosition(x, y)
		slotBar.Show()
		editline = ui.EditLine()
		editline.SetParent(slotBar)
		editline.SetSize(width, height)
		editline.SetPosition(1, 1)
		editline.SetMax(max)
		editline.SetLimitWidth(width)
		editline.SetMultiLine()
		editline.SetText(editlineText)
		editline.Show()
		return slotBar, editline

	def Open(self):
		self.Show()
		self.SetTop()

	def Close(self):
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnPressExitKey(self):
		self.Close()
		return True

# wnd = TextTranslator()
# wnd.Open()