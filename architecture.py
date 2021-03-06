# from parse import main
# from parse import ProcessorConfig

import array
#import numpy

from parse import *
from copy import deepcopy
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
        self.instruction_index = -1
        self.instruction_type = -1
        self.instruction_id = -1
        self.dest_addr = -1
        self.dest_value = -1
        self.src_addr = [-1, -1]
        self.src_ready = [False, False]
        self.src_value = [-1, -1]
        self.rdy2exe_cycle = -1
        self.id = -1


    def clear(self):
        self.__init__()
        print(whoami())


class LSQ:
    def __init__(self):
        self.type = "N" # set to be L/S
        self.addr = -1
        self.value = -1


        self.index = 0
        self.in_use = False
        self.instruction_index = -1
        self.instruction_type = -1
        self.instruction_id = -1
        self.dest_addr = -1
        self.dest_value = -1
        self.offset = -1
        self.id = -1
        self.src_addr = [-1, -1]
        self.src_ready = [False, False]
        self.src_value = [-1, -1]
        self.rdy2exe_cycle = -1

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
        self.tail = 0
        self.active_rs_num_queue=list()

    def print_config(self):
        print("adder config:")
        print("# of rs /", "Cycles in EX /", "Cycles in Mem /", "# of FUs /")
        print(self.config.name, self.config.rs_number, self.config.ex_cycles, self.config.mem_cycles, self.config.fu_number)

    def operation(self, current_cycle, operation, processor):
        # print(whoami())
        print(processor)
        rs = self.rs
        print("adder operation in cycle:", current_cycle)



        # print("processor cycle: ", current_cycle)
        if operation == EXEC:
            print("--------------",self.fu_index,"Adder EXEC Begin:-------------------")
            if self.busy == False:
                print(" Adder got:")
                # for i in range(len(self.config.rs_number)):
                # for i, rs in enumerate(rs):
                # Find an entry in my RS that all dependencies are ready for Execution

                for k in range(self.tail, self.tail+len(rs)):
                # rs.sort(key=lambda rs_entry:rs_entry.instruction_id)
                # for i in range(len(rs)):
                    i = k % len(rs)
                    print("rs[",i, "] is in use",rs[i].in_use)

                    if rs[i].in_use == True and rs[i].instruction_id != -1:


                        # for j in [0,1]:
                        #     if rs[i].src_ready[j] == False and rs[i].src_addr[j] > 63:
                        #         if processor.ROB[rs[i].src_addr[j]].idle == True:
                        #             rs[i].src_ready[j] = True
                        #             addr = processor.RAT[processor.ROB[rs[i].src_addr[j]].pointer]
                        #             rs[i].src_addr[j] = addr
                        #             print("addr is",addr)
                        #             if addr < 32:
                        #                 rs[i].src_value[j] = processor.ARF.reg_int[addr]
                                    # elif  addr >= 32 and addr < 64:
                                    #     rs[i].src_value[j] = processor.ARF.reg_float[addr % 32]

                        if rs[i].src_ready == [True, True] and current_cycle >= rs[i].rdy2exe_cycle:    # start an addition operation
                            # Add current cycle as the execution cycle of corresponding instruction
                            print("rs[", i, "] src_ready is", rs[i].src_ready, "instruction id is",
                                  rs[i].instruction_id)
                            print ("final table", processor.instruction_final_table[rs[i].instruction_id])
                            processor.instruction_final_table[rs[i].instruction_id][1] = current_cycle
                            print("inst index is", rs[i].instruction_index)
                            self.busy = True
                            print("     Adder occupied:", rs[i].instruction_type)
                            rs[i].src_ready = [False, False]
                            self.start_cycle = current_cycle
                            # print(self.config.ex_cycles)
                            self.finish_cycle = current_cycle + self.config.ex_cycles
                            print("queue add ", rs[i].index)
                            self.active_rs_num_queue.append(i)
                            # print("active_rs_num = ", self.active_rs_num)

                            j = (i+1) % len(rs)

                            if rs[j].in_use == True:
                                if rs[j].instruction_id > rs[0].instruction_id and rs[0].instruction_id >=0:
                                    self.tail = 0
                            else:
                                self.tail = i+1



                            if rs[i].instruction_type == 8 or rs[i].instruction_type == 3 or rs[
                                i].instruction_type == 4:
                                rs[i].dest_value = rs[i].src_value[0] - rs[i].src_value[1]
                            else:
                                rs[i].dest_value = rs[i].src_value[0] + rs[i].src_value[1]
                            self.wbing_cycle = self.finish_cycle


                            if processor.ifbranch(rs[i].instruction_index) == True:  ##########added for branch operation##############################################
                                if (rs[i].instruction_type == 3 and rs[i].dest_value == 0) or (
                                        rs[i].instruction_type == 4 and rs[i].dest_value != 0):  ####beq and bne
                                    predict = True
                                else:
                                    predict = False
                                print("predict =", predict)
                                print("branch rs[i].dest_value=", rs[i].dest_value, "rs[i].instruction_type=",
                                      rs[i].instruction_type)
                                processor.BTB_predict(rs[i].instruction_index,predict)  # predict iftaken and validate new BTB entry###################################
                                processor.BTB[rs[i].instruction_index % 8].empty = False

                                # if processor.BTB[rs[i].instruction_index % 8].empty == True:
                                #     processor.BTB[rs[i].instruction_index % 8].empty = False
                                #     processor.BTB[processor.inst_issue_index].issue_enable = True
                                #     processor.BTB_lookup(processor.inst_issue_index)  ##################determine the next instruction##################################
                            # if rs[i].instruction_type == 4 or rs[i].instruction_type == 3:
                            #     rs[i].clear()
                            #     self.wbing_cycle = 0
                                # processor.BTB[rs[i].instruction_index % 8].issue_enable = True

                            print("start cycle:", self.start_cycle)
                            print("finish cycle:", self.finish_cycle)

                            break
            print("--------------",self.fu_index,"Adder EXEC End:-------------------\n")
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
            print("\n-------------",self.fu_index,"Adder WB Begin:----------------")
            if self.busy == True:
                print(" Adder.busy:")
                if self.wbing_cycle == current_cycle:
                    print("     WB cycle:", current_cycle)
                    self.active_rs_num=self.active_rs_num_queue[0]
                    print("     active num:", self.active_rs_num)
                    # Successfully drop it to CDB
                    if processor.CDB.put_to_buffer(rs, self.active_rs_num, self.fu_index, current_cycle) == True:
                        self.active_rs_num_queue.pop(0)
                        self.busy = False
                        # release current RS entry after the WB task has been dropped to CDB
                        # self.rs[self.active_rs_num].in_use = False
                        print("fu index is ", self.fu_index,"active rs number is ",self.active_rs_num)
                        rs[self.active_rs_num].clear()
                        print("rs[", self.active_rs_num, "] released")
                        self.active_rs_num = -1
                    else:
                        print("Drop to CDB failed. FU is kept busy")
            print("-------------",self.fu_index,"Adder WB End:----------------\n")

class LSQ_Adder:
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
        self.wbing_queue=list()
        self.sd_commit_cycle = -1
        self.active_rs_num = -1
        self.start_cycle = -1
        self.finish_cycle = -1
        self.exe_stop_cycle = -1
        self.exe_stop_queue = list()
        self.mem_stop_cycle = 0
        self.fu_index = FU_index # to indicate the ID of this FU. For CDB use
        self.rs = rs
        self.tail = 0
        self.active_rs_num_queue=list()

    def print_config(self):
        print("adder config:")
        print("# of rs /", "Cycles in EX /", "Cycles in Mem /", "# of FUs /")
        print(self.config.name, self.config.rs_number, self.config.ex_cycles, self.config.mem_cycles, self.config.fu_number)

    def operation(self, current_cycle, operation, processor):
        # print(whoami())
        print(processor)
        rs = self.rs
        print("adder operation in cycle:", current_cycle)



        # print("processor cycle: ", current_cycle)
        if operation == EXEC:
            print("--------------",self.fu_index,"LSQ Adder EXEC Begin:-------------------")


            # if len(self.exe_stop_queue)> 0 and current_cycle == self.exe_stop_queue[0]:
            if current_cycle == self.exe_stop_cycle:
                print("exe stop cycle")
                self.busy = False
                # self.exe_stop_queue.pop(0)
            if self.busy == False:
                print("ld Adder got:")
                # for i in range(len(self.config.rs_number)):
                # for i, rs in enumerate(rs):
                # Find an entry in my RS that all dependencies are ready for Execution



                for k in range(self.tail, self.tail+len(rs)):
                # rs.sort(key=lambda rs_entry:rs_entry.instruction_id)
                # for i in range(len(rs)):
                    i = k % len(rs)
                    print("sd rs[",i, "] is in use",rs[i].dest_addr)

                    if rs[i].in_use == True and rs[i].instruction_id != -1:
                        print("rs[", i, "] exe cycle is", rs[i].rdy2exe_cycle)
                        print("rs[", i, "] src_ready is",rs[i].src_ready[1])

                        # for j in [0,1]:
                        #     if rs[i].src_ready[j] == False and rs[i].src_addr[j] > 63:
                        #         if processor.ROB[rs[i].src_addr[j]].idle == True:
                        #             rs[i].src_ready[j] = True
                        #             addr = processor.RAT[processor.ROB[rs[i].src_addr[j]].pointer]
                        #             rs[i].src_addr[j] = addr
                        #             print("addr is",addr)
                        #             if addr < 32:
                        #                 rs[i].src_value[j] = processor.ARF.reg_int[addr]
                                    # elif  addr >= 32 and addr < 64:
                                    #     rs[i].src_value[j] = processor.ARF.reg_float[addr % 32]

                        if rs[i].src_ready[1] == True and current_cycle >= rs[i].rdy2exe_cycle:    # start an addition operation
                            # Add current cycle as the execution cycle of corresponding instruction
                            # print ("final table", processor.instruction_final_table[rs[i].instruction_id])
                            processor.instruction_final_table[rs[i].instruction_id][1] = current_cycle
                            print("inst index is", rs[i].instruction_index)
                            self.busy = True
                            print("     Adder occupied:", rs[i].instruction_type)
                            rs[i].src_ready = [False, False]
                            self.start_cycle = current_cycle
                            # print(self.config.ex_cycles)
                            self.finish_cycle = current_cycle + self.config.ex_cycles
                            print("queue add ", rs[i].index)
                            self.active_rs_num_queue.append(i)
                            # print("active_rs_num = ", self.active_rs_num)

                            # j = (i+1) % len(rs)
                            # if rs[j].in_use == True:
                            #     if rs[j].instruction_id > rs[0].instruction_id and rs[0].instruction_id >=0:
                            #         self.tail = 0
                            # else:
                            #     self.tail = i+1

                            rs[i].addr=rs[i].src_value[1]+rs[i].offset
                            flag = False
                            # Ld
                            if rs[i].instruction_type == 1:

                                for k in range(len(rs)):
                                    if rs[k].addr == rs[i].addr and i!=k:
                                        flag = True
                                        break

                                # The value can be found in LSQ
                                if flag == True and rs[k].instruction_type == 2:
                                    rs[i].value = rs[k].value
                                    rs[i].dest_value = rs[k].value
                                    processor.instruction_final_table[rs[i].instruction_id][2]=self.finish_cycle

                                    self.exe_stop_cycle = self.finish_cycle+1

                                    self.wbing_cycle = self.finish_cycle+1

                                # Cannot be found in LSQ
                                else:

                                    print("rs addr for ", rs[i].addr)
                                    print("mem value for ",processor.MEM[rs[i].addr])

                                    rs[i].value = processor.MEM[rs[i].addr]
                                    rs[i].dest_value = rs[i].value

                                    mem_next_start_cycle = self.finish_cycle+ self.config.mem_cycles-1

                                    if mem_next_start_cycle > self.mem_stop_cycle+self.config.mem_cycles-1:

                                        processor.instruction_final_table[rs[i].instruction_id][2] = mem_next_start_cycle
                                        self.mem_stop_cycle=mem_next_start_cycle

                                    else:
                                        processor.instruction_final_table[rs[i].instruction_id][2] = self.mem_stop_cycle+self.config.mem_cycles
                                        self.mem_stop_cycle = self.mem_stop_cycle+self.config.mem_cycles
                                        # self.wbing_cycle = self.finish_cycle + self.config.mem_cycles


                                    self.exe_stop_cycle = self.finish_cycle+1
                                # rs[i].dest_value = rs[i].src_value[0] - rs[i].src_value[1]

                                    self.wbing_cycle = self.mem_stop_cycle + 1
                                self.wbing_queue.append(self.wbing_cycle)
                                self.exe_stop_queue.append(self.exe_stop_cycle)
                            # Sd
                            elif rs[i].instruction_type == 2:

                                rs[i].value = rs[i].src_value[0]
                                # rs[i].addr =
                                print("sd in rs[", i, "] addr ", rs[i].addr)
                                # processor.MEM[rs[i].addr] = rs[i].value




                                # rs[i].dest_value = rs[i].src_value[0] + rs[i].src_value[1]
                                self.sd_commit_cycle = current_cycle
                            # if rs[i].instruction_type == 4 or rs[i].instruction_type == 3:
                            #     rs[i].clear()
                            #     self.wbing_cycle = 0
                                # processor.BTB[rs[i].instruction_index % 8].issue_enable = True
                            # self.busy = False
                            print("start cycle:", self.start_cycle)
                            print("finish cycle:", self.finish_cycle)

                            break
            print("--------------",self.fu_index,"Adder EXEC End:-------------------\n")
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
            print("\n-------------",self.fu_index,"LSQ Adder WB Begin:----------------")
            # if self.busy == True:
            if True:
                print(" Adder.busy:")

                if self.sd_commit_cycle == current_cycle:
                    self.active_rs_num = self.active_rs_num_queue.pop()

                    # self.busy = False
                    # release current RS entry after the WB task has been dropped to CDB
                    # self.rs[self.active_rs_num].in_use = False
                    print("sd fu index is ", self.fu_index, "active rs number is ", self.active_rs_num)

                    print("sd rs[", self.active_rs_num, "] released")
                    # self.active_rs_num = -1

                    print("sd rob num", rs[self.active_rs_num].dest_addr, "] released")

                    processor.ROB[rs[self.active_rs_num].dest_addr-64].value_ready = True
                    processor.ROB[rs[self.active_rs_num].dest_addr-64].value_rdy2commit_cycle = current_cycle + 1
                    processor.ROB[rs[self.active_rs_num].dest_addr-64].if_sd = True
                    processor.ROB[rs[self.active_rs_num].dest_addr-64].sd_fu_index = self.fu_index-(processor.config.adder.fu_number+processor.config.fpadder.fu_number+processor.config.fpmul.fu_number)
                    processor.ROB[rs[self.active_rs_num].dest_addr - 64].sd_rs_index = self.active_rs_num



                if len(self.wbing_queue) > 0:
                    if self.wbing_queue[0] == current_cycle:
                        print("     WB cycle:", current_cycle)
                        self.active_rs_num=self.active_rs_num_queue[0]
                        print("     active num:", self.active_rs_num)
                        # Successfully drop it to CDB
                        if processor.CDB.put_to_buffer(rs, self.active_rs_num, self.fu_index, current_cycle) == True:
                            self.wbing_queue.pop(0)
                            self.active_rs_num_queue.pop(0)
                            self.busy = False
                            # release current RS entry after the WB task has been dropped to CDB
                            # self.rs[self.active_rs_num].in_use = False
                            print("fu index is ", self.fu_index,"active rs number is ",self.active_rs_num)
                            rs[self.active_rs_num].clear()
                            print("ld rs[", self.active_rs_num, "] released")
                            self.active_rs_num = -1
                        else:
                            print("Drop to CDB failed. FU is kept busy")
            print("-------------",self.fu_index,"LSQ Adder WB End:----------------\n")

class Queue:
    def __init__(self):
        self.queue = list()

    def addtoq(self,dataval):
    # Insert method to add element
        if dataval not in self.queue:
            self.queue.insert(0,dataval)
            return True
        return False

    def addbottom(self,dataval):
    # Insert method to add element
        if dataval not in self.queue:
            self.queue.append(dataval)
            return True
        return False

    # Pop method to remove element
    def removefromq(self):
        if len(self.queue)>0:
            return self.queue.pop(0)

        return ("No elements in Queue!")

    def currentsize(self):
        return len(self.queue)

    # Only query, not dequeue
    def queryfirstelement(self):
        if self.currentsize() > 0:
            return self.queue[0]


class FUPipeLineInfo:
    wbing_cycle = -1
    active_rs_num = -1
    start_cycle = -1
    finish_cycle = -1

class PipelinedFU:
    # adder_rs_number = 0

    def __init__(self, adder_config, FU_index, rs, function):
        print("instantiate Pipielined FU")
        self.config = adder_config
        # self.rs = [ReservationStation() for i in range(self.config.rs_number)]
        # for i in range(0, 3):
        # for i, rs in enumerate(self.rs):
        #     self.rs.index = i
        # print("rs number", rs.__len__())
        # self.busy = False

        self.fu_index = FU_index # to indicate the ID of this FU. For CDB use
        self.rs = rs
        self.exeQueue = Queue()
        self.function = function       # 1 for sum, 2 for mul
        self.active_rs_num_queue=list()
        self.tail = 0

    def print_config(self):
        print("Pipielined FU config:")
        print("# of rs /", "Cycles in EX /", "Cycles in Mem /", "# of FUs /")
        print(self.config.name, self.config.rs_number, self.config.ex_cycles, self.config.mem_cycles, self.config.fu_number)

    def operation(self, current_cycle, operation, processor):
        # print(whoami())
        print(processor)
        rs = self.rs
        print("Pipielined FU operation in cycle:", current_cycle)

        # print("processor cycle: ", current_cycle)
        if operation == EXEC:
            print("--------------",self.fu_index,"Pipielined FU EXEC Begin:-------------------")
            if True:        # Alway not busy
                print(" Pipelined FU got:")
                # for i in range(len(self.config.rs_number)):
                # for i, rs in enumerate(rs):
                # Find an entry in my RS that all dependencies are ready for Execution
                for k in range(self.tail, self.tail + len(rs)):
                    i = k % len(rs)
                    print("rs[",i, "] is in use",rs[i].in_use)
                    if rs[i].in_use == True:

                        # for j in [0,1]:
                        #     if rs[i].src_ready[j] == False and rs[i].src_addr[j] > 63:
                        #         if processor.ROB[rs[i].src_addr[j]].idle == True:
                        #             rs[i].src_ready[j] = True
                        #             addr = processor.RAT[processor.ROB[rs[i].src_addr[j]].pointer]
                        #             rs[i].src_addr[j] = addr
                        #             print("addr is",addr)
                        #             if addr < 32:
                        #                 rs[i].src_value[j] = processor.ARF.reg_int[addr]
                        #             if  addr >= 32 and addr < 64:
                        #                 rs[i].src_value[j] = processor.ARF.reg_float[addr - 32]

                        if rs[i].src_ready == [True, True] and current_cycle >= rs[i].rdy2exe_cycle:    # start an addition operation
                            # Add current cycle as the execution cycle of corresponding instruction
                            processor.instruction_final_table[rs[i].instruction_id][1] = current_cycle

                            # self.busy = True
                            print("     Adder occupied:", rs[i].instruction_type)

                            pipelineinfo = FUPipeLineInfo()
                            rs[i].src_ready = [False, False]
                            pipelineinfo.start_cycle = current_cycle
                            # print(self.config.ex_cycles)
                            pipelineinfo.finish_cycle = current_cycle + self.config.ex_cycles
                            # pipelineinfo.active_rs_num = rs[i].index
                            self.active_rs_num_queue.append(i)
                            # print("active_rs_num = ", pipelineinfo.active_rs_num)

                            self.tail = i + 1

                            if self.function == 1:          # Add
                                if rs[i].instruction_type == 9:
                                    rs[i].dest_value = rs[i].src_value[0] - rs[i].src_value[1]
                                else:
                                    rs[i].dest_value = rs[i].src_value[0] + rs[i].src_value[1]
                            elif self.function == 2:        # Multiply
                                rs[i].dest_value = rs[i].src_value[0] * rs[i].src_value[1]
                            pipelineinfo.wbing_cycle = pipelineinfo.finish_cycle
                            print("FU EXE wbing cycle is", pipelineinfo.wbing_cycle)
                            print("start cycle:", pipelineinfo.start_cycle)
                            print("finish cycle:", pipelineinfo.finish_cycle)

                            # ENQUEUE
                            self.exeQueue.addbottom(pipelineinfo)
                            print("Operate self.exeQueue.currentsize()", self.exeQueue.currentsize())
                            break

            print("--------------",self.fu_index,"Pipielined FU EXEC End:-------------------\n")
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
            print("\n-------------",self.fu_index,"Pipielined FU WB Begin:----------------")
            print("WB self.exeQueue.currentsize()", self.exeQueue.currentsize())
            if self.exeQueue.currentsize() > 0:
                print ("FU wbing cyle is ", self.exeQueue.queryfirstelement().wbing_cycle)
                if self.exeQueue.queryfirstelement().wbing_cycle == current_cycle:
                    print("     FU WB cycle:", current_cycle)



                    currentExe = self.exeQueue.queryfirstelement()

                    currentExe.active_rs_num = self.active_rs_num_queue[0]
                    # print("     active num:", self.active_rs_num)


                    # Successfully drop it to CDB
                    if processor.CDB.put_to_buffer(rs, currentExe.active_rs_num, self.fu_index, current_cycle) == True:
                        self.active_rs_num_queue.pop(0)
                        self.busy = False
                        # release current RS entry after the WB task has been dropped to CDB
                        # self.rs[self.active_rs_num].in_use = False
                        rs[currentExe.active_rs_num].clear()
                        print("rs[", currentExe.active_rs_num, "] released")
                        # self.active_rs_num = -1

                        # remove this execution in FU, as it has been write back
                        self.exeQueue.removefromq()
                    else:
                        print("Drop to CDB failed. FU is kept busy")
            print("-------------", self.fu_index, "Pipielined FU WB End:----------------\n")


class buffer_entry:
    inst_id = -1        # Issue sequence of Inst
    inst_type = -1
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

    def put_to_buffer(self, rs, active_rs_number, fu_index, cycle):
        print("put_to_buffer")

        temp = buffer_entry()

#        temp.inst_id = rs.instruction_id        # the Issue sequence
        temp.inst_wb_cycle = cycle
        temp.inst_id = rs[active_rs_number].instruction_id         # the unique ID of each Issed instruction
        temp.dest_addr = rs[active_rs_number].dest_addr
        temp.dest_value = rs[active_rs_number].dest_value
        temp.inst_type = rs[active_rs_number].instruction_type
        temp.fu_index = fu_index
        temp.rs = rs                             # Get the whole RS table of the FU
        temp.active_rs_number = active_rs_number
        print("fu index is", fu_index)
        if self.buffer[fu_index].entries.currentsize() < self.buffer[fu_index].maxSize:
            self.buffer[fu_index].entries.addbottom(temp)
            print("inst id is",rs[active_rs_number].instruction_id,"fu_index is", fu_index)
            return True
        else:
            return False    # The CDB buffer is full. The FU should stall (if not-pipelined)

    # need to be called after WB of all the FUs
    def arbiter(self, processor):
        buffer = deepcopy(self.buffer)
        temp = []
        # copy the first element in each FU buffer together to select

        for i in range(len(buffer)):
            # print("loop buffer length is ", buffer[i].entries.currentsize())
            # print("loop self buffer length is ", self.buffer[i].entries.currentsize())
            if buffer[i].entries.currentsize() != 0:
                temp.append(buffer[i].entries.removefromq())

        # print("length of temp is",len(temp))
        # print("before buffer length is ", self.buffer[1].entries.currentsize())
        if len(temp) > 0:
            temp.sort(key=lambda buffer_entry: buffer_entry.inst_wb_cycle)

            # only keep earliest ones
            for i in range(len(temp)):
                if temp[i].inst_wb_cycle != temp[0].inst_wb_cycle:
                    print("prepare to remove")
                    temp.remove(temp[i])

            # sort again by inst_id
            temp.sort(key=lambda buffer_entry: buffer_entry.inst_id)
            # winner is temp(0) now. It is the header of the queue for that FU.
            # The dequeued element is the type of buffer_entry()
            print("fu_index is", temp[0].fu_index)

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
            print("processor.ROB[rob_entry].instruction_index is",processor.ROB[rob_entry].instruction_index)
            if temp[0].inst_type == 3 or temp[0].inst_type == 4:
                processor.instruction_final_table[processor.ROB[rob_entry].instruction_ID][3]= -1
                processor.ROB[rob_entry].value_rdy2commit_cycle = current_cycle
            else:
                print("ID", processor.ROB[rob_entry].instruction_ID)
                processor.instruction_final_table[processor.ROB[rob_entry].instruction_ID][3] = current_cycle
                processor.ROB[rob_entry].value_rdy2commit_cycle = current_cycle + 1

            print("ROB", rob_entry, "updated to:", processor.ROB[rob_entry].reg_value,
                  "register number is ",processor.ROB[rob_entry].reg_number,
            processor.ROB[rob_entry].value_ready,
            processor.ROB[rob_entry].value_rdy2commit_cycle)

            # update all the rs that pending this value
            # for i, rs in enumerate(rs):
            # for j in range(len(processor.RS_Integer_Adder))
            # if rs[0].id == 1:
            #     rs = processor.RS_Integer_Adder
            # elif rs[0].id == 2:
            #     rs = processor.RS_Float_Adder
            # elif rs[0].id == 3:
            #     rs = processor.RS_Float_Mul
            # else:
            #     rs = processor.RS_LSQ

            # TODO: still need further update on different rs
            list = [processor.RS_Integer_Adder, processor.RS_Float_Adder, processor.RS_Float_Mul, processor.RS_LSQ]
            for rs in list:
                for k in range(len(rs)):
                    for i in range(len(rs[k])):
                        if rs[k][i].in_use == True:
                            for j in [0, 1]:
                                if rs[k][i].src_ready[j] == False:
                                    print("         update RS_Integer_Adder entry: i is", i, "j is", j)
                                    print("         temp dest address is ",temp[0].dest_addr)
                                    print("         ",rs[k][i].src_addr[j], temp[0].dest_addr)
                                    if rs[k][i].src_addr[j] == temp[0].dest_addr:
                                        rs[k][i].src_ready[j] = True
                                        rs[k][i].src_addr[j] = -1
                                        rs[k][i].src_value[j] = temp[0].dest_value
                                        print("             updated RS entry:",k, i, j)



class ARF:
    def __init__(self, int_val, float_val):
        self.reg_int = array.array('i') # unsigned long
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
        self.instruction_ID = -1
        self.if_sd = False
        self.if_sd_counter = 0
        self.sd_fu_index = -1
        self.sd_rs_index = -1
        self.pointer = -1

    def clear(self):
        self.idle = True
        self.reg_number = -1
        self.reg_value = -1
        self.value_ready = False
        self.value_rdy2commit_cycle = -1

# class Issue:
#     def __init__(self, processor):
class BTB:
    def __init__(self):
        self.next_PC=0
        self.iftaken=True
        self.empty=True
        self.issue_enable=True
        print("BTB: ", self.next_PC)

class Processor(object):
    def __init__(self, num_rob, num_cdb, reg_int, reg_float, mem_val, num_inst, inst_list):
        # TODO: process CDB

        # declare an final instruction table for every inst
        # Issue, Exec, Mem, WB, Commit
        # self.instruction_final_table = [[-1 for j in range(5)] for i in range(num_inst)]
        self.instruction_final_table = []
        self.cycle = 1  # current cycle

        self.BTB = [BTB() for i in range(8)] #    ************************* create BTB  ***************************************
        self.ROB = [ROB() for i in range(num_rob)]  # set 1000 ROB entries
        print(self.ROB.__len__())
        self.ROB_head = 0
        self.ROB_tail = 0
        self.ROB_num = num_rob

        self.INDEX_LSQ = 0
        self.INDEX_INT_ADDER = 0
        self.INDEX_FLOAT_ADDER = 0
        self.INDEX_FLOAT_MUL = 0

        self.ARF = ARF(reg_int, reg_float)
        self.RAT = array.array('i')  # unsigned int
        for i in range(64):
            self.RAT.append(i)
        # self.RAT.append(1)
        # print(self.RAT[0])
        # print(self.RAT.__len__())
        self.MEM = mem_val
        self.rs_entry_copy = 0

        # read processor configuration
        self.config = ProcessorConfig()
        self.config.read_config()
        self.config.print_config()
        print("mem is",self.MEM)
        # for j in range(self.config.ldst.rs_number):
            # LSQ_list =
        self.RS_LSQ = [[LSQ() for i in range(self.config.ldst.rs_number)] for i in range(self.config.ldst.fu_number)]
        for i in range(self.config.ldst.fu_number):
            # self.RS_LSQ[i].tail = 0
            for j in range(self.config.ldst.rs_number):
                self.RS_LSQ[i][j].index = j
                self.RS_LSQ[i][j].id = 4

        # for j in range(self.config.adder.fu_number):
            # int_adder_list =
        self.RS_Integer_Adder = [[ReservationStation() for i in range(self.config.adder.rs_number)] for i in range(self.config.adder.fu_number)]
        for i in range(self.config.adder.fu_number):
            for j in range(self.config.adder.rs_number):
                self.RS_Integer_Adder[i][j].index = j
                self.RS_Integer_Adder[i][j].id = 1

        # for j in range(self.config.fpadder.fu_number):
            # float_adder_list =
        self.RS_Float_Adder = [[ReservationStation() for i in range(self.config.fpadder.rs_number)] for i in range(self.config.fpadder.fu_number)]
        for i in range(self.config.fpadder.fu_number):
            for j in range(self.config.fpadder.rs_number):
                self.RS_Float_Adder[i][j].index = j
                self.RS_Float_Adder[i][j].id = 2

        # for j in range(self.config.fpadder.fu_number):
            # float_mul_list =
        self.RS_Float_Mul = [[ReservationStation() for i in range(self.config.fpmul.rs_number)] for i in range(self.config.fpmul.fu_number)]
        for i in range(self.config.fpmul.fu_number):
            for j in range(self.config.fpmul.rs_number):
                self.RS_Float_Mul[i][j].index = j
                self.RS_Float_Mul[i][j].id = 3


        # init adder
        print("----------------------------------------")

        # print(self.RS_Integer_Adder)
        # self.adder = Adder(self.config.adder)

        # print("RS integer adder", self.RS_Integer_Adder)

        self.Integer_Adder = [Adder(self.config.adder, i, self.RS_Integer_Adder[i]) for i in range(self.config.adder.fu_number)]
        self.FP_Adder = [PipelinedFU(self.config.fpadder, j, self.RS_Float_Adder[j-self.config.adder.fu_number], 1) for j in range(self.config.adder.fu_number,self.config.adder.fu_number+self.config.fpadder.fu_number)]
        self.FP_Mul = [PipelinedFU(self.config.fpmul, k, self.RS_Float_Mul[k-self.config.adder.fu_number-self.config.fpadder.fu_number], 2) for k in range(self.config.adder.fu_number+self.config.fpadder.fu_number, self.config.adder.fu_number+self.config.fpadder.fu_number+self.config.fpmul.fu_number)]
        self.LSQ_Integer_Adder = [LSQ_Adder(self.config.ldst, g, self.RS_LSQ[g-(self.config.adder.fu_number+self.config.fpadder.fu_number+self.config.fpmul.fu_number)]) for g in range(self.config.adder.fu_number+self.config.fpadder.fu_number+self.config.fpmul.fu_number,self.config.adder.fu_number+self.config.fpadder.fu_number+self.config.fpmul.fu_number+self.config.ldst.fu_number)]
        # self.adder.print_config()
        # self.adder.operation(self.cycle)

        self.inst_num = num_inst
        # print("proc inst num: ", self.inst_num)s
        self.inst_list = inst_list
        self.inst_issue_index = 0
        # Instruction unique ID
        self.inst_ID_last = 0

        # TODO: number of FUs, each buffer size
        self.CDB = CDB(self.config.adder.fu_number+self.config.fpadder.fu_number+self.config.fpmul.fu_number+self.config.ldst.fu_number, 1)

        # TheQueue = Queue()
        # TheQueue.addtoq(self.CDB)
        # print(TheQueue.removefromq())

    def clock(self):
        self.cycle += 1
        print("cycle changing to: ", self.cycle)


    def ifbranch(self, index):
        if self.inst_list[index].inst==3 or self.inst_list[index].inst==4: # only works on beq and bne
            return True
        else:
            return False

    def BTB_add_entry(self, index, offset):
        id=index%8
        self.BTB[id].next_PC=index+1+offset#****************need current PC*******************************

    def BTB_lookup(self, index):        #   ************************************ index from PC need to calculated beforehand***********************************
        id=index%8
        if self.BTB[id].iftaken==True:
            self.inst_issue_index=self.BTB[id].next_PC#****************need to pass the predicted PC to the next instruction**********
        else:
            self.inst_issue_index+=1

    def BTB_predict(self,index,predict_Correct):#***************need input of prediction_correctness*****************#
        id=index%8
        self.BTB[id].empty=False
        self.BTB[id].iftaken=predict_Correct
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
    # def execs(self):
    #     self.Integer_Adder.operation(self.cycle, EXEC, self)

    def issue(self):
        print("\ninst list not empty")
        if self.inst_issue_index <= self.inst_num - 1:
            print("current Inst type=", self.inst_list[self.inst_issue_index].inst)
            print("current parsed instruction=", self.inst_issue_index, "current Issued Instruction=",
                  self.inst_ID_last)
            if self.ifbranch(self.inst_issue_index) == True:  # determine if it is a branch instruction#############################
                # rollback_Buffer()
                if self.BTB[self.inst_issue_index].empty == True:  # find out if BTB entry is empty##################################################
                    self.BTB_add_entry(self.inst_issue_index, self.inst_list[self.inst_issue_index].offset)  # add entry#############################
                if self.issue_one_inst(self.inst_list[self.inst_issue_index]) == 0:
                    self.BTB_lookup(self.inst_issue_index)  ##################determine the next instruction##################################
                    # print("Issue Inst", self.inst_issue_index, self.inst_list[self.inst_issue_index].str, "succeed")
                else:
                    print("wait for the new BTB entry to be ready after EXE")
                    # self.inst_ID_last = self.inst_ID_last + 1 ###############making the issued ID and parsed ID consistant
                    # print("BTB_next_pc=",self.BTB[self.inst_issue_index].next_PC, "next_Instruction=",self.inst_issue_index, "next_issued_instr=",self.inst_ID_last)
            else:
                if self.issue_one_inst(self.inst_list[self.inst_issue_index]) == 0:
                    print("Issue Inst", self.inst_issue_index, self.inst_list[self.inst_issue_index].str, "succeed")
                    self.inst_issue_index += 1  # need stall function  solved
                else:
                    print("Issue Inst", self.inst_issue_index, "failed")

    def issue_1(self):
        print("\ninst list not empty")
        if self.inst_issue_index <= self.inst_num - 1:
            print("current Inst type=", self.inst_list[self.inst_issue_index].inst)
            print("current parsed instruction=", self.inst_issue_index, "current Issued Instruction=",self.inst_ID_last)
            if self.ifbranch(self.inst_issue_index) == True:  # determine if it is a branch instruction#############################
                if self.BTB[self.inst_issue_index].empty == True:  # find out if BTB entry is empty##################################################
                    if self.BTB[self.inst_issue_index].issue_enable == True:  ########## prevent further redundant issue ###########
                        if self.issue_one_inst(self.inst_list[self.inst_issue_index]) == 0:
                            self.BTB[self.inst_issue_index].issue_enable = False  ########## prevent further redundant issue ###########
                            self.BTB_add_entry(self.inst_issue_index, self.inst_list[self.inst_issue_index].offset)  # add entry#############################
                            print("Issue Inst", self.inst_issue_index, self.inst_list[self.inst_issue_index].str,
                                  "succeed")
                        else:
                            print("wait for the new BTB entry to be ready after EXE")
                else:
                    if self.BTB[self.inst_issue_index].issue_enable == True:  ########## prevent further redundant issue ###########
                        if self.issue_one_inst(self.inst_list[self.inst_issue_index]) == 0:
                            self.BTB_lookup(self.inst_issue_index)  ##################determine the next instruction##################################
                            print("Issue Inst", self.inst_issue_index, self.inst_list[self.inst_issue_index].str,"succeed")
                        else:
                            print("wait for the new BTB entry to be ready after EXE")
                    else:
                        self.BTB[self.inst_issue_index].issue_enable = True
                        self.BTB_lookup(self.inst_issue_index)  ##################determine the next instruction##################################
                    # self.inst_ID_last = self.inst_ID_last + 1 ###############making the issued ID and parsed ID consistant
                    # print("BTB_next_pc=",self.BTB[self.inst_issue_index].next_PC, "next_Instruction=",self.inst_issue_index, "next_issued_instr=",self.inst_ID_last)
            else:
                if self.issue_one_inst(self.inst_list[self.inst_issue_index]) == 0:
                    print("Issue Inst", self.inst_issue_index, self.inst_list[self.inst_issue_index].str, "succeed")
                    self.inst_issue_index += 1  # need stall function  solved
                else:
                    print("Issue Inst", self.inst_issue_index, "failed")

    def back_2_issue(self):
        print("\ninst list not empty")
        if self.inst_issue_index <= self.inst_num - 1:
            print("current Inst type=", self.inst_list[self.inst_issue_index].inst)
            print("current parsed instruction=", self.inst_issue_index, "current Issued Instruction=",
                  self.inst_ID_last)
            if self.ifbranch(
                    self.inst_issue_index) == True:  # determine if it is a branch instruction#############################
                if self.BTB[
                    self.inst_issue_index].empty == True:  # find out if BTB entry is empty##################################################
                    if self.BTB[
                        self.inst_issue_index].issue_enable == True:  ########## prevent further redundant issue ###########
                        if self.issue_one_inst(self.inst_list[self.inst_issue_index]) == 0:
                            print("fist branch issue succeed")
                            self.BTB[
                                self.inst_issue_index].issue_enable = False  ########## prevent further redundant issue ###########
                            self.BTB_add_entry(self.inst_issue_index, self.inst_list[
                                self.inst_issue_index].offset)  # add entry#############################
                            print("Issue Inst", self.inst_issue_index, self.inst_list[self.inst_issue_index].str,
                                  "succeed")
                        else:
                            print("wait for the new BTB entry to be ready after EXE")
                else:
                    if self.issue_one_inst(self.inst_list[self.inst_issue_index]) == 0:
                        self.BTB[self.inst_issue_index].issue_enable = True
                        self.BTB_lookup(
                            self.inst_issue_index)  ##################determine the next instruction##################################
                        print("Issue Inst", self.inst_issue_index, self.inst_list[self.inst_issue_index].str, "succeed")
                    else:
                        print("wait for the new BTB entry to be ready after EXE")
                    # self.inst_ID_last = self.inst_ID_last + 1 ###############making the issued ID and parsed ID consistant
                    # print("BTB_next_pc=",self.BTB[self.inst_issue_index].next_PC, "next_Instruction=",self.inst_issue_index, "next_issued_instr=",self.inst_ID_last)
            else:
                if self.issue_one_inst(self.inst_list[self.inst_issue_index]) == 0:
                    print("Issue Inst", self.inst_issue_index, self.inst_list[self.inst_issue_index].str, "succeed")
                    self.inst_issue_index += 1  # need stall function  solved
                else:
                    print("Issue Inst", self.inst_issue_index, "failed")

    def back_issue(self):
        print("\ninst list not empty")
        if self.inst_issue_index <= self.inst_num - 1:
            print("current Inst type=", self.inst_list[self.inst_issue_index].inst)
            print("current parsed instruction=", self.inst_issue_index, "current Issued Instruction=",
                  self.inst_ID_last)
            if self.ifbranch(
                    self.inst_issue_index) == True:  # determine if it is a branch instruction#############################
                if self.BTB[
                    self.inst_issue_index].empty == True:  # find out if BTB entry is empty##################################################
                    if self.BTB[
                        self.inst_issue_index].issue_enable == True:  ########## prevent further redundant issue ###########
                        if self.issue_one_inst(self.inst_list[self.inst_issue_index]) == 0:
                            print("fist branch issue succeed")
                            self.BTB[
                                self.inst_issue_index].issue_enable = False  ########## prevent further redundant issue ###########
                            self.BTB_add_entry(self.inst_issue_index, self.inst_list[
                                self.inst_issue_index].offset)  # add entry#############################
                            print("Issue Inst", self.inst_issue_index, self.inst_list[self.inst_issue_index].str,
                                  "succeed")
                        else:
                            print("wait for the new BTB entry to be ready after EXE")
                else:
                    if self.BTB[
                        self.inst_issue_index].issue_enable == True:  ########## prevent further redundant issue ###########
                        if self.issue_one_inst(self.inst_list[self.inst_issue_index]) == 0:
                            self.BTB_lookup(
                                self.inst_issue_index)  ##################determine the next instruction##################################
                            print("Issue Inst", self.inst_issue_index, self.inst_list[self.inst_issue_index].str,
                                  "succeed")
                        else:
                            print("wait for the new BTB entry to be ready after EXE")
                    # self.inst_ID_last = self.inst_ID_last + 1 ###############making the issued ID and parsed ID consistant
                    # print("BTB_next_pc=",self.BTB[self.inst_issue_index].next_PC, "next_Instruction=",self.inst_issue_index, "next_issued_instr=",self.inst_ID_last)
            else:
                if self.issue_one_inst(self.inst_list[self.inst_issue_index]) == 0:
                    print("Issue Inst", self.inst_issue_index, self.inst_list[self.inst_issue_index].str, "succeed")
                    self.inst_issue_index += 1  # need stall function  solved
                else:
                    print("Issue Inst", self.inst_issue_index, "failed")

    def issue_new(self):
        print("\ninst list not empty")
        if self.inst_issue_index <= self.inst_num - 1:
            print("current Inst type=", self.inst_list[self.inst_issue_index].inst)
            print("current parsed instruction=", self.inst_issue_index, "current Issued Instruction=",
                  self.inst_ID_last)
            if self.ifbranch(
                    self.inst_issue_index) == True:  # determine if it is a branch instruction#############################
                if self.BTB[
                    self.inst_issue_index].empty == True:  # find out if BTB entry is empty##################################################
                    if self.BTB[
                        self.inst_issue_index].issue_enable == True:  ########## prevent further redundant issue ###########
                        if self.issue_one_inst(self.inst_list[self.inst_issue_index]) == 0:
                            print("fist branch issue succeed")
                            self.BTB[
                                self.inst_issue_index].issue_enable = False  ########## prevent further redundant issue ###########
                            self.BTB_add_entry(self.inst_issue_index, self.inst_list[
                                self.inst_issue_index].offset)  # add entry#############################
                            print("Issue Inst", self.inst_issue_index, self.inst_list[self.inst_issue_index].str,
                                  "succeed")
                        else:
                            print("wait for the new BTB entry to be ready after EXE")
                else:
                    if self.BTB[
                        self.inst_issue_index].issue_enable == True:  ########## prevent further redundant issue ###########
                        if self.issue_one_inst(self.inst_list[self.inst_issue_index]) == 0:
                            self.BTB_lookup(
                                self.inst_issue_index)  ##################determine the next instruction##################################
                            print("Issue Inst", self.inst_issue_index, self.inst_list[self.inst_issue_index].str,
                                  "succeed")
                        else:
                            print("wait for the new BTB entry to be ready after EXE")
                    else:
                        self.BTB[self.inst_issue_index].issue_enable = True
                        if self.issue_one_inst(self.inst_list[self.inst_issue_index]) == 0:
                            self.BTB_lookup(
                                self.inst_issue_index)  ##################determine the next instruction##################################
                    # self.inst_ID_last = self.inst_ID_last + 1 ###############making the issued ID and parsed ID consistant
                    # print("BTB_next_pc=",self.BTB[self.inst_issue_index].next_PC, "next_Instruction=",self.inst_issue_index, "next_issued_instr=",self.inst_ID_last)
            else:
                if self.issue_one_inst(self.inst_list[self.inst_issue_index]) == 0:
                    print("Issue Inst", self.inst_issue_index, self.inst_list[self.inst_issue_index].str, "succeed")
                    self.inst_issue_index += 1  # need stall function  solved
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
        ID = 0

        # Load/Store inst


        # 2.1 Check if the ROB has empty entry.
        # If no, return -1
        # If yes, go on to check RS
        for i in range(self.ROB_head, self.ROB_head + self.ROB_num):
            rob_entry_no = i % self.ROB_num
            print("check ROB entry:", rob_entry_no)
            if self.ROB[rob_entry_no].idle == True:
                # only update ROB header when RS is also available
                # self.ROB_header = (self.ROB_header+1) % self.ROB_num
                ROB_no = rob_entry_no
                flag = True
                break

        print("ROB head index is ", self.ROB_head)
        if flag == False:
            return -1


        print("inst index is", inst.inst)

        # BEN and BEQ
        # TODO offset should be added
        # Ld and Sd
        if inst.inst == 1 or inst.inst == 2:
            flag = False
            print("RS LSQ number is", len(self.RS_LSQ))

            for x in range(self.INDEX_LSQ, self.INDEX_LSQ + len(self.RS_LSQ)):
                j = x % (len(self.RS_LSQ))
                print("input j is", j)

                for i in range(0, len(self.RS_LSQ[j])):
                    print("self.RS_LSQ_Adder[", j, "][", i, "].in_use is", self.RS_LSQ[j][i].in_use)
                    if self.RS_LSQ[j][i].in_use == False:

                        RS_no = i

                        # Unique ID for each instruction. For CDB arbiter, the inst with smaller ID is first served
                        inst.ID = self.inst_ID_last
                        self.inst_ID_last = self.inst_ID_last + 1

                        # 2.1 Update ROB
                        if inst.inst == 1:
                            self.ROB[rob_entry_no].reg_number = inst.F+32



                        self.ROB[rob_entry_no].idle = False
                        self.ROB[rob_entry_no].instruction_index = inst.index
                        self.ROB[rob_entry_no].instruction_ID = inst.ID

                        # 2.2 Update RAT
                        # RAT with dest 0-63 points to ARF
                        # RAT with dest >= 64 ... points to ROB
                        # self.RAT[inst.dest] = 64 + ROB_no

                        # 2.3 Update RS
                        self.RS_LSQ[j][i].in_use = True
                        self.RS_LSQ[j][i].instruction_type = inst.inst

                        # if inst.inst == 1:

                        self.RS_LSQ[j][i].dest_addr = ROB_no + 64
                        self.RS_LSQ[j][i].dest_value = -1

                        print("load store", self.RS_LSQ[j][i].dest_addr)

                        self.RS_LSQ[j][i].offset = inst.offset
                        self.RS_LSQ[j][i].instruction_index = inst.index
                        self.RS_LSQ[j][i].instruction_id = inst.ID

                        src_F = self.RAT[inst.F+32]
                        print("src_0 is", src_F)

                        src_R = self.RAT[inst.R]

                        # if src_R >=64:
                        #     if self.ROB[src_R-64].value_ready == True:
                        #         src_R = self.ROB[src_R-64].reg_number

                        print("src_1 is", src_R)

                        self.RS_LSQ[j][i].src_addr = [src_F, src_R]
                        self.RS_LSQ[j][i].start_cycle = -1
                        self.RS_LSQ[j][i].finish_cycle = -1

                        # If both source is in ARF
                        if (src_F < 64 and src_R < 64):
                            self.RS_LSQ[j][i].src_ready = [True, True]
                            self.RS_LSQ[j][i].src_value = [self.ARF.reg_float[src_F-32],
                                                                     self.ARF.reg_int[src_R]]

                        # if source 0 is from ROB, source 1 is from ARF
                        if (src_F >= 64 and src_R < 64):
                            self.RS_LSQ[j][i].src_ready = [False, True]
                            self.RS_LSQ[j][i].src_value = [-1, self.ARF.reg_int[src_R]]

                        # if source 0 is from ARF, source 1 is from ROB
                        if (src_F < 64 and src_R >= 64):

                            if self.ROB[src_R - 64].value_ready == True:
                                src_R = self.ROB[src_R - 64].reg_value
                                self.RS_LSQ[j][i].src_ready = [True, True]
                                self.RS_LSQ[j][i].src_value = [self.ARF.reg_float[src_F-32], src_R]
                            else:
                                self.RS_LSQ[j][i].src_ready = [True, False]
                                self.RS_LSQ[j][i].src_value = [self.ARF.reg_float[src_F-32], -1]

                        # if both are from ROB
                        if (src_F >= 64 and src_R >= 64):

                            if self.ROB[src_R - 64].value_ready == True:
                                src_R = self.ROB[src_R - 64].reg_value
                                self.RS_LSQ[j][i].src_ready = [False, True]
                                self.RS_LSQ[j][i].src_value = [-1, src_R]
                            else:

                                self.RS_LSQ[j][i].src_ready = [False, False]
                                self.RS_LSQ[j][i].src_value = [-1, -1]

                        self.RS_LSQ[j][i].rdy2exe_cycle = self.cycle + 1

                        # 2.2 Update RAT
                        # RAT with dest 0-63 points to ARF
                        # RAT with dest >= 64 ... points to ROB
                        if inst.inst == 1:
                            self.RAT[inst.F + 32] = 64 + ROB_no

                        flag = True
                        self.INDEX_LSQ = j + 1
                        print("go to break")
                        break
                if flag:
                    break

            # return 0
        # BEN and BEQ
        elif inst.inst == 3 or inst.inst == 4:
            flag = False

            print("RS Integer adder BEQ BNE number is", len(self.RS_Integer_Adder))

            for x in range(self.INDEX_INT_ADDER, self.INDEX_INT_ADDER + len(self.RS_Integer_Adder)):
                j = x % (len(self.RS_Integer_Adder))
                print("input j is", j)

                for i in range(0, len(self.RS_Integer_Adder[j])):
                    print("self.RS_Integer_Adder[", j, "][", i, "].in_use is", self.RS_Integer_Adder[j][i].in_use)
                    if self.RS_Integer_Adder[j][i].in_use == False:

                        RS_no = i

                        # Unique ID for each instruction. For CDB arbiter, the inst with smaller ID is first served
                        inst.ID = self.inst_ID_last
                        self.inst_ID_last = self.inst_ID_last + 1

                        # 2.1 Update ROB
                        # self.ROB[rob_entry_no].reg_number = inst.dest
                        self.ROB[rob_entry_no].idle = False
                        self.ROB[rob_entry_no].instruction_index = inst.index
                        self.ROB[rob_entry_no].instruction_ID = inst.ID

                        src_0 = self.RAT[inst.source_0]
                        print("src_0 is", src_0)
                        print("src_1 is", inst.source_1)
                        src_1 = self.RAT[inst.source_1]

                        # 2.3 Update RS
                        self.RS_Integer_Adder[j][i].in_use = True
                        self.RS_Integer_Adder[j][i].instruction_type = inst.inst
                        self.RS_Integer_Adder[j][i].dest_addr = ROB_no + 64
                        self.RS_Integer_Adder[j][i].dest_value = -1
                        self.RS_Integer_Adder[j][i].instruction_index = inst.index
                        self.RS_Integer_Adder[j][i].instruction_id = inst.ID


                        src_0 = self.RAT[inst.source_0]
                        print("src_0 is", src_0)


                        src_1 = self.RAT[inst.source_1]
                        print("src_1 is", src_1)

                        self.RS_Integer_Adder[j][i].src_addr = [src_0, src_1]
                        self.RS_Integer_Adder[j][i].start_cycle = -1
                        self.RS_Integer_Adder[j][i].finish_cycle = -1

                        # If both source is in ARF
                        if (src_0 < 64 and src_1 < 64):
                            self.RS_Integer_Adder[j][i].src_ready = [True, True]
                            self.RS_Integer_Adder[j][i].src_value = [self.ARF.reg_int[src_0],
                                                                     self.ARF.reg_int[src_1]]

                        # if source 0 is from ROB, source 1 is from ARF
                        if (src_0 >= 64 and src_1 < 64):

                            if self.ROB[src_0 - 64].value_ready == True:
                                src_0 = self.ROB[src_0 - 64].reg_value
                                self.RS_Integer_Adder[j][i].src_ready = [True, True]
                                self.RS_Integer_Adder[j][i].src_value = [src_0, self.ARF.reg_int[src_1]]
                            else:
                                self.RS_Integer_Adder[j][i].src_ready = [False, True]
                                self.RS_Integer_Adder[j][i].src_value = [-1, self.ARF.reg_int[src_1]]

                        # if source 0 is from ARF, source 1 is from ROB
                        if (src_0 < 64 and src_1 >= 64):

                            if self.ROB[src_1 - 64].value_ready == True:
                                src_1 = self.ROB[src_1 - 64].reg_value
                                self.RS_Integer_Adder[j][i].src_ready = [True, True]
                                self.RS_Integer_Adder[j][i].src_value = [self.ARF.reg_int[src_0], src_1]
                            else:
                                self.RS_Integer_Adder[j][i].src_ready = [True, False]
                                self.RS_Integer_Adder[j][i].src_value = [self.ARF.reg_int[src_0], -1]

                        # if both are from ROB
                        if (src_0 >= 64 and src_1 >= 64):

                            if self.ROB[src_0 - 64].value_ready == True:
                                src_0 = self.ROB[src_0 - 64].reg_value
                                if self.ROB[src_1 - 64].value_ready == True:
                                    src_1 = self.ROB[src_1 - 64].reg_value
                                    self.RS_Integer_Adder[j][i].src_ready = [True, True]
                                    self.RS_Integer_Adder[j][i].src_value = [src_0, src_1]
                                else:
                                    self.RS_Integer_Adder[j][i].src_ready = [True, False]
                                    self.RS_Integer_Adder[j][i].src_value = [src_0, -1]
                            else:
                                if self.ROB[src_1 - 64].value_ready == True:
                                    src_1 = self.ROB[src_1 - 64].reg_value
                                    self.RS_Integer_Adder[j][i].src_ready = [False, True]
                                    self.RS_Integer_Adder[j][i].src_value = [-1, src_1]
                                else:
                                    self.RS_Integer_Adder[j][i].src_ready = [False, False]
                                    self.RS_Integer_Adder[j][i].src_value = [-1 -1]


                        # 2.2 Update RAT
                        # RAT with dest 0-63 points to ARF
                        # RAT with dest >= 64 ... points to ROB
                        # self.RAT[inst.dest] = 64 + ROB_no

                        self.RS_Integer_Adder[j][i].rdy2exe_cycle = self.cycle + 1

                        flag = True
                        self.INDEX_INT_ADDER = j + 1
                        print("go to break")
                        break
                if flag:
                    break
        # Integer addition and subtraction
        elif inst.inst == 5 or inst.inst == 7 or inst.inst == 8:
            flag = False

            print("RS Integer Adder number is", len(self.RS_Integer_Adder))

            for x in range(self.INDEX_INT_ADDER, self.INDEX_INT_ADDER+len(self.RS_Integer_Adder)):
                j = x % (len(self.RS_Integer_Adder))
                print("input j is", j)

                for i in range(0, len(self.RS_Integer_Adder[j])):
                    print("self.RS_Integer_Adder[",j,"][",i,"].in_use is", self.RS_Integer_Adder[j][i].in_use)
                    if self.RS_Integer_Adder[j][i].in_use == False:

                        RS_no = i

                        # Unique ID for each instruction. For CDB arbiter, the inst with smaller ID is first served
                        inst.ID = self.inst_ID_last
                        self.inst_ID_last = self.inst_ID_last + 1

                        # 2.1 Update ROB
                        self.ROB[rob_entry_no].reg_number = inst.dest
                        self.ROB[rob_entry_no].idle = False
                        self.ROB[rob_entry_no].instruction_index = inst.index
                        self.ROB[rob_entry_no].instruction_ID = inst.ID



                        # 2.3 Update RS
                        self.RS_Integer_Adder[j][i].in_use = True
                        self.RS_Integer_Adder[j][i].instruction_type = inst.inst
                        self.RS_Integer_Adder[j][i].dest_addr = ROB_no + 64
                        self.RS_Integer_Adder[j][i].dest_value = -1
                        self.RS_Integer_Adder[j][i].instruction_index = inst.index
                        self.RS_Integer_Adder[j][i].instruction_id = inst.ID

                        src_0 = self.RAT[inst.source_0]

                        # if src_0 >=64:
                        #     if self.ROB[src_0-64].value_ready == True:
                        #         src_0 = self.ROB[src_0-64].reg_number

                        print("Int ALU src_0 is", src_0)

                        if inst.inst == 7:

                            src_1 = int(inst.source_1)

                            print("Int ALU src_1 is", src_1)

                            self.RS_Integer_Adder[j][i].src_addr = [src_0, src_1]
                            self.RS_Integer_Adder[j][i].start_cycle = -1
                            self.RS_Integer_Adder[j][i].finish_cycle = -1

                            # If both source is in ARF
                            if (src_0 < 64):
                                self.RS_Integer_Adder[j][i].src_ready = [True, True]
                                self.RS_Integer_Adder[j][i].src_value = [self.ARF.reg_int[src_0],
                                                                         src_1]

                            # if source 0 is from ROB
                            if (src_0 >= 64):
                                if self.ROB[src_0 - 64].value_ready == True:
                                    src_0 = self.ROB[src_0-64].reg_value
                                    self.RS_Integer_Adder[j][i].src_ready = [True, True]
                                    self.RS_Integer_Adder[j][i].src_value = [src_0, src_1]
                                else:
                                    self.RS_Integer_Adder[j][i].src_ready = [False, True]
                                    self.RS_Integer_Adder[j][i].src_value = [-1, src_1]

                            self.RS_Integer_Adder[j][i].rdy2exe_cycle = self.cycle + 1

                        else:
                            src_1 = self.RAT[inst.source_1]

                            # if src_1 >= 64:
                            #     if self.ROB[src_1 - 64].value_ready == True:
                            #         src_1 = self.ROB[src_1 - 64].reg_number

                            print("src_1 is", src_1)

                            self.RS_Integer_Adder[j][i].src_addr = [src_0, src_1]
                            self.RS_Integer_Adder[j][i].start_cycle = -1
                            self.RS_Integer_Adder[j][i].finish_cycle = -1

                            # If both source is in ARF
                            if (src_0 < 64 and src_1 < 64):
                                self.RS_Integer_Adder[j][i].src_ready = [True, True]
                                self.RS_Integer_Adder[j][i].src_value = [self.ARF.reg_int[src_0], self.ARF.reg_int[src_1]]

                            # if source 0 is from ROB, source 1 is from ARF
                            if (src_0 >= 64 and src_1 < 64):
                                self.RS_Integer_Adder[j][i].src_ready = [False, True]
                                self.RS_Integer_Adder[j][i].src_value = [-1, self.ARF.reg_int[src_1]]

                            # if source 0 is from ARF, source 1 is from ROB
                            if (src_0 < 64 and src_1 >= 64):
                                self.RS_Integer_Adder[j][i].src_ready = [True, False]
                                self.RS_Integer_Adder[j][i].src_value = [self.ARF.reg_int[src_0], -1]

                            # if both are from ROB
                            if (src_0 >= 64 and src_1 >= 64):
                                self.RS_Integer_Adder[j][i].src_ready = [False, False]
                                self.RS_Integer_Adder[j][i].src_value = [-1, -1]

                            self.RS_Integer_Adder[j][i].rdy2exe_cycle = self.cycle + 1

                        # 2.2 Update RAT
                        # RAT with dest 0-63 points to ARF
                        # RAT with dest >= 64 ... points to ROB
                        self.RAT[inst.dest] = 64 + ROB_no

                        flag = True
                        self.INDEX_INT_ADDER = j+1
                        print("go to break")
                        break
                if flag:
                    break
        # Float addition and subtraction
        elif inst.inst == 6 or inst.inst == 9:
            flag = False

            print("RS Float adder number is", len(self.RS_Float_Adder))

            for x in range(self.INDEX_FLOAT_ADDER, self.INDEX_FLOAT_ADDER + len(self.RS_Float_Adder)):
                j = x % (len(self.RS_Float_Adder))
                print("input j is", j)

                for i in range(0, len(self.RS_Float_Adder[j])):
                    print("self.RS_Float_Adder[", j, "][", i, "].in_use is", self.RS_Float_Adder[j][i].in_use)
                    if self.RS_Float_Adder[j][i].in_use == False:

                        RS_no = i

                        # Unique ID for each instruction. For CDB arbiter, the inst with smaller ID is first served
                        inst.ID = self.inst_ID_last
                        self.inst_ID_last = self.inst_ID_last + 1

                        # 2.1 Update ROB
                        self.ROB[rob_entry_no].reg_number = inst.dest+32
                        self.ROB[rob_entry_no].idle = False
                        self.ROB[rob_entry_no].instruction_index = inst.index
                        self.ROB[rob_entry_no].instruction_ID = inst.ID



                        # 2.3 Update RS
                        self.RS_Float_Adder[j][i].in_use = True
                        self.RS_Float_Adder[j][i].instruction_type = inst.inst
                        self.RS_Float_Adder[j][i].dest_addr = ROB_no + 64
                        self.RS_Float_Adder[j][i].dest_value = -1
                        self.RS_Float_Adder[j][i].instruction_index = inst.index
                        self.RS_Float_Adder[j][i].instruction_id = inst.ID

                        src_0 = self.RAT[inst.source_0+32]

                        # if src_0 >= 64:
                        #     if self.ROB[src_0 - 64].value_ready == True:
                        #         src_0 = self.ROB[src_0 - 64].reg_number

                        print("src_0 is", src_0)

                        src_1 = self.RAT[inst.source_1+32]

                        # if src_1 >= 64:
                        #     if self.ROB[src_1 - 64].value_ready == True:
                        #         src_1 = self.ROB[src_1 - 64].reg_number

                        print("src_1 is", src_1)

                        self.RS_Float_Adder[j][i].src_addr = [src_0, src_1]
                        self.RS_Float_Adder[j][i].start_cycle = -1
                        self.RS_Float_Adder[j][i].finish_cycle = -1

                        # If both source is in ARF
                        if (src_0 < 64 and src_1 < 64):
                            self.RS_Float_Adder[j][i].src_ready = [True, True]
                            self.RS_Float_Adder[j][i].src_value = [self.ARF.reg_float[src_0-32],
                                                                     self.ARF.reg_float[src_1-32]]

                        # if source 0 is from ROB, source 1 is from ARF
                        if (src_0 >= 64 and src_1 < 64):
                            self.RS_Float_Adder[j][i].src_ready = [False, True]
                            self.RS_Float_Adder[j][i].src_value = [-1, self.ARF.reg_float[src_1-32]]

                        # if source 0 is from ARF, source 1 is from ROB
                        if (src_0 < 64 and src_1 >= 64):
                            self.RS_Float_Adder[j][i].src_ready = [True, False]
                            self.RS_Float_Adder[j][i].src_value = [self.ARF.reg_float[src_0-32], -1]

                        # if both are from ROB
                        if (src_0 >= 64 and src_1 >= 64):
                            self.RS_Float_Adder[j][i].src_ready = [False, False]
                            self.RS_Float_Adder[j][i].src_value = [-1, -1]

                        self.RS_Float_Adder[j][i].rdy2exe_cycle = self.cycle + 1

                        # 2.2 Update RAT
                        # RAT with dest 0-63 points to ARF
                        # RAT with dest >= 64 ... points to ROB
                        self.RAT[inst.dest+32] = 64 + ROB_no
                        print("dest is", self.RAT[inst.dest + 32])
                        flag = True
                        self.INDEX_FLOAT_ADDER = j + 1
                        print("go to break")
                        break
                if flag:
                    break
        # Float multiplication
        elif inst.inst == 10:

            flag = False

            print("RS Float Mux number is", len(self.RS_Float_Mul))

            for x in range(self.INDEX_FLOAT_MUL, self.INDEX_FLOAT_MUL + len(self.RS_Float_Mul)):
                j = x % (len(self.RS_Float_Mul))
                # print("input j is", j, "length is ", len(self.RS_Float_Mul[j]))

                for i in range(0, len(self.RS_Float_Mul[j])):
                    print("self.RS_Float_Adder[", j, "][", i, "].in_use is", self.RS_Float_Adder[j][i].in_use)
                    if self.RS_Float_Mul[j][i].in_use == False:

                        RS_no = i

                        # Unique ID for each instruction. For CDB arbiter, the inst with smaller ID is first served
                        inst.ID = self.inst_ID_last
                        self.inst_ID_last = self.inst_ID_last + 1

                        # 2.1 Update ROB
                        self.ROB[rob_entry_no].reg_number = inst.dest+32
                        self.ROB[rob_entry_no].idle = False
                        self.ROB[rob_entry_no].instruction_index = inst.index
                        self.ROB[rob_entry_no].instruction_ID = inst.ID



                        # 2.3 Update RS
                        self.RS_Float_Mul[j][i].in_use = True
                        self.RS_Float_Mul[j][i].instruction_type = inst.inst
                        self.RS_Float_Mul[j][i].dest_addr = ROB_no + 64
                        self.RS_Float_Mul[j][i].dest_value = -1
                        self.RS_Float_Mul[j][i].instruction_index = inst.index
                        self.RS_Float_Mul[j][i].instruction_id = inst.ID

                        src_0 = self.RAT[inst.source_0 + 32]

                        # if src_0 >= 64:
                        #     if self.ROB[src_0 - 64].value_ready == True:
                        #         src_0 = self.ROB[src_0 - 64].reg_number

                        print("src_0 is", src_0)

                        src_1 = self.RAT[inst.source_1 + 32]

                        # if src_1 >= 64:
                        #     if self.ROB[src_1 - 64].value_ready == True:
                        #         src_1 = self.ROB[src_1 - 64].reg_value

                        print("src_1 is", src_1)

                        self.RS_Float_Mul[j][i].src_addr = [src_0, src_1]
                        self.RS_Float_Mul[j][i].start_cycle = -1
                        self.RS_Float_Mul[j][i].finish_cycle = -1

                        # If both source is in ARF
                        if (src_0 < 64 and src_1 < 64):
                            self.RS_Float_Mul[j][i].src_ready = [True, True]
                            self.RS_Float_Mul[j][i].src_value = [self.ARF.reg_float[src_0 - 32],
                                                                   self.ARF.reg_float[src_1 - 32]]

                        # if source 0 is from ROB, source 1 is from ARF
                        if (src_0 >= 64 and src_1 < 64):
                            self.RS_Float_Mul[j][i].src_ready = [False, True]
                            self.RS_Float_Mul[j][i].src_value = [-1, self.ARF.reg_float[src_1 - 32]]

                        # if source 0 is from ARF, source 1 is from ROB
                        if (src_0 < 64 and src_1 >= 64):
                            self.RS_Float_Mul[j][i].src_ready = [True, False]
                            self.RS_Float_Mul[j][i].src_value = [self.ARF.reg_float[src_0 - 32], -1]

                        # if both are from ROB
                        if (src_0 >= 64 and src_1 >= 64):
                            self.RS_Float_Mul[j][i].src_ready = [False, False]
                            self.RS_Float_Mul[j][i].src_value = [-1, -1]

                        self.RS_Float_Mul[j][i].rdy2exe_cycle = self.cycle + 1

                        # 2.2 Update RAT
                        # RAT with dest 0-63 points to ARF
                        # RAT with dest >= 64 ... points to ROB
                        self.RAT[inst.dest+32] = 64 + ROB_no
                        print("dest is", self.RAT[inst.dest+32])

                        flag = True
                        self.INDEX_FLOAT_MUL= j + 1
                        print("go to break")
                        break
                if flag:
                    break



        # 2.3 Check if RS has empty entry
        # If no, return -1
        # If yes, update RS, ROB, RAT with instruction
        # Note: Right now, this function has not decided which RS to be put

        print("out of break")

        # Issue aborted
        if flag == False:
            return -1
        else:
            self.ROB_head = (self.ROB_head + 1) % self.ROB_num


        #
        # print("ROB[",ROB_no,"]:", self.ROB[ROB_no].idle, self.ROB[ROB_no].reg_number, self.ROB[ROB_no].reg_value,
        #       self.ROB[ROB_no].instruction_index)
        # print("RS[", RS_no,"]:", self.RS_Integer_Adder[RS_no].in_use, self.RS_Integer_Adder[RS_no].dest_addr, self.RS_Integer_Adder[RS_no].dest_value, self.RS_Integer_Adder[RS_no].src_addr,
        #       self.RS_Integer_Adder[RS_no].src_ready, self.RS_Integer_Adder[RS_no].src_value, self.RS_Integer_Adder[RS_no].instruction_index)
        # print("Current cycle is",self.cycle)

        # Add a new line for final output instruction table
        # record Issue cycle
        self.instruction_final_table.append([self.cycle, -1, -1, -1, -1,inst.str])
        print("final table is", self.instruction_final_table)

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

    # def write_back_check(self):
    #     for i in range (self.config.adder.fu_number):
    #         self.Integer_Adder[i].operation(self.cycle, WRITE_BACK_CHECK, self)    # inform CDB that adder wants to write back
    #         print("CDB Queue:-----------------------------------------------------")
#       print(self.CDB.arbiter_q)

    def write_back(self):
        print("++++++++++++++++++++++++++++++++")
        for i in range(self.config.adder.fu_number):
            self.Integer_Adder[i].operation(self.cycle, WRITE_BACK, self)
        for i in range(self.config.fpadder.fu_number):
            self.FP_Adder[i].operation(self.cycle, WRITE_BACK, self)
        for i in range(self.config.fpmul.fu_number):
            self.FP_Mul[i].operation(self.cycle, WRITE_BACK, self)
        for i in range(self.config.ldst.fu_number):
            self.LSQ_Integer_Adder[i].operation(self.cycle, WRITE_BACK, self)
        print("-----------CDB Begin------------")
        self.CDB.arbiter(self)
        print("-----------CDB End--------------")

    def execs(self):

        for i in range(self.config.adder.fu_number):
            self.Integer_Adder[i].operation(self.cycle, EXEC, self)
        for i in range(self.config.fpadder.fu_number):
            self.FP_Adder[i].operation(self.cycle, EXEC, self)
        for i in range(self.config.fpmul.fu_number):
            self.FP_Mul[i].operation(self.cycle, EXEC, self)
        for i in range(self.config.ldst.fu_number):
            self.LSQ_Integer_Adder[i].operation(self.cycle, EXEC, self)

    def commit(self):  # pc 1103
        print("-------------Commit begin:----------------")
        # TODO: when commit, if the RAT entry does not point to this ROB entry, abandon this register value in ROB, and do not update ARF
        rob_H = self.ROB[self.ROB_tail]  # ROB header entry

        if rob_H.value_ready == True and self.cycle>=self.ROB[self.ROB_tail].value_rdy2commit_cycle:  # ready to commit

            # if rob_H.if_sd == True and rob_H.if_sd_counter < self.config.ldst.mem_cycles-1:
            #
            #     # print("sd fu index is",rob_H.sd_fu_index, "sd rs index is",rob_H.sd_rs_index)
            #     # if rob_H.if_sd_counter == 0:
            #     #
            #     #
            #     #
            #     print("if store",rob_H.if_sd_counter)
            #     # rob_H.if_sd_counter+=1
            #
            # el
            if rob_H.if_sd == True and rob_H.if_sd_counter < self.config.ldst.mem_cycles-1:
                rob_H.if_sd = False
                rob_H.if_sd_counter = 0

                self.instruction_final_table[rob_H.instruction_ID][4] = self.cycle
                self.RAT[rob_H.reg_number] = rob_H.reg_number  # update RAT to the latest ARF ID
                print("sd commit index is ", rob_H.reg_number, "value is", self.RAT[rob_H.reg_number])
                if rob_H.reg_number > 31:
                    self.ARF.reg_float[rob_H.reg_number % 32] = rob_H.reg_value  # update ARF to the latest value in ROB
                else:
                    print("sd for int num", rob_H.reg_number, rob_H.reg_value)
                    self.ARF.reg_int[rob_H.reg_number % 32] = rob_H.reg_value  # update ARF to the latest value in ROB
                self.ROB[self.ROB_tail].clear()  # remove current ROB head entry

                self.ROB[self.ROB_tail].pointer = rob_H.reg_number

                self.ROB_tail = (self.ROB_tail + 1) % 64  # update ROB header to the next one

                self.MEM[self.RS_LSQ[rob_H.sd_fu_index][rob_H.sd_rs_index].addr] = \
                self.RS_LSQ[rob_H.sd_fu_index][rob_H.sd_rs_index].src_value[0]

                self.RS_LSQ[rob_H.sd_fu_index][rob_H.sd_rs_index].clear()

                # self.MEM[self.RS_LSQ[rob_H.sd_fu_index][rob_H.sd_rs_index].addr] = self.RS_LSQ[rob_H.sd_fu_index][rob_H.sd_rs_index].src_value[0]

                # self.RS_LSQ[rob_H.sd_fu_index][rob_H.sd_rs_index].clear()




            else:
                # Add current cycle as the wb cycle of corresponding instruction
                self.instruction_final_table[rob_H.instruction_ID][4] = self.cycle

                if self.RAT[rob_H.reg_number] == self.ROB_tail+64:
                    self.RAT[rob_H.reg_number] = rob_H.reg_number  # update RAT to the latest ARF ID
                    print("commit index is ", rob_H.reg_number, "value is",rob_H.reg_value)
                    if rob_H.reg_number > 31:
                        self.ARF.reg_float[rob_H.reg_number % 32] = rob_H.reg_value  # update ARF to the latest value in ROB
                    else:
                        print("for int num",rob_H.reg_number, rob_H.reg_value)
                        self.ARF.reg_int[rob_H.reg_number % 32] = rob_H.reg_value  # update ARF to the latest value in ROB
                self.ROB[self.ROB_tail].clear()  # remove current ROB head entry

                self.ROB[self.ROB_tail].pointer = rob_H.reg_number

                self.ROB_tail = (self.ROB_tail + 1) % 64  # update ROB header to the next one

        print(self.ROB_tail)
        print("-------------Commit end:----------------")
# def init_adder(config):
#
#     # adder = Adder(config)
#     # adder.print_config()
#
#     # return adder
#     print("init_adder()")
