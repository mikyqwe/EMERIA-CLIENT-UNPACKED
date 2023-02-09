import uiScriptLocale

LOCALE_PATH = uiScriptLocale.LOGIN_PATH
#Big-List
#SERVER_BOARD_HEIGHT = 180 + 390
#SERVER_LIST_HEIGHT = 171 + 350
#Small list like german
SERVER_BOARD_HEIGHT = 220 + 180
SERVER_LIST_HEIGHT = 171 + 180
SERVER_BOARD_WEIGHT = 375 

ID_LIMIT_COUNT = 19
PW_LIMIT_COUNT = 16

BASE_PATH_INTERFACE = "login_interface/"
BASE_PATH = BASE_PATH_INTERFACE

FLAGS_DIRECTION = 265 # Orientamento bandiere su asse X (diminuire per andare a destra, aumentare per andare a sinistra)

window = {
	"name" : "LoginWindow",
	"sytle" : ("movable",),

	"x" : 0,
	"y" : 0,

	"width" : SCREEN_WIDTH,
	"height" : SCREEN_HEIGHT,

	"children" :
	(

		## BASE Board
		{
			"name" : "bg1", "type" : "expanded_image", "x" : 0, "y" : 0,
			"x_scale" : float(SCREEN_WIDTH) / 1366.0, "y_scale" : float(SCREEN_HEIGHT) / 780.0,
			"image" : BASE_PATH_INTERFACE + "background_base.jpg" ,
			
			"children":
			(
				{
					"name" : "FrameTop",
					"type" : "expanded_image",
					
					"x" : 0,
					"y" : 0,
					
					"image" : BASE_PATH_INTERFACE + "frame_top_rect.jpg",
					"rect" : (0.0 , 0.0 , -1.0+ (float(SCREEN_WIDTH)/float(118.0)) ,0.0,),
				},
				{
					"name" : "FrameBottom",
					"type" : "expanded_image",
					
					"x" : 0,
					"y" : SCREEN_HEIGHT-30,
					
					"image" : BASE_PATH_INTERFACE + "frame_bottom_rect.jpg",
					"rect" : (0.0 , 0.0 , -1.0+ (float(SCREEN_WIDTH)/float(118.0)) ,0.0,),
				},
				{
					"name" : "RectLine",
					"type" : "expanded_image",
					
					"x" : 0,
					"y" : SCREEN_HEIGHT-80,
					
					"image" : BASE_PATH_INTERFACE + "rect_line.tga",
					"rect" : (0.0 , 0.0 , -1.0+ (float(SCREEN_WIDTH)/float(100.0)) ,0.0,),
				},
			),
		},
		{
			"name" : "LogoImage",
			"type" : "image",
			
			"x" : SCREEN_WIDTH/2 -100,
			"y" : SCREEN_HEIGHT/2 - 260 - 30,
			
			"image" : BASE_PATH_INTERFACE + "logo.tga",
		},
		{
			"name" : "LogoImageOver",
			"type" : "image",
			
			"x" : SCREEN_WIDTH/2 -100,
			"y" : SCREEN_HEIGHT/2 - 260 - 30,
			
			"image" : BASE_PATH_INTERFACE + "logo_over.tga",
		},
		## LoginBoard
		{
			"name" : "LoginBoard",
			"type" : "window",

			"x" : SCREEN_WIDTH/2 - (80+60) + (75-50)/2,
			"y" : SCREEN_HEIGHT/2  - 115,

			"width" : 250,
			"height" : 320 ,

			"children" :
			(
				{
					"name" : "UserNameTextImage",
					"type" : "image",
					
					"x" : 80 + 5,
					"y" : 0,
					
					"image": BASE_PATH + "main/username.tga",
				},
				{
					"name" : "PasswordTextImage",
					"type" : "image",
					
					"x" : 80 + 5,
					"y" : 90,
					
					"image": BASE_PATH + "main/password.tga",
				},
				{
					"name" : "BgTextBoxID",
					"type" : "image",
					
					"x" : 30 + 10,
					"y" : 40,
					
					"image" : BASE_PATH + "main/bg_textbox.tga",
					
					"children" : 
					(
						{
							"name" : "ID_EditLine",
							"type" : "editline",

							"x" : 4 + 15,
							"y" : 9,

							"width" : 176,
							"height" : 28,

							"input_limit" : ID_LIMIT_COUNT,
							"enable_codepage" : 0,

							"r" : 1.0,
							"g" : 1.0,
							"b" : 1.0,
							"a" : 1.0,
						},
					),
				},
				{
					"name" : "BgTextBoxPSW",
					"type" : "image",
					
					"x" : 30 + 10,
					"y" : 120,
					
					"image" : BASE_PATH + "main/bg_textbox.tga",
					
					"children" : 
					(
						{
							"name" : "Password_EditLine",
							"type" : "editline",

							"x" : 4 + 15,
							"y" : 9,

							"width" : 176,
							"height" : 28,

							"input_limit" : PW_LIMIT_COUNT,
							"secret_flag" : 1,
							"enable_codepage" : 0,

							"r" : 1.0,
							"g" : 1.0,
							"b" : 1.0,
							"a" : 1.0,
						},
					),
				},
				
				
				{
					"name" : "LoginButton",
					"type" : "button",

					"x" : 60 + 10 + 2,
					"y" : 155 + 7,

					"default_image" : BASE_PATH_INTERFACE + "other_button/login_button_default.tga",
					"over_image" : BASE_PATH_INTERFACE + "other_button/login_button_over.tga",
					"down_image" : BASE_PATH_INTERFACE + "other_button/login_button_down.tga",
				},
				
				
				{
					"name" : "SaveButton",
					"type" : "button",

					"x" : 75 + 10 + 5,
					"y" : 215,

					"default_image" : BASE_PATH_INTERFACE + "other_button/save_button_default.tga",
					"over_image" : BASE_PATH_INTERFACE + "other_button/save_button_over.tga",
					"down_image" : BASE_PATH_INTERFACE + "other_button/save_button_down.tga",
				},
				{
					"name" : "channel_board",
					"type" : "window",
					
					"x": 0,
					"y": 270,
					
					"width" : 245,
					"height" : 45,
					
					"children" :
					
					(
						{
							"name" : "channel_online_button1",
							"type" : "radio_button",
							
							"x" :  63 * 0,
							"y" : 0,
							
							"default_image" : BASE_PATH_INTERFACE + "channel_button/channel_selection_online_unselected.tga",
							"over_image" : BASE_PATH_INTERFACE + "channel_button/channel_selection_online_over.tga",
							"down_image" : BASE_PATH_INTERFACE + "channel_button/channel_selection_online_selected.tga",
						},
						{
							"name" : "channel_offline_button1",
							"type" : "radio_button",
							
							"x" :  63 * 0,
							"y" : 0,
							
							"default_image" : BASE_PATH_INTERFACE + "channel_button/channel_selection_offline_unselected.tga",
							"over_image" : BASE_PATH_INTERFACE + "channel_button/channel_selection_offline_over.tga",
							"down_image" : BASE_PATH_INTERFACE + "channel_button/channel_selection_offline_selected.tga",
						},
						{
							"name" : "channel_online_button2",
							"type" : "radio_button",
							
							"x" :  63 * 1,
							"y" : 0,
							
							"default_image" : BASE_PATH_INTERFACE + "channel_button/channel_selection_online_unselected2.tga",
							"over_image" : BASE_PATH_INTERFACE + "channel_button/channel_selection_online_over2.tga",
							"down_image" : BASE_PATH_INTERFACE + "channel_button/channel_selection_online_selected2.tga",
						},
						{
							"name" : "channel_offline_button2",
							"type" : "radio_button",
							
							"x" :63 * 1,
							"y" : 0,
							
							"default_image" : BASE_PATH_INTERFACE + "channel_button/channel_selection_offline_unselected2.tga",
							"over_image" : BASE_PATH_INTERFACE + "channel_button/channel_selection_offline_over2.tga",
							"down_image" : BASE_PATH_INTERFACE + "channel_button/channel_selection_offline_selected2.tga",
						},
						{
							"name" : "channel_online_button3",
							"type" : "radio_button",
							
							"x" : 63 * 2,
							"y" : 0,
							
							"default_image" : BASE_PATH_INTERFACE + "channel_button/channel_selection_online_unselected3.tga",
							"over_image" : BASE_PATH_INTERFACE + "channel_button/channel_selection_online_over3.tga",
							"down_image" : BASE_PATH_INTERFACE + "channel_button/channel_selection_online_selected3.tga",
						},
						{
							"name" : "channel_offline_button3",
							"type" : "radio_button",
							
							"x" : 63 * 2,
							"y" : 0,
							
							"default_image" : BASE_PATH_INTERFACE + "channel_button/channel_selection_offline_unselected3.tga",
							"over_image" : BASE_PATH_INTERFACE + "channel_button/channel_selection_offline_over3.tga",
							"down_image" : BASE_PATH_INTERFACE + "channel_button/channel_selection_offline_selected3.tga",
						},
						{
							"name" : "channel_online_button4",
							"type" : "radio_button",
							
							"x" : 63 * 3,
							"y" : 0,
							
							"default_image" : BASE_PATH_INTERFACE + "channel_button/channel_selection_online_unselected4.tga",
							"over_image" : BASE_PATH_INTERFACE + "channel_button/channel_selection_online_over4.tga",
							"down_image" : BASE_PATH_INTERFACE + "channel_button/channel_selection_online_selected4.tga",
						},
						{
							"name" : "channel_offline_button4",
							"type" : "radio_button",
							
							"x" : 63 * 3,
							"y" : 0,
							
							"default_image" : BASE_PATH_INTERFACE + "channel_button/channel_selection_offline_unselected4.tga",
							"over_image" : BASE_PATH_INTERFACE + "channel_button/channel_selection_offline_over4.tga",
							"down_image" : BASE_PATH_INTERFACE + "channel_button/channel_selection_offline_selected4.tga",
						},
					),
				},
			),
		},
		#saved account
		{
			"name" : "account_board",
			"type" : "window",
			
			"x": SCREEN_WIDTH-200,
			"y": SCREEN_HEIGHT/2 - 180,
			
			"width" : 160,
			"height" : 276,
			
			"children" :
			
			(
				{
					"name" : "SavedAccountTextImage",
					"type" : "image",
					
					"x" : 176/2 - 150/2,
					"y" : 0,
					
					"image" : BASE_PATH_INTERFACE + "main/saved_accounts_image_text.tga",
					
				},
				#account1 
				{
					"name" : "AccountSlot1",
					"type" : "image",
					
					"x" : 0,
					"y" : 40,
					
					"image" : BASE_PATH + "main/account_slot.tga",
					
					"children":
					(
						{
							"name" : "AccountName1",
							"type" : "text",
							
							"x" : 4+ 11,
							"y" : 8,
							
							"text" : "account_1",
							"fontsize" : "LARGE",
						},
					),
				},
				{
					"name" : "play_1",
					"type" : "button",
					
					"x" : 0 + 30 - 5,
					"y" : 40 + 30,
					
					"default_image" : BASE_PATH_INTERFACE + "account_button/play_button_default.tga",
					"over_image" : BASE_PATH_INTERFACE + "account_button/play_button_over.tga",
					"down_image" : BASE_PATH_INTERFACE + "account_button/play_button_down.tga",						
				},
				{
					"name" : "delete_1",
					"type" : "button",
					
					"x" : 0 + 100 - 5,
					"y" : 40 + 30,
					
					"default_image" : BASE_PATH_INTERFACE + "account_button/delete_button_default.tga",
					"over_image" : BASE_PATH_INTERFACE + "account_button/delete_button_over.tga",
					"down_image" : BASE_PATH_INTERFACE + "account_button/delete_button_down.tga",						
				},
				#account2
				{
					"name" : "AccountSlot2",
					"type" : "image",
					
					"x" : 0,
					"y" : 40 + (65*1),
					
					"image" : BASE_PATH + "main/account_slot.tga",
					
					"children":
					(
						{
							"name" : "AccountName2",
							"type" : "text",
							
							"x" : 4+ 11,
							"y" : 8,
							
							"text" : "account_2",
							"fontsize" : "LARGE",
						},
					),
				},
				{
					"name" : "play_2",
					"type" : "button",
					
					"x" : 0 + 30 - 5,
					"y" : 40 + (65*1) + 30,
					
					"default_image" : BASE_PATH_INTERFACE + "account_button/play_button_default.tga",
					"over_image" : BASE_PATH_INTERFACE + "account_button/play_button_over.tga",
					"down_image" : BASE_PATH_INTERFACE + "account_button/play_button_down.tga",						
				},
				{
					"name" : "delete_2",
					"type" : "button",
					
					"x" : 0 + 100 - 5,
					"y" : 40 + (65*1) + 30,
					
					"default_image" : BASE_PATH_INTERFACE + "account_button/delete_button_default.tga",
					"over_image" : BASE_PATH_INTERFACE + "account_button/delete_button_over.tga",
					"down_image" : BASE_PATH_INTERFACE + "account_button/delete_button_down.tga",						
				},
				#account3
				{
					"name" : "AccountSlot3",
					"type" : "image",
					
					"x" : 0,
					"y" : 40+ (65*2),
					
					"image" : BASE_PATH + "main/account_slot.tga",
					
					"children":
					(
						{
							"name" : "AccountName3",
							"type" : "text",
							
							"x" : 4+ 11,
							"y" : 8,
							"text" : "account_3",
							"fontsize" : "LARGE",
						},
					),
				},
				{
					"name" : "play_3",
					"type" : "button",
					
					"x" : 0 + 30 - 5,
					"y" : 40+ (65*2) + 30,
					
					"default_image" : BASE_PATH_INTERFACE + "account_button/play_button_default.tga",
					"over_image" : BASE_PATH_INTERFACE + "account_button/play_button_over.tga",
					"down_image" : BASE_PATH_INTERFACE + "account_button/play_button_down.tga",						
				},
				{
					"name" : "delete_3",
					"type" : "button",
					
					"x" : 0 + 100 - 5,
					"y" : 40+ (65*2) + 30,
					
					"default_image" : BASE_PATH_INTERFACE + "account_button/delete_button_default.tga",
					"over_image" : BASE_PATH_INTERFACE + "account_button/delete_button_over.tga",
					"down_image" : BASE_PATH_INTERFACE + "account_button/delete_button_down.tga",						
				},
				#account4
				{
					"name" : "AccountSlot4",
					"type" : "image",
					
					"x" : 0,
					"y" : 40 + + (65*3),
					
					"image" : BASE_PATH + "main/account_slot.tga",
					
					"children":
					(
						{
							"name" : "AccountName4",
							"type" : "text",
							
							"x" : 4+ 11,
							"y" : 8,
							
							"text" : "account_4",
							"fontsize" : "LARGE",
						},
					),
				},
				{
					"name" : "play_4",
					"type" : "button",
					
					"x" : 0 + 30 - 5,
					"y" : 40 + + (65*3) + 30,
					
					"default_image" : BASE_PATH_INTERFACE + "account_button/play_button_default.tga",
					"over_image" : BASE_PATH_INTERFACE + "account_button/play_button_over.tga",
					"down_image" : BASE_PATH_INTERFACE + "account_button/play_button_down.tga",						
				},
				{
					"name" : "delete_4",
					"type" : "button",
					
					"x" : 0 + 100 - 5,
					"y" : 40 + + (65*3) + 30,
					
					"default_image" : BASE_PATH_INTERFACE + "account_button/delete_button_default.tga",
					"over_image" : BASE_PATH_INTERFACE + "account_button/delete_button_over.tga",
					"down_image" : BASE_PATH_INTERFACE + "account_button/delete_button_down.tga",						
				},
			),
		},
		{
			"name" : "buttonBoard",
			"type" : "window",
			
			"x" : 5,
			"y" : SCREEN_HEIGHT -75,
			
			"width" : 530, 
			"height" : 45, 
			
			"children" :
			(
				{
					"name" : "HomePageButton",
					"type" : "button",
					
					"x" : 13,
					"y" : 2,
					
					"default_image" : BASE_PATH_INTERFACE + "other_button/sito_default.tga",
					"over_image" : BASE_PATH_INTERFACE + "other_button/sito_over.tga",
					"down_image" : BASE_PATH_INTERFACE + "other_button/sito_down.tga",
				},
				{
					"name" : "ForumButton",
					"type" : "button",
					
					"x" : 0+ 80 * 1,
					"y" : 1,
					
					"default_image" : BASE_PATH_INTERFACE + "other_button/forum_default.tga",
					"over_image" : BASE_PATH_INTERFACE + "other_button/forum_over.tga",
					"down_image" : BASE_PATH_INTERFACE + "other_button/forum_down.tga",
				},
				{
					"name" : "ShopButton",
					"type" : "button",
					
					"x" : 0 + 80 * 2 - 4,
					"y" : 1,
					
					"default_image" : BASE_PATH_INTERFACE + "other_button/shop_default.tga",
					"over_image" : BASE_PATH_INTERFACE + "other_button/shop_over.tga",
					"down_image" : BASE_PATH_INTERFACE + "other_button/shop_down.tga",
				},
				{
					"name" : "RegisterButton"  ,
					"type" : "button",
					
					"x" : 0 + 80 * 3 - 4 - 7,
					"y" : 3,
					
					"default_image" : BASE_PATH_INTERFACE + "other_button/register_default.tga",
					"over_image" : BASE_PATH_INTERFACE + "other_button/register_over.tga",
					"down_image" : BASE_PATH_INTERFACE + "other_button/register_down.tga",
				},
				{
					"name" : "RankingButton"  ,
					"type" : "button",
					
					"x" : 0 + 80 * 4 - 7,
					"y" : 4,
					
					"default_image" : BASE_PATH_INTERFACE + "other_button/ranking_default.tga",
					"over_image" : BASE_PATH_INTERFACE + "other_button/ranking_over.tga",
					"down_image" : BASE_PATH_INTERFACE + "other_button/ranking_down.tga",
				},
				{
					"name" : "OptionButton" ,
					"type" : "button",
					
					"x" : 0 + 80 * 5 - 6,
					"y" : 4,
					
					"default_image" : BASE_PATH_INTERFACE + "other_button/option_default.tga",
					"over_image" : BASE_PATH_INTERFACE + "other_button/option_over.tga",
					"down_image" : BASE_PATH_INTERFACE + "other_button/option_down.tga",
				},
				{
					"name" : "CloseButton",
					"type" : "button",

					"x" : 0 + 80 * 6 - 6,
					"y" : 4,

					"default_image" : BASE_PATH_INTERFACE + "other_button/exit_default.tga",
					"over_image" : BASE_PATH_INTERFACE + "other_button/exit_over.tga",
					"down_image" : BASE_PATH_INTERFACE + "other_button/exit_down.tga",
				},
			),
		},
		{
			"name" : "FacebookCoverButton",
			"type" : "image",
			
			"x" : SCREEN_WIDTH - 185,
			"y" : SCREEN_HEIGHT - 90,
			
			"image" : BASE_PATH_INTERFACE +"other_button/cover_button.tga",
			"children" :
			(
				{
					"name" : "FacebookButton",
					"type" : "button",
					
					"x" : 16,
					"y" : 4,
					
					"default_image" : BASE_PATH_INTERFACE + "other_button/facebook_default.tga",
					"over_image" : BASE_PATH_INTERFACE + "other_button/facebook_over.tga",
					"down_image" : BASE_PATH_INTERFACE + "other_button/facebook_down.tga",
				},
			),
		},
		{
			"name" : "YoutubeCoverButton",
			"type" : "image",
			
			"x" : SCREEN_WIDTH - 90,
			"y" : SCREEN_HEIGHT - 90,
			
			"image" : BASE_PATH_INTERFACE +"other_button/cover_button.tga",
			"children" :
			(
				{
					"name" : "YoutubeButton",
					"type" : "button",
					
					"x" : 16,
					"y" : 4,
					
					"default_image" : BASE_PATH_INTERFACE + "other_button/youtube_default.tga",
					"over_image" : BASE_PATH_INTERFACE + "other_button/youtube_over.tga",
					"down_image" : BASE_PATH_INTERFACE + "other_button/youtube_down.tga",
				},
			),
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
}
