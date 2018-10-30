# from parse import main
# from parse import ProcessorConfig

import array


# def whoami():
#     import inspect
#     frame = inspect.currentframe()
#     return inspect.getframeinfo(frame).function

def whoami():
    import sys
    return sys.getframe(1).f_code.co_name


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

    def print_config(self):
        print("adder config:")
        print("# of rs /", "Cycles in EX /", "Cycles in Mem /", "# of FUs /")
        print(self.config.name, self.config.rs_number, self.config.ex_cycles, self.config.mem_cycles, self.config.fu_number)

    def operation(self, current_cycle):
        print("processor cycle: ", current_cycle)
        # for i in range(len(self.config.rs_number)):
        for rs in self.rs:
            if rs.in_use == True:
                if rs.src_ready == [True, True]:    # start an addition operation
                    rs.src_ready = [False, False]
                    rs.start_cycle = current_cycle
                    rs.finish_cycle = current_cycle + self.config.ex_cycles
                    rs.dest_value = rs.src_value[0] + rs.src_value[1]
                    print("adder:")
                    print("start cycle:", rs.start_cycle)
                    print("finish cycle:", rs.finish_cycle)
                elif rs.finish_cycle == current_cycle: # exactly the cycle to write back
                    print("adder:")
                    print("WBing in cycle: ", current_cycle)
                    rs.in_use = False


class ARF:
    def __init__(self):
        self.reg_int = array.array('L') # unsigned long
        for i in range(32):
            self.reg_int.append(0)

        self.reg_float = array.array('d') # double
        for i in range(32):
            self.reg_float.append(0)


class ROB:
    def __init__(self):
        # print(whoami())
        self.idle = 0
        self.index = 0
        self.reg_number = 0
        self.value_ready = False


class Processor(object):
    def __init__(self):
        self.cycle = -10  # current cycle
        self.ROB = [ROB() for i in range(1000)]  # set 1000 ROB entries
        # print(self.ROB.__len__())
        self.ARF = ARF()
        self.RAT = array.array('I')  # unsigned int
        # self.RAT.append(1)
        # print(self.RAT[0])
        # print(self.RAT.__len__())

        # read processor configuration
        self.config = ProcessorConfig()
        self.config.read_config()
        self.config.print_config()

        # init adder
        self.adder = Adder(self.config.adder)
        self.adder.print_config()
        # self.adder.operation(self.cycle)

    def do_adder(self):
        print(whoami())
        # print(__name__)
        self.adder.operation(self.cycle)


# def init_adder(config):
#
#     # adder = Adder(config)
#     # adder.print_config()
#
#     # return adder
#     print("init_adder()")
