# from architecture import init_adder
from architecture import *
from Parse_Config import Config
from Parse_Inst import *
from Output import *

# file = open("testfile.txt", "w")
# file.write("Hello World")
# file.close()
#
# file = open("testfile.txt", "r")
# x = file.read(5)
# print(x)
# file.close()

# with open("processor_config.txt", "r") as f:
#     data = f.readlines()
#     for line in data:
#         words = line.split()
#         print(words)

# Class example
# class MyClass:
#     """A simple example class"""
#     i = 12345
#
#     def func(self):
#         return 'hello world'
#
# x = MyClass()
# print(x.func())
# x.counter = 1
# while x.counter < 10:
#     x.counter = x.counter * 2
# print(x.counter)
# del x.counter

# ---------------------------------------





# f = open('processor_config.txt', 'r')
# lines = f.readlines()
# f.close()
#
# proc_config = ProcessorConfig()
# proc_config.read_config()
# proc_config.print_config()
#
# for i, line in enumerate(lines):
#     if "Integer adder" in line and i+1 < len(lines):
#         print(lines[i+1])
#         words = line.split()
#
#         print(words)
#
#         break

def main():
    # init_adder(proc_config.adder)
    num_ROB=0
    num_CDB=0

    # reg_int_val = []
    # reg_float_val = []
    # for i in range(32):     # 0-31
       # reg_int_val.append(i)
       # reg_float_val.append(i)
    # print(init_val)

    reg_int_val = [0]*32
    reg_float_val = [0]*32

    # mem_val = []
    mem_val = [0]*64
    # for i in range(64):     # 0-63
       # mem_val.append(0)
    num_ROB, num_CDB = Config.Read_Config(num_ROB, num_CDB, reg_int_val, reg_float_val, mem_val)

    # print(reg_float_val)

    
    # processor.do_adder()

    # cycle: 100
    inst_list, inst_num = parse_inst()
    print("inst num", inst_num, inst_list)
    # for i in range(len(inst_list)):
    #     print(inst_list)

    processor = Processor(num_ROB, -1, reg_int_val, reg_float_val, mem_val, inst_num, inst_list)

    for i in range(0, 30):

        print("------branch issue------")
        print("inst issue ID", processor.inst_ID_last)
        print("inst index", processor.inst_issue_index)
        print("------branch issue END------")
        # processor.commit()
        processor.issue()

        processor.execs()
        processor.write_back()
        processor.commit()
        processor.clock()

    output_txt(processor.instruction_final_table, processor.ARF.reg_int, processor.ARF.reg_float, processor.MEM)

    # print("-----------------------------------------------------------------")
    # processor.issue()
    # # processor.issue_one_inst(inst_list[0])
    # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    # print("Issue, Exec, Mem, WB, Commit")
    # print(processor.instruction_final_table)
    #
    # print("-----------------------------------------------------------------")
    # # processor.clock()
    # processor.execs()
    # processor.write_back()
    # processor.commit()
    # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    # print("Issue, Exec, Mem, WB, Commit")
    # print(processor.instruction_final_table)
    #
    # processor.clock()
    # processor.issue()
    # processor.execs()
    # processor.write_back()
    # processor.commit()
    # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    # print("Issue, Exec, Mem, WB, Commit")
    # print(processor.instruction_final_table)
    #
    # processor.clock()
    # processor.execs()
    # processor.write_back()
    # processor.commit()
    # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    # print("Issue, Exec, Mem, WB, Commit")
    # print(processor.instruction_final_table)
    #
    # processor.clock()
    # processor.execs()
    # processor.write_back()
    # processor.commit()
    # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    # print("Issue, Exec, Mem, WB, Commit")
    # print(processor.instruction_final_table)
    #
    # processor.clock()
    # processor.execs()
    # processor.write_back()
    # processor.commit()
    # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    # print(processor.instruction_final_table)
    #
    # processor.clock()
    # processor.execs()
    # processor.write_back()
    # processor.commit()
    #
    # processor.clock()
    # processor.execs()
    # processor.write_back()
    # processor.commit()
    #
    #output_txt(processor.instruction_final_table)


if __name__ == '__main__':
    main()
