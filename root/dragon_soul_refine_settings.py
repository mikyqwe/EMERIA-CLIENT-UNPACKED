import item

default_grade_need_count = [4, 3, 3, 2, 2]
default_grade_fee = [50000, 100000, 150000, 200000, 500000]
default_step_need_count = [2, 2, 2, 2]
default_step_fee = [1000000, 3000000, 8000000, 20000000]

strength_fee = {
	item.MATERIAL_DS_REFINE_NORMAL : 50000,
	item.MATERIAL_DS_REFINE_BLESSED : 100000,
	item.MATERIAL_DS_REFINE_HOLLY : 200000,
	#item.MATERIAL_DS_REFINE_MASTER : 40000,
}

default_strength_max_table = [
	[2, 2, 3, 3, 4],
	[3, 3, 3, 4, 4],
	[4, 4, 4, 4, 4],
	[4, 4, 4, 4, 5],
	[4, 4, 4, 5, 6],
	[4, 4, 4, 5, 6],
]

default_refine_info = {
	"grade_need_count" : default_grade_need_count,
	"grade_fee" : default_grade_fee,
	"step_need_count" : default_step_need_count,
	"step_fee" : default_step_fee,
	"strength_max_table" : default_strength_max_table,
}

dragon_soul_refine_info = {
	11 : default_refine_info,
	12 : default_refine_info,
	13 : default_refine_info,
	14 : default_refine_info,
	15 : default_refine_info,
	16 : default_refine_info,
}
