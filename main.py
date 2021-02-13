import colorama
from converter.convert_engine import *
from converter.terminal_messages import *
from analyst.analyst_engine import analysis_type_a
from tqdm import tqdm
# **************************************PROGRAM STARTING*****************************************
colorama.init()

print_logo()
print_program_description()
dialog_user_start()

scan_directory()  # collect all data files and get configuration dictionaries

#CHECK FOR KYIVSTAR VOC:
scan_bs_voc()  # harvest address and azimuth voc (KyivStar separated tabs)

#PRECHECK FILES:
files_preview()

#MAIN CONVERT FUNCTION:
burning()

#SAVE HEAP RESULT:
save_heap()

#DIVIDE BY SUBSCRIBERS FILES:
save_divide_by_subscribers()

#COMBINE A & B TYPE (MERGE):
merge_types()

a_list = get_a_subscribers_list()
ab_list = get_merged_subscribers_list()
for subscriber in tqdm(a_list):
    df = export_subscriber_a_tab(subscriber)
    analysis_type_a(df, subscriber)




#FINISH
print('commit test')
print_the_end()
