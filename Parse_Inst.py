class Instruction:
    def __init__(self, inst, dest, source_0, source_1, index, str):
        self.inst = inst
        self.dest = dest
        self.source_0 = source_0
        self.source_1 = source_1
        self.index = index
        self.str = str
        self.ID = -1

# IDEA:
# 1. Read the instruction file
# 2. Return the list with Instruction type objects
def parse_inst():
    print("processing data......")
    inst_list = []
    i=0
    with open('testcase1_Instruction.txt', mode='r') as  f1:
        f11 = f1.readlines()
    for x in f11:

        y = x.split(' ')

        if len(y) == 4:

            operand_construct = Inst_No(y[0])
            print(operand_construct)

            print(y[1].split(',')[0])
            dest_operand_1 = int(y[1].split(',')[0][1:])
            print (dest_operand_1)

            print(y[2].split(',')[0])
            source_operand_0 = int(y[2].split(',')[0][1:])
            print(source_operand_0)

            print(y[3].split('\n')[0])
            source_operand_1 = int(y[3].split(',')[0][1:])
            print(source_operand_1)

            p = Instruction(operand_construct, dest_operand_1, source_operand_0, source_operand_1, i, x)
            print ("p's inst is",p.inst,"index is",p.index)

            inst_list.append(p)
            i+=1
        # TODO: Ld/Sd Left since there are only two operands
        if len(y) == 3:
            print(y[0])

            print(y[1].split(',')[0])

            print(y[2].split('\n')[0])
            i+=1
    return inst_list, len(inst_list)
    print("end!")

def Inst_No (inst_type):
    if inst_type == "Ld":
        return 1
    elif inst_type == "Sd":
        return 2
    elif inst_type == "Beq":
        return 3
    elif inst_type == "Bne":
        return 4
    elif inst_type == "Add":
        return 5
    elif inst_type == "Add.d":
        return 6
    elif inst_type == "Addi":
        return 7
    elif inst_type == "Sub":
        return 8
    elif inst_type == "Sub.d":
        return 9
    elif inst_type == "Mult.d":
        return 10

