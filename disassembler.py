input_file = open("Input.txt", "r")
output_file = open("Output.s", "w")

hex_instructions = input_file.read()
hex_instructions = hex_instructions.splitlines()
binary_list = []
for hex in hex_instructions:
    integer = int(hex, 16)
    binary = format(integer, '0>32b')
    binary_list.append(binary)

instruction_list = []
for binary in binary_list:
    instruction = ""
    opcode = binary[-7:]
    print(opcode)
    if opcode == '0110011':
        rd = binary[-12:-7]
        funct3 = binary[-15:-12]
        rs1 = binary[-20:-15]
        rs2 = binary[-25:-20]
        funct7 = binary[-32:-25]

        if funct7 == '0000000':
            if funct3 == '000':
                instruction.append("add ")
            elif funct3 == '100':
                instruction.append("xor ")
            elif funct3 == '110':
                instruction.append("or ")
            elif funct3 == '111':
                instruction.append("and ")
            elif funct3 == '001':
                instruction.append("sll ")
            elif funct3 == '101':
                instruction.append("srl ")

input_file.close()
output_file.close()
