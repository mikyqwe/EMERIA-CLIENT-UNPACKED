########## INCEPE SMEKERIA ########## ORA 23:58
import uiScriptLocale

LOCATIE_FISIERE = "selectwindow_new/"
LOCATIE_FISIERE_BUTOANE = "selectwindow_new/butoane/"
BOARD_X = SCREEN_WIDTH * (65) / 800
DIFERENTA_BUTOANE = 75
BUTON_DREAPTA_STANGADREAPTA = 250
BUTON_DREAPTA_SUSJOS = 25
BOARD_ITEM_ADD_POSITION = -40

window = {
	"name" : "SelectCharacterWindow",
	"x" : 0,
	"y" : 0,
	"width" : SCREEN_WIDTH,
	"height" : SCREEN_HEIGHT,
	"children" :(
		## Board
		{
			"name" : "BackGround", 
			"type" : "expanded_image",
			"x" : 0, "y" : 0,
			"x_scale" : float(SCREEN_WIDTH) / 1366.0,
			"y_scale" : float(SCREEN_HEIGHT) / 768.0,
			"image" : LOCATIE_FISIERE + "background.tga",
		},
		## Buttons
		{
			"name" : "character_level_big",
			"type" : "text",
			"x" : 94, "y" : 3*75+40,
			"text" : "",
			"fontname" : "Tahoma:35",
			"horizontal_align" : "left",
		},
		{
			"name" : "character_playtime",
			"type" : "text",
			"x" : 94+145, "y" : 3*75+40,
			"text" : "",
			"fontname" : "Tahoma:35",
			"horizontal_align" : "left",
		},
		{
			"name" : "statistici",
			"type" : "image",
			"x" : 80, "y" : 3*75,
			"image" : LOCATIE_FISIERE + "statistici.tga",
			"horizontal_align" : "left",
		},
				{
					"name" : "EmpireFlag_A",
					"type" : "expanded_image",
					"x" : 21,
					"y" : 12,
					"image" : LOCATIE_FISIERE + "shinnso.tga"
				},
				{
					"name" : "EmpireFlag_B",
					"type" : "expanded_image",
					"x" : 21,
					"y" : 12,
					"image" : LOCATIE_FISIERE + "cunjo.tga"
				},
				{
					"name" : "EmpireFlag_C",
					"type" : "expanded_image",
					"x" : 21,
					"y" : 12,
					"image" : LOCATIE_FISIERE + "jinno.tga"
				},
				{
					"name" : "character_hth",
					"type" : "text",
					"x" : 17 + 25,
					"y" : 102 + 100 - 21 + BOARD_ITEM_ADD_POSITION + 250,
					"children" :
					(
						{
							"name" : "gauge_hth",
							"type" : "newgauge",

							"x" : 30,
							"y" : 4,

							"width" : 200,
							"color" : "verde",
						},
						{
							"name" : "character_hth_value",
							"type" : "text",

							"x" : 134 + 36 + 100,
							"y" : 1,

							"text" : "Puncte de viata",

							"text_horizontal_align" : "center",
						},
					),
				},
				{
					"name" : "character_int",
					"type" : "text",
					"x" : 17 + 25,
					"y" : 128 + 100 - 21 + BOARD_ITEM_ADD_POSITION + 250,
					"children" :
					(
						{
							"name" : "gauge_int",
							"type" : "newgauge",

							"x" : 30,
							"y" : 4,

							"width" : 200,
							"color" : "mov",
						},
						{
							"name" : "character_int_value",
							"type" : "text",

							"x" : 134 + 25 + 100,
							"y" : 1,

							"text" : "Inteligenta",

							"text_horizontal_align" : "center",
						},
					),
				},
				{
					"name" : "character_str",
					"type" : "text",

					"x" : 17 + 25,
					"y" : 154 + 100 - 21 + BOARD_ITEM_ADD_POSITION + 250,


					"children" :
					(
						{
							"name" : "gauge_str",
							"type" : "newgauge",

							"x" : 30,
							"y" : 4,

							"width" : 200,
							"color" : "rosu",
						},
						{
							"name" : "character_str_value",
							"type" : "text",

							"x" : 134 + 11 + 100,
							"y" : 1,

							"text" : "Tarie",

							"text_horizontal_align" : "center",
						},
					),
				},
				{
					"name" : "character_dex",
					"type" : "text",

					"x" : 17 + 25,
					"y" : 180 + 100 - 21 + BOARD_ITEM_ADD_POSITION + 250,

					# "text" : uiScriptLocale.SELECT_DEX_GRADE,

					"children" :
					(
						{
							"name" : "gauge_dex",
							"type" : "newgauge",

							"x" : 30,
							"y" : 4,

							"width" : 200,
							"color" : "galben",
						},
						{
							"name" : "character_dex_value",
							"type" : "text",

							"x" : 134 + 25 + 100,
							"y" : 1,

							"text" : "Dexteritate",

							"text_horizontal_align" : "center",
						},
					),
				},
		{
			"name" : "base_stats",
			"type" : "image",
			"x" : 80, "y" : 5*75,
			"image" : LOCATIE_FISIERE + "base_stats.tga",
			"horizontal_align" : "left",
		},
		{
			"name" : "slot_button_01",
			"type" : "button",
			"x" : BUTON_DREAPTA_STANGADREAPTA,
			"y" : BUTON_DREAPTA_SUSJOS,

			"horizontal_align" : "right",

			"default_image" : LOCATIE_FISIERE_BUTOANE + "slot_gol0.tga",
			"over_image" : LOCATIE_FISIERE_BUTOANE + "slot_gol1.tga",
			"down_image" : LOCATIE_FISIERE_BUTOANE + "slot_gol2.tga",
			"children" :
				(
					{
						"name" : "character_name_value_01",
						"type" : "text",

						"x" : 95, ## LATIME
						"y" : 23, ## LUNGIME

						"text" : "",
						"fontsize" : "LARGE",
						"text_horizontal_align" : "center"
					},
					{
						"name" : "character_level_value_01",
						"type" : "text",

						"x" : 125,
						"y" : 39,

						"text" : "",
						"fontsize" : "LARGE",
					},
					{
						"name" : "character_raza_value_01",
						"type" : "text",

						"x" : 95, ## LATIME
						"y" : 9, ## LUNGIME

						"text" : "",
						"fontsize" : "LARGE",
					},
				),
		},
		{
			"name" : "slot_button_01_active",
			"type" : "button",

			"x" : BUTON_DREAPTA_STANGADREAPTA,
			"y" : BUTON_DREAPTA_SUSJOS,

			"horizontal_align" : "right",

			"default_image" : LOCATIE_FISIERE_BUTOANE + "slot_gol1.tga",
			"over_image" :LOCATIE_FISIERE_BUTOANE + "slot_gol1.tga",
			"down_image" : LOCATIE_FISIERE_BUTOANE + "slot_gol1.tga",

			"children" :
				(
					{
						"name" : "character_name_value_01_a",
						"type" : "text",

						"x" : 95, ## LATIME
						"y" : 23, ## LUNGIME

						"text" : "",
						"fontsize" : "LARGE",
						"text_horizontal_align" : "center"
					},
					{
						"name" : "character_level_value_01_a",
						"type" : "text",

						"x" : 125,
						"y" : 39,

						"text" : "",
						"fontsize" : "LARGE",
					},
					{
						"name" : "character_raza_value_01_a",
						"type" : "text",

						"x" : 95, ## LATIME
						"y" : 9, ## LUNGIME

						"text" : "",
						"fontsize" : "LARGE",
					},
				),
		},
		{
			"name" : "slot_button_02",
			"type" : "button",

			'x' : BUTON_DREAPTA_STANGADREAPTA,
			'y' : BUTON_DREAPTA_SUSJOS + DIFERENTA_BUTOANE,
			
			"horizontal_align" : "right",
			
			"default_image" : LOCATIE_FISIERE_BUTOANE + "slot_gol0.tga",
			"over_image" : LOCATIE_FISIERE_BUTOANE + "slot_gol1.tga",
			"down_image" : LOCATIE_FISIERE_BUTOANE + "slot_gol2.tga",

			"children" :
				(
					{
						"name" : "character_name_value_02",
						"type" : "text",

						"x" : 95, ## LATIME
						"y" : 23, ## LUNGIME

						"text" : "",
						"fontsize" : "LARGE",
						"text_horizontal_align" : "center"
					},
					{
						"name" : "character_level_value_02",
						"type" : "text",

						"x" : 125,
						"y" : 39,

						"text" : "",
						"fontsize" : "LARGE",
					},
					{
						"name" : "character_raza_value_02",
						"type" : "text",

						"x" : 95, ## LATIME
						"y" : 9, ## LUNGIME

						"text" : "",
						"fontsize" : "LARGE",
					},
				),
		},
		{
			"name" : "slot_button_02_active",
			"type" : "button",

			'x' : BUTON_DREAPTA_STANGADREAPTA,
			'y' : BUTON_DREAPTA_SUSJOS + DIFERENTA_BUTOANE,
			
			"horizontal_align" : "right",

			"default_image" : LOCATIE_FISIERE_BUTOANE + "slot_gol1.tga",
			"over_image" :LOCATIE_FISIERE_BUTOANE + "slot_gol1.tga",
			"down_image" : LOCATIE_FISIERE_BUTOANE + "slot_gol1.tga",

			"children" :
				(
					{
						"name" : "character_name_value_02_a",
						"type" : "text",

						"x" : 95, ## LATIME
						"y" : 23, ## LUNGIME

						"text" : "",
						"fontsize" : "LARGE",
						"text_horizontal_align" : "center"
					},
					{
						"name" : "character_level_value_02_a",
						"type" : "text",

						"x" : 125,
						"y" : 39,

						"text" : "",
						"fontsize" : "LARGE",
					},
					{
						"name" : "character_raza_value_02_a",
						"type" : "text",

						"x" : 95, ## LATIME
						"y" : 9, ## LUNGIME

						"text" : "",
						"fontsize" : "LARGE",
					},
				),
		},
		{
			"name" : "slot_button_03",
			"type" : "button",

			'x' : BUTON_DREAPTA_STANGADREAPTA,
			'y' : BUTON_DREAPTA_SUSJOS + 2*DIFERENTA_BUTOANE,
			
			"horizontal_align" : "right",

			"default_image" : LOCATIE_FISIERE_BUTOANE + "slot_gol0.tga",
			"over_image" : LOCATIE_FISIERE_BUTOANE + "slot_gol1.tga",
			"down_image" : LOCATIE_FISIERE_BUTOANE + "slot_gol2.tga",

			"children" :
				(
					{
						"name" : "character_name_value_03",
						"type" : "text",

						"x" : 95, ## LATIME
						"y" : 23, ## LUNGIME

						"text" : "",
						"fontsize" : "LARGE",
						"text_horizontal_align" : "center"
					},
					{
						"name" : "character_level_value_03",
						"type" : "text",

						"x" : 125,
						"y" : 39,

						"text" : "",
						"fontsize" : "LARGE",
					},
					{
						"name" : "character_raza_value_03",
						"type" : "text",

						"x" : 95, ## LATIME
						"y" : 9, ## LUNGIME

						"text" : "",
						"fontsize" : "LARGE",
					},
				),
		},
		{
			"name" : "slot_button_03_active",
			"type" : "button",

			'x' : BUTON_DREAPTA_STANGADREAPTA,
			'y' : BUTON_DREAPTA_SUSJOS + 2*DIFERENTA_BUTOANE,
			
			"horizontal_align" : "right",

			"default_image" : LOCATIE_FISIERE_BUTOANE + "slot_gol1.tga",
			"over_image" :LOCATIE_FISIERE_BUTOANE + "slot_gol1.tga",
			"down_image" : LOCATIE_FISIERE_BUTOANE + "slot_gol1.tga",

			"children" :
				(
					{
						"name" : "character_name_value_03_a",
						"type" : "text",

						"x" : 95, ## LATIME
						"y" : 23, ## LUNGIME

						"text" : "",
						"fontsize" : "LARGE",
						"text_horizontal_align" : "center"
					},
					{
						"name" : "character_level_value_03_a",
						"type" : "text",

						"x" : 125,
						"y" : 39,

						"text" : "",
						"fontsize" : "LARGE",
					},
					{
						"name" : "character_raza_value_03_a",
						"type" : "text",

						"x" : 95, ## LATIME
						"y" : 9, ## LUNGIME

						"text" : "",
						"fontsize" : "LARGE",
					},
				),
		},
		{
			"name" : "slot_button_04",
			"type" : "button",
			
			'x' : BUTON_DREAPTA_STANGADREAPTA,
			'y' : BUTON_DREAPTA_SUSJOS + 3*DIFERENTA_BUTOANE,
			
			"horizontal_align" : "right",
			
			"default_image" : LOCATIE_FISIERE_BUTOANE + "slot_gol0.tga",
			"over_image" : LOCATIE_FISIERE_BUTOANE + "slot_gol1.tga",
			"down_image" : LOCATIE_FISIERE_BUTOANE + "slot_gol2.tga",

			"children" :
				(
					{
						"name" : "character_name_value_04",
						"type" : "text",

						"x" : 95, ## LATIME
						"y" : 23, ## LUNGIME

						"text" : "",
						"fontsize" : "LARGE",
						"text_horizontal_align" : "center"
					},
					{
						"name" : "character_level_value_04",
						"type" : "text",

						"x" : 125,
						"y" : 39,

						"text" : "",
						"fontsize" : "LARGE",
					},
					{
						"name" : "character_raza_value_04",
						"type" : "text",

						"x" : 95, ## LATIME
						"y" : 9, ## LUNGIME

						"text" : "",
						"fontsize" : "LARGE",
					},
				),
		},
		{
			"name" : "slot_button_04_active",
			"type" : "button",

			'x' : BUTON_DREAPTA_STANGADREAPTA,
			'y' : BUTON_DREAPTA_SUSJOS + 3*DIFERENTA_BUTOANE,
			
			"horizontal_align" : "right",
			
			"default_image" : LOCATIE_FISIERE_BUTOANE + "slot_gol1.tga",
			"over_image" :LOCATIE_FISIERE_BUTOANE + "slot_gol1.tga",
			"down_image" : LOCATIE_FISIERE_BUTOANE + "slot_gol1.tga",

			"children" :
				(
					{
						"name" : "character_name_value_04_a",
						"type" : "text",

						"x" : 95, ## LATIME
						"y" : 23, ## LUNGIME

						"text" : "",
						"fontsize" : "LARGE",
						"text_horizontal_align" : "center"
					},
					{
						"name" : "character_level_value_04_a",
						"type" : "text",

						"x" : 125,
						"y" : 39,

						"text" : "",
						"fontsize" : "LARGE",
					},
					{
						"name" : "character_raza_value_04_a",
						"type" : "text",

						"x" : 95, ## LATIME
						"y" : 9, ## LUNGIME

						"text" : "",
						"fontsize" : "LARGE",
					},
				),
		},
		{
			"name" : "create_button",
			"type" : "button",
			'x' : BUTON_DREAPTA_STANGADREAPTA,
			"y" : BUTON_DREAPTA_SUSJOS + 4*DIFERENTA_BUTOANE,
			"horizontal_align" : "right",
			"default_image" : LOCATIE_FISIERE_BUTOANE + "crate_character0.tga",
			"over_image" : LOCATIE_FISIERE_BUTOANE + "crate_character1.tga",
			"down_image" : LOCATIE_FISIERE_BUTOANE + "crate_character2.tga",
		},
		{
			"name" : "start_button",
			"type" : "button",
			'x' : -5,
			"y" : SCREEN_HEIGHT * (540) / 645,
			"horizontal_align" : "center",
			"default_image" : LOCATIE_FISIERE_BUTOANE + "play0.tga",
			"over_image" : LOCATIE_FISIERE_BUTOANE + "play1.tga",
			"down_image" : LOCATIE_FISIERE_BUTOANE + "play2.tga",
		},
		{
			"name" : "delete_button",
			"type" : "button",
			'x' : -140,
			"y" : SCREEN_HEIGHT * (540) / 645,
			"horizontal_align" : "center",
			"default_image" : LOCATIE_FISIERE_BUTOANE + "delete0.tga",
			"over_image" : LOCATIE_FISIERE_BUTOANE + "delete1.tga",
			"down_image" : LOCATIE_FISIERE_BUTOANE + "delete2.tga",
			 
		},
		{
			"name" : "exit_button",
			"type" : "button",
			"x" : SCREEN_WIDTH - 115, "y" : 980,
			"default_image" : LOCATIE_FISIERE_BUTOANE + "logout0.tga",
			"over_image" : LOCATIE_FISIERE_BUTOANE + "logout1.tga",
			"down_image" : LOCATIE_FISIERE_BUTOANE + "logout2.tga",
		},
		{
			"name" : "item_shop_button",
			"type" : "button",
			"x" : SCREEN_WIDTH - 1910, "y" : 980,
			"default_image" : LOCATIE_FISIERE_BUTOANE + "item_mall0.tga",
			"over_image" :  LOCATIE_FISIERE_BUTOANE + "item_mall1.tga",
			"down_image" : LOCATIE_FISIERE_BUTOANE + "item_mall2.tga",
		},
	),
}
########## GATA SMEKERIA ########## ORA 18:35