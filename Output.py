#from pandas.core.frame import DataFrame
def output_txt(instruction_final_table):

    inst_set = []

    inst_final_table = [[]]

    with open('testcase1_Instruction.txt', mode='r') as  f1:
        f11 = f1.readlines()

    for x in f11:
        y = x.split('\n')
        inst_set.append(y[0])

    f = open ("instruction_final_table.txt", "w+")

    for i in range(len(inst_set)):
        print("i is", i)
        inst_final_table.append([inst_set[i], instruction_final_table[i]])
        print(inst_final_table)
        #f.write("something")
        f.write(inst_set[i]+" "+str(instruction_final_table[i]))

    f.close()


def No2Inst (num):
    if num == 1:
        return "Ld"
    elif num == 2:
        return "Sd"
    elif num == 3:
        return "Beq"
    elif num == 4:
        return "Bne"
    elif num == 5:
        return "Add"
    elif num == 6:
        return "Add.d"
    elif num == 7:
        return "Addi"
    elif num == 8:
        return "Sub"
    elif num == 9:
        return "Sub.d"
    elif num == 10:
        return "Mult.d"