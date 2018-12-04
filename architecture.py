# from parse import main
# from parse import ProcessorConfig

import array
#import numpy

from parse import *

from Parse_Inst import *


# def whoami():
#     import inspect
#     frame = inspect.currentframe()
#     return inspect.getframeinfo(frame).function

# Constants

EXEC = 0
WRITE_BACK = 1
WRITE_BACK_CHECK = 2


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
        self.index = 0
        self.in_use = False
        self.instruction_type = -1
        self.instruction_id = -1
        self.dest_addr = -1
        self.dest_value = -1
        self.src_addr = [-1, -1]
        self.src_ready = [False, False]
        self.src_value = [-1, -1]
        self.rdy2exe_cycle = -1

    def clear(self):
        self.__init__()
        print(whoami())


class LSQ:
    def __init__(self):
        self.type = "N"
        self.addr = -1
        self.value = -1

    def clear(self):
        self.__init__()


class Adder:
    # adder_rs_number = 0

    def __init__(self, adder_config, FU_index, rs):
        print("instantiate adder")
        self.config = adder_config
        # self.rs = [ReservationStation() for i in range(self.config.rs_number)]
        # for i in range(0, 3):
        # for i, rs in enumerate(self.rs):
        #     self.rs.index = i
        # print("rs number", rs.__len__())
        self.busy = False
        # self.wbing_value = -1
        self.wbing_cycle = -1
        self.active_rs_num = -1
        self.start_cycle = -1
        self.finish_cycle = -1
        self.fu_index = FU_index # to indicate the ID of this FU. For CDB use
        self.rs = rs

    def print_config(self):
        print("adder config:")
        print("# of rs /", "Cycles in EX /", "Cycles in Mem /", "# of FUs /")
        print(self.config.name, self.config.rs_number, self.config.ex_cycles, self.config.mem_cycles, self.config.fu_number)

    def operation(self, current_cycle, operation, processor):
        # print(whoami())
        print(processor)
        rs = processor.RS_Integer
        print("adder operation in cycle:", current_cycle)
        # print("processor cycle: ", current_cycle)
        if operation == EXEC:
            print("Adder EXEC:")
            if self.busy == False:
                print(" Adder got:")
                # for i in range(len(self.config.rs_number)):
                # for i, rs in enumerate(rs):
                # Find an entry in my RS that all dependencies are ready for Execution
                for i in range(len(rs)):
                    if rs[i].in_use == True:
                        if rs[i].src_ready == [True, True] and current_cycle >= rs[i].rdy2exe_cycle:    # start an addition operation
                            # Add current cycle as the execution cycle of corresponding instruction
                            processor.instruction_final_table[rs[i].instruction_index][1] = current_cycle

                            self.busy = True
                            print("     Adder occupied:")
                            # rs[i].src_ready = [False, False]
                            self.start_cycle = current_cycle
                            # print(self.config.ex_cycles)
                            self.finish_cycle = current_cycle + self.config.ex_cycles
                            self.active_rs_num = rs[i].index
                            print("active_rs_num = ", self.active_rs_num)
                            rs[i].dest_value = rs[i].src_value[0] + rs[i].src_value[1]
                            self.wbing_cycle = self.finish_cycle
                            print("start cycle:", self.start_cycle)
                            print("finish cycle:", self.finish_cycle)

            # elif self.busy == True:
                # print("Adder busy:")
                # if self.finish_cycle == current_cycle:  # exactly the cycle to write back
                    # self.busy = False
                    # print("adder:")
                    # print("WBing in cycle: ", current_cycle)
                    # self.rs[self.active_rs_num].in_use = False
                    # self.active_rs_num = -1
                    # self.wbing_cycle = current_cycle + 1
                    # self.wbing_value = self.rs[self.active_rs_num].dest_value

        # Before WB, the processor collect all the WB requests from FUs, and choose the inst with lowest ID
#        elif operation == WRITE_BACK_CHECK:
#            if self.busy == True:
#                if self.wbing_cycle <= current_cycle:
#                    processor.CDB.arbiter_q.append(rs[self.active_rs_num].instruction_id)

        elif operation == WRITE_BACK:
            # TODO: for memory load inst, its LSQ entry is cleared after getting value from memory or from previous load in LSQ
            # TODO: for memory store inst STR R1, R2(0), its LSQ entry is enqueued when the STR is issued, and dequeued when the commit is finished
            # The memory address is calculated in Ex stage. When R1 is ready to the LSQ, it broadcasts to all LSQ entry (Load) pending the memory address R2+0.
            # When R2 is ready, the memory address is calculated, and it broadcasts to all LSQ entry (Load) pending the memory address R2+0
            print("Adder WB:")
            if self.busy == True:
                print(" Adder.busy:")
                if self.wbing_cycle == current_cycle:
                    print("     WB cycle:")

                    # Successfully drop it to CDB
                    if processor.CDB.put_to_buffer(rs, self.active_rs_num, self.fu_index, current_cycle) == True:
                        self.busy = False
                        # release current RS entry after the WB task has been dropped to CDB
                        # self.rs[self.active_rs_num].in_use = False
                        rs[self.active_rs_num].clear()
                        print("rs[", self.active_rs_num, "] released")
                        self.active_rs_num = -1
                    else:
                        print("Drop to CDB failed. FU is kept busy")


class Queue:
    def __init__(self):
        self.queue = list()

    def addtoq(self,dataval):
    # Insert method to add element
        if dataval not in self.queue:
            self.queue.insert(0,dataval)
            return True
        return False

    # Pop method to remove element
    def removefromq(self):
        if len(self.queue)>0:
            return self.queue.pop()
        return ("No elements in Queue!")

    def currentsize(self):
        return len(self.queue)


class buffer_entry:
    inst_id = -1        # Issue sequence of Inst
    inst_wb_cycle = -1  # wbing cycle, for arbiter
    dest_addr = -1
    dest_value = -1          # list cannot be initialized here!
    fu_index = -1
    rs = None
    active_rs_number = -1   # which rs entry I should write to


class buffer_FU:
    def __init__(self, bufferSize):
        self.name = ""
        self.maxSize = bufferSize
        # self.entries = [buffer_entry() for i in range(bufferSize)]
        self.entries = Queue()
        # TheQueue.addtoq(self.CDB)
        # print(TheQueue.removefromq())


# Called after all the FUs' WB has been called.
class CDB:
    def __init__(self, numOfFUs, bufferSize):
#        self.arbiter_q = list()
        self.buffersize = bufferSize
        # for each FU, there is a buffer of size self.buffersize
        self.buffer = []        # empty array

        print("-----------------------------")

        for i in range(numOfFUs):       # The buffer is matched with FU by fu.index
            self.buffer.append(buffer_FU(self.buffersize))

        for i in range(len(self.buffer)):
            print(self.buffer[i])

        #     for j in range(self.buffersize):
        #         self.buffer[i][j].dest = -1
        #         self.buffer[i][j].value = -1

#    def arbiter(self):
        # print(self.arbiter_q)

    # need to be called by a FU when Write Back
    def put_to_buffer(self, rs, active_rs_number, fu_index, cycle):
        print("put_to_buffer")

        temp = buffer_entry()

#        temp.inst_id = rs.instruction_id        # the Issue sequence
        temp.inst_wb_cycle = cycle
        temp.inst_id = rs[active_rs_number].instruction_id         # the unique ID of each Issed instruction
        temp.dest_addr = rs[active_rs_number].dest_addr
        temp.dest_value = rs[active_rs_number].dest_value
        temp.fu_index = fu_index
        temp.rs = rs                             # Get the whole RS table of the FU
        temp.active_rs_number = active_rs_number

        if self.buffer[fu_index].entries.currentsize() < self.buffer[fu_index].maxSize:
            self.buffer[fu_index].entries.addtoq(temp)
            return True
        else:
            return False    # The CDB buffer is full. The FU should stall (if not-pipelined)

    # need to be called after WB of all the FUs
    def arbiter(self, processor):
        buffer = self.buffer.copy()
        temp = []
        # copy the first element in each FU buffer together to select
        for i in range(len(buffer)):
            if buffer[i].entries.currentsize() != 0:
                temp.append(buffer[i].entries.removefromq())

        if len(temp) > 0:
            temp.sort(key=lambda buffer_entry: buffer_entry.inst_wb_cycle)

            # only keep earliest ones
            for i in range(len(temp)):
                if temp[i].inst_wb_cycle != temp[0].inst_wb_cycle:
                    temp[i].remove()

            # sort again by inst_id
            temp.sort(key=lambda buffer_entry: buffer_entry.inst_id)
            # winner is temp(0) now. It is the header of the queue for that FU.
            # The dequeued element is the type of buffer_entry()
            self.buffer[temp[0].fu_index].entries.removefromq()
            # Todo: Write Back the temp[0] to RS (of FU temp[0].fu_index) and ROB

            # DO REAL Write Back Now
            rs = temp[0].rs
            current_cycle = processor.cycle

            # update corresponding ROB entry
            print("         update ROB entry ", temp[0].dest_addr)
            rob_entry = temp[0].dest_addr - 64  # rob entry 0 starts with number 64
            processor.ROB[rob_entry].reg_value = temp[0].dest_value
            processor.ROB[rob_entry].value_ready = True

            # Add current cycle as the WB cycle of corresponding instruction
            processor.instruction_final_table[processor.ROB[rob_entry].instruction_index][3] = current_cycle

            processor.ROB[rob_entry].value_rdy2commit_cycle = current_cycle + 1
            print("ROB", rob_entry, "updated to:", processor.ROB[rob_entry].reg_value,
                  processor.ROB[rob_entry].value_ready,
                  processor.ROB[rob_entry].value_rdy2commit_cycle)

            # update all the rs that pending this value
            # for i, rs in enumerate(rs):
            for i in range(len(rs)):
                if rs[i].in_use == True:
                    for j in [0, 1]:
                        if rs[i].src_ready[j] == False:
                            print("         update RS entry:", i, j)
                            print(rs[i].dest_addr, rs[i].src_addr[0], rs[i].src_addr[1])
                            if rs[i].src_addr[j] == temp[0].dest_addr:
                                rs[i].src_ready[j] = True
                                rs[i].src_addr[j] = -1
                                rs[i].src_value[j] = temp[0].dest_value
                                print("             updated RS entry:", i, j)


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
        self.instruction_index = -1

    def clear(self):
        self.idle = True
        self.reg_number = -1
        self.reg_value = -1
        self.value_ready = False
        self.value_rdy2commit_cycle = -1

# class Issue:
#     def __init__(self, processor):


class Processor(object):
    def __init__(self, num_rob, num_cdb, reg_int, reg_float, mem_val, num_inst, inst_list):
        # TODO: process CDB

        # declare an final instruction table for every inst
        # Issue, Exec, Mem, WB, Commit
        self.instruction_final_table = [[-1 for j in range(5)] for i in range(num_inst)]

        self.cycle = 100  # current cycle

        self.ROB = [ROB() for i in range(num_rob)]  # set 1000 ROB entries
        print(self.ROB.__len__())
        self.ROB_header = 0
        self.ROB_tail = 0
        self.ROB_num = num_rob

        self.ARF = ARF(reg_int, reg_float)
        self.RAT = array.array('i')  # unsigned int
        for i in range(64):
            self.RAT.append(i)
        # self.RAT.append(1)
        # print(self.RAT[0])
        # print(self.RAT.__len__())
        self.MEM = MEM(mem_val)

        # read processor configuration
        self.config = ProcessorConfig()
        self.config.read_config()
        self.config.print_config()

        self.RS_Integer = [ReservationStation() for i in range(self.config.adder.rs_number)]
        for i in range(len(self.RS_Integer)):
            self.RS_Integer[i].index = i

        # init adder
        print("----------------------------------------")
        print(self.RS_Integer)
        self.adder = Adder(self.config.adder, 0, self.RS_Integer)
        self.adder.print_config()
        # self.adder.operation(self.cycle)

        self.inst_num = num_inst
        # print("proc inst num: ", self.inst_num)
        self.inst_list = inst_list
        self.inst_issue_index = 0
        # Instruction unique ID
        self.inst_ID_last = 0

        # TODO: number of FUs, each buffer size
        self.CDB = CDB(2, 1)

        # TheQueue = Queue()
        # TheQueue.addtoq(self.CDB)
        # print(TheQueue.removefromq())

    def clock(self):
        self.cycle += 1
        print("cycle changing to: ", self.cycle)

    # def do_adder(self):
    #     print(whoami())
    #     # print(__name__)
    #     self.adder.operation(self.cycle, EXEC, self, self.RS_Integer)


    #     # TODO: Check what FU (adder or multiplier) the following inst needs
    #     # TODO: Check if both RS (for this instruction) and ROB have empty entries. If so, issue it. Otherwise, skip issue in this cycle
    #     # TODO: Circular buffer for ROB. Use head and tail to indicate the start and end of the ROB queue
    #     # TODO: Check RAT to find out if the dependent registers are in ARF or ROB. Fill the RS with value or ROB entry
    #     self.ROB[0].idle = 0
    #     # self.ROB[0].index = 0
    #     self.ROB[0].reg_number = inst.dest
    #     self.ROB[0].reg_value = 0
    #     # TODO: Check data dependency
    #     self.ROB[0].value_ready = False
    #     print("ROB[0]:", self.ROB[0].idle, self.ROB[0].reg_number, self.ROB[0].reg_value, self.ROB[0].value_ready)
    #
    #     # TODO: RAT entry as ROB index
    #     self.RAT[inst.dest] = 0
    #
    #     # TODO: Check if rs is full
    #     self.adder.rs[0].in_use = True
    #     self.adder.rs[0].start_cycle = self.cycle + 1
    #     # self.adder.rs[0].finish_cycle = self.adder
    #     self.adder.rs[0].src_value[0] = inst.source_0
    #     self.adder.rs[0].src_value[1] = inst.source_1
    #     self.adder.rs[0].src_ready = [True, True]
    #     rs_temp = self.adder.rs[0]
    #     print("adder.rs[0]:", rs_temp.src_value, rs_temp.in_use, rs_temp.instruction_type, rs_temp.dest_addr, rs_temp.dest_value,
    #           rs_temp.src_addr, rs_temp.src_ready, rs_temp.src_value)
    #
    def execs(self):
        self.adder.operation(self.cycle, EXEC, self)

    def issue(self):
        print("inst list not empty")
        if self.inst_issue_index <= self.inst_num - 1:
            if self.issue_one_inst(self.inst_list[self.inst_issue_index]) == 0:
                print("Issue Inst", self.inst_issue_index, self.inst_list[self.inst_issue_index].str, "succeed")
                self.inst_issue_index += 1
            else:
                print("Issue Inst", self.inst_issue_index, "failed")

    def issue_one_inst(self, inst):
        print(whoami())
        # 1. TODO: Check what FU (adder or multiplier) the following inst needs
        # 3. TODO: Circular buffer for ROB. Use head and tail to indicate the start and end of the ROB queue
        # 4. TODO: Check RAT to find out if the dependent registers are in ARF or ROB. Fill the RS with value or ROB entry
        # 2. TODO: Check if both RS (for this instruction) and ROB have empty entries. If so, issue it. Otherwise, skip issue in this cycle

        flag = False
        ROB_no = -1
        RS_no = -1

        # 2.1 Check if the ROB has empty entry.
        # If no, return -1
        # If yes, go on to check RS
        for i in range(self.ROB_header, self.ROB_header+self.ROB_num):
            rob_entry_no = i % self.ROB_num
            print("check ROB entry:", rob_entry_no)
            if self.ROB[rob_entry_no].idle == True:
                # only update ROB header when RS is also available
                # self.ROB_header = (self.ROB_header+1) % self.ROB_num
                ROB_no = rob_entry_no
                flag = True
                break

        print("ROB header is ", self.ROB_header)
        if flag == False:
            return -1

        # 2.3 Check if RS has empty entry
        # If no, return -1
        # If yes, update RS, ROB, RAT with instruction
        #
        # Note: Right now, this function has not decided which RS to be put

        flag = False

        print("RS number is",len(self.RS_Integer))

        for i in range(len(self.RS_Integer)):
            if self.RS_Integer[i].in_use == False:

                RS_no = i

                # Unique ID for each instruction. For CDB arbiter, the inst with smaller ID is first served
                inst.ID = self.inst_ID_last
                self.inst_ID_last = self.inst_ID_last + 1

                # 2.1 Update ROB
                self.ROB[rob_entry_no].reg_number = inst.dest
                self.ROB[rob_entry_no].idle = False
                self.ROB[rob_entry_no].instruction_index = inst.index

                # 2.2 Update RAT
                # RAT with dest 0-63 points to ARF
                # RAT with dest >= 64 ... points to ROB
                self.RAT[inst.dest] = 64 + ROB_no

                # 2.3 Update RS
                self.RS_Integer[i].in_use = True
                self.RS_Integer[i].instruction_type = inst.inst
                self.RS_Integer[i].dest_addr = ROB_no + 64
                self.RS_Integer[i].dest_value = -1
                self.RS_Integer[i].instruction_index = inst.index
                self.RS_Integer[i].instruction_id = inst.ID

                src_0 = self.RAT[inst.source_0]
                print("src_0 is", src_0)
                print("src_1 is", inst.source_1)
                src_1 = self.RAT[inst.source_1]

                self.RS_Integer[i].src_addr = [src_0, src_1]
                self.RS_Integer[i].start_cycle = -1
                self.RS_Integer[i].finish_cycle = -1

                # If both source is in ARF
                if (src_0 < 64 and src_1 < 64):
                    self.RS_Integer[i].src_ready = [True, True]
                    self.RS_Integer[i].src_value = [self.ARF.reg_int[src_0], self.ARF.reg_int[src_1]]

                # if source 0 is from ROB, source 1 is from ARF
                if (src_0 >= 64 and src_1 < 64):
                    self.RS_Integer[i].src_ready = [False, True]
                    self.RS_Integer[i].src_value = [-1, self.ARF.reg_int[src_1]]

                # if source 0 is from ARF, source 1 is from ROB
                if (src_0 < 64 and src_1 >= 64):
                    self.RS_Integer[i].src_ready = [True, False]
                    self.RS_Integer[i].src_value = [self.ARF.reg_int[src_0], -1]

                # if both are from ROB
                if (src_0 >= 64 and src_1 >= 64):
                    self.RS_Integer[i].src_ready = [False, False]
                    self.RS_Integer[i].src_value = [-1, -1]

                self.RS_Integer[i].rdy2exe_cycle = self.cycle + 1

                flag = True
                break

        # Issue aborted
        if flag == False:
            return -1
        else:
            self.ROB_header = (self.ROB_header + 1) % self.ROB_num


        print("ROB[",ROB_no,"]:", self.ROB[ROB_no].idle, self.ROB[ROB_no].reg_number, self.ROB[ROB_no].reg_value,
              self.ROB[ROB_no].instruction_index)
        print("RS[",RS_no,"]:", self.RS_Integer[RS_no].in_use, self.RS_Integer[RS_no].dest_addr, self.RS_Integer[RS_no].dest_value, self.RS_Integer[RS_no].src_addr,
            self.RS_Integer[RS_no].src_ready, self.RS_Integer[RS_no].src_value,self.RS_Integer[RS_no].instruction_index)
        print("Current cycle is",self.cycle)

        # Add a new line for final output instruction table
        # record Issue cycle
        self.instruction_final_table[inst.index][0] = self.cycle

        # print("ROB[0]:", self.ROB[0].idle, self.ROB[0].reg_number, self.ROB[0].reg_value, self.ROB[0].value_ready)

        # # 7. TODO: RAT entry as ROB index
        # self.RAT[inst.dest] = 0
        #
        # # 8. TODO: Check if rs is full
        # self.adder.rs[0].in_use = True
        # self.adder.rs[0].start_cycle = self.cycle + 1
        # # self.adder.rs[0].finish_cycle = self.adder
        # self.adder.rs[0].src_value[0] = inst.source_0
        # self.adder.rs[0].src_value[1] = inst.source_1
        # self.adder.rs[0].src_ready = [True, True]
        # rs_temp = self.adder.rs[0]
        # print("adder.rs[0]:", rs_temp.src_value, rs_temp.in_use, rs_temp.instruction_type, rs_temp.dest_addr, rs_temp.dest_value,
        #       rs_temp.src_addr, rs_temp.src_ready, rs_temp.src_value, rs_temp.start_cycle, rs_temp.finish_cycle)

        # Issue success
        return 0

    def write_back_check(self):
        self.adder.operation(self.cycle, WRITE_BACK_CHECK, self)    # inform CDB that adder wants to write back
        print("CDB Queue:-----------------------------------------------------")
#        print(self.CDB.arbiter_q)

    def write_back(self):
        print("++++++++++++++++++++++++++++++++")
        print(self)
        self.write_back_check()
        self.adder.operation(self.cycle, WRITE_BACK, self)

        self.CDB.arbiter(self)

    def execs(self):
        self.adder.operation(self.cycle, EXEC, self)

    def commit(self):  # pc 1103
        print("Commit begin:")
        # TODO: when commit, if the RAT entry does not point to this ROB entry, abandon this register value in ROB, and do not update ARF
        rob_H = self.ROB[self.ROB_tail]  # ROB header entry
        if rob_H.value_ready == True and self.cycle==self.ROB[self.ROB_tail].value_rdy2commit_cycle:  # ready to commit

            # Add current cycle as the wb cycle of corresponding instruction
            self.instruction_final_table[rob_H.instruction_index][4] = self.cycle

            self.RAT[rob_H.reg_number] = rob_H.reg_number  # update RAT to the latest ARF ID
            if rob_H.reg_number > 31:
                self.ARF.reg_float[rob_H.reg_number % 32] = rob_H.reg_value  # update ARF to the latest value in ROB
            else:
                self.ARF.reg_int[rob_H.reg_number % 32] = rob_H.reg_value  # update ARF to the latest value in ROB
            self.ROB[self.ROB_tail].clear()  # remove current ROB head entry
            self.ROB_tail = (self.ROB_tail + 1) % 64  # update ROB header to the next one

        print(self.ROB_tail)

# def init_adder(config):
#
#     # adder = Adder(config)
#     # adder.print_config()
#
#     # return adder
#     print("init_adder()")
