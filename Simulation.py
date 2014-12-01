#Memory Management Simulation System
import argparse

class Process(object):
    """docstring for Process"""
    def __init__(self, processList):
        if (len(processList) < 4):
            print "Error Initializing Process!\nNot Enough Arguments..."
            return
            
        self.name = processList[0]
        self.reqMemFrames = processList[1]
        self.arrivalAndExitTimes = processList[2:]

class MainMemorySimulator(object):
    """docstring for MainMemory"""
    def __init__(self, processes):
        self.time = 0
        self.isContig = True
        self.numMemFrames = 1600
        self.numOpSysProc = 80
        self.memFrames = []
        for (
    

            

if __name__ == '__main__':
    bool OUT_OF_MEMORY
    #Some Pseudocode

    #parse cli arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("file", dest = file, help = 'input file')
    parser.add_argument("allocMethod", dest = allocMethod, help = 'designate the allocation method')
    args = parser.parse_args()
    print args.ex #something like this

    
    -- 
        -- read user processes from in-file 
        -- get type of memory allocation algorithm to use
    - set up user processes (allocated at time 0)
    - display initial memory
    - call simulation of proper algorithm
    
   #psuedo 
    #with open(file):
    #    readline(Make Process)
   # DOWN HERE WE READ FROM FILE< IN EACH LINE WE CREATE NEW PROCESS CLASS FILE SHOULD HAVE AT LEAST 4 ELEMENTS per LINE

