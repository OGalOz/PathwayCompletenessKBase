

import csv



def tsv_to_d2_list(file_name):
        d2_list = []
        with open(file_name) as list_values:
                list_reader = csv.reader(list_values, delimiter='\t')
                for list_object in list_reader:
                        d2_list.append(list_object)
        return d2_list


def csv_to_d2_list(file_name):
        d2_list = []
        with open(file_name) as list_values:
                list_reader = csv.reader(list_values, delimiter=',')
                for list_object in list_reader:
                        d2_list.append(list_object)
        return d2_list



#This function takes a list of lists and prints it out to a file with a given name.
def print_d2_list_out_to_tsv_file(input_list, output_filename):
                with open(output_filename, 'w') as f:
                        for item in input_list:
                                my_string = ''
                                for part in item:
                                        my_string += str(part) + '\t'
                                f.write("%s\n" % my_string)



def check_if_tsv_or_csv(filename):
    if filename[-3:] == 'tsv':
        return 'tsv'
    elif filename[-3:] == 'csv':
        return 'csv'
    else:
        return 'Unknown'

