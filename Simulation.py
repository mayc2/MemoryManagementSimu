#Memory Management Simulation System
import sys

class Process(object):
    """docstring for Process"""
    def __init__(self, processArgs):
        if len(processArgs) < 4:                        # Process wasn't provided at least a name, req frames
            print "Error Initializing Process!"         #   and one set of arrival and exit times
            print "Not Enough Arguments..."
            return
            
        self.name = processArgs[0]                      # Process Name
        self.reqMemFrames = int(processArgs[1])              # Process Size
        self.arrivalTimes = []
        self.exitTimes = []
        i = 0
        for x in processArgs[2:]:                   # List of arrival and exit times
            if i%2 == 0:
                self.arrivalTimes.append(int(x))
            else:
                self.exitTimes.append(int(x))
            i += 1

class MainMemorySimulator(object):
    """docstring for MainMemory"""
    def __init__(self, processList):
        self.simTime = 0                    # Master Time Handler
        self.lastTime = 0                   # Time that last process exits
        self.processes = processList        # Master List of all Processes
        self.freeSpace = [(0,1600)]                 # List of tuples of start and end of free space
        self.runningProcesses = []          # List of Processes currently running
        self.memFrames = ""                 # String Representation of Memory
        self.numMemFrames = 1600            # Total amount of space (memFrames size)
        self.numOpSysProc = 80              # Number of spaces in Memory Representation
                                            #   dedicated to op sys processes

        for p in processList:                   # Finding all processes that start at 0
            if p.arrivalTimes[0] == 0:
                (free_check, begin, end) = self.find_first_free_space( p.reqMemFrames )
                if free_check:
                    #TO-DO: sort
                    tSize = p.reqMemFrames + begin
                    if tSize > 0:
                        self.freeSpace.append( (tSize,end) )
                    self.runningProcesses.append(p) # and adding them to runningProcesses list
                    self.free_sort()
                else:
                    print "ERROR: OUT-OF-MEMORY"
                    sys.exit()

            for et in p.exitTimes:
                if et > self.lastTime:
                    self.lastTime = et

        runningProcessListItr = 0           # Index handler for running processes
        inProcFrameItr = 1                  # Index handler for each frame in a process
        roomLeft = False                    # Bool to check for memory overflow
        memFrameItr = self.numOpSysProc     # Master index handler for memory representation

        for i in range(0, self.numOpSysProc):   # Adding Operating System Frames to beginning
            self.memFrames += "#"

        while memFrameItr < self.numMemFrames:      # Fill in each spot of memory representation
            if runningProcessListItr < len(self.runningProcesses): # If there are running processes
                self.memFrames += self.processes[runningProcessListItr].name # Add process name to mem rep
                inProcFrameItr += 1                                        # Move to next frame in process
                if inProcFrameItr > self.processes[runningProcessListItr].reqMemFrames: # If process needs no more frames
                    runningProcessListItr += 1               # Move to next process
                    inProcFrameItr = 1              # Reset in process index handler
            else:                                   # If no more processes need to be added
                roomLeft = True                     # Indicate there is no overflow issue
                self.memFrames += "."               # Indicate free memory spots
            
            memFrameItr += 1
        
        if not roomLeft:                            # State there is an overflow issue
            print "ERROR: OUT-OF-MEMORY"

        self.printMemory()                          # Print the structure
    
    def getkey(self, tuple1):
        return tuple1[0]

    #resort freeSpace List to be in order after appending
    def free_sort(self):
        sorted( self.freeSpace, key=self.getkey )

    #finds first available free space
    def find_first_free_space( self, reqMemFrames ):
        for space in self.freeSpace:
            if ( space[1] - space[0] ) >= reqMemFrames:
                self.freeSpace.remove(space)
                return ( True, space[0], space[1] )
        return ( False, 0 , 0 )

    def printMemory(self):
        print "Memory at time %d" %self.simTime
        i = 0
        printList = []
        while i < self.numMemFrames:
            if i + 79 < self.numMemFrames:
                printList.append(self.memFrames[i:i + 80])
            else:
                printList.append(self.memFrames[i:])
            i += 80

        for m in printList:
            print m

    def incrementTime(self):
        self.simTime += 1

    def run(self, quiet_mode, alloc_method):
        while self.simTime <= self.lastTime:
            change = False
            t = 0
            if not quiet_mode:
                #get time, t, input from user
                pass

            #increment time
            self.incrementTime()
            # print "time incremented to " + str(self.simTime)

            #check for exiting processes
            for p in self.processes:
                if p.exitTimes[0] == self.simTime:
                    self.deallocate(p)

            #check for entering processes
            for p in self.processes:
                if p.arrivalTimes[0] == self.simTime:
                    self.select_n_cal( alloc_method, p )

            #prints at time requested or on every change for quiet_mode
            if quiet_mode and change:
                self.printMemory()
            elif self.simTime == t:
                self.printMemory()

    def defragment(self):
        pass

    def deallocate(self, aProcess):
        pass

    def select_n_cal(self, alloc_method, aProcess):
        if alloc_method == "first":
            self.exec_first()
        elif alloc_method == "best":
            self.exec_best()
        elif alloc_method == "next":
            self.exec_next()
        elif alloc_method == "worst":
            self.exec_worst()
        elif alloc_method == "noncontig":
            self.exec_noncontig()        

    def exec_first(self):
        pass

    def exec_best(self):
        pass

    def exec_next(self):
        pass

    def exec_worst(self):
        pass

    def exec_noncontig(self):
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

    #Creating Process and populating list
    processList = []
    with open(file_name, "r") as in_file:
        for line in in_file:
            line = line.split()
            if len(line) > 1:
                processList.append(Process(line))

    #initializing MainMemorySimulator
    M = MainMemorySimulator(processList)

    #Run Iterations
    M.run( quiet_mode, alloc_method )