#Memory Management Simulation System
import sys

#PROCESS CLASS
class Process(object):
    """docstring for Process"""
    def __init__(self, processArgs):
        if len(processArgs) < 4:                        # Process wasn't provided at least a name, req frames
            print "Error Initializing Process!"         #   and one set of arrival and exit times
            print "Not Enough Arguments..."
            return
            
        self.name = processArgs[0]                      # Process Name
        self.reqMemFrames = int(processArgs[1])         # Process Size
        self.memLoc = (0,0)                             # location if allocated, else (0,0)
        self.arrivalTimes = []                          # list of arrival times, in order
        self.exitTimes = []                             # list of exit times, in order
        self.done = False                               # True if last arrival time has occurred (note still needs to exit and be removed)

        i = 0
        for x in processArgs[2:]:                   # List of arrival and exit times
            if i%2 == 0:
                self.arrivalTimes.append(int(x))
            else:
                self.exitTimes.append(int(x))
            i += 1

#MEMORY SIMULATION CLASS
class MainMemorySimulator(object):
    """docstring for MainMemory"""
    def __init__(self, processList):
        self.simTime = 0                    # Master Time Handler
        self.lastTime = 0                   # Time that last process exits
        self.processes = processList        # Master List of all Processes
        self.freeSpace = [(80,1599)]        # List of tuples of start and end of free space
        self.runningProcesses = []          # List of Processes currently running
        self.memFrames = ""                 # String Representation of Memory
        self.numMemFrames = 1600            # Total amount of space (memFrames size)
        self.numOpSysProc = 80              # Number of spaces in Memory Representation dedicated to op sys processes
        self.change = False
        self.t = 0

        # Finding all processes that start at 0
        for p in processList:
            if p.arrivalTimes[0] == 0:
                (free_check, begin, end) = self.find_first_free_space( p.reqMemFrames )
                if free_check:
                    tSize = p.reqMemFrames + begin - 1
                    p.memLoc = ( begin, tSize )
                    if ( end - tSize ) > 0:
                        self.freeSpace.append( (tSize + 1 , end) )
                    self.runningProcesses.append(p) # and adding them to runningProcesses list
                    self.free_sort()
                    self.remove_entry_time( p )
                else:
                    print "ERROR: OUT-OF-MEMORY"
                    sys.exit()

            for et in p.exitTimes:
                if et > self.lastTime:
                    self.lastTime = et

        self.printMemory()                          # Print the structure
    
    def getfreekey(self, tuple1):
        return tuple1[0]

    #resort freeSpace List to be in order after appending
    def free_sort(self):
        sorted( self.freeSpace, key=self.getfreekey )

    def getprocesskey(self, aProcess):
        return aProcess.memLoc[0]

    def processes_sort(self):
        sorted( self.runningProcesses, key=self.getprocesskey )

    #finds first available free space
    def find_first_free_space( self, reqMemFrames ):
        for space in self.freeSpace:
            if ( space[1] - space[0] ) >= reqMemFrames:
                self.freeSpace.remove(space)
                return ( True, space[0], space[1] )
        return ( False, 0 , 0 )

    #scans through runnning processes and prints
    def printMemory(self):
        self.memFrames = ""                 #output string
        memFrameItr = self.numOpSysProc     # Master index handler for memory representation
        temp_processes = list(self.runningProcesses)
        temp_space = list(self.freeSpace)

        for i in range(0, self.numOpSysProc):   # Adding Operating System Frames to beginning
            self.memFrames += "#"

        self.processes_sort()

        while memFrameItr < self.numMemFrames:      # Fill in each spot of memory representation
            for p in temp_processes:
                if memFrameItr == p.memLoc[0]:
                    while memFrameItr <= p.memLoc[1]:
                        self.memFrames += p.name
                        memFrameItr += 1
                    temp_processes.remove( p )
            for space in temp_space:
                if space[0] == memFrameItr:
                    while memFrameItr <= space[1]:
                        self.memFrames += "."
                        memFrameItr += 1
                    temp_space.remove( space )

        #printing set string of memory from above in correct format            
        print "Memory at time %d:" %self.simTime
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

        print ""

    def incrementTime(self):
        self.simTime += 1

    #run iterations
    def run(self, quiet_mode, alloc_method):
        while self.simTime <= self.lastTime:
            #increment time
            self.incrementTime()

            if not quiet_mode and self.simTime > self.t:
                #get time, t, input from user
                while self.t < self.simTime:
                    self.t = int(raw_input("Enter next time to view memory (0 to exit) : current time is %d --> " %self.simTime))
                    if self.t == 0:
                        sys.exit()
                    if self.t <self.simTime:
                        print "Invalid Input: Enter time past current time of %d" %self.simTime

            #check for exiting processes + deallocate if found
            for p in self.processes:
                if p.exitTimes[0] == self.simTime:
                    self.deallocate(p)

            #check for entering processes + allocate if found
            for p in self.processes:
                if not p.done:
                    if p.arrivalTimes[0] == self.simTime:
                        self.select_n_cal( alloc_method, p )

            #prints at time requested or on every change for quiet_mode
            if quiet_mode and self.change:
                self.change = False
                self.printMemory()
            elif self.simTime == self.t:
                self.printMemory()
            elif self.t > self.lastTime and self.simTime == self.lastTime:
                print "Program Simulation is about to end, printing memory before exiting"
                self.printMemory() 

    #defragment memory if free blocks don't allow allocation
    def defragment(self):
        print "Performing degragmentation..."
        self.processes_sort()
        last_spot = 79
        processes_moved = 0
        move_check = False
        for p in range(0, len(self.runningProcesses)):
            move_check = True
            if p == 0:
                last_spot = self.runningProcesses[0].memLoc[1]
                continue

            while self.runningProcesses[p].memLoc[0] > self.runningProcesses[p - 1].memLoc[1] + 1:
                if move_check:
                    processes_moved += 1
                    move_check = False
                temp1 = self.runningProcesses[p].memLoc[0] - 1
                temp2 = self.runningProcesses[p].memLoc[1] - 1
                self.runningProcesses[p].memLoc = ( temp1, temp2 )

            if self.runningProcesses[p].memLoc[1] > last_spot:
                last_spot = self.runningProcesses[p].memLoc[1]
        
        self.freeSpace = [(last_spot + 1, 1599)]
        print "Defragmentation completed."
        percent = ((1599.00 - last_spot) / 1600.00) * 100
        print "Relocated", processes_moved, "processes to create a free memory block of", (1599 - last_spot), "units (%.2f%% of total memory).\n" %percent
        self.printMemory()
    
    #deallocates a proces from memory
    def deallocate(self, aProcess):
        self.runningProcesses.remove( aProcess )
        
        begin = aProcess.memLoc[0]
        end = aProcess.memLoc[1]
        
        #handle if blcok being freed is next to current free block
        check_before = False
        check_after = False
        before_tup = ( 0, 0 )
        after_tup = ( 0 , 0 )
        for space in self.freeSpace:
            #block is after free space
            if space[0] == ( end + 1 ):
                check_after = True
                after_tup = space
            #block is before free space
            if space[1] == ( begin - 1):
                check_before = True
                before_tup = space
        #if between two free blocks
        if check_before and check_after:
            self.freeSpace.remove( before_tup )
            self.freeSpace.remove( after_tup )
            self.freeSpace.append( (before_tup[0], after_tup[1]) )
        #if only before a free block
        elif check_before:
            self.freeSpace.remove( before_tup )
            self.freeSpace.append( (before_tup[0], end) )
        #if only after a free block
        elif check_after:
            self.freeSpace.remove( after_tup )
            self.freeSpace.append( (begin,  after_tup[1]) )
        #else not next to a free block
        else:
            self.freeSpace.append( (begin, end) )

        self.remove_exit_time( aProcess )

        self.free_sort()
        self.change = True

    #selects the proper algorithm based on command line argument
    def select_n_cal(self, alloc_method, aProcess):
        if alloc_method == "first":
            self.exec_first( aProcess )
        elif alloc_method == "best":
            self.exec_best( aProcess )
        elif alloc_method == "next":
            self.exec_next( aProcess )
        elif alloc_method == "worst":
            self.exec_worst( aProcess )
        elif alloc_method == "noncontig":
            self.exec_noncontig( aProcess ) 
        # fTime = aProcess.arrivalTimes[0]
        # if fTime != self.remove_entry_time( aProcess ):
            # print "ERROR: Removed Wrong arrival time from process " + aProcess.name
            # sys.exit()
        # else:
        self.change = True

    #removes entry time from process list after process has been added to memory
    def remove_entry_time(self, aProcess):
        if len(aProcess.arrivalTimes) == 1:
            aProcess.done = True
        index = self.processes.index( aProcess )
        return self.processes[index].arrivalTimes.pop(0)

    #removes a exit time from process list after process leaves memory
    #if last exit time, it removes process from processes
    def remove_exit_time(self, aProcess):
        if aProcess.done == True:
            i = self.processes.index( aProcess )
            self.processes.pop( i )
        else:
            index = self.processes.index( aProcess )
            self.processes[index].exitTimes.pop(0)
            aProcess.memLoc = ( 0, 0 )

    #implements First-Fit Memory Allocation Algorithm
    def exec_first(self, aProcess):
        print "first:",aProcess.name,"gets here at time " + str(self.simTime)

        n = 0
        while n < 2: 
            (free_check, begin, end) = self.find_first_free_space( aProcess.reqMemFrames )
            if free_check:
                tSize = aProcess.reqMemFrames + begin - 1
                aProcess.memLoc = ( begin, tSize )
                if ( end - tSize ) > 0:
                    self.freeSpace.append( (tSize + 1 , end) )
                self.runningProcesses.append( aProcess ) # and adding them to runningProcesses list
                self.free_sort()
                self.remove_entry_time( aProcess )
                n = 2
            elif n == 0:
                self.defragment()
                n += 1
            else:
                print "ERROR: OUT-OF-MEMORY"
                sys.exit()
    
    #implements Best-Fit Memory Allocation Algorithm
    def exec_best(self, aProcess):
        print "best:",aProcess.name,"gets here at time " + str(self.simTime)
        pass

    #implements Next-Fit Memory Allocation Algorithm
    def exec_next(self, aProcess):
        print "next:",aProcess.name,"gets here at time " + str(self.simTime)
        pass

    #implements Worst-Fit Memory Allocation Algorithm
    def exec_worst(self, aProcess):
        print "worst:",aProcess.name,"gets here at time " + str(self.simTime)
        pass

    #implements Non-Contiguous Memory Allocation Algorithm
    def exec_noncontig(self, aProcess):
        print "noncontig:",aProcess.name,"gets here at time " + str(self.simTime)
        pass


########################    END CLASS   ###########################################################


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

#############################     MAIN FUNCTION     #############################################

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