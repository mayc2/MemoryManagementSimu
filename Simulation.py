#Memory Management Simulation System
import sys

class Process(object):
    """docstring for Process"""
    def __init__(self, processArgs):
        if len(processList) < 4:                        # Process wasn't provided at least a name, req frames
            print "Error Initializing Process!"         #   and one set of arrival and exit times
            print "Not Enough Arguments..."
            return
            
        self.name = processArgs[0]                      # Process Name
        self.reqMemFrames = processArgs[1]              # Process Size
        self.arrivalAndExitTimes = processArgs[2:]      # List of arrival and exit times

class MainMemorySimulator(object):
    """docstring for MainMemory"""
    def __init__(self, processList):
        self.simTime = 0                    # Master Time Handler
        self.processes = processList        # Master List of all Processes
        self.runningProcesses = []          # List of Processes currently running
        self.memFrames = ""                 # String Representation of Memory
        self.numMemFrames = 1600            # Total amount of space (memFrames size)
        self.numOpSysProc = 80              # Number of spaces in Memory Representation
                                            #   dedicated to op sys processes
        
        for p in processList:                   # Finding all processes that start at 0
            if p.arrivalAndExitTimes[0] == 0:
                self.runningProcesses.append(p) # and adding them to runningProcesses list

        runningProcessListItr = 0           # Index handler for running processes
        inProcFrameItr = 1                  # Index handler for each frame in a process
        roomLeft = False                    # Bool to check for memory overflow
        memFrameItr = self.numOpSysProc     # Master index handler for memory representation

        for i in range(0, self.numOpSysProc):   # Adding Operating System Frames to beginning
            self.memFrames += "#"

        while memFrameItr < self.numMemFrames:      # Fill in each spot of memory representation
            if runningProcessListItr < len(self.runningProcesses): # If there are running processes
                self.memFrames += self.processes[processListItr].name # Add process name to mem rep
                inProcFrameItr++                                        # Move to next frame in process
                if inProcFrameItr > self.processes[processListItr].reqMemFrames: # If process needs no more frames
                    processListItr++                # Move to next process
                    inProcFrameItr = 1              # Reset in process index handler
            else:                                   # If no more processes need to be added
                roomLeft = True                     # Indicate there is no overflow issue
                self.memFrames += "."               # Indicate free memory spots
            
             memFrameItr++
        
        if not roomLeft:                            # State there is an overflow issue
            print "ERROR: OUT-OF-MEMORY"

        self.printMemory()                          # Print the structure
    
    def printMemory(self):
        print "Memory at time %d" %self.simTime
        print self.memFrames

    def run(self, mode):
        if (mode == "first"):
            pass
        elif (mode == "best"):
            pass
        elif (mode == "next"):
            pass
        elif (mode == "worst"):
            pass
        elif (mode == "noncontig"):
            pass


def check_filename(file_name):
    if file_name[len(file_name) - 4:] == ".txt":
        return True
    return False
    
def check_allocmethod(alloc_method):
    possible = ["first", "best", "next", "worst", "noncontig"]
    for a in possible:
        if alloc_method == a:
            return True
    return False

def parse(argv):
    #memsim -q <input-file> { first | best | next | worst }
    quiet_mode = False
    file_name = ""
    alloc_method = ""
    if len(argv) == 4:
        if argv[1] == "-q":
            quiet_mode = True
        else:
            print "USAGE: memsim [-q] <input-file> { first | best | next | worst }"
            sys.exit()
        file_name = argv[2]
        alloc_method = argv[3]
    elif len(argv) == 3:
        file_name = argv[1]
        alloc_method = argv[2]
    else:
        print "USAGE: memsim [-q] <input-file> { first | best | next | worst }"
        sys.exit()
    if check_allocmethod(alloc_method) and check_filename(file_name):
        return (quiet_mode, file_name, alloc_method)
    else:
        print "USAGE: memsim [-q] <input-file> { first | best | next | worst }"
        sys.exit()

#main function
if __name__ == '__main__':
    #Some Pseudocode

    #parse cli arguments
    (quiet_mode, file_name, alloc_method) = parse(sys.argv)

    print quiet_mode
    print file_name
    print alloc_method
    # -- 
    #     -- read user processes from in-file 
    #     -- get type of memory allocation algorithm to use
    # - set up user processes (allocated at time 0)
    # - display initial memory
    # - call simulation of proper algorithm
    
   #psuedo 
    #with open(file):
    #    readline(Make Process)
   # DOWN HERE WE READ FROM FILE< IN EACH LINE WE CREATE NEW PROCESS CLASS FILE SHOULD HAVE AT LEAST 4 ELEMENTS per LINE

