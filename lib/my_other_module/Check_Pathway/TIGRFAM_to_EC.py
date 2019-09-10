#This program takes you from the TigrFam Domain annotation to the reactions in KBase.
#You can start by taking the bug's Tigrfam domain annotation output file-
#    For each of its 'Domain Accession IDs' (eg TIGR00611), use the 
#    Tigrinfo.csv file and find the E.C. number. From the E.C. number, use 
#    the modelSeed file to find the related reaction IDs. Create a table with all three
#    values (Domain Accession ID, EC number, reaction ID). 
#
#
#
#TD: Write program that takes TIGRFAM IDs and for each ID returns an E.C. number if one is available.
#TD : Speed up the search in the function TIGRID_to_EC_num(TIGRID, tigr_list_d2) using index. 


from my_other_module.parsing_functions import tsv_to_d2_list

# FILENAMES -----------------------------------

Data_Directory_Filepath = "/kb/module/data/"

KEGG_Pathways_Filepath = Data_Directory_Filepath + 'KEGG.pathways.txt'
REACTIONS_Filepath = Data_Directory_Filepath + 'reactions.tsv'
TIGRINFO_Filepath = Data_Directory_Filepath + 'tigrinfo.tsv'

#End_of_Filenames#################################----------------



#This function takes a list of TIGRFAM IDs and adds to it a list of EC numbers in relation.
def tfam_main(TIGRFAM_IDS_d1):

    #output list looks like [[TIGRFAM ID, related EC], [TIGRFAM ID, related EC] , ... ]
    output_list = [["TIGRFAM ID","E.C. Number"]]
    tfam_d2_list = tsv_to_d2_list(TIGRINFO_Filepath)
    for id in TIGRFAM_IDS_d1:
        ec_num = TIGRID_to_EC_num(id, tfam_d2_list)
        output_list.append([id, ec_num])

    return output_list




#This function takes a string (TIGR Id eg TIGR00011) and returns a related EC number if it exists.
def TIGRID_to_EC_num(TIGRID, tigr_list_d2):
    
    #Check for errors:
    if type(TIGRID) != str:
        #print("The inputted Tigrfam ID must be a string")
        return ""
    if len(TIGRID) > 10:
        #print("It's likely that you are not inputting a Tigrfam ID because it contains too many characters.")
        return "?"
    
    #The tigrIds are in column index 1, ec numbers column index 5.
    # The following search could be sped up using the index:
    i = 1
    found = False
    while i < len(tigr_list_d2):
        if TIGRID == tigr_list_d2[i][1]:
            ec_num = tigr_list_d2[i][5]
            found = True
            i  = len(tigr_list_d2)

        else:
            i += 1
    
    if found== True:
        if check_EC_num(ec_num) == 1:
            #print("EC Number for TigrID: " + TIGRID + " is not useful.")
            return "?"
        else:
            return ec_num

    

#Function returns 0 if EC number is good, 1 if EC number is bad.
def check_EC_num(ec_num):
    
    #First we check if EC number is anything at all
    if ec_num == None:
        return 1
    elif len(ec_num) < 7:
        return 1
    elif '-' in ec_num:
        return 1
    else:
        return 0



def test():

    tigr_list_d2 = csv_to_d2_list(TIGRINFO_Filepath)
    print("TIGR00009:")
    x = TIGRID_to_EC_num("TIGR00009", tigr_list_d2)
    print(x)
    print("TIGR01:")
    x = TIGRID_to_EC_num("TIGR01", tigr_list_d2)
    print(x)
    print("TIGR00024:")
    x = TIGRID_to_EC_num("TIGR00024", tigr_list_d2)
    print(x)
    print("TIGR00045:")
    x = TIGRID_to_EC_num("TIGR00045", tigr_list_d2)
    print(x)

#test()
    
