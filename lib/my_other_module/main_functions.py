#This file is intended to organize the various types of overall functions the app uses so they aren't written directly into the Impl file.


import os
from my_other_module.parsing_functions import tsv_to_d2_list, csv_to_d2_list, print_d2_list_out_to_tsv_file, d2_list_to_html_table_file, get_TIGRFAM_IDs_from_KBaseGeneFamilies_DomainAnnotation_2, string_to_html_file
from my_other_module.Check_Pathway.check_pathways_vs_reactions import main_cp, sub_cp
from my_other_module.Check_Pathway.TIGRFAM_to_EC import tfam_main
from my_other_module.Aux_Functions.aux_1 import tfams_and_ecs_d2_to_ecs_d1, extract_tfam_IDs
from my_other_module.Check_Pathway.EC_num_to_reaction_id import EC_to_Rxn_Ids 
from my_other_module.HTML_Details import make_bar_graph_from_data
import logging



#Inputs to the function:
#    bug_filepath - (str) the path to the file which contains the information about the bug
#    output_file_pathway - (str) The path to a file which doesn't exist yet, just a name to print the file to.
#    entity_title - (str) The name of the bug/object we are analyzing.
def reactions_file_to_pathway_reactions_and_percentages(bug_filepath, output_file_pathway, entity_title):

        # Here is where we call the function that checks the pathway
        cp_output_list_d3 = main_cp(bug_filepath)

        # We print the output from the previous function to a file named 'output_file_pathway'
        print_d2_list_out_to_tsv_file(cp_output_list_d3, output_file_pathway)

        # We name the html_pathway we'll be printing to.
        html_pathway = output_file_pathway[:-3] + 'html'

        # We make a bar graph from the data
        html_file_string = make_bar_graph_from_data(cp_output_list_d3, entity_title)

        # We print the output from the previous function the file named html_pathway
        string_to_html_file(html_file_string, html_pathway)


        return html_pathway


# Inputs:
#   Domain_annotations_dict (dict) is a dict as given by workspace get objects 2.
#   output_file_pathway (str) represents the output file name
#   entity_title (str) is the name of the object we are analyzing.
def TIGRFAM_file_to_pathway_reactions_and_percentages(Domain_annotations_dict, output_file_pathway, entity_title):
        
    # We run a special function to extract TIGRFAM IDs from the KBase object
    tfam_ids_d1 = get_TIGRFAM_IDs_from_KBaseGeneFamilies_DomainAnnotation_2(Domain_annotations_dict)

    #Here we get the d2 list of tfam ids and related ec numbers
    #The list looks like: [[tfam, ec],[tfam,ec],...]
    tfams_and_ecs_d2 = tfam_main(tfam_ids_d1)

    #Here we convert the tfams and ecs d2 list into just a list of ec numbers.
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

    #We name the output pathway
    html_pathway = output_file_pathway[:-3] + 'html'

    #We create the html file
    html_file_string = make_bar_graph_from_data(measured_pathways_d3, entity_title)

    #We print html file to pathway
    string_to_html_file(html_file_string, html_pathway)

    return html_pathway




