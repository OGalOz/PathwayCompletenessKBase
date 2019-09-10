#This file is to create assisting functions to clear up space


def tfams_and_ecs_d2_to_ecs_d1(tfams_ecs_d2):
    ecs_d1 = []
    for i in range(1,len(tfams_ecs_d2)):
        #This checks if it's an E.C. number by seeing if it has 3 '.'s inside.
        if len((tfams_ecs_d2[i][1].split('.'))) == 4:
            ecs_d1.append(tfams_ecs_d2[i][1])
    return ecs_d1



