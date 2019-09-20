#This file takes care of detailed HTML creation, e.g. making a bar graph with JavaScript.

import logging
from operator import itemgetter



#Uses Javascript - this one takes data in table form [[Pathway,[bs],[bs],percentage][Pathway,[bs],[bs],percentage], etc.]
def make_bar_graph_from_data(table_list_d2, entity_title):


    f = open("/kb/module/data/bar_chart_html.html","r")
    html_str = f.read()
    f.close()

    #Here we divide the bar chart into the parts that matter, index 1 is where we will insert all of the important information.
    html_list = html_str.split('***')

    #This should be 3
    logging.info(len(html_list))
    

    #The inserted html string will just be a python dictionary with the following form:
    # {"labels":['a','b',...], "datasets":[{"label":"Pathway Completeness","data":[65,59,80,81,56,55,40],"fill":false, "borderWidth":1}]}

    new_data_dict = {}
    data_sets_sub_dict = {"label":"Pathway Completeness for " + entity_title, "fill": False, "borderWidth":1}
    labels = []
    percentages = []
    backgroundColor = []
    


    """#Sorting list
    first_row = table_list_d2[0]
    table_list_d2 = table_list_d2[1:]
    sorted(table_list_d2, key=itemgetter(3), reverse=True)
    table_list_d2.insert(0, first_row)"""

    for i in range(1,len(table_list_d2)-1):
        if table_list_d2[i][3] > 0:
            labels.append(table_list_d2[i][0])
            percentages.append(table_list_d2[i][3]*100)
            #Define color of bar here?
            if (i % 4) == 0:
                backgroundColor.append('rgba(255, 99, 132, 0.2)')
            elif (i % 4) == 1:
                backgroundColor.append('rgba(75, 192, 192, 0.2)')
            elif (i % 4) == 2:
                backgroundColor.append('rgba(54, 162, 235, 0.2)')
            else:
                backgroundColor.append('rgba(201, 203, 207, 0.2)')



    percentages, labels = zip(*sorted(zip(percentages, labels),reverse=True))
    
    data_sets_sub_dict["data"] = list(percentages)
    data_sets_sub_dict["backgroundColor"] = backgroundColor
    new_data_dict["datasets"] = [data_sets_sub_dict]
    new_data_dict["labels"] = list(labels)




    #replacing 'False' with 'false'
    javascript_object = str(new_data_dict).replace('False','false')


    final_html_str = html_list[0] + javascript_object + html_list [2]

    return final_html_str
    



