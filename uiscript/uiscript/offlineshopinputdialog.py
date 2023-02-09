import uiScriptLocale
PATH = "d:/ymir work/ui/"
WINDOW_WIDTH = 225
WINDOW_HEIGHT = 275 + 30
DESC_WINDOW_WIDTH = WINDOW_WIDTH - 150
DESC_WINDOW_HEIGHT = WINDOW_HEIGHT - 220
window = {
	"name": "OfflineShopInputDialog",
	"x": 0,
	"y": 0,
	"style": ("movable", "float", "animate"),
	"width": WINDOW_WIDTH,
	"height": WINDOW_HEIGHT,
	"children":
	(
		{
			"name": "board",
			"type": "board",
			"style": ("attach",),
			"x": 0,
			"y": 0,
			"width": WINDOW_WIDTH,
			"height": WINDOW_HEIGHT,
			"children":
			(
				{
					"name": "TitleBar",
					"type": "titlebar",
					"style": ("attach",),
					"x": 8,
					"y": 7,
					"width": WINDOW_WIDTH - 14,
					"color": "yellow",
					"children":
					(
						{
							"name": "TitleName",
							"type": "text",
							"x": WINDOW_WIDTH / 2,
							"y": 3,
							"text": uiScriptLocale.OFFSHOP_TITLE_SYSTEM,
							"text_horizontal_align": "center"
						},
					)
				},
				{
					"name": "board_select_open_header_1",
					"type": "expanded_image",
					"style": ("attach",),
					"x": 25,
					"y": 38,
					"image": "d:/ymir work/ui/offlineshop_bg2.tga"
				},
				{
					"name": "board_select_open_text_1",
					"type": "text",
					"x": 72,
					"y": 40,
					"text": uiScriptLocale.OFFSHOP_CREATE_SYSTEM,
				},
				{
					"name": "OfflineShopTime",
					"type": "sliderbar",
					"x": 26,
					"y": 70
				},
				{
					"name": "time_value",
					"type": "text",
					"x": 66,
					"y": 80,
					"text": uiScriptLocale.DURATA_OFFSHOP,
				},
				{
					"name": "TimeInputValue",
					"type": "text",
					"x": 129,
					"y": 80,
					"text": "168 Ore",
					"color": 4284940032L
				},
				{
					"name": "shop_name",
					"type": "text",
					"x": 85,
					"y": 97,
					"text": uiScriptLocale.OFFSHOP1_NAME,
				},
				{
					"name": "InputSlot",
					"type": "slotbar",
					"x": 28,
					"y": 120,
					"width": 165,
					"height": 15,
					"children":
					(
						{
							"name": "InputValue",
							"type": "editline",
							"x": 1,
							"y": 1,
							"width": 165,
							"height": 15,
							"input_limit": 32
						},
					)
				},
				{
					"name": "board_select_open_header_2",
					"type": "expanded_image",
					"style": ("attach",),
					"x": 25,
					"y": 184,
					"image": "d:/ymir work/ui/offlineshop_bg2.tga"
				},
				{
					"name": "board_select_open_text_2",
					"type": "text",
					"x": 55,
					"y": 186,
					"text": uiScriptLocale.OFFSHOP1_MENU,
				},
				{
					"name": "AgreeButton",
					"type": "button",
					"x": 68,
					"y": 150,
					"default_image": "d:/ymir work/ui/public/large_button_01.sub",
					"over_image": "d:/ymir work/ui/public/large_button_02.sub",
					"down_image": "d:/ymir work/ui/public/large_button_03.sub",
					"text": uiScriptLocale.CREA_OFFSHOP1,
				},
				{
					"name": "BankButton",
					"type": "button",
					"x": 25,
					"y": 212,
					"default_image": "d:/ymir work/ui/public/large_button_01.sub",
					"over_image": "d:/ymir work/ui/public/large_button_02.sub",
					"down_image": "d:/ymir work/ui/public/large_button_03.sub",
					"text": uiScriptLocale.RETIRE_MONEY,
				},
				{
					"name": "RetrieveItems",
					"type": "button",
					"x": 114,
					"y": 212,
					"default_image": "d:/ymir work/ui/public/large_button_01.sub",
					"over_image": "d:/ymir work/ui/public/large_button_02.sub",
					"down_image": "d:/ymir work/ui/public/large_button_03.sub",
					"text": uiScriptLocale.RETIRE_ITEM,
				},
				{
					"name": "SearchButton",
					"type": "button",
					"x": 25,
					"y": 235,
					"default_image": "d:/ymir work/ui/public/large_button_01.sub",
					"over_image": "d:/ymir work/ui/public/large_button_02.sub",
					"down_image": "d:/ymir work/ui/public/large_button_03.sub",
					"text": uiScriptLocale.SEARCH_ITEM,
				},
				{
					"name": "CloseOfflineShop",
					"type": "button",
					"x": 114,
					"y": 235,
					"default_image": "d:/ymir work/ui/public/large_button_01.sub",
					"over_image": "d:/ymir work/ui/public/large_button_02.sub",
					"down_image": "d:/ymir work/ui/public/large_button_03.sub",
					"text": uiScriptLocale.OFFSHOP1_CLOSE,
				},
				
				{
					"name": "EditModeShopOffline",
					"type": "button",
					"x": 68,
					"y": 235+20,
					"default_image": "d:/ymir work/ui/public/large_button_01.sub",
					"over_image": "d:/ymir work/ui/public/large_button_02.sub",
					"down_image": "d:/ymir work/ui/public/large_button_03.sub",
					"text": uiScriptLocale.OFFSHOP1_EDIT,
				},
			),
		},
	),
}
