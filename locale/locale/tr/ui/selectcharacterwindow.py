import uiScriptLocale
import app

ROOT_PATH = "d:/ymir work/ui/public/"
LOCALE_PATH = uiScriptLocale.SELECT_PATH

BOARD_X = SCREEN_WIDTH * (65) / 800
BOARD_Y = SCREEN_HEIGHT * (220) / 600



BOARD_ITEM_ADD_POSITION = -40

BASE_PATH = "selectwindow/"

window = {
	"name" : "SelectCharacterWindow",

	"x" : 0,
	"y" : 0,

	"width" : SCREEN_WIDTH,
	"height" : SCREEN_HEIGHT,

	"children" :
	(
		## Board
		{
			"name" : "BackGround", "type" : "expanded_image", "x" : 0, "y" : 0,
			"x_scale" : float(SCREEN_WIDTH) / 1900.0, "y_scale" : float(SCREEN_HEIGHT) / 1280.0,
			"image" : BASE_PATH + "background.jpg",
			
			"children" : 
			(
				{
					"name" : "FrameTop",
					"type" : "expanded_image",
					"x" : 0, "y" : 0,
					"rect" : (0.0 , 0.0 , -1.0+ (float(SCREEN_WIDTH)/float(800.0)) ,0.0,),
					"image" : BASE_PATH + "frame_up.tga",
				},
				
				{
					"name" : "HalfTree",
					"type" : "image",
					
					"x" : SCREEN_WIDTH/2 - 471/2, "y" : SCREEN_HEIGHT - 215,
					"image" : BASE_PATH + "tronco.tga",
				},
				
				{
					"name" : "ShadowFrameBottom",
					"type" : "expanded_image",
					
					"x" : 0,
					"y" : SCREEN_HEIGHT-45-30 - 10,
					
					"rect" : (0.0 , 0.0 , -1.0+ (float(SCREEN_WIDTH)/float(800.0)) ,0.0,),
					"image" : BASE_PATH + "shadow_frame.tga",
				},
				
				{
					"name" : "FrameBottom",
					"type" : "expanded_image",
					"x" : 0, "y" : SCREEN_HEIGHT-30,
					"rect" : (0.0 , 0.0 , -1.0+ (float(SCREEN_WIDTH)/float(800.0)) ,0.0,),
					"image" : BASE_PATH + "frame_down.tga",
				},
				
				
			),
		},
		

		{
			"name" : "character_play_time",
			"type" : "text",

			"x" : SCREEN_WIDTH  - 200,
			"y" : SCREEN_HEIGHT - 20,

			"text" : uiScriptLocale.SELECT_PLAYTIME,

			"children" :
			(
				{
					"name" : "character_play_time_slot",
					"type" : "image",

					"x" : 83,
					"y" : -2,

					"image" : "d:/ymir work/ui/public/Parameter_Slot_03.sub",
				},
				{
					"name" : "character_play_time_value",
					"type" : "text",

					"x" : 83 + 91/2,
					"y" : 0,

					"text" : "",

					"text_horizontal_align" : "center",
				},
			),
		},
		## Character Board
		{
			"name" : "character_board",
			"type" : "window",

			"x" : 0,
			"y" : SCREEN_HEIGHT- 95,

			"width" : SCREEN_WIDTH,
			"height" : 100,

			"children" :
			(

				{
					"name" : "character_name_text_image",
					"type" : "image",

					"x" : SCREEN_WIDTH/2 - 75 + 18 + 40,
					"y" : 8 + 7,

					"image" : BASE_PATH + "character_name_text_image.tga",
				},
				
				{
					"name" : "character_name_slot",
					"type" : "image",

					"x" : SCREEN_WIDTH/2 - 130 + 40,
					"y" : 20 + 7,

					"image" : BASE_PATH + "name_slot.tga",
					
					"children":
					(
						{
							"name" : "character_name_value",
							"type" : "text",
							
							"x" : 260/2 + 10,
							"y" : 12,
							
							"text" :  "char_name",
							"text_horizontal_align" : "center",
						},
						{
							"name" : "character_level_text",
							"type" : "text",
							
							"x" : 260/2 - 100,
							"y" : 12,
							
							"text" :  "char_name",
							#"text_horizontal_align" : "center",
						},
					),
				},
				
				
				
				## Buttons
				{
					"name" : "start_button",
					"type" : "button",

					"x" : SCREEN_WIDTH - 150,
					"y" : 15,

					"default_image" : BASE_PATH + "tasti/play_default.tga",
					"over_image" : BASE_PATH + "tasti/play_over.tga",
					"down_image" : BASE_PATH + "tasti/play_down.tga",
				},
				{
					"name" : "create_button",
					"type" : "button",

					"x" : 106,
					"y" : 22,

					"default_image" : BASE_PATH + "tasti/creation_default.tga",
					"over_image" : BASE_PATH + "tasti/creation_over.tga",
					"down_image" : BASE_PATH + "tasti/creation_down.tga",
				},
				{
					"name" : "exit_button",
					"type" : "button",

					"x" : 5,
					"y" : 22,
					
					"default_image" : BASE_PATH + "tasti/back_default.tga",
					"over_image" : BASE_PATH + "tasti/back_over.tga",
					"down_image" : BASE_PATH + "tasti/back_down.tga",
				},
				{
					"name" : "delete_button",
					"type" : "button",

					"x" : 106+96+5,
					"y" : 22,
					
					"default_image" : BASE_PATH + "tasti/remove_default.tga",
					"over_image" : BASE_PATH + "tasti/remove_over.tga",
					"down_image" : BASE_PATH + "tasti/remove_down.tga",
				},
			),
		},

		## Buttons
		{
			"name" : "left_button",
			"type" : "button",

			"x" : SCREEN_WIDTH/2 - 270,
			"y" : SCREEN_HEIGHT - 340,

			"default_image" : BASE_PATH + "tasti/sinistra_default.tga",
			"over_image" : BASE_PATH + "tasti/sinistra_over.tga",
			"down_image" : BASE_PATH + "tasti/sinistra_down.tga",
		},
		{
			"name" : "right_button",
			"type" : "button",

			"x" : SCREEN_WIDTH /2 + 270 - 63,
			"y" : SCREEN_HEIGHT - 340,

			"default_image" : BASE_PATH + "tasti/destra_default.tga",
			"over_image" : BASE_PATH + "tasti/destra_over.tga",
			"down_image" : BASE_PATH + "tasti/destra_down.tga",
		},


	),
}