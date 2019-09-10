# First, we get an object with each row being a specific pathway, eg Glycolysis or Gluconeogenesis.
# Then we look at the reactions and check how many of those are present in our populated organism reactions list.

from my_other_module.parsing_functions import tsv_to_d2_list

#FILENAMES -----------------------------------


#CHECK - might have /app after module
#Pathways_File_Name = '/kb/module/data/KEGG_pathways.tsv'

#END OF FILENAMES -----------------------------


#main_cp returns a d3 list of lists to be printed to a file. It compares a bug's
# reactions file to the main pathways file provided above at Pathways_File_Name
def main_cp(bug_filename):
        

        Pathways_File_Name = '/kb/module/data/KEGG_pathways.tsv'

        #These are the two inputs to the comparison (All the pathways, and the reactions in the bug).
        pathways_list_d2 = tsv_to_d2_list(Pathways_File_Name)
        bug_rxn_list_d2 = tsv_to_d2_list(bug_filename)
	
	#measured pathways list looks like:
        measured_pathways_list_d3 = pathway_measure(pathways_list_d2, bug_rxn_list_d2)	


	#Here we add the filename we want to the list:
        to_print_filename = bug_filename[:-4] + '_P_c_a.txt'
	
        measured_pathways_list_d3.append(to_print_filename)

        #measured_pathways_list_d3 looks like [[pathway 1] [pathway 2] [pathway 3] ... [pathway n], filename]
        return measured_pathways_list_d3


#The following function checks all the pathways and measures an organism's completeness using its reaction list.
# It returns a d3 list with one row for each pathway and it's measure related to an organism.
def pathway_measure(pathways_list_d2, bug_rxn_list_d2):
	
	#You need a d1 list of all the reactions in the bug:
        bug_rxn_list_d1 = []
        for i in range(1, len(bug_rxn_list_d2)):
                if len(bug_rxn_list_d2[i]) > 11:
                    bug_rxn_list_d1.append(bug_rxn_list_d2[i][12])
		


	#Each item in measured_pathways_list: [name, [reactions yes], [reactions no], percentage yes]
        measured_pathways_list_d3 = [['Pathway name', 'Reactions Present', 'reactions not present', 'percentage']]

        for i in range (1, len(pathways_list_d2)):

		#pathway info will be [name, [reactions yes], [reactions no], percentage yes]
                pathway_info = []		

		#The following line gets a list with the pathway's info from the data text file.
                crnt_pathway = pathways_list_d2[i]
                pathway_info.append(crnt_pathway[2])

		

		#The following line returns a list of the reactions extant in the pathway
                crnt_reactions = get_reactions(crnt_pathway)

                pathway_info = compare_reactions(crnt_reactions, bug_rxn_list_d1, pathway_info)
	
                measured_pathways_list_d3.append(pathway_info)
	
        return measured_pathways_list_d3


#The 4th index of the pathways files contains the list of reactions
def get_reactions(pathway_list):
    rxns_list = pathway_list[4].split('|')
    return rxns_list


#The following function compares the reactions from the pathway to the reactions in the bug. Incomplete.
def compare_reactions(pathway_rxn_list, bug_rxn_list_d1, pathway_info):
	
    rxns_present = []
    rxns_not_present = []
    for rxn in pathway_rxn_list:
        if rxn in bug_rxn_list_d1:
            rxns_present.append(rxn)
        else:
            rxns_not_present.append(rxn)
    		
    pathway_info.append(rxns_present)
    pathway_info.append(rxns_not_present)
    if len(rxns_not_present) == 0 and len(rxns_present)== 1:
        pathway_info.append(0)
    else:
        pathway_info.append(float(len(rxns_present)/len(pathway_rxn_list)))
    return pathway_info
