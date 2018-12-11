class Data_Instruction:
    def __init__(self, inst, dest, offset, source, index, str):
        self.inst = inst
        self.F = dest
        self.offset = offset
        self.R = source
        self.index = index
        self.str = str
        self.ID = -1

class Control_Instruction:
    def __init__(self, inst, source_0, source_1, offset, index, str):
        self.inst = inst
        self.source_0 = source_0
        self.source_1 = source_1
        self.offset = offset
        self.index = index
        self.str = str
        self.ID = -1

class ALU_Instruction:
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
            # Control instruction
            if ALU_Inst_Type(y[0]) == 3 or ALU_Inst_Type(y[0]) == 4:

                # operand added
                operand_construct = ALU_Inst_Type(y[0])
                print(operand_construct)

                # comparator 0 (R->integer)
                print(y[1].split(',')[0])
                source_operand_0 = int(y[1].split(',')[0][1:])
                print (source_operand_0)

                # comparator 1 (R->integer)
                print(y[2].split(',')[0])
                source_operand_1 = int(y[2].split(',')[0][1:])
                print(source_operand_1)

                # offset (Integer)
                print(y[3].split('\n')[0])
                offset = int(y[3].split('\n')[0])
                print(offset)

                p = Control_Instruction(operand_construct, source_operand_0, source_operand_1, offset, i, x)
                print ("p's inst is",p.inst,"offset is",p.offset)


            else:
                operand_construct = ALU_Inst_Type(y[0])
                print(operand_construct)

                # if operand is Addi, the last input is immediate.
                if operand_construct == 7:

                    print(y[1].split(',')[0])
                    dest_operand = int(y[1].split(',')[0][1:])
                    print(dest_operand)

                    print(y[2].split(',')[0])
                    source_operand_0 = int(y[2].split(',')[0][1:])
                    print(source_operand_0)

                    print(y[3].split('\n')[0])
                    source_operand_1 = y[3].split('\n')[0]
                    print(source_operand_1)

                # if operand is float, the register are floating number.
                elif operand_construct == 6 or operand_construct == 9 or operand_construct == 10:

                    print(y[1].split(',')[0])
                    dest_operand = int(y[1].split(',')[0][1:])
                    print(dest_operand+32)

                    print(y[2].split(',')[0])
                    source_operand_0 = int(y[2].split(',')[0][1:])
                    print(source_operand_0+32)

                    print(y[3].split('\n')[0])
                    source_operand_1 = int(y[3].split('\n')[0][1:])
                    print(source_operand_1+32)
                else:

                    print(y[1].split(',')[0])
                    dest_operand = int(y[1].split(',')[0][1:])
                    print(dest_operand)

                    print(y[2].split(',')[0])
                    source_operand_0 = int(y[2].split(',')[0][1:])
                    print(source_operand_0)

                    print(y[3].split('\n')[0])
                    source_operand_1 = int(y[3].split('\n')[0][1:])
                    print(source_operand_1)

                p = ALU_Instruction(operand_construct, dest_operand, source_operand_0, source_operand_1, i, x)
                print ("p's inst is",p.inst,"index is",p.index)

            inst_list.append(p)
            i+=1
        # TODO: Ld/Sd Left since there are only two operands
        if len(y) == 3:

            # operand added
            operand_construct = ALU_Inst_Type(y[0])
            print(operand_construct)

            # Destination (F register)
            print(y[1].split(',')[0])
            dest_operand = int(y[1].split(',')[0][1:])
            print(dest_operand+32)

            # offset (Integer)
            print(y[2].split('(')[0])
            offset = int(y[2].split('(')[0])
            print(offset)

            # Source (R register)
            print(y[2].split('(')[1].split(')')[0])
            source_operand = int(y[2].split('(')[1].split(')')[0][1:])
            print(source_operand)

            p = Data_Instruction(operand_construct, dest_operand, offset, source_operand, i, x)
            print("p's inst is", p.inst, "offset is", p.offset)
            inst_list.append(p)
            i+=1
    return inst_list, len(inst_list)
    print("end!")

def ALU_Inst_Type (inst_type):

    # LSQ
    if inst_type == "Ld":
        return 1
    elif inst_type == "Sd":
        return 2

    # Integer Adder
    elif inst_type == "Beq":
        return 3
    elif inst_type == "Bne":
        return 4
    elif inst_type == "Add":
        return 5
    elif inst_type == "Addi":
        return 7
    elif inst_type == "Sub":
        return 8

    # Float Adder
    elif inst_type == "Add.d":
        return 6
    elif inst_type == "Sub.d":
        return 9


    # Float Multiplier
    elif inst_type == "Mult.d":
        return 10
    return 0
