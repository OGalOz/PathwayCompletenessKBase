# This file has simple functions mapping from ModelSEED IDs to E.C. Numbers,
#    and ModelSEED IDs to other Aliases such as "XCyc", and KEGG.

#######File Locations############

DB_Mappings = '/Users/omreeg/Programs/Arkin_Lab_Research_Home/DB_Mappings'

DB_Data_Dr = '/Users/omreeg/Programs/Arkin_Lab_Research_Home/DB_Mappings/Data/General/Model_SEED/'

EC_to_MSeed = DB_Data_Dr + 'Unique_ModelSEED_ECs_to_Reactions.txt'
MSeed_to_EC = DB_Data_Dr + 'Unique_ModelSEED_Reaction_ECs.txt'
MSeed_to_Aliases = DB_Data_Dr + 'Unique_ModelSEED_Reaction_Aliases.txt' 
MSeed_to_Names =  DB_Data_Dr + 'Unique_ModelSEED_Reaction_Names.txt'

#######FileNames End ############

import sys
sys.path.insert(0, DB_Mappings)
from DB_Aux_Programs.capture import tsv_to_d2_list, csv_to_d2_list


#ModelSEED IDs look like 'rxnXXXXX', EC numbers 'X.X.X.X' where 'X' is from [0-9]
def model_seed_to_EC(model_seed_id, file_list_d2):

    #Initializing list to return
    list_of_matching_ECs_d1 = []

    #Search###
    found_all = False
 
    #Start Index might be variable depending on our knowledge of the list.
    start_index = 1
    i = start_index    

    found_some = False

    while found_all == False and i < len(file_list_d2):
        current_id = file_list_d2[i][0]
        if current_id == model_seed_id:
            list_of_matching_ECs_d1.append(file_list_d2[i][1])
            found_some = True
            i += 1
        else:
            if found_some == True:
                found_all = True            
                i += 1
            else:
                i += 1
    #print(i)
    return list_of_matching_ECs_d1    


#ModelSEED IDs look like 'rxnXXXXX', EC numbers 'X.X.X.X' where 'X' is from [0-9]
def EC_to_ModelSEED(EC_num, file_list_d2):

    #Initializing list to return
    list_of_matching_model_seed_ids_d1 = []

    #Search###
    found_all = False

    #Start Index might be variable depending on our knowledge of the list.
    start_index = 1
    i = start_index

    found_some = False

    while found_all == False and i < len(file_list_d2):
        current_id = file_list_d2[i][1]
        if current_id == EC_num:
            list_of_matching_model_seed_ids_d1.append(file_list_d2[i][0])
            found_some = True
            i += 1
        else:
            if found_some == True:
                found_all = True
                i += 1
            else:
                i += 1
    print(i)
    return list_of_matching_model_seed_ids_d1







def main():
    #Index 0 is the model seed IDs, Index 1 is EC numbers
    file_list_d2 = tsv_to_d2_list(EC_to_MSeed)
    #model_seed_id = 'rxn00076'
    #print(model_seed_to_EC(model_seed_id, file_list_d2))
    EC_num = '1.1.1.100'
    print(EC_to_ModelSEED(EC_num, file_list_d2))
    


#main()
