
BASE_PATH = "createwindow/"
EXTERN_PATH = "selectwindow/"
HEIGTH_TASKBAR = 40 + 29

window = {
	"name" : "CreateCharacterWindow",

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
				# {
					# "name" : "half_tree",
					# "type" : "image",
					
					# "x" : ,
					# "y" : ,
					
					# "image" : "",
				# },
				{
					"name" : "FrameTop",
					"type" : "expanded_image",
					"x" : 0, "y" : 0,
					"rect" : (0.0 , 0.0 , -1.0+ (float(SCREEN_WIDTH)/float(800.0)) ,0.0,),
					"image" : BASE_PATH + "frame_up.tga",
				},
				
				{
					"name" : "ShadowFrameBottom",
					"type" : "expanded_image",
					
					"x" : 0,
					"y" : SCREEN_HEIGHT-45-30 - 10 +11,
					
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
			"name" : "character_slot",
			"type" : "window",

			"x" : SCREEN_WIDTH/2 - 173/2,
			"y" : SCREEN_HEIGHT - HEIGTH_TASKBAR,
			
			"width" : 173,
			"height": 24,
			
			"children" :
			(
				{
					"name" : "character_name_slot",
					"type" : "image",

					"x" : 0,
					"y" : 0,

					"image" : BASE_PATH + "barranome.tga",
				},
				{
					"name" : "character_name_value",
					"type" : "editline",

					"x" : 2 + 20,
					"y" : 1 + 5,

					"input_limit" : 12,

					"width" : 173 - 18,
					"height" : 23 - 7,
				},
			),
		},
		
		{
			"name" : "gender_button_01",
			"type" : "radio_button",

			"x" : SCREEN_WIDTH/2 - 173/2 - 200 + (55-19)+ (55-6),
			"y" : SCREEN_HEIGHT - HEIGTH_TASKBAR,

			"default_image" : BASE_PATH + "tasti/" + "maschio_default.tga",
			"over_image"	: BASE_PATH + "tasti/" + "maschio_over.tga",
			"down_image"	: BASE_PATH + "tasti/" + "maschio_down.tga",
		},
		
		{
			"name" : "gender_button_02",
			"type" : "radio_button",

			"x" : SCREEN_WIDTH/2 - 173/2 - 100 + (55-19) ,
			"y" : SCREEN_HEIGHT - HEIGTH_TASKBAR,

			"default_image" : BASE_PATH + "tasti/" + "femmina_default.tga",
			"over_image"	: BASE_PATH + "tasti/" + "femmina_over.tga",
			"down_image"	: BASE_PATH + "tasti/" + "femmina_down.tga",
		},

		{
			"name" : "shape_button_01",
			"type" : "radio_button",

			"x" : SCREEN_WIDTH/2 + 173/2 + 20,
			"y" : SCREEN_HEIGHT - HEIGTH_TASKBAR,

			"default_image" : BASE_PATH + "tasti/" + "vestito1_default.tga",
			"over_image"	: BASE_PATH + "tasti/" + "vestito1_over.tga",
			"down_image"	: BASE_PATH + "tasti/" + "vestito1_down.tga",
		},
		{
			"name" : "shape_button_02",
			"type" : "radio_button",

			"x" : SCREEN_WIDTH/2 + 173/2 + 20 + 100 - 48,
			"y" : SCREEN_HEIGHT - HEIGTH_TASKBAR,

			"default_image" : BASE_PATH + "tasti/" + "vestito2_default.tga",
			"over_image"	: BASE_PATH + "tasti/" + "vestito2_over.tga",
			"down_image"	: BASE_PATH + "tasti/" + "vestito2_down.tga",
		},

		{
			"name" : "create_button",
			"type" : "button",

			"x" : SCREEN_WIDTH - 120,
			"y" : SCREEN_HEIGHT - HEIGTH_TASKBAR,
			
			"default_image" : BASE_PATH + "tasti/" + "creation_default.tga",
			"over_image"	: BASE_PATH + "tasti/" + "creation_over.tga",
			"down_image"	: BASE_PATH + "tasti/" + "creation_down.tga",
		},
		{
			"name" : "cancel_button",
			"type" : "button",

			"x" : 30,
			"y" : SCREEN_HEIGHT - HEIGTH_TASKBAR,

			"default_image" : BASE_PATH + "tasti/" + "back_default.tga",
			"over_image"	: BASE_PATH + "tasti/" + "back_over.tga",
			"down_image"	: BASE_PATH + "tasti/" + "back_down.tga",
		},

		## Buttons
		{
			"name" : "left_button",
			"type" : "button",

			"x" : SCREEN_WIDTH/2 - 63 - 250 ,
			"y" : SCREEN_HEIGHT /2 - 100,
			
			
			"default_image" : BASE_PATH + "tasti/" + "sinistra_default.tga",
			"over_image"	: BASE_PATH + "tasti/" + "sinistra_over.tga",
			"down_image"	: BASE_PATH + "tasti/" + "sinistra_down.tga",
		},
		{
			"name" : "right_button",
			"type" : "button",

			"x" : SCREEN_WIDTH/2 + 250 ,
			"y" : SCREEN_HEIGHT /2 - 100,

			"default_image" : BASE_PATH + "tasti/" + "destra_default.tga",
			"over_image"	: BASE_PATH + "tasti/" + "destra_over.tga",
			"down_image"	: BASE_PATH + "tasti/" + "destra_down.tga",
		},


	),
}