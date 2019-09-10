#The purpose of this program is to allow you to enter an EC number and in return
# get a list of the associated reaction IDs as listed in KBase.
#It uses the file 'reactions.tsv' as provided at 'https://raw.githubusercontent.com/ModelSEED/ModelSEEDDatabase/dev/Biochemistry/reactions.tsv

# First step is to import file into arrays with each line of the file represented as one array/ list.


from capture import get_list_of_reactions

#USER INPUT---------------------------------------------------------------------------

filename = 'Data/reactions.tsv'





#CLOSE_USER_INPUT--------------------------------------------------------------------


RXN_LIST = get_list_of_reactions(filename)


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



def main():
	stop = 'n'
	while stop == 'n':
		print("type EC number here, type 'y' to end program")
		EC_Number = input()
		if EC_Number != 'y':
			print(return_reaction_ids_from_ec_num(EC_Number, RXN_LIST))
		else:
			stop = 'y'
main()





