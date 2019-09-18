#This file is intended to organize the various types of overall functions the app uses so they aren't written directly into the Impl file.


import os
from my_other_module.parsing_functions import tsv_to_d2_list, csv_to_d2_list, print_d2_list_out_to_tsv_file, d2_list_to_html_table_file
from my_other_module.Check_Pathway.check_pathways_vs_reactions import main_cp, sub_cp
from my_other_module.Check_Pathway.TIGRFAM_to_EC import tfam_main
from my_other_module.Aux_Functions.aux_1 import tfams_and_ecs_d2_to_ecs_d1, extract_tfam_IDs
from my_other_module.Check_Pathway.EC_num_to_reaction_id import EC_to_Rxn_Ids 
import logging



#This bug_filepath needs to be the reactions file
def reactions_file_to_pathway_reactions_and_percentages(bug_filepath, output_file_pathway):
        cp_output_list_d3 = main_cp(bug_filepath)
        print_d2_list_out_to_tsv_file(cp_output_list_d3, output_file_pathway)
        html_pathway = output_file_pathway[:-3] + 'html'
        d2_list_to_html_table_file(cp_output_list_d3, html_pathway)


#This bug_filepath needs to be the TIGRFAM annotations file.
def TIGRFAM_file_to_pathway_reactions_and_percentages(bug_tfam_filepath, output_file_pathway):
        
    #First step is to convert the bug tsv or csv file to a d2 list.
    #IMPORTANT: MAKE SURE TO KNOW IF IT'S A CSV OR TSV FILE!!!!!!
    bug_tfam_d2_list = csv_to_d2_list(bug_tfam_filepath)

    #Here we take all the TFAM Ids from the list
    tfam_ids_d1 = extract_tfam_IDs(bug_tfam_d2_list)

    #Here we get the d2 list of tfam ids and related ec numbers
    #The list looks like: [[tfam, ec],[tfam,ec],...]
    tfams_and_ecs_d2 = tfam_main(tfam_ids_d1)

    #Here we convert the tfams and ecs d2 list into just a list of ecs.
    ecs_d1 = tfams_and_ecs_d2_to_ecs_d1(tfams_and_ecs_d2)
    
    #Here we convert the d1 list of ECs to reactions.
    #For this we need to import the table from reactions. Must ensure rxn ids look like 'R00012'
    rxn_list_d2 = tsv_to_d2_list("/kb/module/data/reactions.tsv")


    #NOTE that this function returns abbreviations (R0004) not rxn ids (rxn0004)
    rxns_d1 = EC_to_Rxn_Ids(ecs_d1,rxn_list_d2)[1]
    #logging.info(rxns_d1)
    
    
    #Now we need to compare the reactions to the pathways as before, but with a 
    # new function.
    measured_pathways_d3 = sub_cp(rxns_d1)

    
    #For now just print the output
    #print_d2_list_out_to_tsv_file(tfams_and_ecs, output_file_pathway)
    
    #The output file pathway comes from 
    print_d2_list_out_to_tsv_file(measured_pathways_d3, output_file_pathway)






