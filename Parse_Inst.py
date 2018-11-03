class Instruction:
    def __init__(self, inst, dest, source_0, source_1):
        self.inst = inst
        self.dest = dest
        self.source_0 = source_0
        self.source_1 = source_1


def parse_Inst():
    print("processing data......")
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

            p = Instruction(operand_construct, dest_operand_1, source_operand_0, source_operand_1)
            print ("p's inst is",p.inst)

        if len(y) == 3:
            print(y[0])

            print(y[1].split(',')[0])

            print(y[2].split('\n')[0])
    print("end!")

def Inst_No (inst_type):
    if inst_type == "Ld":
        return 1
    elif inst_type == "Sd":
        return 2
    elif inst_type == "Sd":
        return 3
    elif inst_type == "Beq":
        return 4
    elif inst_type == "Bne":
        return 5
    elif inst_type == "Add":
        return 6
    elif inst_type == "Add.d":
        return 7
    elif inst_type == "Addi":
        return 8
    elif inst_type == "Sub":
        return 9
    elif inst_type == "Sub.d":
        return 10
    elif inst_type == "Mult.d":
        return 11

parse_Inst()