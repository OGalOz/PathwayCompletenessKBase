#This file is to create assisting functions to clear up space



# This function extracts EC Numbers from a table and returns a d1 list.
# Inputs:
# tfams_ecs_d2: (python list) has depth 2 -  a table from a specific source? 
# 
# Returns:
# ecs_d1: (python list) a list of EC numbers from the input table
def tfams_and_ecs_d2_to_ecs_d1(tfams_ecs_d2):
    ecs_d1 = []
    for i in range(1,len(tfams_ecs_d2)):
        #This checks if it's an E.C. number by seeing if it has 3 '.'s inside.
        if len((tfams_ecs_d2[i][1].split('.'))) == 4:
            ecs_d1.append(tfams_ecs_d2[i][1])
        else:
            pass
    return ecs_d1



#This function extracts tfam ids from a table
# Inputs:
#   bug_tfam_d2_list: (python list) a table with inputs from a TFAM file?

# Returns:
#   tfams_ids_d1: (python list) depth 1, just all tfam IDs from the table

def extract_tfam_IDs(bug_tfam_d2_list):
    tfam_ids_d1 = []
    for i in range(1,len(bug_tfam_d2_list)):
        tfam_ids_d1.append(bug_tfam_d2_list[i][5])
    return tfam_ids_d1



