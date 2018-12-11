#from pandas.core.frame import DataFrame

from copy import deepcopy

def output_txt(instruction_final_table, reg_int, reg_float):

    inst_set = []

    # inst_final_table = [[]]

    # with open('testcase1_Instruction.txt', mode='r') as  f1:
    #     f11 = f1.readlines()

    print("length of final table", len(instruction_final_table))
    f = open("instruction_final_table.txt", "w+")
    for i in range(len(instruction_final_table)):

        # y = x.split('\n')
        # inst_set.append(y[0])
        # print("appending Inst:", y[0])
        #





        print("Inst index is", i)

        print(instruction_final_table)
        #f.write("something")
        temp = deepcopy(instruction_final_table[i])
        if temp[2] == -1:
            temp[2] = "Null"
            temp[2].strip('"\'')
        # f.write(inst_set[i]+" "+str(instruction_final_table[i])+"\n")
        print("attention")
        print(temp[5] + " " + str(temp[0:5]) + "\n")
        f.write(temp[5].split('\n')[0] + " " + str(temp[0:5]) + "\n")



    f.write("\n")
    f.write("Reg Integer:\n")
    for i in range(0, 16):
        f.write("R"+str(i)+"\t")
    f.write("\n")
    for i in range(0, 16):
        f.write(str(reg_int[i])+"\t")
    f.write("\n\n")

    for i in range(16, 32):
        f.write("R"+str(i)+"\t")
    f.write("\n")
    for i in range(16, 32):
        f.write(str(reg_int[i])+"\t")
    f.write("\n")


    f.write("\n")
    f.write("Reg Float:\n")
    for i in range(0, 16):
        f.write("F"+str(i)+"\t")
    f.write("\n")
    for i in range(0, 16):
        print(str(reg_float[i])+"\t")
        # f.write("{:.2f}".format(reg_float[i])+"\t")
        f.write(str(reg_float[i]) + "\t")
    f.write("\n\n")

    for i in range(16, 32):
        f.write("F"+str(i)+"\t")
    f.write("\n")
    for i in range(16, 32):
        f.write(str(reg_float[i])+"\t")
    f.write("\n")


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
