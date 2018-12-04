Commi# ece2162project
ECE2162 Project
test

ISSUE:
  1. Instructions are issued in order, i.e., if either the ROB and RS are full, the issue should skip at this cycle. 
  2. We should check ROB and RS at the beginning stage of the ISSUE
  3. The order of the execution of ISSUE def
    1. Check which kind of inst it is to deicde which RS it will go to
    2. Check ROB to see which entry is empty
    3. If both are empty, then update ROB idle 0->1, RAT update, RS is filled with source_register mapped with RAT(ROB/ARF)   
    
    note: if we define two variables for head and tile for ROB, then we can decide which entry of ROB to be filled and ereased. 


EXECTUION
  
  
  1. For every idle FU check if there is any entry in the RS 
    If YES, check if the entry has the value or ROB

2. LOAD/STORE RS will also need to be considered 

WRITE BACK
  1. 
    
Commit
  1. TODO: If the correpsonding ROB value is the old value and cannot be found the RAT table for corresponding R, then we just abandon the old value. 


## (Seems done)1. CDB -> 
buffer (# of halting Register value) -> if buffer is full, the value will be stored in function unit, function unit cannot do write back, a CDB unit (class) must be implemented for all Write Back
if conflict, the instruction with lower index can be written back first 

## 2. Memory -> 
L/S Queue -> 
1. PC -> instruction index
2. Load will check the last entry of Store first, Load will only execute after all Store execute. 
3. Forwarding -> Load will get value from LSQ in MEM (One cycle)
4. Store will be dequeued after Commit
5. Load will be dequeued after WB

## 3. Floating ->
pipeline(adder)+Issue+instruction read



## 4. Branch -> 
Prediction (PC = instruction index)
Predictor
1. BTB -> 8 entries to store the target (last three bits of the index)
2. 8 One-bit predictors for every entry
3. Prediction is done in the first cycle of execution (ISSUE)
4. The branch can be resolved after EXE stage
5. At the first, there is no value in the predictor. The predicted value will be settled after execution of the branch (Beq/Bne). 

Recover
RAT -> checkpoint before entering a branch/ only overwrite when the current entry contains ROB (The new entries pointing to ARF come from the Commit of instructions before the branch after the branch prediction) / -1 

RS (Head and Tail) -> delete the entries added after branch 
                      (add index to instructuion during ISSUE, if mispredict, delete the entries after the entry corresponding to the                           branch)
                      
ROB (Head and Tail) -> delete the entries added after branch 
                      (add index to instructuion during ISSUE, if mispredict, delete the entries after the entry corresponding to the                           branch)

Function unit -> 
Pipeline (floating point Add.d, Sub.d, Mult.d)
Implement a queue containing the input instructions
find out the instructions index after the branch 
Delete

Unpipeline (Integer Add Sub Add.i)
Judge whether the instruction is after the branch 
delete if it is



























