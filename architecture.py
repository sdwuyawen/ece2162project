# from parse import main
# from parse import ProcessorConfig

import array

from Parse_Inst import *


# def whoami():
#     import inspect
#     frame = inspect.currentframe()
#     return inspect.getframeinfo(frame).function

def whoami():
    import sys
    return sys._getframe(1).f_code.co_name


class FunctionUnitSetting:
    def __init__(self, unit_name):
        self.name = unit_name
        self.rs_number = -1
        self.ex_cycles = -1
        self.mem_cycles = -1
        self.fu_number = -1


class ProcessorConfig:
    # adder_rs_number = 0
    # adder_ex_cycles = 0
    # adder_fu_number = 0

    def __init__(self):
        self.adder = FunctionUnitSetting("adder")
        self.fpadder = FunctionUnitSetting("fpadder")
        self.fpmul = FunctionUnitSetting("fpmul")
        self.ldst = FunctionUnitSetting("load/store unit")

    # print(adder.ex_cycles)
    # print(adder.name)

    def print_config(self):
        print("processor config:")
        print("# of rs /", "Cycles in EX /", "Cycles in Mem /", "# of FUs /")
        print(self.adder.name, self.adder.rs_number, self.adder.ex_cycles, self.adder.mem_cycles, self.adder.fu_number)
        print(self.fpadder.name, self.fpadder.rs_number, self.fpadder.ex_cycles, self.fpadder.mem_cycles,
              self.fpadder.fu_number)
        print(self.fpmul.name, self.fpmul.rs_number, self.fpmul.ex_cycles, self.fpmul.mem_cycles, self.fpmul.fu_number)
        print(self.ldst.name, self.ldst.rs_number, self.ldst.ex_cycles, self.ldst.mem_cycles, self.ldst.fu_number)
        # print("adder_rs_number:", self.adder_rs_number)

    def read_config_one(self, item, keyword, lines):
        for i, line in enumerate(lines):
            if keyword in line and i + 1 < len(lines):
                # print(lines[i + 1])
                words = line.split()
                print("words", words)
                conf = lines[i + 1].split()
                item.rs_number = int(conf[0])
                item.ex_cycles = int(conf[1])
                item.mem_cycles = int(conf[2])
                item.fu_number = int(conf[3])

                # print(item.ex_cycles)

                break

    def read_config(self):
        f = open('processor_config.txt', 'r')
        lines = f.readlines()
        f.close()

        self.read_config_one(self.adder, "Integer adder", lines)
        self.read_config_one(self.fpadder, "FP adder", lines)
        self.read_config_one(self.fpmul, "FP multiplier", lines)
        self.read_config_one(self.ldst, "Load/store unit", lines)

        # for i, line in enumerate(lines):
        #     if "Integer adder" in line and i + 1 < len(lines):
        #         print(lines[i + 1])
        #         words = line.split()
        #         print("words", words)
        #         conf = lines[i + 1].split()
        #         self.adder.rs_number = conf[0]
        #         self.adder.ex_cycles = conf[1]
        #         self.adder.mem_cycles = conf[2]
        #         self.adder.fu_number = conf[3]
        #
        #         print(self.adder.ex_cycles)
        #
        #         break


class ReservationStation:
    def __init__(self):
        self.in_use = False
        self.instruction_type = -1
        self.dest_addr = -1
        self.dest_value = -1
        self.src_addr = [-1, -1]
        self.src_ready = [False, False]
        self.src_value = [-1, -1]
        self.start_cycle = -1
        self.finish_cycle = -1


class Adder:
    # adder_rs_number = 0

    def __init__(self, adder_config):
        print("instantiate adder")
        self.config = adder_config
        self.rs = [ReservationStation() for i in range(self.config.rs_number)]
        print("rs number", self.rs.__len__())
        self.busy = False

    def print_config(self):
        print("adder config:")
        print("# of rs /", "Cycles in EX /", "Cycles in Mem /", "# of FUs /")
        print(self.config.name, self.config.rs_number, self.config.ex_cycles, self.config.mem_cycles, self.config.fu_number)

    def operation(self, current_cycle):
        print(whoami())
        print("processor cycle: ", current_cycle)
        if self.busy == False:
            # for i in range(len(self.config.rs_number)):
            for rs in self.rs:
                if rs.in_use == True:
                    if rs.src_ready == [True, True]:    # start an addition operation
                        self.busy = True
                        rs.src_ready = [False, False]
                        self.start_cycle = current_cycle
                        self.finish_cycle = current_cycle + self.config.ex_cycles
                        rs.dest_value = rs.src_value[0] + rs.src_value[1]
                        print("adder:")
                        print("start cycle:", rs.start_cycle)
                        print("finish cycle:", rs.finish_cycle)
                    elif rs.finish_cycle == current_cycle: # exactly the cycle to write back
                        self.busy = False
                        print("adder:")
                        print("WBing in cycle: ", current_cycle)
                        rs.in_use = False


class ARF:
    def __init__(self, int_val, float_val):
        self.reg_int = array.array('L') # unsigned long
        for i in range(32):
            self.reg_int.append(int_val[i])
        print("ARF: int val:", self.reg_int)

        self.reg_float = array.array('d') # double
        for i in range(32):
            self.reg_float.append(float_val[i])
        print("ARF: float val:", self.reg_float)


class MEM:
    def __init__(self, values):
        self.value = values
        print("MEM: ", self.value)


class ROB:
    def __init__(self):
        # print(whoami())
        self.idle = True
        # self.index = 0
        self.reg_number = -1
        self.reg_value = -1
        self.value_ready = False
        # TODO: = WB + 1
        self.value_rdy2commit_cycle = -1

    def clear(self):
        self.idle = True
        self.reg_number = -1
        self.reg_value = -1
        self.value_ready = False
        self.value_rdy2commit_cycle = -1

# class Issue:
#     def __init__(self, processor):


class Processor(object):
    def __init__(self, num_rob, num_cdb, reg_int, reg_float, mem_val):
        # TODO: process CDB
        self.cycle = 100  # current cycle

        self.ROB = [ROB() for i in range(num_rob)]  # set 1000 ROB entries
        print(self.ROB.__len__())
        self.ROB_header = 0
        self.ROB_tail = 0

        self.ARF = ARF(reg_int, reg_float)
        self.RAT = array.array('i')  # unsigned int
        for i in range(64):
            self.RAT.append(-1)
        # self.RAT.append(1)
        # print(self.RAT[0])
        # print(self.RAT.__len__())
        self.MEM = MEM(mem_val)

        # read processor configuration
        self.config = ProcessorConfig()
        self.config.read_config()
        self.config.print_config()

        # init adder
        self.adder = Adder(self.config.adder)
        self.adder.print_config()
        # self.adder.operation(self.cycle)

    def clock(self):
        self.cycle += 1
        print("cycle changing to: ", self.cycle)

    def do_adder(self):
        print(whoami())
        # print(__name__)
        self.adder.operation(self.cycle)

    def issue(self, inst):
        print(whoami())
        # TODO: Check what FU (adder or multiplier) the following inst needs
        # TODO: Check if both RS (for this instruction) and ROB have empty entries. If so, issue it. Otherwise, skip issue in this cycle
        # TODO: Circular buffer for ROB. Use head and tail to indicate the start and end of the ROB queue
        # TODO: Check RAT to find out if the dependent registers are in ARF or ROB. Fill the RS with value or ROB entry
        self.ROB[0].idle = 0
        # self.ROB[0].index = 0
        self.ROB[0].reg_number = inst.dest
        self.ROB[0].reg_value = 0
        # TODO: Check data dependency
        self.ROB[0].value_ready = False
        print("ROB[0]:", self.ROB[0].idle, self.ROB[0].reg_number, self.ROB[0].reg_value, self.ROB[0].value_ready)

        # TODO: RAT entry as ROB index
        self.RAT[inst.dest] = 0

        # TODO: Check if rs is full
        self.adder.rs[0].in_use = True
        self.adder.rs[0].start_cycle = self.cycle + 1
        # self.adder.rs[0].finish_cycle = self.adder
        self.adder.rs[0].src_value[0] = inst.source_0
        self.adder.rs[0].src_value[1] = inst.source_1
        self.adder.rs[0].src_ready = [True, True]
        rs_temp = self.adder.rs[0]
        print("adder.rs[0]:", rs_temp.src_value, rs_temp.in_use, rs_temp.instruction_type, rs_temp.dest_addr, rs_temp.dest_value,
              rs_temp.src_addr, rs_temp.src_ready, rs_temp.src_value, rs_temp.start_cycle, rs_temp.finish_cycle)

    def exec(self):
        self.adder.operation(self.cycle)

# def init_adder(config):
#
#     # adder = Adder(config)
#     # adder.print_config()
#
#     # return adder
#     print("init_adder()")
