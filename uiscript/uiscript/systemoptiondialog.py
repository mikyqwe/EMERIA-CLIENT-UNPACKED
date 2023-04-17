import uiScriptLocale
import app

ROOT_PATH = "d:/ymir work/ui/public/"

TEMPORARY_X = +13
TEXT_TEMPORARY_X = -10
BUTTON_TEMPORARY_X = 5
PVP_X = -10

if app.ENABLE_ENVIRONMENT_EFFECT_OPTION:
	window = {
		"name" : "SystemOptionDialog",
		"style" : ("movable", "float",),

		"x" : 0,
		"y" : 0,

		"width" : 305,
		"height" : 505,

		"children" :
		(
			{
				"name" : "board",
				"type" : "board",

				"x" : 0,
				"y" : 0,

				"width" : 305,
				"height" : 505,

				"children" :
				(
					## Title
					{
						"name" : "titlebar",
						"type" : "titlebar",
						"style" : ("attach",),

						"x" : 8,
						"y" : 8,

						"width" : 284,
						"color" : "gray",

						"children" :
						(
							{
							"name":"titlename", "type":"text", "x":0, "y":3,
							"horizontal_align":"center", "text_horizontal_align":"center",
							"text": uiScriptLocale.SYSTEMOPTION_TITLE,
							 },
						),
					},


					## Music
					{
						"name" : "music_name",
						"type" : "text",

						"x" : 30,
						"y" : 75,

						"text" : uiScriptLocale.OPTION_MUSIC,
					},

					{
						"name" : "music_volume_controller",
						"type" : "sliderbar",

						"x" : 110,
						"y" : 75,
					},

					{
						"name" : "bgm_button",
						"type" : "button",

						"x" : 20,
						"y" : 100,

						"text" : uiScriptLocale.OPTION_MUSIC_CHANGE,

						"default_image" : ROOT_PATH + "Middle_Button_01.sub",
						"over_image" : ROOT_PATH + "Middle_Button_02.sub",
						"down_image" : ROOT_PATH + "Middle_Button_03.sub",
					},

					{
						"name" : "bgm_file",
						"type" : "text",

						"x" : 100,
						"y" : 102,

						"text" : uiScriptLocale.OPTION_MUSIC_DEFAULT_THEMA,
					},

					## Sound
					{
						"name" : "sound_name",
						"type" : "text",

						"x" : 30,
						"y" : 50,

						"text" : uiScriptLocale.OPTION_SOUND,
					},

					{
						"name" : "sound_volume_controller",
						"type" : "sliderbar",

						"x" : 110,
						"y" : 50,
					},

					{
						"name" : "camera_mode",
						"type" : "text",

						"x" : 40 + TEXT_TEMPORARY_X,
						"y" : 135+2,

						"text" : uiScriptLocale.OPTION_CAMERA_DISTANCE,
					},

					{
						"name" : "camera_short",
						"type" : "radio_button",

						"x" : 110,
						"y" : 135,

						"text" : uiScriptLocale.OPTION_CAMERA_DISTANCE_SHORT,

						"default_image" : ROOT_PATH + "Middle_Button_01.sub",
						"over_image" : ROOT_PATH + "Middle_Button_02.sub",
						"down_image" : ROOT_PATH + "Middle_Button_03.sub",
					},

					{
						"name" : "camera_long",
						"type" : "radio_button",

						"x" : 110+70,
						"y" : 135,

						"text" : uiScriptLocale.OPTION_CAMERA_DISTANCE_LONG,

						"default_image" : ROOT_PATH + "Middle_Button_01.sub",
						"over_image" : ROOT_PATH + "Middle_Button_02.sub",
						"down_image" : ROOT_PATH + "Middle_Button_03.sub",
					},

					{
						"name" : "fog_mode",
						"type" : "text",

						"x" : 30,
						"y" : 160+2,

						"text" : uiScriptLocale.OPTION_FOG,
					},

					{
						"name" : "fog_level0",
						"type" : "radio_button",

						"x" : 110,
						"y" : 160,

						"text" : uiScriptLocale.OPTION_FOG_DENSE,

						"default_image" : ROOT_PATH + "small_Button_01.sub",
						"over_image" : ROOT_PATH + "small_Button_02.sub",
						"down_image" : ROOT_PATH + "small_Button_03.sub",
					},

					{
						"name" : "fog_level1",
						"type" : "radio_button",

						"x" : 110+50,
						"y" : 160,

						"text" : uiScriptLocale.OPTION_FOG_MIDDLE,

						"default_image" : ROOT_PATH + "small_Button_01.sub",
						"over_image" : ROOT_PATH + "small_Button_02.sub",
						"down_image" : ROOT_PATH + "small_Button_03.sub",
					},

					{
						"name" : "fog_level2",
						"type" : "radio_button",

						"x" : 110 + 100,
						"y" : 160,

						"text" : uiScriptLocale.OPTION_FOG_LIGHT,

						"default_image" : ROOT_PATH + "small_Button_01.sub",
						"over_image" : ROOT_PATH + "small_Button_02.sub",
						"down_image" : ROOT_PATH + "small_Button_03.sub",
					},

					{
						"name" : "tiling_mode",
						"type" : "text",

						"x" : 40 + TEXT_TEMPORARY_X,
						"y" : 185+2,

						"text" : uiScriptLocale.OPTION_TILING,
					},

					{
						"name" : "tiling_cpu",
						"type" : "radio_button",

						"x" : 110,
						"y" : 185,

						"text" : uiScriptLocale.OPTION_TILING_CPU,

						"default_image" : ROOT_PATH + "small_Button_01.sub",
						"over_image" : ROOT_PATH + "small_Button_02.sub",
						"down_image" : ROOT_PATH + "small_Button_03.sub",
					},

					{
						"name" : "tiling_gpu",
						"type" : "radio_button",

						"x" : 110+50,
						"y" : 185,

						"text" : uiScriptLocale.OPTION_TILING_GPU,

						"default_image" : ROOT_PATH + "small_Button_01.sub",
						"over_image" : ROOT_PATH + "small_Button_02.sub",
						"down_image" : ROOT_PATH + "small_Button_03.sub",
					},

					{
						"name" : "tiling_apply",
						"type" : "button",

						"x" : 110+100,
						"y" : 185,

						"text" : uiScriptLocale.OPTION_TILING_APPLY,

						"default_image" : ROOT_PATH + "middle_Button_01.sub",
						"over_image" : ROOT_PATH + "middle_Button_02.sub",
						"down_image" : ROOT_PATH + "middle_Button_03.sub",
					},
					{
						"name" : "night_mode",
						"type" : "text",

						"x" : 40 + TEXT_TEMPORARY_X,
						"y" : 335,

						"text" : uiScriptLocale.OPTION_NIGHT_MODE,
					},

					{
						"name" : "night_mode_on",
						"type" : "button",

						"x" : 110,
						"y" : 335,

						"text" : uiScriptLocale.OPTION_NIGHT_MODE_ON,

						"default_image" : ROOT_PATH + "small_Button_01.sub",
						"over_image" : ROOT_PATH + "small_Button_02.sub",
						"down_image" : ROOT_PATH + "small_Button_03.sub",
					},

					{
						"name" : "night_mode_off",
						"type" : "button",

						"x" : 110+50,
						"y" : 335,

						"text" : uiScriptLocale.OPTION_NIGHT_MODE_OFF,

						"default_image" : ROOT_PATH + "small_Button_01.sub",
						"over_image" : ROOT_PATH + "small_Button_02.sub",
						"down_image" : ROOT_PATH + "small_Button_03.sub",
					},


	#				{
	#					"name" : "shadow_mode",
	#					"type" : "text",

	#					"x" : 30,
	#					"y" : 210,

	#					"text" : uiScriptLocale.OPTION_SHADOW,
	#				},

	#				{
	#					"name" : "shadow_bar",
	#					"type" : "sliderbar",

	#					"x" : 110,
	#					"y" : 210,
	#				},
				),
			},
		),
	}
else:
	window = {
		"name" : "SystemOptionDialog",
		"style" : ("movable", "float", "animate",),

		"x" : 0,
		"y" : 0,

		"width" : 305,
		"height" : 330,

		"children" :
		(
			{
				"name" : "board",
				"type" : "board",

				"x" : 0,
				"y" : 0,

				"width" : 305,
				"height" : 330,

				"children" :
				(
					## Title
					{
						"name" : "titlebar",
						"type" : "titlebar",
						"style" : ("attach",),

						"x" : 8,
						"y" : 8,

						"width" : 284,
						"color" : "gray",

						"children" :
						(
							{
							"name":"titlename", "type":"text", "x":0, "y":3,
							"horizontal_align":"center", "text_horizontal_align":"center",
							"text": uiScriptLocale.SYSTEMOPTION_TITLE,
							 },
						),
					},


					## Music
					{
						"name" : "music_name",
						"type" : "text",

						"x" : 30,
						"y" : 75,

						"text" : uiScriptLocale.OPTION_MUSIC,
					},

					{
						"name" : "music_volume_controller",
						"type" : "sliderbar",

						"x" : 110,
						"y" : 75,
					},

					{
						"name" : "bgm_button",
						"type" : "button",

						"x" : 20,
						"y" : 100,

						"text" : uiScriptLocale.OPTION_MUSIC_CHANGE,

						"default_image" : ROOT_PATH + "Middle_Button_01.sub",
						"over_image" : ROOT_PATH + "Middle_Button_02.sub",
						"down_image" : ROOT_PATH + "Middle_Button_03.sub",
					},

					{
						"name" : "bgm_file",
						"type" : "text",

						"x" : 100,
						"y" : 102,

						"text" : uiScriptLocale.OPTION_MUSIC_DEFAULT_THEMA,
					},

					## Sound
					{
						"name" : "sound_name",
						"type" : "text",

						"x" : 30,
						"y" : 50,

						"text" : uiScriptLocale.OPTION_SOUND,
					},

					{
						"name" : "sound_volume_controller",
						"type" : "sliderbar",

						"x" : 110,
						"y" : 50,
					},

					{
						"name" : "camera_mode",
						"type" : "text",

						"x" : 40 + TEXT_TEMPORARY_X,
						"y" : 135+2,

						"text" : uiScriptLocale.OPTION_CAMERA_DISTANCE,
					},

					{
						"name" : "camera_short",
						"type" : "radio_button",

						"x" : 110,
						"y" : 135,

						"text" : uiScriptLocale.OPTION_CAMERA_DISTANCE_SHORT,

						"default_image" : ROOT_PATH + "Middle_Button_01.sub",
						"over_image" : ROOT_PATH + "Middle_Button_02.sub",
						"down_image" : ROOT_PATH + "Middle_Button_03.sub",
					},

					{
						"name" : "camera_long",
						"type" : "radio_button",

						"x" : 110+70,
						"y" : 135,

						"text" : uiScriptLocale.OPTION_CAMERA_DISTANCE_LONG,

						"default_image" : ROOT_PATH + "Middle_Button_01.sub",
						"over_image" : ROOT_PATH + "Middle_Button_02.sub",
						"down_image" : ROOT_PATH + "Middle_Button_03.sub",
					},

					{
						"name" : "fog_mode",
						"type" : "text",

						"x" : 30,
						"y" : 160+2,

						"text" : uiScriptLocale.OPTION_FOG,
					},

					{
						"name" : "fog_level0",
						"type" : "radio_button",

						"x" : 110,
						"y" : 160,

						"text" : uiScriptLocale.OPTION_FOG_DENSE,

						"default_image" : ROOT_PATH + "small_Button_01.sub",
						"over_image" : ROOT_PATH + "small_Button_02.sub",
						"down_image" : ROOT_PATH + "small_Button_03.sub",
					},

					{
						"name" : "fog_level1",
						"type" : "radio_button",

						"x" : 110+50,
						"y" : 160,

						"text" : uiScriptLocale.OPTION_FOG_MIDDLE,

						"default_image" : ROOT_PATH + "small_Button_01.sub",
						"over_image" : ROOT_PATH + "small_Button_02.sub",
						"down_image" : ROOT_PATH + "small_Button_03.sub",
					},

					{
						"name" : "fog_level2",
						"type" : "radio_button",

						"x" : 110 + 100,
						"y" : 160,

						"text" : uiScriptLocale.OPTION_FOG_LIGHT,

						"default_image" : ROOT_PATH + "small_Button_01.sub",
						"over_image" : ROOT_PATH + "small_Button_02.sub",
						"down_image" : ROOT_PATH + "small_Button_03.sub",
					},

					{
						"name" : "tiling_mode",
						"type" : "text",

						"x" : 40 + TEXT_TEMPORARY_X,
						"y" : 185+2,

						"text" : uiScriptLocale.OPTION_TILING,
					},

					{
						"name" : "tiling_cpu",
						"type" : "radio_button",

						"x" : 110,
						"y" : 185,

						"text" : uiScriptLocale.OPTION_TILING_CPU,

						"default_image" : ROOT_PATH + "small_Button_01.sub",
						"over_image" : ROOT_PATH + "small_Button_02.sub",
						"down_image" : ROOT_PATH + "small_Button_03.sub",
					},

					{
						"name" : "tiling_gpu",
						"type" : "radio_button",

						"x" : 110+50,
						"y" : 185,

						"text" : uiScriptLocale.OPTION_TILING_GPU,

						"default_image" : ROOT_PATH + "small_Button_01.sub",
						"over_image" : ROOT_PATH + "small_Button_02.sub",
						"down_image" : ROOT_PATH + "small_Button_03.sub",
					},

					{
						"name" : "tiling_apply",
						"type" : "button",

						"x" : 110+100,
						"y" : 185,

						"text" : uiScriptLocale.OPTION_TILING_APPLY,

						"default_image" : ROOT_PATH + "middle_Button_01.sub",
						"over_image" : ROOT_PATH + "middle_Button_02.sub",
						"down_image" : ROOT_PATH + "middle_Button_03.sub",
					},
							

					{
						"name" : "fov_option",
						"type" : "text",

						"x" : 30,
						"y" : 380,

						"text" : uiScriptLocale.FOV_OPTION,
					},
					{
						"name" : "fov_controller",
						"type" : "sliderbar",

						"x" : 110,
						"y" : 380,
					},
					{
						"name" : "fov_reset_button",
						"type" : "button",

						"x" : 30 + 205,
						"y" : 380,

						"tooltip_text" : uiScriptLocale.FOV_RESET_OPTION_TOOLTIP,

						"default_image" : "d:/ymir work/ui/game/windows/reset_badge_button_default.tga",
						"over_image" : "d:/ymir work/ui/game/windows/reset_badge_button_over.tga",
						"down_image" : "d:/ymir work/ui/game/windows/reset_badge_button_down.tga",
					},
					{
						"name" : "fov_value_text",
						"type" : "text",

						"x" : 30 + 230,
						"y" : 380,

						"text" : "0",
					},
					
					## ENABLE_DOG_MODE
					{
						"name" : "dogmode_on_off",
						"type" : "text",

						"multi_line" : 1,

						"x" : 40 + TEXT_TEMPORARY_X,
						"y" : 346+3,
						"text" : uiScriptLocale.DOG_MODE1,
					},
					{
						"name" : "dog_mode_open",
						"type" : "radio_button",

						"x" : 110,
						"y" : 346,

						"text" : uiScriptLocale.DOG_MODE3,

						"default_image" : ROOT_PATH + "middle_button_01.sub",
						"over_image" : ROOT_PATH + "middle_button_02.sub",
						"down_image" : ROOT_PATH + "middle_button_03.sub",
					},
					{
						"name" : "dog_mode_close",
						"type" : "radio_button",

						"x" : 110 + 70,
						"y" : 346,

						"text" : uiScriptLocale.DOG_MODE2,

						"default_image" : ROOT_PATH + "middle_button_01.sub",
						"over_image" : ROOT_PATH + "middle_button_02.sub",
						"down_image" : ROOT_PATH + "middle_button_03.sub",
					},					

	#				{
	#					"name" : "shadow_mode",
	#					"type" : "text",

	#					"x" : 30,
	#					"y" : 210,

	#					"text" : uiScriptLocale.OPTION_SHADOW,
	#				},

	#				{
	#					"name" : "shadow_bar",
	#					"type" : "sliderbar",

	#					"x" : 110,
	#					"y" : 210,
	#				},
				),
			},
		),
	}
import app
if app.__BL_GRAPHIC_ON_OFF__:
	window["height"] = window["height"] + 90
	window["children"][0]["height"] = window["children"][0]["height"] + 90
	window["children"][0]["children"] = window["children"][0]["children"] + (
		{
			"name" : "graphic_on_off_window",
			"type" : "window",
		
			"x" : 0,
			"y" : 210,

			"width" : 305,
			"height" : 150,
			
			"children" :
			[
				## 그래픽 ON/OFF: EFFECT
				{
					"name" : "effect_level",
					"type" : "text",

					"x" : 40 + TEXT_TEMPORARY_X,
					"y" : 0+2,

					"text" : uiScriptLocale.GRAPHICONOFF_EFFECT_LEVEL, 
				},
				
				{
					"name" : "effect_level1",
					"type" : "radio_button",

					"x" : 112,
					"y" : 0,

					"text" :  uiScriptLocale.GRAPHICONOFF_EFFECT_LEVEL1,
					"tooltip_text" : uiScriptLocale.GRAPHICONOFF_EFFECT_LEVEL1_TOOLTIP,

					"default_image" : ROOT_PATH + "minimize_empty_button_01.sub",
					"over_image" : ROOT_PATH + "minimize_empty_button_02.sub",
					"down_image" : ROOT_PATH + "minimize_empty_button_03.sub",
				},
				
				{
					"name" : "effect_level2",
					"type" : "radio_button",

					"x" : 112 + 20,
					"y" : 0,

					"text" :  uiScriptLocale.GRAPHICONOFF_EFFECT_LEVEL2,
					"tooltip_text" : uiScriptLocale.GRAPHICONOFF_EFFECT_LEVEL2_TOOLTIP,

					"default_image" : ROOT_PATH + "minimize_empty_button_01.sub",
					"over_image" : ROOT_PATH + "minimize_empty_button_02.sub",
					"down_image" : ROOT_PATH + "minimize_empty_button_03.sub",
				},
				
				{
					"name" : "effect_level3",
					"type" : "radio_button",

					"x" : 112 + 40,
					"y" : 0,

					"text" :  uiScriptLocale.GRAPHICONOFF_EFFECT_LEVEL3,
					"tooltip_text" : uiScriptLocale.GRAPHICONOFF_EFFECT_LEVEL3_TOOLTIP,

					"default_image" : ROOT_PATH + "minimize_empty_button_01.sub",
					"over_image" : ROOT_PATH + "minimize_empty_button_02.sub",
					"down_image" : ROOT_PATH + "minimize_empty_button_03.sub",
				},
				
				{
					"name" : "effect_level4",
					"type" : "radio_button",

					"x" : 112 + 60,
					"y" : 0,

					"text" :  uiScriptLocale.GRAPHICONOFF_EFFECT_LEVEL4,
					"tooltip_text" : uiScriptLocale.GRAPHICONOFF_EFFECT_LEVEL4_TOOLTIP,

					"default_image" : ROOT_PATH + "minimize_empty_button_01.sub",
					"over_image" : ROOT_PATH + "minimize_empty_button_02.sub",
					"down_image" : ROOT_PATH + "minimize_empty_button_03.sub",
				},
				
				{
					"name" : "effect_level5",
					"type" : "radio_button",

					"x" : 112 + 80,
					"y" : 0,

					"text" :  uiScriptLocale.GRAPHICONOFF_EFFECT_LEVEL5,
					"tooltip_text" : uiScriptLocale.GRAPHICONOFF_EFFECT_LEVEL5_TOOLTIP,

					"default_image" : ROOT_PATH + "minimize_empty_button_01.sub",
					"over_image" : ROOT_PATH + "minimize_empty_button_02.sub",
					"down_image" : ROOT_PATH + "minimize_empty_button_03.sub",
				},
				
				{
					"name" : "effect_apply",
					"type" : "button",

					"x" : 110+105,
					"y" : 0,

					"text" : uiScriptLocale.GRAPHICONOFF_EFFECT_APPLY,

					"default_image" : ROOT_PATH + "middle_Button_01.sub",
					"over_image" : ROOT_PATH + "middle_Button_02.sub",
					"down_image" : ROOT_PATH + "middle_Button_03.sub",
				},
				
				## 그래픽 ON/OFF: 개인상점
				{
					"name" : "privateShop_level",
					"type" : "text",

					"x" : 40 + TEXT_TEMPORARY_X,
					"y" : 25+2,

					"text" : uiScriptLocale.GRAPHICONOFF_PRIVATE_SHOP_LEVEL, 
				},
				
					{
						"name" : "hidemode_0",
						"type" : "toggle_button",
						"x" : 0,
						"y" : 0,
						#"text" : uiScriptLocale.HIDE_OPTION3,
						#"default_image" : ROOT_PATH + "middle_button_01.sub",
						#"over_image" : ROOT_PATH + "middle_button_02.sub",
						#"down_image" : ROOT_PATH + "middle_button_03.sub",
					},	

					{
						"name" : "hidemode_1",
						"type" : "toggle_button",
						"x" : 0,
						"y" : 0,
						#"text" : uiScriptLocale.HIDE_OPTION3,
						#"default_image" : ROOT_PATH + "middle_button_01.sub",
						#"over_image" : ROOT_PATH + "middle_button_02.sub",
						#"down_image" : ROOT_PATH + "middle_button_03.sub",
					},				


					{
						"name" : "hidemode_2",
						"type" : "toggle_button",
						"x" : 0,
						"y" : 0,
						#"text" : uiScriptLocale.HIDE_OPTION3,
						#"default_image" : ROOT_PATH + "middle_button_01.sub",
						#"over_image" : ROOT_PATH + "middle_button_02.sub",
						#"down_image" : ROOT_PATH + "middle_button_03.sub",
					},				
					

					{
						"name" : "hidemode_3",
						"type" : "toggle_button",
						"x" : 110,
						"y" : 26,
						"text" : uiScriptLocale.HIDE_OPTION3,
						"default_image" : ROOT_PATH + "middle_button_01.sub",
						"over_image" : ROOT_PATH + "middle_button_02.sub",
						"down_image" : ROOT_PATH + "middle_button_03.sub",
					},
					{
						"name" : "hidemode_4",
						"type" : "toggle_button",
						"x" : 110+80,
						"y" : 26,
						"text" : uiScriptLocale.HIDE_OPTION4,
						"default_image" : ROOT_PATH + "middle_button_01.sub",
						"over_image" : ROOT_PATH + "middle_button_02.sub",
						"down_image" : ROOT_PATH + "middle_button_03.sub",
					},		
					
					{
						"name" : "hidemode_5",
						"type" : "toggle_button",
						"x" : 0,
						"y" : 0,
						#"text" : uiScriptLocale.HIDE_OPTION3,
						#"default_image" : ROOT_PATH + "middle_button_01.sub",
						#"over_image" : ROOT_PATH + "middle_button_02.sub",
						#"down_image" : ROOT_PATH + "middle_button_03.sub",
					},	

					{
						"name" : "hidemode_6",
						"type" : "toggle_button",
						"x" : 0,
						"y" : 0,
						#"text" : uiScriptLocale.HIDE_OPTION3,
						#"default_image" : ROOT_PATH + "middle_button_01.sub",
						#"over_image" : ROOT_PATH + "middle_button_02.sub",
						#"down_image" : ROOT_PATH + "middle_button_03.sub",
					},				
					
						{
							"name" : "hide2_mode",
							"type" : "text",
							"x" : 0,
							"y" : 0,
							#"text" : uiScriptLocale.HIDE_2_OPTION,
						},
						{
							"name" : "hide2mode_0",
							"type" : "toggle_button",
							"x" : 0,
							"y" : 0,
							#"text" : uiScriptLocale.HIDE_2_OPTION0,
							#"default_image" : ROOT_PATH + "large_button_01.sub",
							#"over_image" : ROOT_PATH + "large_button_02.sub",
							#"down_image" : ROOT_PATH + "large_button_03.sub",
						},
						{
							"name" : "hide2mode_2",
							"type" : "toggle_button",
							"x" : 0,
							"y" : 0,
							#"text" : uiScriptLocale.HIDE_2_OPTION2,
							#"default_image" : ROOT_PATH + "middle_button_01.sub",
							#"over_image" : ROOT_PATH + "middle_button_02.sub",
							#"down_image" : ROOT_PATH + "middle_button_03.sub",
						},
						{
							"name" : "hide2mode_1",
							"type" : "toggle_button",
							"x" : 0,
							"y" : 0,
							#"text" : uiScriptLocale.HIDE_2_OPTION1,
							#"default_image" : ROOT_PATH + "large_button_01.sub",
							#"over_image" : ROOT_PATH + "large_button_02.sub",
							#"down_image" : ROOT_PATH + "large_button_03.sub",
						},
						{
							"name" : "hide2mode_3",
							"type" : "toggle_button",
							"x" : 0,
							"y" : 0,
							#"text" : uiScriptLocale.HIDE_2_OPTION3,
							#"default_image" : ROOT_PATH + "middle_button_01.sub",
							#"over_image" : ROOT_PATH + "middle_button_02.sub",
							#"down_image" : ROOT_PATH + "middle_button_03.sub",
						},		


				## 그래픽 ON/OFF: Drop Item
				{
					"name" : "dropItem_level",
					"type" : "text",

					"x" : 40 + TEXT_TEMPORARY_X,
					"y" : 50+2,

					"text" : uiScriptLocale.GRAPHICONOFF_DROP_ITEM_LEVEL, 
				},
				
				{
					"name" : "dropItem_level1",
					"type" : "radio_button",

					"x" : 112,
					"y" : 50,

					"text" :  uiScriptLocale.GRAPHICONOFF_DROP_ITEM_LEVEL1,
					"tooltip_text" : uiScriptLocale.GRAPHICONOFF_DROP_ITEM_LEVEL1_TOOLTIP, 

					"default_image" : ROOT_PATH + "minimize_empty_button_01.sub",
					"over_image" : ROOT_PATH + "minimize_empty_button_02.sub",
					"down_image" : ROOT_PATH + "minimize_empty_button_03.sub",
				},
				
				{
					"name" : "dropItem_level2",
					"type" : "radio_button",

					"x" : 112 + 20,
					"y" : 50,

					"text" :  uiScriptLocale.GRAPHICONOFF_DROP_ITEM_LEVEL2,
					"tooltip_text" : uiScriptLocale.GRAPHICONOFF_DROP_ITEM_LEVEL2_TOOLTIP, 

					"default_image" : ROOT_PATH + "minimize_empty_button_01.sub",
					"over_image" : ROOT_PATH + "minimize_empty_button_02.sub",
					"down_image" : ROOT_PATH + "minimize_empty_button_03.sub",
				},
				
				{
					"name" : "dropItem_level3",
					"type" : "radio_button",

					"x" : 112 + 40,
					"y" : 50,

					"text" :  uiScriptLocale.GRAPHICONOFF_DROP_ITEM_LEVEL3,
					"tooltip_text" : uiScriptLocale.GRAPHICONOFF_DROP_ITEM_LEVEL3_TOOLTIP, 

					"default_image" : ROOT_PATH + "minimize_empty_button_01.sub",
					"over_image" : ROOT_PATH + "minimize_empty_button_02.sub",
					"down_image" : ROOT_PATH + "minimize_empty_button_03.sub",
				},
				
				{
					"name" : "dropItem_level4",
					"type" : "radio_button",

					"x" : 112 + 60,
					"y" : 50,

					"text" :  uiScriptLocale.GRAPHICONOFF_DROP_ITEM_LEVEL4,
					"tooltip_text" : uiScriptLocale.GRAPHICONOFF_DROP_ITEM_LEVEL4_TOOLTIP, 

					"default_image" : ROOT_PATH + "minimize_empty_button_01.sub",
					"over_image" : ROOT_PATH + "minimize_empty_button_02.sub",
					"down_image" : ROOT_PATH + "minimize_empty_button_03.sub",
				},
				
				{
					"name" : "dropItem_level5",
					"type" : "radio_button",

					"x" : 112 + 80,
					"y" : 50,

					"text" :  uiScriptLocale.GRAPHICONOFF_DROP_ITEM_LEVEL5,
					"tooltip_text" : uiScriptLocale.GRAPHICONOFF_DROP_ITEM_LEVEL5_TOOLTIP, 

					"default_image" : ROOT_PATH + "minimize_empty_button_01.sub",
					"over_image" : ROOT_PATH + "minimize_empty_button_02.sub",
					"down_image" : ROOT_PATH + "minimize_empty_button_03.sub",
				},
				
				{
					"name" : "dropItem_apply",
					"type" : "button",

					"x" : 110+105,
					"y" : 50,

					"text" : uiScriptLocale.GRAPHICONOFF_DROP_ITEM_APPLY,

					"default_image" : ROOT_PATH + "middle_Button_01.sub",
					"over_image" : ROOT_PATH + "middle_Button_02.sub",
					"down_image" : ROOT_PATH + "middle_Button_03.sub",
				},
				
				## 그래픽 ON/OFF: 펫
				{
					"name" : "pet_status",
					"type" : "text",

					"x" : 40 + TEXT_TEMPORARY_X,
					"y" : 75+2,

					"text" : uiScriptLocale.GRAPHICONOFF_PET_STATUS,
				},
				
				{
					"name" : "pet_on",
					"type" : "radio_button",

					"x" : 110,
					"y" : 75,

					"text" : uiScriptLocale.GRAPHICONOFF_PET_STATUS_ON,
					"tooltip_text" : uiScriptLocale.GRAPHICONOFF_PET_STATUS_ON_TOOLTIP,
					

					"default_image" : ROOT_PATH + "small_Button_01.sub",
					"over_image" : ROOT_PATH + "small_Button_02.sub",
					"down_image" : ROOT_PATH + "small_Button_03.sub",
				},
				
				{
					"name" : "pet_off",
					"type" : "radio_button",

					"x" : 110 + 50,
					"y" : 75,

					"text" : uiScriptLocale.GRAPHICONOFF_PET_STATUS_OFF,
					"tooltip_text" : uiScriptLocale.GRAPHICONOFF_PET_STATUS_OFF_TOOLTIP,

					"default_image" : ROOT_PATH + "small_Button_01.sub",
					"over_image" : ROOT_PATH + "small_Button_02.sub",
					"down_image" : ROOT_PATH + "small_Button_03.sub",
				},
				
				## 그래픽 ON/OFF: NPC Name
				{
					"name" : "npcName_status",
					"type" : "text",

					"x" : 40 + TEXT_TEMPORARY_X,
					"y" : 100+2,

					"text" : uiScriptLocale.GRAPHICONOFF_NPC_NAME_STATUS,
				},
				
				{
					"name" : "npcName_on",
					"type" : "radio_button",

					"x" : 110,
					"y" : 100,

					"text" : uiScriptLocale.GRAPHICONOFF_NPC_NAME_STATUS_ON,
					"tooltip_text" : uiScriptLocale.GRAPHICONOFF_NPC_NAME_STATUS_ON_TOOLTIP,

					"default_image" : ROOT_PATH + "small_Button_01.sub",
					"over_image" : ROOT_PATH + "small_Button_02.sub",
					"down_image" : ROOT_PATH + "small_Button_03.sub",
				},
				
				{
					"name" : "npcName_off",
					"type" : "radio_button",

					"x" : 110 + 50,
					"y" : 100,

					"text" : uiScriptLocale.GRAPHICONOFF_NPC_NAME_STATUS_OFF,
					"tooltip_text" : uiScriptLocale.GRAPHICONOFF_NPC_NAME_STATUS_OFF_TOOLTIP,  

					"default_image" : ROOT_PATH + "small_Button_01.sub",
					"over_image" : ROOT_PATH + "small_Button_02.sub",
					"down_image" : ROOT_PATH + "small_Button_03.sub",
				},
			],
		},
	)