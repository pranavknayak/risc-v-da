The code is written entirely in a single file, in Python.
To run the program, cd to the folder containing the file 'disassembler.py'.
Run it with the command 'python3 disassembler.py'.
The program will prompt you to input the filename/filepath of the file containing the assembly instructions in hexadecimal format, and will write the corresponding RISC-V Assembly into a '.s' file with the same filename.
Unrecognized bits in any of the fields will print out a descriptive error message specifying which field returned the error, and which instruction it most closely matched up until the unrecognized bit was read.
