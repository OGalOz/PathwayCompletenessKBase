#The purpose of this program is to allow you to enter an EC number and in return
# get a list of the associated reaction IDs as listed in KBase.
#It also allows you to input a reaction ID and get an EC number in return
#It uses the file 'reactions.tsv' as provided at 'https://raw.githubusercontent.com/ModelSEED/ModelSEEDDatabase/dev/Biochemistry/reactions.tsv

from my_other_module.parsing_functions import tsv_to_d2_list



# FILENAMES -----------------------------------

Data_Directory_Filepath = "/kb/module/data/"


KEGG_Pathways_Filepath = Data_Directory_Filepath + 'KEGG.pathways.txt'
REACTIONS_Filepath = Data_Directory_Filepath + 'reactions.tsv'
TIGRINFO_Filepath = Data_Directory_Filepath + 'tigrinfo.tsv'

#End_of_Filenames#################################----------------


#This function takes a d1 list of EC numbers [EC 1, EC 2, EC 3, ... EC n]
#And it returns all the associated rxn numbers and an ordered list of ecs and rxns.
#Inputs:
# EC_list_d1 (python list): a list of EC numbers
# Rxn_list_d2: (python list): depth 2 list
#
#Outputs:
# combined_lists_d4: (python list): a list of depth 4 with reactions in two formats.
#
def EC_to_Rxn_Ids(EC_list_d1, Rxn_list_d2):

    # a list that's organized with EC numbers and associated reactions.
    all_rxns_d3 = [['EC Number',['Associated Rxn Numbers'] ]]

    # a list that just has all the reactions- for pathway completeness tests
    all_rxns_d1 = []
    for ec_num in EC_list_d1:
        #Reaction abbreviations look like 'R0005', reaction ids look like rxn004
        rxn_list_d1 = return_reaction_abbreviations_from_ec_num(ec_num, Rxn_list_d2)
        
        
        all_rxns_d3.append([ec_num,rxn_list_d1])
        for rxn in rxn_list_d1:
            all_rxns_d1.append(rxn)

    combined_lists_d4 = [all_rxns_d3, all_rxns_d1]

    return combined_lists_d4 

# If necessary:
RXN_List_d2 = tsv_to_d2_list(REACTIONS_Filepath)


# In the arrays in RXN_LIST, index 0 is "reaction id" (rxn0001), index 1 is abbreviation (R0004), index 13 is the "EC number"
#Inputs:
# EC_Number (str): an E.C number (Form X.X.X.X)
# RXN_LIST (python list): Depth 2 list with all reactions from a database file
#
#Outputs:
# rxn_ids (python list): Depth 1 list with reaction IDs "rxn0004" 
def return_reaction_ids_from_ec_num(EC_Number, RXN_LIST):
	rxn_ids = []
	for i in range(len(RXN_LIST)):
		current_row = RXN_LIST[i]
                # Here we check if the current row's 14th index (13 in python) has equivalence to given EC Number
		if check_existence(current_row[13],EC_Number):
                        # If it does have equivalence, we add the row's reaction id (index 0)
			rxn_ids.append(current_row[0])
	return rxn_ids

# Input and parameters same as the function right above this one except output has reaction abbreviations "R0004"
def return_reaction_abbreviations_from_ec_num(EC_Number, RXN_LIST):
        rxn_ids = []
        for i in range(len(RXN_LIST)):
                current_row = RXN_LIST[i]
                if check_existence(current_row[13],EC_Number):
                        rxn_ids.append(current_row[1])
        return rxn_ids



#This part of the program is written because some reactions are associated
#With multiple EC numbers; in that case, the EC numbers are listed "#1|#2|#3|... etc"
# a & b are both strings
def check_existence(a,b):
	if a == b:
		return True
	elif "|" in a:
		all_EC_nums = a.split("|")
		for ec_num in all_EC_nums:
			if ec_num == b:
				return True
        else:
            pass
	return False

# Inputs:
# reaction_ID (str): e.g. rxn0004
# RXN_List (python list): Depth 2, a table of all reactions from a database.
def return_ec_num_from_reaction_id(reaction_ID, RXN_List):

    estimated_index = int(reaction_id[3:])
    location = find_reaction_location(rxn_id, estimated_index, Rxn_List)
    if location != 0:
        EC_num = RXN_List[location][13]
    else:
        print("location not found")
        return 1    
    return EC_num




def test():
	stop = 'n'
	while stop == 'n':
		print("type EC number here, type 'y' to end program")
		EC_Number = input()
		if EC_Number != 'y':
			print(return_reaction_ids_from_ec_num(EC_Number, RXN_List_d2))
		else:
			stop = 'y'
#test()







