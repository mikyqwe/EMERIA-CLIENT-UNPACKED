import uiScriptLocale

IMG_PATH = "d:/ymir work/ui/intro/login/"
IMG_LANG_PATH = "d:/ymir work/ui/intro/login/lang_buttons/"

CH_START_X = 4
CH_STEP_X = 80

CH_TEXT_1_Y = 30
CH_TEXT_2_Y = 50

BUTTON_START_X = 25
BUTTON_START_Y = 411
BUTTON_STEP_X = 385
BUTTON_STEP_Y = 46

SAFE_INPUT_X = 425
SAFE_INPUT_START_Y = 115
SAFE_INPUT_STEP_Y = 55

LANG_BUTTON_STEP_X = 60

window = {
	"sytle" : ("movable",),
	"x" : 0, "y" : 0,
	"width" : SCREEN_WIDTH,
	"height" : SCREEN_HEIGHT,
	"children" : 
	(
		{
			"name" : "background", 
			"type" : "expanded_image",
			"x" : 0, "y" : 0,
			"x_scale" : float(SCREEN_WIDTH) / 1920.0,
			"y_scale" : float(SCREEN_HEIGHT) / 1080.0,
			"image" : IMG_PATH + "background.jpg",
			"children" : 
			(
				{ "name" : "video_layer",  "type" : "window", "x" : 0, "y" : 0, "width" : SCREEN_WIDTH, "height" : SCREEN_HEIGHT, },
				{
					"name" : "board_main",
					"type" : "window",
					"x" : 0, "y" : 0,
					"width" : 860, "height" : 430,
					"vertical_align" : "center",
					"horizontal_align" : "center",
					"children" :
					(
						{
							"name" : "board",
							"type" : "image",
							"x" : 0, "y" : 0,
							"image" : IMG_PATH + "base_board.png",
							"children" :
							(
								
								## LOGIN
								{
									"name" : "input_user",
									"type" : "image",
									"x" : 300, "y" : 121,
									"image" : IMG_PATH + "input_slot_id_normal.png",
									"children" : 
									(
										{
											"name" : "id_focus_background",
											"type" : "image",
											"x" : 0, "y" : 0,
											"image" : IMG_PATH + "input_slot_id_focus.png",
										},
										{
											"name" : "id",
											"type" : "editline",
											"x" : 50, "y" : 12,
											"width" : 256, "height" : 16,
											"color" : 0xffbeaa87,
											"fontsize":"LARGE",
											"input_limit": 16,
										},
									),
								},
								{
									"name" : "input_password",
									"type" : "image",
									"x" : 300, "y" : 166,
									"image" : IMG_PATH + "input_slot_pw_normal.png",
									"children" : 
									(
										{
											"name" : "pw_focus_background",
											"type" : "image",
											"x" : 0, "y" : 0,
											"image" : IMG_PATH + "input_slot_pw_focus.png",
										},
										{
											"name" : "pwd",
											"type" : "editline",
											"x" : 50, "y" : 12,
											"width" : 256, "height" : 16,
											"color" : 0xffbeaa87,
											"fontsize":"LARGE",
											"input_limit": 16,
											"secret_flag": 1,
										},
									),
								},
								{
									"name" : "input_pin",
									"type" : "image",
									"x" : 300, "y" : 211,
									"image" : IMG_PATH + "input_slot_pin_normal.png",
									"children" : 
									(
										{
											"name" : "pin_focus_background",
											"type" : "image",
											"x" : 0, "y" : 0,
											"image" : IMG_PATH + "input_slot_pin_focus.png",
										},
										{
											"name" : "pin",
											"type" : "editline",
											"x" : 50, "y" : 12,
											"width" : 256, "height" : 16,
											"color" : 0xffbeaa87,
											"fontsize":"LARGE",
											"input_limit": 4,
											"secret_flag": 1,
										},
									),
								},
								
								
								
								{
									"name" : "login_button",
									"type" : "button",
									"x" : 299, "y" : 272,
									"default_image" : IMG_PATH + "button_login_normal.png",
									"over_image" : IMG_PATH + "button_login_hover.png",
									"down_image" : IMG_PATH + "button_login_down.png",
								},
								{
									"name" : "forgot_pw_button",
									"type" : "button",
									"x" : 366, "y" : 337,
									"default_image" : IMG_PATH + "forgot_pw_normal.png",
									"over_image" : IMG_PATH + "forgot_pw_hover.png",
									"down_image" : IMG_PATH + "forgot_pw_down.png",
								},
								{
									"name" : "sign_in_button",
									"type" : "button",
									"x" : 462, "y" : 373,
									"default_image" : IMG_PATH + "sign_in_normal.png",
									"over_image" : IMG_PATH + "sign_in_hover.png",
									"down_image" : IMG_PATH + "sign_in_down.png",
								},
								
								#####################################################
								
								{
									"name" : "channel_1_info",
									"type" : "image",
									"x" : 23, "y" : 161,
									"image" : IMG_PATH + "input_slot_side.png",
									"children" : 
									(
										{
											"name" : "ch1_online",
											"type" : "image",
											"x" : 8, "y" : 12,
											"image" : IMG_PATH + "point_online.png",
										},
										{
											"name" : "ch1_offline",
											"type" : "image",
											"x" : 8, "y" : 12,
											"image" : IMG_PATH + "point_offline.png",
										},
										{
											"name" : "state_ch1",
											"type" : "text",

											"x" : 26, "y" : 10,
											"color" : 0xff727272,
											"fontsize":"SLARGE",

											"text" : "Channel 1",
										},
										{
											"name" : "select_btn_ch1",
											"type" : "radio_button",
											"x" : 204, "y" : 8,
											"default_image" : IMG_PATH + "sel_channel_btn_normal.png",
											"over_image" : IMG_PATH + "sel_channel_btn_hover.png",
											"down_image" : IMG_PATH + "sel_channel_btn_active.png",
										},
									),
								},
								{
									"name" : "channel_2_info",
									"type" : "image",
									"x" : 23, "y" : 206,
									"image" : IMG_PATH + "input_slot_side.png",
									"children" : 
									(
										{
											"name" : "ch2_online",
											"type" : "image",
											"x" : 8, "y" : 12,
											"image" : IMG_PATH + "point_online.png",
										},
										{
											"name" : "ch2_offline",
											"type" : "image",
											"x" : 8, "y" : 12,
											"image" : IMG_PATH + "point_offline.png",
										},
										{
											"name" : "state_ch2",
											"type" : "text",

											"x" : 26, "y" : 10,
											"color" : 0xff727272,
											"fontsize":"SLARGE",

											"text" : "Channel 2",
										},
										{
											"name" : "select_btn_ch2",
											"type" : "radio_button",
											"x" : 204, "y" : 8,
											"default_image" : IMG_PATH + "sel_channel_btn_normal.png",
											"over_image" : IMG_PATH + "sel_channel_btn_hover.png",
											"down_image" : IMG_PATH + "sel_channel_btn_active.png",
										},
									),
								},
								{
									"name" : "channel_3_info",
									"type" : "image",
									"x" : 23, "y" : 250,
									"image" : IMG_PATH + "input_slot_side.png",
									"children" : 
									(
										{
											"name" : "ch3_online",
											"type" : "image",
											"x" : 8, "y" : 12,
											"image" : IMG_PATH + "point_online.png",
										},
										{
											"name" : "ch3_offline",
											"type" : "image",
											"x" : 8, "y" : 12,
											"image" : IMG_PATH + "point_offline.png",
										},
										{
											"name" : "state_ch3",
											"type" : "text",

											"x" : 26, "y" : 10,
											"color" : 0xff727272,
											"fontsize":"SLARGE",

											"text" : "Channel 3",
										},
										{
											"name" : "select_btn_ch3",
											"type" : "radio_button",
											"x" : 204, "y" : 8,
											"default_image" : IMG_PATH + "sel_channel_btn_normal.png",
											"over_image" : IMG_PATH + "sel_channel_btn_hover.png",
											"down_image" : IMG_PATH + "sel_channel_btn_active.png",
										},
									),
								},
								{
									"name" : "channel_4_info",
									"type" : "image",
									"x" : 23, "y" : 295,
									"image" : IMG_PATH + "input_slot_side.png",
									"children" : 
									(
										{
											"name" : "ch4_online",
											"type" : "image",
											"x" : 8, "y" : 12,
											"image" : IMG_PATH + "point_online.png",
										},
										{
											"name" : "ch4_offline",
											"type" : "image",
											"x" : 8, "y" : 12,
											"image" : IMG_PATH + "point_offline.png",
										},
										{
											"name" : "state_ch4",
											"type" : "text",

											"x" : 26, "y" : 10,
											"color" : 0xff727272,
											"fontsize":"SLARGE",

											"text" : "Channel 4",
										},
										{
											"name" : "select_btn_ch4",
											"type" : "radio_button",
											"x" : 204, "y" : 8,
											"default_image" : IMG_PATH + "sel_channel_btn_normal.png",
											"over_image" : IMG_PATH + "sel_channel_btn_hover.png",
											"down_image" : IMG_PATH + "sel_channel_btn_active.png",
										},
									),
								},
								
								## ACCOUNT-MANAGEMENT
								{
									"name" : "input_safe_f1",
									"type" : "image",
									"x" : 604, "y" : 161,
									"image" : IMG_PATH + "input_slot_side.png",
									"children" : 
									(
										{
											"name" : "f1_login_button",
											"type" : "button",
											"x" : 175, "y" : 8,
											"default_image" : IMG_PATH + "button_sel_account_normal.png",
											"over_image" : IMG_PATH + "button_sel_account_hover.png",
											"down_image" : IMG_PATH + "button_sel_account_down.png",
										},
										{
											"name" : "f1_delete_button",
											"type" : "button",
											"x" : 204, "y" : 8,
											"default_image" : IMG_PATH + "button_del_account_normal.png",
											"over_image" : IMG_PATH + "button_del_account_hover.png",
											"down_image" : IMG_PATH + "button_del_account_down.png",
										},
										{
											"name" : "f1_save_button",
											"type" : "button",
											"x" : 204, "y" : 8,
											"default_image" : IMG_PATH + "button_safe_normal.png",
											"over_image" : IMG_PATH + "button_safe_hover.png",
											"down_image" : IMG_PATH + "button_safe_down.png",
										},
										{
											"name" : "number_text_0",
											"type" : "text",

											"x" : 13, "y" : 10,
											"color" : 0xff727272,
											"fontsize": "SLARGE",

											"text" : "1.",
										},
										{
											"name" : "account_text_0",
											"type" : "text",

											"x" : 30, "y" : 10,
											"color" : 0xff727272,
											"fontsize": "SLARGE",

											"text" : "Free Slot",
										},
									),
								},
								{
									"name" : "input_safe_f2",
									"type" : "image",
									"x" : 604, "y" : 206,
									"image" : IMG_PATH + "input_slot_side.png",
									"children" : 
									(
										{
											"name" : "f2_login_button",
											"type" : "button",
											"x" : 175, "y" : 8,
											"default_image" : IMG_PATH + "button_sel_account_normal.png",
											"over_image" : IMG_PATH + "button_sel_account_hover.png",
											"down_image" : IMG_PATH + "button_sel_account_down.png",
										},
										{
											"name" : "f2_delete_button",
											"type" : "button",
											"x" : 204, "y" : 8,
											"default_image" : IMG_PATH + "button_del_account_normal.png",
											"over_image" : IMG_PATH + "button_del_account_hover.png",
											"down_image" : IMG_PATH + "button_del_account_down.png",
										},
										{
											"name" : "f2_save_button",
											"type" : "button",
											"x" : 204, "y" : 8,
											"default_image" : IMG_PATH + "button_safe_normal.png",
											"over_image" : IMG_PATH + "button_safe_hover.png",
											"down_image" : IMG_PATH + "button_safe_down.png",
										},
										{
											"name" : "number_text_1",
											"type" : "text",

											"x" : 13, "y" : 10,
											"color" : 0xff727272,
											"fontsize": "SLARGE",

											"text" : "2.",
										},
										{
											"name" : "account_text_1",
											"type" : "text",

											"x" : 30, "y" : 10,
											"color" : 0xff727272,
											"fontsize": "SLARGE",

											"text" : "Free Slot",
										},
									),
								},
								{
									"name" : "input_safe_f3",
									"type" : "image",
									"x" : 604, "y" : 251,
									"image" : IMG_PATH + "input_slot_side.png",
									"children" : 
									(
										{
											"name" : "f3_login_button",
											"type" : "button",
											"x" : 175, "y" : 8,
											"default_image" : IMG_PATH + "button_sel_account_normal.png",
											"over_image" : IMG_PATH + "button_sel_account_hover.png",
											"down_image" : IMG_PATH + "button_sel_account_down.png",
										},
										{
											"name" : "f3_delete_button",
											"type" : "button",
											"x" : 204, "y" : 8,
											"default_image" : IMG_PATH + "button_del_account_normal.png",
											"over_image" : IMG_PATH + "button_del_account_hover.png",
											"down_image" : IMG_PATH + "button_del_account_down.png",
										},
										{
											"name" : "f3_save_button",
											"type" : "button",
											"x" : 204, "y" : 8,
											"default_image" : IMG_PATH + "button_safe_normal.png",
											"over_image" : IMG_PATH + "button_safe_hover.png",
											"down_image" : IMG_PATH + "button_safe_down.png",
										},
										{
											"name" : "number_text_2",
											"type" : "text",

											"x" : 13, "y" : 10,
											"color" : 0xff727272,
											"fontsize": "SLARGE",

											"text" : "3.",
										},
										{
											"name" : "account_text_2",
											"type" : "text",

											"x" : 30, "y" : 10,
											"color" : 0xff727272,
											"fontsize": "SLARGE",

											"text" : "Free Slot",
										},
									),
								},
								{
									"name" : "input_safe_f4",
									"type" : "image",
									"x" : 604, "y" : 296,
									"image" : IMG_PATH + "input_slot_side.png",
									"children" : 
									(
										{
											"name" : "f4_login_button",
											"type" : "button",
											"x" : 175, "y" : 8,
											"default_image" : IMG_PATH + "button_sel_account_normal.png",
											"over_image" : IMG_PATH + "button_sel_account_hover.png",
											"down_image" : IMG_PATH + "button_sel_account_down.png",
										},
										{
											"name" : "f4_delete_button",
											"type" : "button",
											"x" : 204, "y" : 8,
											"default_image" : IMG_PATH + "button_del_account_normal.png",
											"over_image" : IMG_PATH + "button_del_account_hover.png",
											"down_image" : IMG_PATH + "button_del_account_down.png",
										},
										{
											"name" : "f4_save_button",
											"type" : "button",
											"x" : 204, "y" : 8,
											"default_image" : IMG_PATH + "button_safe_normal.png",
											"over_image" : IMG_PATH + "button_safe_hover.png",
											"down_image" : IMG_PATH + "button_safe_down.png",
										},
										{
											"name" : "number_text_3",
											"type" : "text",

											"x" : 13, "y" : 10,
											"color" : 0xff727272,
											"fontsize": "SLARGE",

											"text" : "4.",
										},
										{
											"name" : "account_text_3",
											"type" : "text",

											"x" : 30, "y" : 10,
											"color" : 0xff727272,
											"fontsize": "SLARGE",

											"text" : "Free Slot",
										},
									),
								},
								##########################################################################################
							),
						},
					),
				},
				
				{
					"name" : "exit_button",
					"type" : "button",
					"vertical_align" : "center", "horizontal_align" : "center",
					"x" : 0, "y" : 260,
					"default_image" : IMG_PATH + "button_exit_normal.png",
					"over_image" : IMG_PATH + "button_exit_hover.png",
					"down_image" : IMG_PATH + "button_exit_down.png",
				},
				
				{
					"name" : "lang_button_0",
					"type" : "button",
					"x" : SCREEN_WIDTH-90-LANG_BUTTON_STEP_X*10, "y" : SCREEN_HEIGHT-50,
					"default_image" : IMG_LANG_PATH + "button_cz.png",
					"over_image" :  IMG_LANG_PATH + "button_cz_hov.png",
					"down_image" : IMG_LANG_PATH + "button_cz.png",
				},
				{
					"name" : "lang_button_1",
					"type" : "button",
					"x" : SCREEN_WIDTH-90-LANG_BUTTON_STEP_X*9, "y" : SCREEN_HEIGHT-50,
					"default_image" : IMG_LANG_PATH + "button_de.png",
					"over_image" :  IMG_LANG_PATH + "button_de_hov.png",
					"down_image" : IMG_LANG_PATH + "button_de.png",
				},
				{
					"name" : "lang_button_2",
					"type" : "button",
					"x" : SCREEN_WIDTH-90-LANG_BUTTON_STEP_X*8, "y" : SCREEN_HEIGHT-50,
					"default_image" : IMG_LANG_PATH + "button_en.png",
					"over_image" :  IMG_LANG_PATH + "button_en_hov.png",
					"down_image" : IMG_LANG_PATH + "lbutton_en.png",
				},
				{
					"name" : "lang_button_3",
					"type" : "button",
					"x" : SCREEN_WIDTH-90-LANG_BUTTON_STEP_X*7, "y" : SCREEN_HEIGHT-50,
					"default_image" : IMG_LANG_PATH + "button_es.png",
					"over_image" :  IMG_LANG_PATH + "button_es_hov.png",
					"down_image" : IMG_LANG_PATH + "button_es.png",
				},
				{
					"name" : "lang_button_4",
					"type" : "button",
					"x" : SCREEN_WIDTH-90-LANG_BUTTON_STEP_X*6, "y" : SCREEN_HEIGHT-50,
					"default_image" : IMG_LANG_PATH + "button_gr.png",
					"over_image" :  IMG_LANG_PATH + "button_gr_hov.png",
					"down_image" : IMG_LANG_PATH + "button_gr.png",
				},
				{
					"name" : "lang_button_5",
					"type" : "button",
					"x" : SCREEN_WIDTH-90-LANG_BUTTON_STEP_X*5, "y" : SCREEN_HEIGHT-50,
					"default_image" : IMG_LANG_PATH + "button_hu.png",
					"over_image" :  IMG_LANG_PATH + "button_hu_hov.png",
					"down_image" : IMG_LANG_PATH + "button_hu.png",
				},
				{
					"name" : "lang_button_6",
					"type" : "button",
					"x" : SCREEN_WIDTH-90-LANG_BUTTON_STEP_X*4, "y" : SCREEN_HEIGHT-50,
					"default_image" : IMG_LANG_PATH + "button_it.png",
					"over_image" :  IMG_LANG_PATH + "button_it_hov.png",
					"down_image" : IMG_LANG_PATH + "button_it.png",
				},
				{
					"name" : "lang_button_7",
					"type" : "button",
					"x" : SCREEN_WIDTH-90-LANG_BUTTON_STEP_X*3, "y" : SCREEN_HEIGHT-50,
					"default_image" : IMG_LANG_PATH + "button_pl.png",
					"over_image" :  IMG_LANG_PATH + "button_pl_hov.png",
					"down_image" : IMG_LANG_PATH + "button_pl.png",
				},
				{
					"name" : "lang_button_8",
					"type" : "button",
					"x" : SCREEN_WIDTH-90-LANG_BUTTON_STEP_X*2, "y" : SCREEN_HEIGHT-50,
					"default_image" : IMG_LANG_PATH + "button_pt.png",
					"over_image" :  IMG_LANG_PATH + "button_pt_hov.png",
					"down_image" : IMG_LANG_PATH + "button_pt.png",
				},
				{
					"name" : "lang_button_9",
					"type" : "button",
					"x" : SCREEN_WIDTH-90-LANG_BUTTON_STEP_X*1, "y" : SCREEN_HEIGHT-50,
					"default_image" : IMG_LANG_PATH + "button_ro.png",
					"over_image" :  IMG_LANG_PATH + "button_ro_hov.png",
					"down_image" : IMG_LANG_PATH + "button_ro.png",
				},
				{
					"name" : "lang_button_10",
					"type" : "button",
					"x" : SCREEN_WIDTH-90-LANG_BUTTON_STEP_X*0, "y" : SCREEN_HEIGHT-50,
					"default_image" : IMG_LANG_PATH + "button_tr.png",
					"over_image" :  IMG_LANG_PATH + "button_tr_hov.png",
					"down_image" : IMG_LANG_PATH + "button_tr.png",
				},
				{
					"name" : "animation_button",
					"type" : "button",
					"x" : SCREEN_WIDTH - 147, "y" : 10,
					"default_image" : "d:/ymir work/ui/intro_elendos/button/button_dark_normal.sub",
					"over_image" :  "d:/ymir work/ui/intro_elendos/button/button_dark_hover.sub",
					"down_image" : "d:/ymir work/ui/intro_elendos/button/button_dark_down.sub",
					"text" : "Show Animation", "text_color" : 0xffffffff, "text_outline" : 1,
				},
			),
		},
	),
}