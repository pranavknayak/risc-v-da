input_file = open("Input.txt", "r")
output_file = open("Output.s", "w")

hex_instructions = input_file.read()
hex_instructions = hex_instructions.splitlines()
binary_list = []
for hex in hex_instructions:
    integer = int(hex, 16)
    binary = format(integer, '0>32b')
    binary_list.append(binary)

instruction_list = [""]*len(hex_instructions)
instruction_count = 0
for binary in binary_list:
    instruction = ""
    opcode = binary[-7:]
    # R-type instruction handler
    if opcode == '0110011':
        rd = binary[-12:-7]
        funct3 = binary[-15:-12]
        rs1 = binary[-20:-15]
        rs2 = binary[-25:-20]
        funct7 = binary[-32:-25]

        if funct7 == '0000000':
            if funct3 == '000':
                instruction += "add "
            elif funct3 == '100':
                instruction += "xor "
            elif funct3 == '110':
                instruction += "or "
            elif funct3 == '111':
                instruction += "and "
            elif funct3 == '001':
                instruction += "sll "
            elif funct3 == '101':
                instruction += "srl "
        elif funct7 == '0100000':
            if funct3 == '000':
                instruction += "sub "
            elif funct3 == '101':
                instruction += "sra "
        rd = str(int(rd, 2))
        rs1 = str(int(rs1, 2))
        rs2 = str(int(rs2, 2))

        instruction = instruction + "x" + rd + ", x" + rs1 + ", x" + rs2

    #elif opcode == ''

    instruction_list[instruction_count] += instruction
    output_file.write(instruction_list[instruction_count])
    output_file.write("\n")
    instruction_count += 1
input_file.close()
output_file.close()
