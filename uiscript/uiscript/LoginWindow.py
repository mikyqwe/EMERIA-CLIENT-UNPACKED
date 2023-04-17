PATH_INTERFACE = "interface_pics/"

INPUT_LIMIT = 16
SPACE = 34

window = {
	"name" : "LoginWindow",
	"sytle" : ("movable",),

	"x" : 0,
	"y" : 0,

	"width" : SCREEN_WIDTH,
	"height" : SCREEN_HEIGHT,

	"children" :
	(
		{
			"name" : "background", "type" : "expanded_image", "x" : 0, "y" : 0,
			"x_scale" : float(SCREEN_WIDTH) / 1920.0, "y_scale" : float(SCREEN_HEIGHT) / 1080.0,
			"image" : PATH_INTERFACE + "bg.png",
			"children" :
			(
				{
					"name" : "top_logo_bg",
					"type" : "image",
					"x" : (SCREEN_WIDTH - 616)/2,
					"y" : 10,
					"image" : PATH_INTERFACE + "top_bg.png",
				},

				{
					"name" : "background_painel", "type" : "expanded_image", "x" : 0, "y" : 70,
					"horizontal_align" : "center", "vertical_align" : "center",
					"image" : PATH_INTERFACE + "panel_bg.png",
					"children" : 
					(

						{
							"name" : "login_bg",
							"type" : "image",
							"x" : 120,
							"y" : 180,
							"image" : PATH_INTERFACE + "id_pw.png",
							"children":
							[

								{
									"name" : "ID_placeholder",
									"type" : "image",
									"x" : 0,
									"y" : 0,
									"image" : PATH_INTERFACE + "login_text_placeholder.png",
								},
								{
									"name" : "ID_EditLine",
									"type" : "editline",

									"x" : 10,
									"y" : 15,
									
									"width" : 219,
									"height" : 26,

									"input_limit" : INPUT_LIMIT,
									"enable_codepage" : 0,
								},

								{
									"name" : "PW_placeholder",
									"type" : "image",
									"x" : 0,
									"y" : 99 - 48,
									"image" : PATH_INTERFACE + "password_text_placeholder.png",
								},
								{
									"name" : "Password_EditLine",
									"type" : "editline",

									"x" : 10,
									"y" : 75,

									"width" : 219,
									"height" : 26,

									"input_limit" : INPUT_LIMIT,
									"secret_flag" : 1,
									"enable_codepage" : 0,
								},
							],
						},

						{
							"name" : "button_login", "type" : "button", "x" : -7, "y" : -40,
							"horizontal_align" : "center", "vertical_align" : "center",
							"default_image" : PATH_INTERFACE + "buttons/login_def.png",
							"over_image" : PATH_INTERFACE + "buttons/login_act.png",
							"down_image" : PATH_INTERFACE + "buttons/login_def.png",
						},

						{
							"name" : "real_acc_save_button", "type" : "button", "x" : 50, "y" : -40,
							"horizontal_align" : "center", "vertical_align" : "center",
							"default_image" : PATH_INTERFACE + "buttons/save_def.png",
							"over_image" : PATH_INTERFACE + "buttons/save_act.png",
							"down_image" : PATH_INTERFACE + "buttons/save_down.png",
						},

						{
							"name" : "rs_1", "type" : "button", "x" : -7, "y" : -10,
							"horizontal_align" : "center", "vertical_align" : "center",
							"default_image" : PATH_INTERFACE + "text_create_acc.png",
							"over_image" : PATH_INTERFACE + "text_create_acc_act.png",
							"down_image" : PATH_INTERFACE + "text_create_acc.png",
						},

						{
							"name" : "rs_2", "type" : "button", "x" : -7, "y" : 5,
							"horizontal_align" : "center", "vertical_align" : "center",
							"default_image" : PATH_INTERFACE + "text_forget_pass.png",
							"over_image" : PATH_INTERFACE + "text_forget_pass_act.png",
							"down_image" : PATH_INTERFACE + "text_forget_pass.png",
						},


						{
							"name" : "button_ch_state_1", "type" : "image", "x" : -95, "y" : 55,
							"horizontal_align" : "center", "vertical_align" : "center",
							"image" : PATH_INTERFACE + "channels/ch_off.png"
						},
						{
							"name" : "button_ch_1", "type" : "radio_button", "x" : -95, "y" : 55,
							"horizontal_align" : "center", "vertical_align" : "center",
							"default_image" : PATH_INTERFACE + "channels/ch1_def.png",
							"over_image" : PATH_INTERFACE + "channels/ch1_act.png",
							"down_image" : PATH_INTERFACE + "channels/ch1_act.png",
						},

						{
							"name" : "button_ch_state_2", "type" : "image", "x" : -40, "y" : 55,
							"horizontal_align" : "center", "vertical_align" : "center",
							"image" : PATH_INTERFACE + "channels/ch_off_1.png"
						},
						{
							"name" : "button_ch_2", "type" : "radio_button", "x" : -40, "y" : 55,
							"horizontal_align" : "center", "vertical_align" : "center",
							"default_image" : PATH_INTERFACE + "channels/ch2_def.png",
							"over_image" : PATH_INTERFACE + "channels/ch2_act.png",
							"down_image" : PATH_INTERFACE + "channels/ch2_act.png",
						},

						{
							"name" : "button_ch_state_3", "type" : "image", "x" : 15, "y" : 55,
							"horizontal_align" : "center", "vertical_align" : "center",
							"image" : PATH_INTERFACE + "channels/ch_off.png"
						},

						{
							"name" : "button_ch_3", "type" : "radio_button", "x" : 15, "y" : 55,
							"horizontal_align" : "center", "vertical_align" : "center",
							"default_image" : PATH_INTERFACE + "channels/ch3_def.png",
							"over_image" : PATH_INTERFACE + "channels/ch3_act.png",
							"down_image" : PATH_INTERFACE + "channels/ch3_act.png",
						},
						{
							"name" : "button_ch_state_4", "type" : "image", "x" : 70, "y" : 55,
							"horizontal_align" : "center", "vertical_align" : "center",
							"image" : PATH_INTERFACE + "channels/ch_off_1.png"
						},
						{
							"name" : "button_ch_4", "type" : "radio_button", "x" : 70, "y" : 55,
							"horizontal_align" : "center", "vertical_align" : "center",
							"default_image" : PATH_INTERFACE + "channels/ch4_def.png",
							"over_image" : PATH_INTERFACE + "channels/ch4_act.png",
							"down_image" : PATH_INTERFACE + "channels/ch4_act.png",
						},

						{
							"name" : "account_save_bg",
							"type" : "image",
							"x" : -10,
							"y" : 150,
							"horizontal_align" : "center", "vertical_align" : "center",
							"image" : PATH_INTERFACE + "acc_bg.png",
							"children":
							[
								{
									"name" : "save_image_1", "type" : "image", "x" : 0, "y" : -50,
									"vertical_align" : "center",
									"image" : PATH_INTERFACE + "save_acc_bg.png",
									"children" :
									[
										{
											"name" : "acc_name_text_1", "type" : "text", "x" : -70, "y": -7,
											"horizontal_align" : "center", "vertical_align" : "center", "text_horizontal_align" : "center",
											"fontsize" : "MEDIUM", "text" : "Account1 - Free",
										},
										{
											"name" : "save_button_1", "type" : "button", "x" : 130, "y" : 1,
											"vertical_align" : "center", "horizontal_align" : "right",
											"default_image" : PATH_INTERFACE + "buttons/acc_save_def.png",
											"over_image" : PATH_INTERFACE + "buttons/acc_save_act.png",
											"down_image" : PATH_INTERFACE + "buttons/acc_save_def.png",
										},
										{
											"name" : "delete_account_button_1", "type" : "button", "x" : 65, "y" : 1,
											"vertical_align" : "center", "horizontal_align" : "right",
											"default_image" : PATH_INTERFACE + "buttons/acc_delete_def.png",
											"over_image" : PATH_INTERFACE + "buttons/acc_delete_s.png",
											"down_image" : PATH_INTERFACE + "buttons/acc_delete_def.png",
										},
									],
								},
								{
									"name" : "save_image_2", "type" : "image", "x" : 0, "y" : SPACE*1-50,
									"vertical_align" : "center",
									"image" : PATH_INTERFACE + "save_acc_bg.png",
									"children" :
									[
										{
											"name" : "acc_name_text_2", "type" : "text", "x" : -70, "y": -7,
											"horizontal_align" : "center", "vertical_align" : "center", "text_horizontal_align" : "center",
											"fontsize" : "MEDIUM", "text" : "Account2 - Free",
										},
										{
											"name" : "save_button_2", "type" : "button", "x" : 130, "y" : 1,
											"vertical_align" : "center", "horizontal_align" : "right",
											"default_image" : PATH_INTERFACE + "buttons/acc_save_def.png",
											"over_image" : PATH_INTERFACE + "buttons/acc_save_act.png",
											"down_image" : PATH_INTERFACE + "buttons/acc_save_def.png",
										},
										{
											"name" : "delete_account_button_2", "type" : "button", "x" : 65, "y" : 1,
											"vertical_align" : "center", "horizontal_align" : "right",
											"default_image" : PATH_INTERFACE + "buttons/acc_delete_def.png",
											"over_image" : PATH_INTERFACE + "buttons/acc_delete_s.png",
											"down_image" : PATH_INTERFACE + "buttons/acc_delete_def.png",
										},
									],
								},
								{
									"name" : "save_image_3", "type" : "image", "x" : 0, "y" : SPACE*2-50,
									"vertical_align" : "center",
									"image" : PATH_INTERFACE + "save_acc_bg.png",
									"children" :
									[
										{
											"name" : "acc_name_text_3", "type" : "text", "x" : -70, "y": -7,
											"horizontal_align" : "center", "vertical_align" : "center", "text_horizontal_align" : "center",
											"fontsize" : "MEDIUM", "text" : "Account3 - Free",
										},
										{
											"name" : "save_button_3", "type" : "button", "x" : 130, "y" : 1,
											"vertical_align" : "center", "horizontal_align" : "right",
											"default_image" : PATH_INTERFACE + "buttons/acc_save_def.png",
											"over_image" : PATH_INTERFACE + "buttons/acc_save_act.png",
											"down_image" : PATH_INTERFACE + "buttons/acc_save_def.png",
										},
										{
											"name" : "delete_account_button_3", "type" : "button", "x" : 65, "y" : 1,
											"vertical_align" : "center", "horizontal_align" : "right",
											"default_image" : PATH_INTERFACE + "buttons/acc_delete_def.png",
											"over_image" : PATH_INTERFACE + "buttons/acc_delete_s.png",
											"down_image" : PATH_INTERFACE + "buttons/acc_delete_def.png",
										},
									],
								},
								{
									"name" : "save_image_4", "type" : "image", "x" : 0, "y" : SPACE*3-50,
									"vertical_align" : "center",
									"image" : PATH_INTERFACE + "save_acc_bg.png",
									"children" :
									[
										{
											"name" : "acc_name_text_4", "type" : "text", "x" : -70, "y": -7,
											"horizontal_align" : "center", "vertical_align" : "center", "text_horizontal_align" : "center",
											"fontsize" : "MEDIUM", "text" : "Account4 - Free",
										},
										{
											"name" : "save_button_4", "type" : "button", "x" : 130, "y" : 1,
											"vertical_align" : "center", "horizontal_align" : "right",
											"default_image" : PATH_INTERFACE + "buttons/acc_save_def.png",
											"over_image" : PATH_INTERFACE + "buttons/acc_save_act.png",
											"down_image" : PATH_INTERFACE + "buttons/acc_save_def.png",
										},
										{
											"name" : "delete_account_button_4", "type" : "button", "x" : 65, "y" : 1,
											"vertical_align" : "center", "horizontal_align" : "right",
											"default_image" : PATH_INTERFACE + "buttons/acc_delete_def.png",
											"over_image" : PATH_INTERFACE + "buttons/acc_delete_s.png",
											"down_image" : PATH_INTERFACE + "buttons/acc_delete_def.png",
										},
									],
								},
							],
						},
					),
				},

				{
					"name" : "server_logo_0",
					"type" : "expanded_image",
					"x" : SCREEN_WIDTH/2 - 306/2,
					"y" : (SCREEN_HEIGHT/2 - 106/2) -150,
					"image" : PATH_INTERFACE + "logo_z.png",
				},

				{
					"name" : "server_logo_1",
					"type" : "image",
					"x" : (SCREEN_WIDTH - 306)/2,
					"y" : 10,
					"image" : PATH_INTERFACE + "logo_a.png",
				},
				{
					"name" : "change_server",
					"type" : "button",
					"x" : (SCREEN_WIDTH - 75)/2,
					"y" : 115,
					"default_image" : PATH_INTERFACE + "buttons/change_serv.png",
					"over_image" : PATH_INTERFACE + "buttons/change_serv2.png",
					"down_image" : PATH_INTERFACE + "buttons/change_serv.png",
				},
		## Lang1
				{
					"name" : "Lang1",
					"type" : "button",

					"x" : SCREEN_WIDTH/2 - FLAGS_DIRECTION + 125,
					"y" : SCREEN_HEIGHT -135,

					"width" : 32,
					"height" : 22,

					"default_image" : BASE_PATH_INTERFACE + "flags/flag_it_norm.tga",
					"over_image" : BASE_PATH_INTERFACE + "flags/flag_it_over.tga",
					"down_image" : BASE_PATH_INTERFACE + "flags/flag_it_down.tga",
				},
		
		## Lang2
				{
					"name" : "Lang2",
					"type" : "button",

					"x" : SCREEN_WIDTH/2 - FLAGS_DIRECTION + 125 + 50,
					"y" : SCREEN_HEIGHT -135,

					"width" : 32,
					"height" : 22,
	
					"default_image" : BASE_PATH_INTERFACE + "flags/flag_en_norm.tga",
					"over_image" : BASE_PATH_INTERFACE + "flags/flag_en_over.tga",
					"down_image" : BASE_PATH_INTERFACE + "flags/flag_en_down.tga",
				},
		
			## Lang3
				{
					"name" : "Lang3",
					"type" : "button",

					"x" : SCREEN_WIDTH/2 - FLAGS_DIRECTION + 125 + 50*2,
					"y" : SCREEN_HEIGHT -135,

					"width" : 32,
					"height" : 22,
	
					"default_image" : BASE_PATH_INTERFACE + "flags/flag_de_norm.tga",
					"over_image" : BASE_PATH_INTERFACE + "flags/flag_de_over.tga",
					"down_image" : BASE_PATH_INTERFACE + "flags/flag_de_down.tga",
				},
		
		## Lang4
				{
					"name" : "Lang4",
					"type" : "button",

					"x" : SCREEN_WIDTH/2 - FLAGS_DIRECTION + 125 + 50*3,
					"y" : SCREEN_HEIGHT -135,

					"width" : 32,
					"height" : 22,

					"default_image" : BASE_PATH_INTERFACE + "flags/flag_ro_norm.tga",
					"over_image" : BASE_PATH_INTERFACE + "flags/flag_ro_over.tga",
					"down_image" : BASE_PATH_INTERFACE + "flags/flag_ro_down.tga",
				},
		
		## Lang5
				{
					"name" : "Lang5",
					"type" : "button",

					"x" : SCREEN_WIDTH/2 - FLAGS_DIRECTION + 125 + 50*4,
					"y" : SCREEN_HEIGHT -135,

					"width" : 32,
					"height" : 22,

					"default_image" : BASE_PATH_INTERFACE + "flags/flag_tr_norm.tga",
					"over_image" : BASE_PATH_INTERFACE + "flags/flag_tr_over.tga",
					"down_image" : BASE_PATH_INTERFACE + "flags/flag_tr_down.tga",
				},
		
		## Lang6
				{
					"name" : "Lang6",
					"type" : "button",

					"x" : SCREEN_WIDTH/2 - FLAGS_DIRECTION + 125 + 50*5,
					"y" : SCREEN_HEIGHT -135,
	
					"width" : 32,
					"height" : 22,

					"default_image" : BASE_PATH_INTERFACE + "flags/flag_pl_norm.tga",
					"over_image" : BASE_PATH_INTERFACE + "flags/flag_pl_over.tga",
					"down_image" : BASE_PATH_INTERFACE + "flags/flag_pl_down.tga",
				},
			),
		},
	),
}