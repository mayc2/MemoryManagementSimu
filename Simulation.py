#Memory Management Simulation System
import sys

#PROCESS CLASS
class Process(object):
    """docstring for Process"""
    def __init__(self, processArgs):
        if len(processArgs) < 4:                        # Process wasn't provided at least a name, req frames
            print "Error Initializing Process!"         #   and one set of arrival and exit times
            print "Not Enough Arguments..."
            sys.exit()

        self.name = processArgs[0]                      # Process Name
        self.reqMemFrames = int(processArgs[1])         # Process Size
        self.memLoc = (0,0)                             # location if allocated, else (0,0)
        self.arrivalTimes = []                          # list of arrival times, in order
        self.exitTimes = []                             # list of exit times, in order
        self.done = False                               # True if last arrival time has occurred (note still needs to exit and be removed)
        self.LL = []                                    # if non-contig, list of memory location blocks 
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
    def __init__(self, processList, alloc_method):
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
        self.lastAlloc = 79

        # Finding all processes that start at 0
        for p in processList:
            if p.arrivalTimes[0] == 0:
                (free_check, begin, end) = self.find_first_free_space( p.reqMemFrames )
                if free_check:
                    tSize = p.reqMemFrames + begin - 1
                    p.memLoc = ( begin, tSize )
                    if alloc_method == "noncontig":
                        p.LL.append( p.memLoc )
                    if ( end - tSize ) > 0:
                        self.freeSpace.append( (tSize + 1 , end) )
                    self.fix_free_space()
                    self.runningProcesses.append(p) # and adding them to runningProcesses list
                    print "Allocated",p.name
                    self.lastAlloc = p.memLoc[1]
                    self.free_sort()
                    self.remove_entry_time( p )
                else:
                    print "ERROR: OUT-OF-MEMORY"
                    sys.exit()

            for et in p.exitTimes:
                if et > self.lastTime:
                    self.lastTime = et
        print ""
        self.printMemory()                          # Print the structure
    
    #resort freeSpace List to be in order after appending
    def free_sort(self):
        self.freeSpace.sort()

    def getprocesskey(self, aProcess):
        return aProcess.memLoc

    def processes_sort(self):
        # print "\n\nENTER PROCESSES SORT"
        # before = "BEFORE: "
        # for p in self.runningProcesses:
        #     before += p.name + str(p.memLoc)
        # print before
        self.runningProcesses = sorted( self.runningProcesses, key=self.getprocesskey )
        # after = "\nAFTER: "
        # for p in self.runningProcesses:
        #     after += p.name + str(p.memLoc)
        # print after + "\n\n"

    #finds first available free space
    def find_first_free_space( self, reqMemFrames ):
        for space in self.freeSpace:
            if ( space[1] - space[0] + 1) >= reqMemFrames:
                self.freeSpace.remove(space)
                return ( True, space[0], space[1] )
        return ( False, 0 , 0 )

    #finds smallest availabale free space
    def find_best_free_space( self, reqMemFrames ):
        diff = 1600 - 80
        best_space = ( 0, 0 )
        check = False
        for space in self.freeSpace:
            if (space[1] - space[0] + 1) < diff and (space[1] - space[0] + 1) >= reqMemFrames:
                diff = space[1] - space[0] + 1
                best_space = space
                check = True
        
        if check:
            self.freeSpace.remove(best_space)
            return ( True, best_space[0], best_space[1] )
        return ( False, 0 , 0 )

    #finds first free space after last allocation
    def find_next_free_space( self, reqMemFrames ):
        n = 0
        while True:
            if n == 0:
                for space in self.freeSpace:
                    if space[0] > self.lastAlloc: 
                        if ( space[1] - space[0] + 1) >= reqMemFrames:
                            self.freeSpace.remove(space)
                            return ( True, space[0], space[1] )
                n += 1
            elif n == 1:
                for space in self.freeSpace:
                    if ( space[1] - space[0] + 1) >= reqMemFrames:
                        self.freeSpace.remove(space)
                        return ( True, space[0], space[1] )
                n += 1
            else:
                return ( False, 0 , 0 )

    #finds largest available free space
    def find_worst_free_space( self, reqMemFrames ):
        diff = 0
        worst_space = ( 0, 0 )
        for space in self.freeSpace:
            if (space[1] - space[0] + 1) > diff:
                diff = space[1] - space[0] + 1
                worst_space = space
        
        if (worst_space[1] - worst_space[0] + 1) >= reqMemFrames:
                self.freeSpace.remove(worst_space)
                return ( True, worst_space[0], worst_space[1] )
        return ( False, 0 , 0 )

    def printNonMemory(self):
        self.memFrames = ""                 #output string
        memFrameItr = self.numOpSysProc     # Master index handler for memory representation

        for i in range(0, self.numOpSysProc):   # Adding Operating System Frames to beginning
            self.memFrames += "#"

        while memFrameItr < self.numMemFrames:
            p_found = False
            for p in self.runningProcesses:
                for l in p.LL:
                    if memFrameItr >= l[0] and memFrameItr <= l[1]:
                        self.memFrames += p.name
                        p_found = True
            if not p_found:
                self.memFrames += "."
            memFrameItr += 1

        printList = []
        print "Memory at time %d:" %self.simTime
        i = 0
        while i < self.numMemFrames:
            if i + 79 < self.numMemFrames:
                printList.append(self.memFrames[i:i + 80])
            else:
                printList.append(self.memFrames[i:])
            i += 80

        for m in printList:
            print m

        print ""

    #scans through runnning processes and prints
    def printMemory(self):
        self.memFrames = ""                 #output string
        memFrameItr = self.numOpSysProc     # Master index handler for memory representation

        for i in range(0, self.numOpSysProc):   # Adding Operating System Frames to beginning
            self.memFrames += "#"

        self.processes_sort()

        while memFrameItr < self.numMemFrames:      # Fill in each spot of memory representation
            for p in self.runningProcesses:
                if memFrameItr == p.memLoc[0]:
                    while memFrameItr <= p.memLoc[1]:
                        self.memFrames += p.name
                        memFrameItr += 1

            for space in self.freeSpace:
                if space[0] == memFrameItr:
                    while memFrameItr <= space[1]:
                        self.memFrames += "."
                        memFrameItr += 1

        #printing set string of memory from above in correct format            
        printList = []
        print "Memory at time %d:" %self.simTime
        i = 0
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

    def print_stats(self, alloc_method):
        self.processes_sort()
        self.free_sort()
        for p in self.runningProcesses:
            if alloc_method != "noncontig":
                print "Process",p.name,"located at",p.memLoc,"with size",p.reqMemFrames
            else:
                print "Process",p.name,"located at",p.LL,"with size",p.reqMemFrames
        for space in self.freeSpace:
            print "open space",space

    #run iterations
    def run(self, quiet_mode, alloc_method):
        while self.simTime <= self.lastTime:
            #increment time
            self.incrementTime()

            if not quiet_mode and self.simTime > self.t:
                #get time, t, input from user
                while self.t < self.simTime:
                    self.t = raw_input("Enter next time to view memory (0 to exit) : current time is %d --> " %self.simTime)
                    if self.t == "":
                        print "Invalid Input: Enter time past current time of %d" %self.simTime
                        self.t = 0                        
                    elif self.t == "p":
                        self.print_stats(alloc_method)
                        self.t = self.simTime
                    else:
                        self.t = int(self.t)
                        # self.t = int(raw_input("Enter next time to view memory (0 to exit) : current time is %d --> " %self.simTime))
                        if self.t == 0:
                            sys.exit()
                        if self.t < self.simTime:
                            print "Invalid Input: Enter time past current time of %d" %self.simTime

            #check for exiting processes + deallocate if found
            for p in self.processes:
                if p.exitTimes[0] == self.simTime:
                    if alloc_method != "noncontig":
                        self.deallocate(p)
                    else:
                        self.non_deallocate(p)

            #check for entering processes + allocate if found
            for p in self.processes:
                if not p.done:
                    if p.arrivalTimes[0] == self.simTime:
                        self.select_n_cal( alloc_method, p )

            #prints at time requested or on every change for quiet_mode
            if quiet_mode and self.change:
                self.change = False
                if alloc_method != "noncontig":
                    self.printMemory()
                else:
                    self.printNonMemory()
            elif self.simTime == self.t:
                if alloc_method != "noncontig":
                    self.printMemory()
                else:
                    self.printNonMemory()
            elif self.t > self.lastTime and self.simTime == self.lastTime:
                print "Program Simulation is about to end, printing memory before exiting"
                if alloc_method != "noncontig":
                    self.printMemory() 
                else:
                    self.printNonMemory()

    #defragment memory if free blocks don't allow allocation
    def defragment(self):
        print "Performing degragmentation..."
        self.processes_sort()
        last_spot = 79
        processes_moved = 0
        move_check = False
        for p in range(0, len(self.runningProcesses)):
            move_check = True
            # if p == 0:
            #     last_spot = self.runningProcesses[0].memLoc[1]
            #     continue

            while self.runningProcesses[p].memLoc[0] > last_spot + 1:
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
        print "Deallocated",aProcess.name + "\n"
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
            self.freeSpace.append( (before_tup[0], after_tup[1]) )
            self.freeSpace.remove( before_tup )
            self.freeSpace.remove( after_tup )
        #if only before a free block
        elif check_before:
            self.freeSpace.append( (before_tup[0], end) )
            self.freeSpace.remove( before_tup )
        #if only after a free block
        elif check_after:
            self.freeSpace.append( (begin,  after_tup[1]) )
            self.freeSpace.remove( after_tup )
        #else not next to a free block
        else:
            self.freeSpace.append( (begin, end) )

        self.remove_exit_time( aProcess )

        self.fix_free_space()
        self.change = True

    def non_deallocate(self, aProcess):
        print "Deallocated",aProcess.name + "\n"
        self.runningProcesses.remove( aProcess )

        # print aProcess.LL
        for L in aProcess.LL:
            begin = L[0]
            end = L[1]
            aProcess.LL.remove(L)

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
                self.freeSpace.append( (before_tup[0], after_tup[1]) )
                self.freeSpace.remove( before_tup )
                self.freeSpace.remove( after_tup )
            #if only before a free block
            elif check_before:
                self.freeSpace.append( (before_tup[0], end) )
                self.freeSpace.remove( before_tup )
            #if only after a free block
            elif check_after:
                self.freeSpace.append( (begin,  after_tup[1]) )
                self.freeSpace.remove( after_tup )
            #else not next to a free block
            else:
                self.freeSpace.append( (begin, end) )
            self.fix_free_space()

        # print aProcess.LL
        # print self.freeSpace
        self.remove_exit_time( aProcess )
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

    def fix_free_space(self):
        # print "ENTER SORT"
        # print "BEFORE:",self.freeSpace
        self.free_sort()
        # print "AFTER:",self.freeSpace
        for space in range( 0, len(self.freeSpace) ):
            if space < (len(self.freeSpace) - 1 ):
                if self.freeSpace[space][1] == self.freeSpace[space + 1][0]:
                    begin = self.freeSpace[space][0]
                    middle = self.freeSpace[space][1]
                    end = self.freeSpace[space + 1][1]
                    self.freeSpace.append( (begin, end) )
                    self.freeSpace.remove( (begin, middle) )
                    self.freeSpace.remove( (middle, end) )

    #implements First-Fit Memory Allocation Algorithm
    def exec_first(self, aProcess):
        print "first:",aProcess.name,"of size",aProcess.reqMemFrames,"gets here at time " + str(self.simTime)

        n = 0
        while n < 2: 
            (free_check, begin, end) = self.find_first_free_space( aProcess.reqMemFrames )
            if free_check:
                tSize = aProcess.reqMemFrames + begin - 1
                aProcess.memLoc = ( begin, tSize )
                if  end > tSize:
                    self.freeSpace.append( (tSize + 1 , end) )
                self.fix_free_space()
                self.runningProcesses.append( aProcess ) # and adding them to runningProcesses list
                print "Allocated",aProcess.name
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
        print "best:",aProcess.name,"of size",aProcess.reqMemFrames,"gets here at time " + str(self.simTime)
    
        n = 0
        while n < 2: 
            (free_check, begin, end) = self.find_best_free_space( aProcess.reqMemFrames )
            if free_check:
                tSize = aProcess.reqMemFrames + begin - 1
                aProcess.memLoc = ( begin, tSize )
                if  end > tSize:
                    self.freeSpace.append( (tSize + 1 , end) )
                self.fix_free_space()
                self.runningProcesses.append( aProcess ) # and adding them to runningProcesses list
                print "Allocated",aProcess.name
                self.free_sort()
                self.remove_entry_time( aProcess )
                n = 2
            elif n == 0:
                self.defragment()
                n += 1
            else:
                print "ERROR: OUT-OF-MEMORY"
                sys.exit()

    #implements Next-Fit Memory Allocation Algorithm
    def exec_next(self, aProcess):
        print "next:",aProcess.name,"of size",aProcess.reqMemFrames,"gets here at time " + str(self.simTime)

        n = 0

        while n < 2: 
            (free_check, begin, end) = self.find_next_free_space( aProcess.reqMemFrames )
            if free_check:
                tSize = aProcess.reqMemFrames + begin - 1
                aProcess.memLoc = ( begin, tSize )
                if  end > tSize:
                    self.freeSpace.append( (tSize + 1 , end) )
                self.fix_free_space()
                self.runningProcesses.append( aProcess ) # and adding them to runningProcesses list
                print "Allocated",aProcess.name
                self.lastAlloc = aProcess.memLoc[1]
                self.free_sort()
                self.remove_entry_time( aProcess )
                n = 2
            elif n == 0:
                self.defragment()
                n += 1
            else:
                print "ERROR: OUT-OF-MEMORY"
                sys.exit()

    #implements Worst-Fit Memory Allocation Algorithm
    def exec_worst(self, aProcess):
        print "worst:",aProcess.name,"of size",aProcess.reqMemFrames,"gets here at time " + str(self.simTime)

        n = 0
        while n < 2: 
            (free_check, begin, end) = self.find_worst_free_space( aProcess.reqMemFrames )
            if free_check:
                tSize = aProcess.reqMemFrames + begin - 1
                aProcess.memLoc = ( begin, tSize )
                if end > tSize:
                    self.freeSpace.append( (tSize + 1 , end) )
                self.fix_free_space()
                self.runningProcesses.append( aProcess ) # and adding them to runningProcesses list
                print "Allocated",aProcess.name + "\n"
                self.free_sort()
                self.remove_entry_time( aProcess )
                n = 2
            elif n == 0:
                self.defragment()
                n += 1
            else:
                print "ERROR: OUT-OF-MEMORY"
                sys.exit()

    #implements Non-Contiguous Memory Allocation Algorithm
    def exec_noncontig(self, aProcess):
        print "noncontig:",aProcess.name,"of size",aProcess.reqMemFrames,"gets here at time " + str(self.simTime)+"\n"
        
        curSize = 0
        answer1 = 1599
        answer2 = 0
        while curSize < aProcess.reqMemFrames:
            # print "ANSWER1:",answer1,"ANSWER2:",answer2

            self.free_sort()
            # print "FREESPACE BEFORE:",self.freeSpace
            if len(self.freeSpace) > 0:
                space = self.freeSpace.pop(0)
                # print "REMOVE:",space
                begin = space[0]
                end = space[1]
                if begin < answer1:
                    answer1 = begin
                ssize = space[1] - space[0] + 1

                #free space is larger than remaining required memory blocks
                if curSize+ssize >= aProcess.reqMemFrames:
                    tSize = (aProcess.reqMemFrames - curSize) + begin - 1
                    answer2 += tSize
                    aProcess.LL.append( (answer1, answer2) )
                    if end > tSize:
                        self.freeSpace.append( (tSize + 1 , end) )
                    self.fix_free_space()
                    self.runningProcesses.append( aProcess ) # and adding them to runningProcesses list
                    # print "Allocated",aProcess.name + "\n"
                    self.free_sort()
                    self.remove_entry_time( aProcess )
                else:
                    answer2 += end
                curSize += ssize
            else:
                print "ERROR: OUT-OF-MEMORY"
                sys.exit()                
            # print "current size",curSize,"memfram:",aProcess.reqMemFrames
        # print "FREESPACE AFTER:",self.freeSpace



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
    M = MainMemorySimulator(processList, alloc_method)

    #Run Iterations
    M.run( quiet_mode, alloc_method )