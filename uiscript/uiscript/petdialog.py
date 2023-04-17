#########################################
# title_name		: System Pack		#
# filename			: uiscript			#
# author			: Bvural41			#
# version			: Version 0.0.2		#
# date				: 2015 04 11		#
# update			: 2019 02 05		#
#########################################

import uiScriptLocale
import translate

ROOT_PATH = "d:/ymir work/ui/public/"
LINE_DATA_X 		= 90-63
MIDDLE_BUTTON_WIDTH	= 65

window = {
	"name" : "KategoriToplama",
	"style" : ("movable", "float",),

	"x" : 0,
	"y" : 0,

	"width" : 230,
	"height" : 400-20,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",

			"x" : 0,
			"y" : 0,

			"width" : 230,
			"height" : 400-20,

			"children" :
			(
				{
					"name" : "titlebar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 8,

					"width" : 235-73+52,
					"color" : "gray",

					"children" :
					(
						{
							"name":"titlename",
							"type":"text",

							"x":0,
							"y":3, 

							"text" : "Kategori Toplama", 

							"horizontal_align":"center",
							"text_horizontal_align":"center"
						},
					),
				},
				###################################################################
				{
					"name" : "pick",
					"type" : "text",
					
					"x" : 30,
					"y" : 42,
					
					"text" : "Tümünü Topla",
				},
				{
					"name" : "pet_toplama_hepsi_on_button",
					"type" : "radio_button",

					"x" : 110,
					"y" : 40,
					"text" : translate.karacik,
					
					"default_image" : ROOT_PATH + "Small_button_01.sub",
					"over_image" : ROOT_PATH + "Small_button_02.sub",
					"down_image" : ROOT_PATH + "Small_button_03.sub",
				},
				{
					"name" : "pet_toplama_hepsi_off_button",
					"type" : "radio_button",

					"x" : 110 + 50,
					"y" : 40,

					"text" : translate.karkapali,
					
					"default_image" : ROOT_PATH + "Small_button_01.sub",
					"over_image" : ROOT_PATH + "Small_button_02.sub",
					"down_image" : ROOT_PATH + "Small_button_03.sub",
				},
				###################################################################
				{
					"name" : "pick",
					"type" : "text",
					
					"x" : 30,
					"y" : 72,
					
					"text" : "Kostümler",
				},
				{
					"name" : "pet_toplama_kostum_on_button",
					"type" : "radio_button",

					"x" : 110,
					"y" : 70,
					"text" : translate.karacik,
					
					"default_image" : ROOT_PATH + "Small_button_01.sub",
					"over_image" : ROOT_PATH + "Small_button_02.sub",
					"down_image" : ROOT_PATH + "Small_button_03.sub",
				},
				{
					"name" : "pet_toplama_kostum_off_button",
					"type" : "radio_button",

					"x" : 110 + 50,
					"y" : 70,

					"text" : translate.karkapali,
					
					"default_image" : ROOT_PATH + "Small_button_01.sub",
					"over_image" : ROOT_PATH + "Small_button_02.sub",
					"down_image" : ROOT_PATH + "Small_button_03.sub",
				},
				###################################################################
				{
					"name" : "pick",
					"type" : "text",
					
					"x" : 30,
					"y" : 102,
					
					"text" : "Beceri Kitaplarý",
				},
				{
					"name" : "pet_toplama_bk_on_button",
					"type" : "radio_button",

					"x" : 110,
					"y" : 100,
					"text" : translate.karacik,
					
					"default_image" : ROOT_PATH + "Small_button_01.sub",
					"over_image" : ROOT_PATH + "Small_button_02.sub",
					"down_image" : ROOT_PATH + "Small_button_03.sub",
				},
				{
					"name" : "pet_toplama_bk_off_button",
					"type" : "radio_button",

					"x" : 110 + 50,
					"y" : 100,

					"text" : translate.karkapali,
					
					"default_image" : ROOT_PATH + "Small_button_01.sub",
					"over_image" : ROOT_PATH + "Small_button_02.sub",
					"down_image" : ROOT_PATH + "Small_button_03.sub",
				},
				###################################################################
				{
					"name" : "pick",
					"type" : "text",
					
					"x" : 30,
					"y" : 132,
					
					"text" : "Ruh Taþlarý",
				},
				{
					"name" : "pet_toplama_rt_on_button",
					"type" : "radio_button",

					"x" : 110,
					"y" : 130,
					"text" : translate.karacik,
					
					"default_image" : ROOT_PATH + "Small_button_01.sub",
					"over_image" : ROOT_PATH + "Small_button_02.sub",
					"down_image" : ROOT_PATH + "Small_button_03.sub",
				},
				{
					"name" : "pet_toplama_rt_off_button",
					"type" : "radio_button",

					"x" : 110 + 50,
					"y" : 130,

					"text" : translate.karkapali,
					
					"default_image" : ROOT_PATH + "Small_button_01.sub",
					"over_image" : ROOT_PATH + "Small_button_02.sub",
					"down_image" : ROOT_PATH + "Small_button_03.sub",
				},
				###################################################################
				{
					"name" : "pick",
					"type" : "text",
					
					"x" : 30,
					"y" : 162,
					
					"text" : "+70 Silahlar",
				},
				{
					"name" : "pet_toplama_75_on_button",
					"type" : "radio_button",

					"x" : 110,
					"y" : 160,
					"text" : translate.karacik,
					
					"default_image" : ROOT_PATH + "Small_button_01.sub",
					"over_image" : ROOT_PATH + "Small_button_02.sub",
					"down_image" : ROOT_PATH + "Small_button_03.sub",
				},
				{
					"name" : "pet_toplama_75_off_button",
					"type" : "radio_button",

					"x" : 110 + 50,
					"y" : 160,

					"text" : translate.karkapali,
					
					"default_image" : ROOT_PATH + "Small_button_01.sub",
					"over_image" : ROOT_PATH + "Small_button_02.sub",
					"down_image" : ROOT_PATH + "Small_button_03.sub",
				},
				###################################################################
				{
					"name" : "pick",
					"type" : "text",
					
					"x" : 30,
					"y" : 192,
					
					"text" : "+70 Zýrhlar",
				},
				{
					"name" : "pet_toplama_celik_on_button",
					"type" : "radio_button",

					"x" : 110,
					"y" : 190,
					"text" : translate.karacik,
					
					"default_image" : ROOT_PATH + "Small_button_01.sub",
					"over_image" : ROOT_PATH + "Small_button_02.sub",
					"down_image" : ROOT_PATH + "Small_button_03.sub",
				},
				{
					"name" : "pet_toplama_celik_off_button",
					"type" : "radio_button",

					"x" : 110 + 50,
					"y" : 190,

					"text" : translate.karkapali,
					
					"default_image" : ROOT_PATH + "Small_button_01.sub",
					"over_image" : ROOT_PATH + "Small_button_02.sub",
					"down_image" : ROOT_PATH + "Small_button_03.sub",
				},
				###################################################################
				{
					"name" : "pick",
					"type" : "text",
					
					"x" : 30,
					"y" : 222,
					
					"text" : "Takýlar",
				},
				{
					"name" : "pet_toplama_taki_on_button",
					"type" : "radio_button",

					"x" : 110,
					"y" : 220,
					"text" : translate.karacik,
					
					"default_image" : ROOT_PATH + "Small_button_01.sub",
					"over_image" : ROOT_PATH + "Small_button_02.sub",
					"down_image" : ROOT_PATH + "Small_button_03.sub",
				},
				{
					"name" : "pet_toplama_taki_off_button",
					"type" : "radio_button",

					"x" : 110 + 50,
					"y" : 220,

					"text" : translate.karkapali,
					
					"default_image" : ROOT_PATH + "Small_button_01.sub",
					"over_image" : ROOT_PATH + "Small_button_02.sub",
					"down_image" : ROOT_PATH + "Small_button_03.sub",
				},
				###################################################################
				{
					"name" : "pick",
					"type" : "text",
					
					"x" : 30,
					"y" : 252,
					
					"text" : "+ Basmalar",
				},
				{
					"name" : "pet_toplama_arti_on_button",
					"type" : "radio_button",

					"x" : 110,
					"y" : 250,
					"text" : translate.karacik,
					
					"default_image" : ROOT_PATH + "Small_button_01.sub",
					"over_image" : ROOT_PATH + "Small_button_02.sub",
					"down_image" : ROOT_PATH + "Small_button_03.sub",
				},
				{
					"name" : "pet_toplama_arti_off_button",
					"type" : "radio_button",

					"x" : 110 + 50,
					"y" : 250,

					"text" : translate.karkapali,
					
					"default_image" : ROOT_PATH + "Small_button_01.sub",
					"over_image" : ROOT_PATH + "Small_button_02.sub",
					"down_image" : ROOT_PATH + "Small_button_03.sub",
				},
				###################################################################
				{
					"name" : "pick",
					"type" : "text",
					
					"x" : 30,
					"y" : 282,
					
					"text" : "Sandýklar",
				},
				{
					"name" : "pet_toplama_sandik_on_button",
					"type" : "radio_button",

					"x" : 110,
					"y" : 280,
					"text" : translate.karacik,
					
					"default_image" : ROOT_PATH + "Small_button_01.sub",
					"over_image" : ROOT_PATH + "Small_button_02.sub",
					"down_image" : ROOT_PATH + "Small_button_03.sub",
				},
				{
					"name" : "pet_toplama_sandik_off_button",
					"type" : "radio_button",

					"x" : 110 + 50,
					"y" : 280,

					"text" : translate.karkapali,
					
					"default_image" : ROOT_PATH + "Small_button_01.sub",
					"over_image" : ROOT_PATH + "Small_button_02.sub",
					"down_image" : ROOT_PATH + "Small_button_03.sub",
				},
				###################################################################

				###################################################################
				{
					"name" : "pick",
					"type" : "text",
					
					"x" : 30,
					"y" : 312,
					
					"text" : "Cor Draconis",
				},
				{
					"name" : "pet_toplama_cor_on_button",
					"type" : "radio_button",

					"x" : 110,
					"y" : 310,
					"text" : translate.karacik,
					
					"default_image" : ROOT_PATH + "Small_button_01.sub",
					"over_image" : ROOT_PATH + "Small_button_02.sub",
					"down_image" : ROOT_PATH + "Small_button_03.sub",
				},
				{
					"name" : "pet_toplama_cor_off_button",
					"type" : "radio_button",

					"x" : 110 + 50,
					"y" : 310,

					"text" : translate.karkapali,
					
					"default_image" : ROOT_PATH + "Small_button_01.sub",
					"over_image" : ROOT_PATH + "Small_button_02.sub",
					"down_image" : ROOT_PATH + "Small_button_03.sub",
				},
				###################################################################

				###################################################################
				{
					"name" : "pick",
					"type" : "text",
					
					"x" : 30,
					"y" : 342,
					
					"text" : "Etkinlikler",
				},
				{
					"name" : "pet_toplama_event_on_button",
					"type" : "radio_button",

					"x" : 110,
					"y" : 340,
					"text" : translate.karacik,
					
					"default_image" : ROOT_PATH + "Small_button_01.sub",
					"over_image" : ROOT_PATH + "Small_button_02.sub",
					"down_image" : ROOT_PATH + "Small_button_03.sub",
				},
				{
					"name" : "pet_toplama_event_off_button",
					"type" : "radio_button",

					"x" : 110 + 50,
					"y" : 340,

					"text" : translate.karkapali,
					
					"default_image" : ROOT_PATH + "Small_button_01.sub",
					"over_image" : ROOT_PATH + "Small_button_02.sub",
					"down_image" : ROOT_PATH + "Small_button_03.sub",
				},
				###################################################################
			),
		},
	),
}
