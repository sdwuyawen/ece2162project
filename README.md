# ece2162project
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
    




