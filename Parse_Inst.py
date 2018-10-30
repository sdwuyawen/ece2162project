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
            print(y[0])

            print(y[1].split(',')[0])
            dest_operand_1 = int(y[1].split(',')[0][1:])
            print (dest_operand_1)

            print(y[2].split(',')[0])
            source_operand_0 = int(y[2].split(',')[0][1:])
            print(source_operand_0)

            print(y[3].split('\n')[0])
            source_operand_1 = int(y[3].split(',')[0][1:])
            print(source_operand_1)

            p = Instruction(y[0], dest_operand_1, source_operand_0, source_operand_1)
            print ("p's inst is "+p.inst)

        if len(y) == 3:
            print(y[0])

            print(y[1].split(',')[0])

            print(y[2].split('\n')[0])
    print("end!")


parse_Inst()