import uiScriptLocale
import localeInfo

ROOT_PATH = "d:/ymir work/ui/public/"
PATCH_NEW_LOGIN = "login_w/design/"
BASE_PATH_INTERFACE = "login_w/design/"
BASE_PATH = BASE_PATH_INTERFACE
LOCALE_PATH = uiScriptLocale.LOGIN_PATH

ID_LIMIT_COUNT = 19
PW_LIMIT_COUNT = 16
FLAGS_DIRECTION = 265 # Orientamento bandiere su asse X (diminuire per andare a destra, aumentare per andare a sinistra)

window = {
	"name" : "LoginWindow",
	"style" : ("movable", "float", "attach",),

	"x" : 0,
	"y" : 0,

	"width" : SCREEN_WIDTH,
	"height" : SCREEN_HEIGHT,

	"children" :
	(

		## Board
		{
			"name" : "bg1", "type" : "expanded_image", "x" : 0, "y" : 0,
			"x_scale" : float(SCREEN_WIDTH) / 1920.0, "y_scale" : float(SCREEN_HEIGHT) / 1080.0,
			"image" : PATCH_NEW_LOGIN+"bg.tga",
		},
		{
			"name" : "bg2", "type" : "expanded_image", "x" : 0, "y" : 0,
			"x_scale" : float(SCREEN_WIDTH) / 1920.0, "y_scale" : float(SCREEN_HEIGHT) / 1080.0,
			"image" : PATCH_NEW_LOGIN+"bg.tga",
		},


		{
			"name" : "logo", "type" : "button", 
			"x" : (SCREEN_WIDTH - 335) / 2, "y" : (SCREEN_HEIGHT - 720) /2,
			"default_image" : PATCH_NEW_LOGIN+"zayos_logo_small.tga",
			"over_image" : PATCH_NEW_LOGIN+"zayos_logo_over.tga",
			"down_image" : PATCH_NEW_LOGIN+"zayos_logo_small.tga",
		},


		{
			"name" : "footer", "type" : "image", "x" : 0, "y" : SCREEN_HEIGHT - 263,
			"image" : PATCH_NEW_LOGIN+"Footer.tga",
		},

		{
			"name" : "LoginExitButton",
			"type" : "button",

			"x" : SCREEN_WIDTH-100,
			"y" : 30,

			"default_image" : PATCH_NEW_LOGIN+"leave.tga",
			"over_image" : PATCH_NEW_LOGIN+"leave.tga",
			"down_image" : PATCH_NEW_LOGIN+"leave.tga",
		},

		## Lang1
		{
			"name" : "Lang1",
			"type" : "button",
			"tooltip_text": "Italiano",
			"x" : SCREEN_WIDTH/2 - FLAGS_DIRECTION + 125,
			"y" : SCREEN_HEIGHT -130,

			"width" : 32,
			"height" : 22,

			"default_image" : BASE_PATH_INTERFACE + "flag_it_norm.tga",
			"over_image" : BASE_PATH_INTERFACE + "flag_it_over.tga",
			"down_image" : BASE_PATH_INTERFACE + "flag_it_down.tga",
		},
		
		## Lang2
		{
			"name" : "Lang2",
			"type" : "button",
			"tooltip_text": "English",
			"x" : SCREEN_WIDTH/2 - FLAGS_DIRECTION + 125 + 50,
			"y" : SCREEN_HEIGHT -130,

			"width" : 32,
			"height" : 22,

			"default_image" : BASE_PATH_INTERFACE + "flag_en_norm.tga",
			"over_image" : BASE_PATH_INTERFACE + "flag_en_over.tga",
			"down_image" : BASE_PATH_INTERFACE + "flag_en_down.tga",
		},
		
		## Lang3
		{
			"name" : "Lang3",
			"type" : "button",
			"tooltip_text": "Deutsche",
			"x" : SCREEN_WIDTH/2 - FLAGS_DIRECTION + 125 + 50*2,
			"y" : SCREEN_HEIGHT -130,

			"width" : 32,
			"height" : 22,

			"default_image" : BASE_PATH_INTERFACE + "flag_de_norm.tga",
			"over_image" : BASE_PATH_INTERFACE + "flag_de_over.tga",
			"down_image" : BASE_PATH_INTERFACE + "flag_de_down.tga",
		},
		
		## Lang4
		{
			"name" : "Lang4",
			"type" : "button",
			"tooltip_text": "Romana",
			"x" : SCREEN_WIDTH/2 - FLAGS_DIRECTION + 125 + 50*3,
			"y" : SCREEN_HEIGHT -130,

			"width" : 32,
			"height" : 22,

			"default_image" : BASE_PATH_INTERFACE + "flag_ro_norm.tga",
			"over_image" : BASE_PATH_INTERFACE + "flag_ro_over.tga",
			"down_image" : BASE_PATH_INTERFACE + "flag_ro_down.tga",
		},
		
		## Lang5
		{
			"name" : "Lang5",
			"type" : "button",
			"tooltip_text": "Turkce",
			"x" : SCREEN_WIDTH/2 - FLAGS_DIRECTION + 125 + 50*4,
			"y" : SCREEN_HEIGHT -130,

			"width" : 32,
			"height" : 22,

			"default_image" : BASE_PATH_INTERFACE + "flag_tr_norm.tga",
			"over_image" : BASE_PATH_INTERFACE + "flag_tr_over.tga",
			"down_image" : BASE_PATH_INTERFACE + "flag_tr_down.tga",
		},
		
		## Lang6
		{
			"name" : "Lang6",
			"type" : "button",
			"tooltip_text": "Polska",
			"x" : SCREEN_WIDTH/2 - FLAGS_DIRECTION + 125 + 50*5,
			"y" : SCREEN_HEIGHT -130,

			"width" : 32,
			"height" : 22,

			"default_image" : BASE_PATH_INTERFACE + "flag_pl_norm.tga",
			"over_image" : BASE_PATH_INTERFACE + "flag_pl_over.tga",
			"down_image" : BASE_PATH_INTERFACE + "flag_pl_down.tga",
		},

		{
			"name" : "LoginBoard",
			"type" : "image",

			"x" : (SCREEN_WIDTH - 735) / 2,
			"y" : (SCREEN_HEIGHT - 336) /2,

			"image" : PATCH_NEW_LOGIN + "bg_login.tga",

			"children" :
			(
				{
					"name": "title_1",
					"type": "text",
					"x" : 365,
					"y" : 72,
					"text" : localeInfo.ACCEDI_INTERFACE,
					"text_horizontal_align" : "center",
				},

				{
					"name": "title_2",
					"type": "text",
					"x" : 100,
					"y" : 68,
					"text" : localeInfo.ACCEDI_INTERFACE1,
					"text_horizontal_align" : "center",
				},


				{
					"name": "title_3",
					"type": "text",
					"x" : 630,
					"y" : 68,
					"text" : localeInfo.ACCEDI_INTERFACE2,
					"text_horizontal_align" : "center",
				},


				{
					"name" : "ID_EditLine",
					"type" : "editline",


					"x" : 295,
					"y" : 113,

					"width" : 180,
					"height" : 18,

					"input_limit" : ID_LIMIT_COUNT,
					"enable_codepage" : 0,

					"r" : 1.0,
					"g" : 1.0,
					"b" : 1.0,
					"a" : 1.0,
				},

				{
					"name" : "Password_EditLine",
					"type" : "editline",


					"x" : 295,
					"y" : 113+44,

					"width" : 180,
					"height" : 18,

					"input_limit" : PW_LIMIT_COUNT,
					"secret_flag" : 1,
					"enable_codepage" : 0,

					"r" : 1.0,
					"g" : 1.0,
					"b" : 1.0,
					"a" : 1.0,
				},
				
				{
					"name" : "SaveButton",
					"type" : "button",
					"tooltip_text": localeInfo.BOTTONE_SALVA,

					"x" : 350,
					"y" : 185,

					"default_image" : PATCH_NEW_LOGIN+"save_act.tga",
					"over_image" : PATCH_NEW_LOGIN+"save_def.tga",
					"down_image" : PATCH_NEW_LOGIN+"save_down.tga",

				},

				{
					"name" : "LoginButton",
					"type" : "button",

					"x" : 248,
					"y" : 200+15,

					"default_image" : PATCH_NEW_LOGIN+"sign_in.tga",
					"over_image" : PATCH_NEW_LOGIN+"sign_down.tga",
					"down_image" : PATCH_NEW_LOGIN+"sign_in.tga",

					"text" : uiScriptLocale.LOGIN_CONNECT,
				},
			
			),
		},

	),
}
