#This file is intended to organize the various types of overall functions the app uses so they aren't written directly into the Impl file.


import os
from my_other_module.parsing_functions import tsv_to_d2_list, csv_to_d2_list, print_d2_list_out_to_tsv_file
from my_other_module.Check_Pathway.check_pathways_vs_reactions import main_cp
from my_other_module.Check_Pathway.TIGRFAM_to_EC import tfam_main


#This bug_filepath needs to be the reactions file
def reactions_file_to_pathway_reactions_and_percentages(bug_filepath, output_file_pathway):
        cp_output_list_d3 = main_cp(bug_filepath)
        print_d2_list_out_to_tsv_file(cp_output_list_d3, output_file_pathway)


#This bug_filepath needs to be the TIGRFAM annotations file.
def TIGRFAM_file_to_pathway_reactions_and_percentages(bug_tfam_filepath, output_file_pathway):
        
    #First step is to convert the bug tsv or csv file to a d2 list.
    #IMPORTANT: MAKE SURE TO KNOW IF IT'S A CSV OR TSV FILE!!!!!!
    bug_tfam_d2_list = csv_to_d2_list(bug_tfam_filepath)

    #Here we take all the TFAM Ids from the list
    tfam_ids_d1 = []
    for i in range(1,len(bug_tfam_d2_list)):
        tfam_ids_d1.append(bug_tfam_d2_list[i][5])

    #Here we get the d2 list of tfam ids and related ec numbers
    tfams_and_ecs = tfam_main(tfam_ids_d1)

    
    #For now just print the output
    print_d2_list_out_to_tsv_file(tfams_and_ecs, output_file_pathway)







