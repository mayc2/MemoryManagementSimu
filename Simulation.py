#Memory Management Simulation System
import argparse
import sys

# class Process(object):
#     """docstring for Process"""
#     def __init__(self, processArgs):
#         if len(processList) < 4:
#             print "Error Initializing Process!\nNot Enough Arguments..."
#             return
            
#         self.name = processArgs[0]
#         self.reqMemFrames = processArgs[1]
#         self.arrivalAndExitTimes = processArgs[2:]

# class MainMemorySimulator(object):
#     """docstring for MainMemory"""
#     def __init__(self, processList):
#         self.simTime = 0
#         self.isContig = True
#         self.processes = processList
#         self.numMemFrames = 1600
#         self.numOpSysProc = 80
#         self.memFrames = ""
        
#         processListItr = 0
#         inProcFrameItr = 0
#         roomLeft = False
#         memFrameItr = self.numOpSysProc
#         for i in range(0, self.numOpSysProc):
#             self.memFrames += "#"
#         while memFrameItr < self.numMemFrames:
#             if processListItr < len(self.processes):
#                 # go trhough each process
#             else:
#                 roomLeft = True
#                 self.memFrames += "."
            
#             memFrameItr++
        
#         if not roomLeft:
#             print "ERROR: OUT-OF-MEMORY"

#         self.printMemory()

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

