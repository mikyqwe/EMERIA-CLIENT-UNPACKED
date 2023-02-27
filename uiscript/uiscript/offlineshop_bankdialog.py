import uiScriptLocale
import background


window = {
	"name" : "OfflineShopBankWindow",
	
	"style" : ("movable", "float", ),
	
	"x" : 0,
	"y" : 0,
	
	"width" : 200,
	"height" : 395+20,
	
	"children" :
	(
		{
			"name" : "Board",
			"type" : "board_with_titlebar",
			
			"style" : ("attach", ),
			
			"x" : 0,
			"y" : 0,
			
			"width" : 200,
			"height" : 395+20,
			
			"title" : "Çevrim Dýþý Pazar - Banka",
			
			"children" :
			(	
				# Yazilar
				{
					"name" : "para",
					"type" : "thinboard",

					"x" : 0,
					"y" : 35,
					"width" : 170,
					"height" : 147*2-40,
					"horizontal_align" : "center",

					"children" :
					(
						#Yang_Ep_Won_ThinBoard
						{
							"name" : "Yang_Ep_Won_ThinBoard",
							"type" : "thinboard",
					
							"x" : 0,
							"y" : 256+5,
								
							"width" : 180,
							"height" : 55,	
							"horizontal_align" : "center",							
						},
						{
							"name" : "background",
							"type" : "image",
							"x" : 0,
							"y" : 0,
							"image" : "title.tga",
							"text_horizontal_align":"center"
						},
						{
							"name" : "text1",
							"type" : "text",
							"x" : 40,
							"y" : 5,
							"text" : "Ce este in bancã :",
						#	"text_horizontal_align":"center"
						},
						#Slot & Item Icon
						{"name":"RedOt", "type":"image", "x":15,"y":30,"image" : "d:/ymir work/ui/public/Slot_Base.sub"},
						{"name":"RedOtItem", "type":"image", "x":15,"y":30,"image" : "icon/item/70251.tga"},						
						{"name":"BlueOt", "type":"image", "x":15,"y":60+5,"image" : "d:/ymir work/ui/public/Slot_Base.sub"},
						{"name":"BlueOtItem", "type":"image", "x":15,"y":60+5,"image" : "icon/item/70252.tga"},						
						{"name":"GreenOt", "type":"image", "x":15,"y":90+10,"image" : "d:/ymir work/ui/public/Slot_Base.sub"},
						{"name":"GreenOtItem", "type":"image", "x":15,"y":90+10,"image" : "icon/item/70253.tga"},						
						{"name":"PurpleOt", "type":"image", "x":15,"y":120+15,"image" : "d:/ymir work/ui/public/Slot_Base.sub"},
						{"name":"PurpleOtItem", "type":"image", "x":15,"y":120+15,"image" : "icon/item/70254.tga"},
						{"name":"RuhTasi", "type":"image", "x":15,"y":150+20,"image" : "d:/ymir work/ui/public/Slot_Base.sub"},
						{"name":"RuhTasiItem", "type":"image", "x":15,"y":150+20,"image" : "icon/item/50513.tga"},						
						{"name":"Bar", "type":"image", "x":15,"y":180+25,"image" : "d:/ymir work/ui/public/Slot_Base.sub"},
						{"name":"BarItem", "type":"image", "x":15,"y":180+25,"image" : "icon/item/80007.tga"},
						#Yang & EP & Won Slot
						{"name":"Yang_Icon", "type":"image", "x":9,"y":262+8,"image" : "d:/ymir work/ui/game/windows/money_icon.sub"},
						{"name":"Cheque_Icon", "type":"image", "x":9,"y":262+25+8,"image" : "bank_icon/cheque_icon.sub"},
						{"name":"DragonMoney_Icon", "type":"image", "x":83,"y":262+25+8,"image" : "bank_icon/ep_icon.sub"},						
						{
							"name" : "CurrentMoneySlot",
							"type" : "slotbar",
							
							"x" : 60,
							"y" : 35,
							
							"width" : 180/2+40-30,
							"height" : 15,
							
							"children" :
							(
								{
									"name" : "CurrentMoneyLine",
									"type" : "text",
									
									"x" : 3,
									"y" : 3,
									
									"width" : 210,
									"height" : 15,
									
									"input_limit" : 12,
									"text" : "0123456789",
								},
							),
						},
						{
							"name" : "CurrentMoneySlot",
							"type" : "slotbar",
							
							"x" : 60,
							"y" : 60+10,
							
							"width" : 180/2+40-30,
							"height" : 15,
							
							"children" :
							(
								{
									"name" : "CurrentMoneyLine2",
									"type" : "text",
									
									"x" : 3,
									"y" : 3,
									
									"width" : 210,
									"height" : 15,
									
									"input_limit" : 12,
									"text" : "0123456789",
								},
							),
						},
						{
							"name" : "CurrentMoneySlot",
							"type" : "slotbar",
							
							"x" : 60,
							"y" : 105,
							
							"width" : 180/2+40-30,
							"height" : 15,
							
							"children" :
							(
								{
									"name" : "CurrentMoneyLine3",
									"type" : "text",
									
									"x" : 3,
									"y" : 3,
									
									"width" : 210,
									"height" : 15,
									
									"input_limit" : 12,
									"text" : "0123456789",
								},
							),
						},
						{
							"name" : "CurrentMoneySlot",
							"type" : "slotbar",
							
							"x" : 60,
							"y" : 140,
							
							"width" : 180/2+40-30,
							"height" : 15,
							
							"children" :
							(
								{
									"name" : "CurrentMoneyLine4",
									"type" : "text",
									
									"x" : 3,
									"y" : 3,
									
									"width" : 210,
									"height" : 15,
									
									"input_limit" : 12,
									"text" : "0123456789",
								},
							),
						},
						{
							"name" : "CurrentMoneySlot",
							"type" : "slotbar",
							
							"x" : 60,
							"y" : 175,
							
							"width" : 180/2+40-30,
							"height" : 15,
							
							"children" :
							(
								{
									"name" : "CurrentMoneyLine5",
									"type" : "text",
									
									"x" : 3,
									"y" : 3,
									
									"width" : 210,
									"height" : 15,
									
									"input_limit" : 12,
									"text" : "0123456789",
								},
							),
						},
						{
							"name" : "CurrentMoneySlot",
							"type" : "slotbar",
							
							"x" : 60,
							"y" : 210,
							
							"width" : 180/2+40-30,
							"height" : 15,
							
							"children" :
							(
								{
									"name" : "CurrentMoneyLine6",
									"type" : "text",
									
									"x" : 3,
									"y" : 3,
									
									"width" : 210,
									"height" : 15,
									
									"input_limit" : 12,
									"text" : "0123456789",
								},
							),
						},
						#Line7 = Yang , Line8 = Won , Line9 = Ejderha Parasý
						{
							"name" : "CurrentMoneySlot",
							"type" : "slotbar",
							
							"x" : 27,
							"y" : 260+8,
							
							"width" : 180/2+40-2,
							"height" : 15,
							
							"children" :
							(
								{
									"name" : "CurrentMoneyLine7",
									"type" : "text",
									
									"x" : 3,
									"y" : 3,
									
									"width" : 210,
									"height" : 15,
									
									"input_limit" : 12,
									"text" : "0123456789",
								},
							),
						},
						{
							"name" : "CurrentMoneySlot",
							"type" : "slotbar",
							
							"x" : 27,
							"y" : 260+25+8,
							
							"width" : 180/2-35-2,
							"height" : 15,
							
							"children" :
							(
								{
									"name" : "CurrentMoneyLine8",
									"type" : "text",
									
									"x" : 3,
									"y" : 3,
									
									"width" : 210,
									"height" : 15,
									
									"input_limit" : 12,
									"text" : "0123456789",
								},
							),
						},
						{
							"name" : "CurrentMoneySlot",
							"type" : "slotbar",
							
							"x" : 102,
							"y" : 260+25+8,
							
							"width" : 180/2-35-2,
							"height" : 15,
							
							"children" :
							(
								{
									"name" : "CurrentMoneyLine9",
									"type" : "text",
									
									"x" : 3,
									"y" : 3,
									
									"width" : 210,
									"height" : 15,
									
									"input_limit" : 12,
									"text" : "0123456789",
								},
							),
						},
					),
				},
				
				# butonlar
				{
					"name" : "butonlar",
					"type" : "thinboard",

					"x" : 0,
					"y" : 360,
					"width" : 180,
					"height" : 40,
					"horizontal_align" : "center",

					"children" :
					(
						{
							"name" : "withdraw_button",
							"type" : "button",
							
							"x" : 9,
							"y" : 7,
							
							"text" : "Verificã",
							
							"default_image" : "d:/ymir work/efsun_gui2/offical_button.tga",
							"over_image" : "d:/ymir work/efsun_gui2/offical_button_bastim.tga",
							"down_image" : "d:/ymir work/efsun_gui2/offical_button_bastim.tga",
						},
						{
							"name" : "refesh_button",
							"type" : "button",
							
							"x" : 90,
							"y" : 7,
							
							"text" : "Refresh",
							
							"default_image" : "d:/ymir work/efsun_gui2/offical_button.tga",
							"over_image" : "d:/ymir work/efsun_gui2/offical_button_bastim.tga",
							"down_image" : "d:/ymir work/efsun_gui2/offical_button_bastim.tga",
						},						
					),
				},
			),
		},
	),
}