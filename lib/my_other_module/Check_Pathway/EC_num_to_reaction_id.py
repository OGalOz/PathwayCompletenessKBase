#The purpose of this program is to allow you to enter an EC number and in return
# get a list of the associated reaction IDs as listed in KBase.
#It also allows you to input a reaction ID and get an EC number in return
#It uses the file 'reactions.tsv' as provided at 'https://raw.githubusercontent.com/ModelSEED/ModelSEEDDatabase/dev/Biochemistry/reactions.tsv

# First step is to import file into arrays with each line of the file represented as one array/ list.




# FILENAMES -----------------------------------
Package_Center = "/Users/OmreeG/Dropbox/LBL_Research-Ark_lab/Programs/DB_Mappings"
Programs_Home = "/Users/OmreeG/Dropbox/LBL_Research-Ark_lab/Programs"


Data_Directory_Filepath = "/Users/OmreeG/Dropbox/LBL_Research-Ark_lab/Programs/DB_Mappings/Data/General/"


KEGG_Pathways_Filepath = Data_Directory_Filepath + 'KEGG.pathways.txt'
REACTIONS_Filepath = Data_Directory_Filepath + 'reactions.tsv'
TIGRINFO_Filepath = Data_Directory_Filepath + 'TIGR_Info_Sorted.csv'


Bug_Directory_Filepath = "/Users/OmreeG/Dropbox/LBL_Research-Ark_lab/Programs/Metabolic_Model_Scripts/Data/"


#Note the following file is a CSV
FW602_Tigr_Filepath = Bug_Directory_Filepath + 'FW602_bin_15_Metabolic_Model/FW602-Tigrfam-Domain-Annot.csv'


#End_of_Filenames#################################----------------


import sys
sys.path.insert(0, Package_Center)
sys.path.insert(0, Programs_Home)

#test
from Programs.DB_Mappings.DB_Aux_Programs.capture import tsv_to_d2_list

#imports
from DB_Mappings.DB_Aux_Programs.capture import tsv_to_d2_list
from DB_Mappings.program_files.populate_EC_numbers_in_reaction_list import find_reaction_location



# If necessary:
RXN_List = tsv_to_d2_list(REACTIONS_Filepath)


# In the arrays in RXN_LIST, index 0 is "reaction id", index 13 is the "EC number"

def return_reaction_ids_from_ec_num(EC_Number, RXN_LIST):
	rxn_ids = []
	for i in range(len(RXN_LIST)):
		current_row = RXN_LIST[i]
		if check_existence(current_row[13],EC_Number):
			rxn_ids.append(current_row[0])
	return rxn_ids

#This part of the program is written because some reactions are associated
#With multiple EC numbers; in that case, the EC numbers are listed "#1|#2|#3|... etc"
def check_existence(a,b):
	if a == b:
		return True
	if "|" in a:
		all_EC_nums = a.split("|")
		for ec_num in all_EC_nums:
			if ec_num == b:
				return True
	return False


def return_ec_num_from_reaction_id(reaction_ID, RXN_List)"

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
			print(return_reaction_ids_from_ec_num(EC_Number, RXN_LIST))
		else:
			stop = 'y'
#test()







