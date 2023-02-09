import uiScriptLocale
import localeInfo
 
ROOT = "d:/ymir work/ui/game/"
BOARD_WIDTH = 408
BOARD_HEIGHT = 222
window = {
		"name" : "ExchangeDialog",

		"x" : 0,
		"y" : 0,

		"style" : ("movable", "float",),

		"width" : BOARD_WIDTH,
		"height" : BOARD_HEIGHT,

		"children" :
		(
				{
						"name" : "board",
						"type" : "board",
						"style" : ("attach",),

						"x" : 0,
						"y" : 0,

						"width" : BOARD_WIDTH,
						"height" : BOARD_HEIGHT,

						"children" :
						(
								## Title
								{
										"name" : "TitleBar",
										"type" : "titlebar",
										"style" : ("attach",),

										"x" : 8,
										"y" : 8,

										"width" : 394,
										"color" : "gray",

										"children" :
										(
												{ "name":"TitleName", "type":"text", "x":192, "y":3, "text":uiScriptLocale.EXCHANGE_TITLE, "text_horizontal_align":"center" },
										),
								},

								## MiddleBar
								{
									"name" : "Middle_Bar",
									"type" : "expanded_image",

									"x" : (BOARD_WIDTH / 2) - 3,
									"y" : 33,
									"x_scale" : 2.0, 
									"y_scale" : 1.20,
									"image" : ROOT + "windows/middlebar.sub",
								},

								## Owner
								{
										"name" : "Owner",
										"type" : "window",

										"x" : 208,
										"y" : 33,

										"width" : 200,
										"height" : 189,

										"children" :
										(
												{
														"name" : "Owner_Slot",
														"type" : "grid_table",

														"start_index" : 0,

														"x" : 0,
														"y" : 0,

														"x_count" : 6,
														"y_count" : 4,
														"x_step" : 32,
														"y_step" : 32,
														"x_blank" : 0,
														"y_blank" : 0,

														"image" : "d:/ymir work/ui/public/slot_base.sub",
												},
												{
													"name" : "Owner_Cheque",
													"type" : "button",

													"x" : 10,
													"y" : 134,

													#"image" : "d:/ymir work/ui/public/parameter_slot_02.sub",

													"default_image" : "d:/ymir work/ui/public/parameter_slot_02.sub",
													"over_image" : "d:/ymir work/ui/public/parameter_slot_02.sub",
													"down_image" : "d:/ymir work/ui/public/parameter_slot_02.sub",

													"children" :
													(
														{
															"name" : "Owner_Cheque_Value",
															"type" : "text",

															"x" : 59,
															"y" : 2,

															"text" : "1234567",

															"text_horizontal_align" : "right",
														},
													),
												},
												{
														"name" : "Owner_Money",
														"type" : "button",

														"x" : 10,
														"y" : 160,

														#"image" : "d:/ymir work/ui/public/parameter_slot_02.sub",

														"default_image" : "d:/ymir work/ui/public/parameter_slot_02.sub",
														"over_image" : "d:/ymir work/ui/public/parameter_slot_02.sub",
														"down_image" : "d:/ymir work/ui/public/parameter_slot_02.sub",

														"children" :
														(
																{
																		"name" : "Owner_Money_Value",
																		"type" : "text",
 
																		"x" : 59,
																		"y" : 2,
 
																		"text" : "1234567",
 
																		"text_horizontal_align" : "right",
																},
														),
												},
												{
														"name" : "Owner_Accept_Light",
														"type" : "button",
 
														"x" : 105,
														"y" : 142,
 
														"default_image" : "d:/ymir work/ui/game/windows/accept_button_off.sub",
														"over_image" : "d:/ymir work/ui/game/windows/accept_button_off.sub",
														"down_image" : "d:/ymir work/ui/game/windows/accept_button_on.sub",
												},
												{
														"name" : "Owner_Accept_Button",
														"type" : "toggle_button",
 
														"x" : 130,
														"y" : 142,
 
														"text" : uiScriptLocale.EXCHANGE_ACCEPT,
 
														"default_image" : "d:/ymir work/ui/public/small_button_01.sub",
														"over_image" : "d:/ymir work/ui/public/small_button_02.sub",
														"down_image" : "d:/ymir work/ui/public/small_button_03.sub",
												},
												{	
													"name" : "strOwner_Cheque",	
													"type" : "button",
													"x" : 77,
													"y" : 135,

													"default_image" : "d:/ymir work/ui/game/currencies/won.tga",
													"over_image" : "d:/ymir work/ui/game/currencies/won.tga",
													"down_image" : "d:/ymir work/ui/game/currencies/won.tga",
													"tooltip_text": "Won",
												},
												{	
													"name" : "strOwner_Yang",	
													"type" : "button",
													"x" : 77,
													"y" : 161,

													"default_image" : "d:/ymir work/ui/game/currencies/yang.tga",
													"over_image" : "d:/ymir work/ui/game/currencies/yang.tga",
													"down_image" : "d:/ymir work/ui/game/currencies/yang.tga",
													"tooltip_text": "Yang",
												},
										),
								},
 
								## Target
								{
										"name" : "Target",
										"type" : "window",
 
										"x" : 10,
										"y" : 33,
 
										"width" : 200,
										"height" : 189,
 
										"children" :
										(
												{
														"name" : "Target_Slot",
														"type" : "grid_table",
 
														"start_index" : 0,
 
														"x" : 0,
														"y" : 0,
 
														"x_count" : 6,
														"y_count" : 4,
														"x_step" : 32,
														"y_step" : 32,
														"x_blank" : 0,
														"y_blank" : 0,
 
														"image" : "d:/ymir work/ui/public/slot_base.sub",
												},
												{
													"name" : "Target_Cheque",
													"type" : "image",

													"x" : 0,
													"y" : 134,

													"image" : "d:/ymir work/ui/public/parameter_slot_02.sub",

													"children" :
													(
														{
															"name" : "Target_Cheque_Value",
															"type" : "text",

															"x" : 59,
															"y" : 2,

															"text" : "1234567",

															"text_horizontal_align" : "right",
														},
													),
												},
												{
														"name" : "Target_Money",
														"type" : "image",
 
														"x" : 0,
														"y" : 160,
 
														"image" : "d:/ymir work/ui/public/parameter_slot_02.sub",
 
														"children" :
														(
																{
																		"name" : "Target_Money_Value",
																		"type" : "text",
 
																		"x" : 59,
																		"y" : 2,
 
																		"text" : "1234567",
 
																		"text_horizontal_align" : "right",
																},
														),
												},
												{
														"name" : "Target_Accept_Light",
														"type" : "button",
 
														"x" : 95,
														"y" : 142,
 
														"default_image" : "d:/ymir work/ui/game/windows/accept_button_off.sub",
														"over_image" : "d:/ymir work/ui/game/windows/accept_button_off.sub",
														"down_image" : "d:/ymir work/ui/game/windows/accept_button_on.sub",
												},
												{	
													"name" : "strTarget_Cheque",	
													"type" : "button",
													"x" : 67,
													"y" : 135,

													"default_image" : "d:/ymir work/ui/game/currencies/won.tga",
													"over_image" : "d:/ymir work/ui/game/currencies/won.tga",
													"down_image" : "d:/ymir work/ui/game/currencies/won.tga",
													"tooltip_text": "Won",
												},
												{	
													"name" : "strTarget_Yang",	
													"type" : "button",
													"x" : 67,
													"y" : 161,

													"default_image" : "d:/ymir work/ui/game/currencies/yang.tga",
													"over_image" : "d:/ymir work/ui/game/currencies/yang.tga",
													"down_image" : "d:/ymir work/ui/game/currencies/yang.tga",
													"tooltip_text": "Yang",
												},
										),
								},
						),
				},
		),
	}