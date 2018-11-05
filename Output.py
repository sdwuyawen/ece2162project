#from pandas.core.frame import DataFrame
def output_txt(instruction_final_table, reg_int):

    inst_set = []

    inst_final_table = [[]]

    with open('testcase1_Instruction.txt', mode='r') as  f1:
        f11 = f1.readlines()

    for x in f11:
        y = x.split('\n')
        inst_set.append(y[0])
        print("appending Inst:", y[0])

    f = open ("instruction_final_table.txt", "w+")

    for i in range(len(inst_set)):
        print("Inst index is", i)
        inst_final_table.append([inst_set[i], instruction_final_table[i]])
        print(inst_final_table)
        #f.write("something")
        temp = instruction_final_table[i].copy()
        if temp[2] == -1:
            temp[2] = "Null"
            temp[2].strip('"\'')
        # f.write(inst_set[i]+" "+str(instruction_final_table[i])+"\n")
        f.write(inst_set[i] + " " + str(temp) + "\n")

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
