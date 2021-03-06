MemoryManagementSimu
====================
Authored: Chris May

Memory Management Simulation System

General Notes:
	-contiguous memory management
		* assign user processes to memory at time 0
		* each process requires specific amount of memory frames(10-100)
	-noncontiguous memory management
	-appropriate data structure for main memory
		* logically consists of 1600 memory frames (equal size)
		* resident operating system processes fixed and loaded into memory in first 80 frames
	-if unsuccessfully allocate memory:
		* OUT-OF-MEMORY error message
		* perform defragmentation

MAIN:
	bool OUT_OF_MEMORY
	- parse cli arguments
		-- USAGE: memsim [-q] <input-file> { first | best | next | worst }
		-- read user processes from in-file 
		-- get type of memory allocation algorithm to use
	- set up user processes (allocated at time 0)
	- display initial memory
	- call simulation of proper algorithm

USER PROCESS (in-file) DETAILS:
	- N = number of processes (#define MAX_NUM 26)
	- proc1 proc1 p1_memory p1_arrival_time_1 p1_exit_time_1

	- proc# 
		-- single character (A-Z), identify process
	- p#_memory 
		-- fixed number of memory frames
	- (p#_arrival_time_?, p#_exit_time_?) 
		-- pair of arrival times the process will experience
		-- each process has increasing set of these values
		-- no overhead in adding/removing processes from memory

INITIAL MEMORY DISPLAY:
	- character mappings
		-- '.' : free memory frame
		-- '#' : operating system process memory frame
		-- 'A-Z' (ASCII character) : user process memory frame
	- display 80 characters to a line

SIMULATION:
	- loop (optionally controlled by user)
	- each iteration:
		-- time moves forward to next event
		-- two event types (based on in-file):
			* Process(es) exit the system
				- memory is marked free
				- multiple processes can be marked free in event
				- occurs BEFORE processes enter system
			* New Process(es) enter the system
				- memory allocated using given placement algorithm
				- defragment on failure of placement, then add repeated
		-- Iteration Display:
			* current time
			* memory
			* prompt user for integer t (time)
			* run loop until simulation reaches/passes time t
			* if user enters 0, quit simulation

DEFRAGMENTATION:
	- performed everytime program reaches OUT-OF-MEMORY condition
	- defragment then continue simulation
	- assume no time elapses during defragmentation
	- DISPLAY:
		-- number of processes that were reallocated
		-- size of the newly created contiguous free block of memory
		-- % of free memory available vs. full memory size
		-- memory once its defragmented
		--i.e. "Relocated 12 processes to create a free memory block of 287 units (17.94% of total memory)."
	- if defragmentation doesn't free up enough memory
		-- exit simulation
		-- print error message OUT-OF-MEMORY

NON-CONTIGUOUS MEMORY ALLOCATION:
	- support non-contiguous memory allocation
	- designated by cli option noncontig
	- i.e. "USAGE: memsim [-q] <input-file> { noncontig | first | best | next | worst }"
	- no-defragmentation occurs
	- if a process requires n frames, allocate first n frames encountered
	-if OUT-OF-MEMORY Condition, exit simulation w/ error message


ALGORITHMS:
	- First-Fit algorithm: allocate the first free block
       that's large enough to accommodate P
        starting from the top of memory

    - Next-Fit algorithm: same as First-Fit algorithm, but
       we start after the last-allocated process

    - Best-Fit algorithm: allocate the SMALLEST free block
       that's large enough to accommodate P

    - Worst-Fit algorithm: allocate the LARGEST free block
       that's large enough to accommodate P
