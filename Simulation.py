#Memory Management Simulation System
import argparse

class Process(object):
    """docstring for Process"""
    def __init__(self, processArgs):
        if len(processList) < 4:
            print "Error Initializing Process!\nNot Enough Arguments..."
            return
            
        self.name = processArgs[0]
        self.reqMemFrames = processArgs[1]
        self.arrivalAndExitTimes = processArgs[2:]

class MainMemorySimulator(object):
    """docstring for MainMemory"""
    def __init__(self, processList):
        self.simTime = 0
        self.isContig = True
        self.processes = processList
        self.numMemFrames = 1600
        self.numOpSysProc = 80
        self.memFrames = ""
        
        processListItr = 0
        inProcFrameItr = 0
        roomLeft = False
        memFrameItr = self.numOpSysProc
        for i in range(0, self.numOpSysProc):
            self.memFrames += "#"
        while memFrameItr < self.numMemFrames:
            if processListItr < len(self.processes):
                # go trhough each process
            else:
                roomLeft = true
                self.memFrames += "."
            
            memFrameItr++
        
        if not roomLeft:
            print "Error: Processes require too much memory!"
    
        self.printMemory()
            

if __name__ == '__main__':
    bool OUT_OF_MEMORY
    #Some Pseudocode

    #parse cli arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("file_name", dest = file_name, help = 'input file')
    parser.add_argument("allocMethod", dest = allocMethod, help = 'designate the allocation method')
    args = parser.parse_argbtll fd swi    
    print args.ex #something

    
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

}