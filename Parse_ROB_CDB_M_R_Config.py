import numpy as np
import re
num_ROB=0; num_CDB=0; num_RF=[]; R=[0]*32; F=[0]*32; Mem=[0]*64;
def main():
    #read file
    fc=open("config_Space.txt", "r")
    lines=fc.readlines()
    fc.close()
    # look for patterns
    for line in lines:
        #display
        #print(line)
        if line.find("ROB")!=-1:
            num_ROB=re.findall(r"\d+",line)
            num_ROB=int(num_ROB[0])
        elif line.find("CDB")!=-1:
            num_CDB=re.findall(r"\d+",line)
            num_CDB=int(num_CDB[0])
        elif line.find("R")!=-1 or line.find("F")!=-1:
            line=line[:len(line)-1]
            registers=line.split(', ')
            #print(registers);
            for e in registers:
                if e.startswith('R'):
                    e=e[1:]
                    #print(int(e.split('=')[0]))
                    R[int(e.split('=')[0])]=int(e.split('=')[1])
                elif e.startswith('F'):
                    e=e[1:]
                    F[int(e.split('=')[0])]=float(e.split('=')[1])
            #print(R,F)
           # z=len(x)
        elif line.find("Mem[")!=-1:
            line=line[:len(line)-1]
            Memory=line.split(', ')
            for m in Memory:
                m=m[m.find("[")+1:m.find("]")]+m[m.find("="):]
                #print(m)
                Mem[int(m.split('=')[0])]=float(m.split("=")[1])

    print("ROB=",num_ROB)
    print("CDB=",num_CDB)
    print("R=",R)
    print("F=",F)
    print("Mem=",Mem)
    #print("RF=", num_RF)
main()
